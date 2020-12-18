# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 18:38:54 2020

@author: aleks1212
"""
 
"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import pyaudio
import wave

import time
import os
#import shutil

import pandas as pd


def savewav(foldername, filename):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 3
    
    workpath = os.getcwd()
    dirpath = os.path.join(workpath, foldername)
    filepath = os.path.join(dirpath, filename)
    
    if not(os.path.exists(dirpath)): #создать директорию, если не было
        try:
            os.makedirs(dirpath)
        except OSError:
            print ("Создать директорию %s не удалось" % dirpath)
            return
        else:
            print ("Успешно создана директория %s " % dirpath)
    
    if(os.path.exists(filepath)): #удалить файл если существовал
        try:
            os.remove(filepath)
        except OSError as e:
            print("Ошибка: %s : %s" % (dirpath, e.strerror))
            return
        
        
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("* recording")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
def printdelay(second):
    for i in range(second, -1, -1):
        time.sleep(1)
        print(f'Осталось {i} секунд')
        
def readnotes():
    gamma = pd.read_csv('notes.csv', sep = ';', header = None)
    gamma = gamma[0].tolist()
    notes = list()
    for i in range(2, 3): #7):
        for j in range(12):
            notes.append(gamma[j] + str(i))
    notes.append('C3')
    return notes

def readinstrument():
    data = pd.read_csv('instruments.csv', sep = ';', header = None, encoding= 'unicode_escape')
    
    try:
        f = open('progress.txt', 'r')
        num = int(f.read())
    except Exception as e:
            print(f"Ошибка: {e.strerror}")
            return  
        
    instrument = list()
    instrument.append(data[0][num-1])
    instrument.append(data[1][num-1])
    instrument.append(data[2][num-1])
    
    instrument[1] = instrument[1].replace(':', '-')
    instrument[2] = instrument[2].replace(':', '-')
    
    try:    
        num += 1
        f = open('progress.txt', 'w')
        f.write(str(num))
        f.close()
    except Exception as e:
            print(f"Ошибка: {e.strerror}")
            return      
      
    return instrument
    
        
notes = readnotes()
#print(notes)
instrument = readinstrument()

foldername = os.path.join(instrument[1], str(instrument[0]) + '-' + instrument[2])

for i, note in enumerate(notes):
    filename = str(i + 1) + '-' + note + '_' + instrument[2] + '.wav'
    print(f'Запись файла {filename}: ')
    printdelay(1)
    savewav(foldername, filename)

