# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 21:21:18 2020

@author: aleks1212
"""
import os
import numpy as np
import librosa
#import matplotlib.pyplot as plt
import librosa.display
import librosa.util
import soundfile as sf

def trimmer_handler(path, name):
    x, sr = sf.read(os.path.join(path, name))
    x = trimmer(x)
    x_norm = librosa.util.normalize(x)
    sf.write(os.path.join(path, name), x_norm, sr)
      
def trimmer(x): 
    delta = 60  #количество интервалов на которые делим
    t = 2       #секунды длительность после обрезки
    space = x.shape[0] // delta
    mean_arr = [np.mean(np.abs(x[space * s : space * (s + 1)])) for s in range(delta)]
    s_max = np.argmax(mean_arr)
    for s in range(s_max - 1, 0, -1):
        if mean_arr[s] < 0.1 * mean_arr[s_max]:
            x = x[space * (s + 1) :]
            break
    if x.shape[0] >= t * space * delta // 3:
        x = x[: t * space * delta // 3]
    else:
        n = t * space * delta // 3 - x.shape[0]
        x = np.pad(x, (0, n), mode = 'constant')
    return x

if __name__ == "__main__":  
    root_path = os.getcwd()
    for root, dirs, files in os.walk(root_path):
        if root != root_path:
            for name in files:
                trimmer_handler(root, name)
                print(f"trimmered {name}")

    
