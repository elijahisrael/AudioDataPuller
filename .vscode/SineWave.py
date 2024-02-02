import numpy as np
import sounddevice as sd
from scipy.io import wavfile

# Set the parameters
duration = 3.0  # in seconds
sample_rate = 44100  # typical audio sample rate
frequency = 14000  # in Hertz

# Generate the time values
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate the sine wave
sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

# Play the sine wave
sd.play(sine_wave, sample_rate)
sd.wait()  # wait for the sound to finish playing

# Save the sine wave to a WAV file
wavfile.write("sine_wave_6000hz.wav", sample_rate, sine_wave)
