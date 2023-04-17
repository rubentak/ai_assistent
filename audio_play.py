# %%
import pyaudio
import wave
from audio_get_channels import get_speaker
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

def play_recording():
    filename = os.path.join(script_dir, "audio_output.wav")
    sound = wave.open(filename)
    p = pyaudio.PyAudio()
    print(f"Start playing {sound.getnchannels()} channels at {sound.getframerate()} Hz")
    chunk = 1024
    stream = p.open(format=p.get_format_from_width(sound.getsampwidth()),
                    channels=sound.getnchannels(),
                    rate=sound.getframerate(),
                    output=True,
                    output_device_index=get_speaker())

    data = sound.readframes(chunk)
    while True:
        if data != '':
            stream.write(data)
            data = sound.readframes(chunk)

        if data == b'':
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Finished playing")

play_recording()

#%%
