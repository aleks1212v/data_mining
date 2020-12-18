# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 14:04:31 2020

@author: aleks1212
"""


import librosa
import numpy as np
import matplotlib.pyplot as plt

frequency = 1000
fs = 4 * frequency
time_vector = 1/fs * np.arange(20000)
print(time_vector.shape)

sine_wave = np.sin(2 * np.pi * frequency * time_vector)

window_size = 1024
window = np.hanning(window_size)
hop_length = 8

out  = librosa.core.spectrum.stft(sine_wave, n_fft = window_size, hop_length = hop_length, window=window)
out = 2 * np.abs(out) / np.sum(window)
print(out.shape)
librosa.display.specshow(out, hop_length = hop_length, sr = 20000, x_axis='time', y_axis='log')
plt.colorbar()
'''
fig = plt.figure()
axes = fig.add_subplot(111)
im = axes.pcolormesh(out)
fig.colorbar(im)

plt.figure()
slice = out[:, 10]
plt.plot(slice)
plt.grid()

plt.show()
'''