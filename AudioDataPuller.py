import wave
import pyaudio

Chunk_Size = 1024
Format = pyaudio.paInt16
Channels = 1
Rate = 44100

P = pyaudio.PyAudio()

Audio_Stream = P.open(format = Format, channels = Channels, rate = Rate, input = True, frames_per_buffer = Chunk_Size)

print("Start recording:")

Frames = []
Time = 3
for _ in range(0, int(Rate / Chunk_Size * Time)):
  data = Audio_Stream.read(Chunk_Size) 
  Frames.append(data)

print("Recording stopped")

Audio_Stream.stop_stream()
Audio_Stream.close()
P.terminate()

Wave_File = wave.open("Wave_Output.wav", "wb")
Wave_File.setnchannels(Channels)
Wave_File.setsampwidth(P.get_sample_size(Format))
Wave_File.setframerate(Rate)
Wave_File.writeframes(b''.join(Frames))
Wave_File.close()
