import wave
import pyaudio
import os


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