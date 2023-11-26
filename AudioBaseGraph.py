import pandas as ps
import numpy as np
import matplotlib.pylab as pl
from glob import glob
import librosa 
import librosa.display 
import IPython.display as ipd
import os

# Defines the directory
output_directory = os.path.join(os.path.expanduser("~"), "Desktop", "wav_files")

# Use glob to get a list of all WAV files in the directory
Audio_Files = glob(os.path.join(output_directory, '*.wav'))

# Check if there are any WAV files
if Audio_Files:
    print("List of WAV files:")
    for audio_file in Audio_Files:
      print(audio_file)

      # Play Audio File
      ipd.Audio(audio_file)

      # Load audio using librosa
      audio, sr = librosa.load(audio_file)

      #Graphing the audio into the base audio graph
      print(f'y: {audio[:10]}')
      print(f'shape y: {audio.shape}')
      print(f'SR: {sr}')

      # Trim audio using librosa
      audio_trim, _ = librosa.effects.trim(audio, top_db = 100000)
      ps.Series(audio_trim).plot(figsize=(10, 5), title="Microphone Audio Data")
      pl.show()

else:
  print("No WAV files found in the specified directory.")