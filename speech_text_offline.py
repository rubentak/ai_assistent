import pyaudio
import wave

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
seconds = 3
device_index = 2
filename = "data/output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input_device_index=device_index,
                input=True)

frames = []

for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
#%%
# Path: speach-to-text.py
import speech_recognition as sr

r = sr.Recognizer()
with sr.AudioFile('data/output.wav') as source:
    audio = r.record(source)

try:
    print("Text: " + r.recognize_google(audio))
except Exception as e:
    print("Exception: " + str(e))


# Path: text-to-speech.py
from gtts import gTTS
import os

#%%
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i,dev['name'],dev['maxInputChannels']))

#%%  SECOND TRY
#%%
# speech recognition
import speech_recognition as sr
# transcribe audio file
AUDIO_FILE = "data/output.wav"

# use the audio file as the audio source

r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Google Speech Recognition
try:
    recognised = r.recognize_google(audio, language="de-DE")
    # print recognised text and confidence
    print(recognised)

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

#%%
print(recognised)

# If recognised text contains the word "Barcelona", then play the pilot_functions.py script
if "Barcelona" in recognised:
    print("Barcelona")
    import pilot_functions
    #pilot.get_story()
