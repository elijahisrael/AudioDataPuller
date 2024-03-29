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

     # Fourier Transformed audio data
    X_T = librosa.stft(audio)
    Audio_Db = librosa.amplitude_to_db(np.abs(X_T), ref = np.max)
    Audio_Db.shape

    # Plotting the Fourier Transformed data
    fig, ax = pl.subplots(figsize = (10, 5))
    img = librosa.display.specshow(Audio_Db,
                                     x_axis = "time",
                                     y_axis = "log",
                                     ax = ax)
    print("Shape of audio_db:", Audio_Db.shape)
    ax.set_title("Fourier Spectogram", fontsize = 20)
    fig.colorbar(img, ax = ax, format = '%0.2f')
    pl.show()

else:
  print("No WAV files found in the specified directory.")
