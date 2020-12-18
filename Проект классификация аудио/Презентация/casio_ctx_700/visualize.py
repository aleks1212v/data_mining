# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 12:28:06 2020

@author: aleks1212
"""

import os
import librosa
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import librosa.display
import librosa.util
import soundfile as sf

def signal_plot(path, name):
    x, sr = sf.read(os.path.join(path, name))
    plt.figure(figsize=(14, 5))
    plt.title(name)
    librosa.display.waveplot(x, sr=sr)
    
# Нормализация спектрального центроида для визуализации
def normalize(x, axis=0):
    return sklearn.preprocessing.minmax_scale(x, axis=axis)

def stft_plot(path, name):
    x, sr = sf.read(os.path.join(path, name))
    n_fft = 8192
    window_size = 8192
    window = np.hanning(window_size)
    hop_length = 128
    X = librosa.stft(x, n_fft = window_size, hop_length = hop_length, window = window)
    X = 2 * np.abs(X) / np.sum(window) #нормировка 
    Xdb = librosa.amplitude_to_db(np.abs(X), ref = 1.0, top_db = 80.0)
    #print(Xdb.shape)
    librosa.display.specshow(Xdb, sr=sr, hop_length = hop_length, x_axis='time', y_axis='log')
    plt.title(name)
    plt.colorbar()
    plt.show()
    
def fourie_plot(path, name):
    x, sr = sf.read(os.path.join(path, name))
    #x=x+0.1
    spectrum = np.fft.rfft(x)
    spectrum_db = librosa.amplitude_to_db(np.abs(spectrum), ref = 1.0, top_db = 80.0)
    plt.plot(np.fft.rfftfreq(x.shape[0], 1./sr), np.abs(spectrum_db)/x.shape[0])
    # rfftfreq сделает всю работу по преобразованию номеров элементов массива в герцы
    # нас интересует только спектр амплитуд, поэтому используем abs из numpy (действует на массивы поэлементно)
    # делим на число элементов, чтобы амплитуды были в милливольтах, а не в суммах Фурье. Проверить просто — постоянные составляющие должны совпадать в сгенерированном сигнале и в спектре
    plt.xlabel(u'Частота, Гц')
    plt.ylabel(u'дБ')
    plt.xlim(0, 5000)
    plt.title(name)
    plt.grid(True)
    plt.show()

def spectral_centroid(path, name):
    x, sr = sf.read(os.path.join(path, name))
    spectral_centroids = librosa.feature.spectral_centroid(x, sr=sr)[0]
    print(spectral_centroids.shape)
    # Вычисление временной переменной для визуализации
    plt.figure(figsize=(12, 4))
    frames = range(len(spectral_centroids))
    t = librosa.frames_to_time(frames)
    # Построение спектрального центроида вместе с формой волны
    librosa.display.waveplot(x, sr=sr, alpha=0.4)
    plt.title(name)
    plt.plot(t, normalize(spectral_centroids), color='b')
    plt.show()
   
#спектральный спад
def spectral_rolloff(path, name):
    x, sr = sf.read(os.path.join(path, name))
    spectral_rolloff = librosa.feature.spectral_rolloff(x+0.01, sr=sr)[0]
    frames = range(len(spectral_rolloff))
    t = librosa.frames_to_time(frames)
    plt.figure(figsize=(12, 4))
    librosa.display.waveplot(x, sr=sr, alpha=0.4)
    plt.title(name)
    plt.plot(t, normalize(spectral_rolloff), color='r')
    plt.show()

#спектральная ширина
def spectral_bandwidth(path, name):
    x, sr = sf.read(os.path.join(path, name))
    spectral_bandwidth_2 = librosa.feature.spectral_bandwidth(x+0.01, sr=sr)[0]
    spectral_bandwidth_3 = librosa.feature.spectral_bandwidth(x+0.01, sr=sr, p=3)[0]
    spectral_bandwidth_4 = librosa.feature.spectral_bandwidth(x+0.01, sr=sr, p=4)[0]
    frames = range(len(spectral_bandwidth_2))
    t = librosa.frames_to_time(frames)
    plt.figure(figsize=(15, 9))
    librosa.display.waveplot(x, sr=sr, alpha=0.4)
    plt.title(name)
    plt.plot(t, normalize(spectral_bandwidth_2), color='r')
    plt.plot(t, normalize(spectral_bandwidth_3), color='g')
    plt.plot(t, normalize(spectral_bandwidth_4), color='y')
    plt.legend(('p = 2', 'p = 3', 'p = 4'))
    plt.show()
    
#скорость (число) пересечений нуля
def zero_crossings(path, name):
    x, sr = sf.read(os.path.join(path, name))
    zero_crossings = librosa.zero_crossings(x[:], pad=False)
    print(sum(zero_crossings))  

#мел-частотные кепстральные коэффициенты
def mfcc_plot(path, name):    
    x, sr = sf.read(os.path.join(path, name))
    mfccs = librosa.feature.mfcc(x, sr=sr, n_mfcc = 50, dct_type = 2, norm = 'ortho')
    print(mfccs.shape)
    # Отображение MFCC:
    plt.figure(figsize=(15, 7))
    librosa.display.specshow(mfccs, sr=sr, x_axis='time')
    plt.title(name)
    plt.show()

#признаки цветности  
def chroma_stft(path, name):
    x, sr = sf.read(os.path.join(path, name))
    hop_length = 64
    chromagram = librosa.feature.chroma_stft(x, sr=sr, hop_length=hop_length)
    plt.figure(figsize=(15, 5))
    librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')
    plt.title(name)
    plt.show()

if __name__ == "__main__":  
    root_path = os.getcwd()
    for root, dirs, files in os.walk(os.path.join(root_path, "PIANO (CATEGORY - 01)")):
        for name in files:
            #signal_plot(root, name)
            #stft_plot(root, name)
            #fourie_plot(root, name)
            #spectral_centroid(root, name)
            #spectral_rolloff(root, name)
            #spectral_bandwidth(root, name)
            #zero_crossings(root, name)
            #mfcc_plot(root, name)
            chroma_stft(root, name)