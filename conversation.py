# Import libraries
import os
import openai
import credentials
import sys
import pyttsx3
from speech_text_whisper import get_transcript_whisper
openai.api_key = credentials.api_key
import time
import plotext
import numpy as np
import pyaudio
import struct
import wave
from audio_get_channels import get_cur_mic
from scipy.fftpack import fft


#%% FUNCTIONS TO BE STORED AWAY

def audio_spectrum(num_seconds):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    chunk = 4410
    channels = 1
    fs = 44100
    seconds = num_seconds
    sample_format = pyaudio.paInt16
    filename = os.path.join(script_dir, "audio_output.wav")

    print(f'\n... Recording {seconds} seconds of audio initialized ...\n')

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    input_device_index=get_cur_mic(),
                    frames_per_buffer=chunk,
                    input=True)


    x = np.arange(0, chunk)
    x_fft = np.linspace(0, fs / 2, chunk // 2 + 1)

    frames = []
    start_time = time.time()

    while time.time() - start_time < seconds:
        plotext.clt()
        plotext.cld()
        plotext.clc()

        data = stream.read(chunk, False)
        frames.append(data)
        data_int = struct.unpack(str(2 * chunk) + 'B', data)
        data_np = np.array(data_int, dtype='b')[::2] + 128

        y_freq = data_np
        spec = fft(data_int)
        y_spec = np.abs(np.fft.rfft(data_int)) / chunk

        # plotext.subplots(2, 1)
        # plotext.subplot(1, 1)
        plotext.plot(x, y_freq, color="white", marker="braille")
        # marker braille, fhd, hd, sd, dot, dollar,euro, bitcoin, at, heart, smile, queen, king,

        plotext.plot_size(200, 15)
        plotext.ylim(0, 300)
        plotext.xlabel(f' {seconds} seconds recording   | Elapsed time: {round(time.time() - start_time, 1)} seconds, Time left: {round(seconds - (time.time() - start_time), 1)} seconds')
        plotext.yfrequency(2)
        plotext.xfrequency(0)
        plotext.xlim(0, 4410)
        plotext.horizontal_line(128, color="red", yside="top")

        # plotext.subplot(2, 1)
        # plotext.plot_size(200, 15)
        # plotext.plot(x_fft, y_spec, color="white", marker="braille")
        # plotext.ylim(0, 1)
        # plotext.xfrequency(2)
        # plotext.yfrequency(2)
        # plotext.xaxes("log")
        plotext.show()


    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print('\n... Finished recording ...')


def get_transcript_whisper():
    '''Get transcript of audio file with whisper api'''
    openai.api_key = credentials.api_key
    file = open("audio_output.wav", "rb")
    transcription = openai.Audio.transcribe("whisper-1", file, response_format="json")
    text = transcription["text"]
    return text

def run_GPT3(prompt):
    '''Run GPT-3 with the prompt and return the response'''
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response)
    return response

def run_chatGPT(prompt):
    '''Run chatGPT with the prompt and return the response'''
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    answer = completion.choices[0].message.content
    return answer



#%% CONVERSATION FUNCTIONS

def start_conversation():
    # Record audio file with function imported from audio_record.py
    audio_spectrum(10)
    # Get transcript of audio file with whisper api
    print(f"\n... Audio transcription ...")
    text_output = get_transcript_whisper()
    time.sleep(1)
    print(f"\n... Text recognition ... \n Text recongized: {text_output}")
    print(f"\n... ChatGPT prompt  ...")
    answer = run_chatGPT(text_output)
    print(f"\n... ChatGPT answer ... {answer}")
    print(f"\n... Text to speech ...")
    tts = pyttsx3.init()
    tts.setProperty('rate', 110)
    tts.say(answer)
    tts.runAndWait()

def feedback_question():
    print(f'... Feedback question ...')
    question = f"Do you want to know more about this topic or another one?"
    tts = pyttsx3.init()
    tts.setProperty('rate', 110)
    tts.say(question)
    tts.runAndWait()

def stop_sequence():
    print('... Stop sequence ...')
    stop_phrase = f'Well, if you have more questions, you know where to find me. And next time prepare your questions a little better. Goodbye!'
    tts = pyttsx3.init()
    tts.setProperty('rate', 110)
    tts.say(stop_phrase)
    tts.runAndWait()


def recognize_answer():
    print(f"\n... Listening to answer for 3 seconds ...")
    audio_spectrum(3)
    text_output = get_transcript_whisper()
    print(f"\n... Text recognition \nText recognized: {text_output}")
    # if text contains yes restart conversation else stop assistant
    restart_keywords = ["yes", "another", "topic", "more", "Yes", "Another", "Topic", "More"]
    if any(x in text_output for x in restart_keywords):
        print('... Feedback sequence ...')
        feedback_phrase = f'Seems like you are interested today. What do you want to know more about?'
        tts = pyttsx3.init()
        tts.setProperty('rate', 110)
        tts.say(feedback_phrase)
        tts.runAndWait()

        start_conversation()
        feedback_question()
        recognize_answer()
    else:
        stop_sequence()



#%% Start assistant

print(f"\n--------------------------------- Storyteller assistant started ----------------------------------------- \n")
start_conversation()
time.sleep(1)
feedback_question()
time.sleep(1)
recognize_answer()
print(f"\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Storyteller assistant stopped xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")

#%% Stop assistant
