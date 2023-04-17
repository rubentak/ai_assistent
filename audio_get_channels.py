# pyaudio get channels and device index
import pyaudio
import pandas as pd

# Get all channels printed
def get_all_channels():
    p = pyaudio.PyAudio()
    channels = {}
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        rate = p.get_device_info_by_index(0)['defaultSampleRate']

        print((i, dev['name'], dev['maxInputChannels']), rate)

# Get all channels printed in a df
def get_all_channels_df():
    p = pyaudio.PyAudio()
    channels = {}
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        channels[i] = i, dev['name'], dev['maxInputChannels']

    return pd.DataFrame(channels).T

# Get channel Macbook Pro Microphone
def get_cur_mic():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if 'pro microphone' in dev['name'].lower():
            return i
    return None

def get_speaker():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if 'speaker' in dev['name'].lower():
            return i
    return None

#%%
