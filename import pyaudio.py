import pyaudio
import wave
import pandas as ps
import numpy as np
import matplotlib.pylab as pl
import seaborn as sn
from glob import glob
import librosa 
import librosa.display 
import IPython.display as ipd

def main(): 
Audio_Files = glob('')

# Play Audio File
ipd.Audio(Audio_Files[0])

y, SR = librosa.load(Audio_Files[0])
print(f'y: {y[:10]}')
print(f'shape y: {y, shape}')
print(f'SR: {SR}')

ps.Series(y).plot(fig_size = (10,5), 1w = 1, Adata_title = "Microphone Audio Data: ") 
pl.show()
