from glob import glob
import librosa 
import librosa.display 
import IPython.display as ipd
import os
import playsound as playsound

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

      #plays audio file through speaker
      audio, sr = librosa.load(audio_file)
      playsound.playsound(audio_file)

else:
  print("No WAV files found in the specified directory.")
