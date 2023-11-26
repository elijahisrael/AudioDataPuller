import pyaudio
import wave
import pandas as ps
import numpy as np
import matplotlib.pylab as pl
import seaborn 
from glob import glob
import librosa 
import librosa.display 
import IPython.display as ipd
import os
import playsound as playsound

Chunk_Size = 1024
Format = pyaudio.paInt16
Channels = 1
Rate = 44100

P = pyaudio.PyAudio()

Audio_Stream = P.open(format = Format, channels = Channels, rate = Rate, input = True, frames_per_buffer = Chunk_Size)

print("Start recording:")

Frames = []
Time = 10
for _ in range(0, int(Rate / Chunk_Size * (Time + 1))):
  data = Audio_Stream.read(Chunk_Size) 
  Frames.append(data)

print("Recording stopped")

Audio_Stream.stop_stream()
Audio_Stream.close()
P.terminate()

output_directory = os.path.join(os.path.expanduser("~"), "Desktop", "wav_files")

if not os.path.exists(output_directory):
  os.makedirs(output_directory)

wav_file_path = os.path.join(output_directory, "Wave_Output.wav")

Wave_File = wave.open(wav_file_path, "wb")
Wave_File.setnchannels(Channels)
Wave_File.setsampwidth(P.get_sample_size(Format))
Wave_File.setframerate(Rate)
Wave_File.writeframes(b''.join(Frames))
Wave_File.close()

print(f"Audio saved to '{wav_file_path}'.")

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

      print(f'y: {audio[:10]}')
      print(f'shape y: {audio.shape}')
      print(f'SR: {sr}')

      # Trim audio using librosa
      audio_trim, _ = librosa.effects.trim(audio, top_db = 100000)
      ps.Series(audio_trim).plot(figsize=(10, 5), title="Microphone Audio Data")
      pl.show()

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

      #plays audio
      ipd.Audio(audio_file)
      audio, sr = librosa.load(audio_file)
      playsound.playsound(audio_file)

else:
  print("No WAV files found in the specified directory.")
