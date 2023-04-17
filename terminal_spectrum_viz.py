#%%
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
import struct
import tkinter as tk
from tkinter import TclError

# https://www.youtube.com/watch?v=AShHJdSIxkY

#%%
chunk = 4410
sample_format = pyaudio.paInt16
channels = 1                           # Settings with screen = 1 | Settings without screen = 1
fs = 44100
seconds = 10
device_index = 1                       # Settings with screen = 2 | Settings without screen = 1  | Settings uwithout Wifi = 0
filename = "audio_spectrum.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio
# Implement a linebreak inn the print


print(f'\n... Recording {seconds} seconds of audio initialized ...\n')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                input_device_index = device_index,
                frames_per_buffer=chunk,
                output=True,
                input=True)

data = stream.read(chunk)
#print(data)

print(len(data))
data_int = np.array(struct.unpack(str(2*chunk) + 'B', data), dtype= 'b')[::2] + 128

fix, ax = plt.subplots()
ax.plot(data_int, '-')
plt.show()

#%%
