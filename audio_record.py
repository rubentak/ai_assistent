#%%
import pyaudio
import wave
from audio_get_channels import get_cur_mic
import os

# Audio channels device_index need to be adjusted to the current settings:
# chanel settings with screen = 1 | Settings without screen = 1
# device_settings with screen = 2 | Settings without screen = 1  | Settings without Wifi = 0

# (0, 'IPhone 14NJ Microphone', 1)
# (1, 'External Microphone', 1)
# (2, 'External Headphones', 0)
# (3, 'MacBook Pro Microphone', 1)
# (4, 'MacBook Pro Speakers', 0)
# (5, 'Microsoft Teams Audio', 2)

script_dir = os.path.dirname(os.path.abspath(__file__))

def audio_rec(num_seconds):
    chunk = 4410
    fs = 44100
    channels = 1                           # Adjust as mentioned above
    seconds = num_seconds
    device_index = get_cur_mic()       # Adjust as mentioned above
    sample_format = pyaudio.paInt16
    filename = os.path.join(script_dir, "audio_output.wav")

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print(f'\n... Recording {seconds} seconds of audio initialized ...\n')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    input_device_index=device_index,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

# While the for loop is running and recording, print countdown in seconds
    second_tracking = 0
    second_count = 0
    for i in range(0, int(fs/chunk*seconds)):
        data = stream.read(chunk)
        frames.append(data)
        second_tracking += 1
        if second_tracking == fs/chunk:
            second_count  += 1
            second_tracking = 0
            print(f'... Time left: {seconds - second_count} seconds')
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('\n... Finished recording ...')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

audio_rec(5)

#%%
