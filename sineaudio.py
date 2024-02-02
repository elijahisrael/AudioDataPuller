import numpy as np
import sounddevice as sd

sample_rate = 44100  # Sample rate in Hz
frequency = 440  # Frequency of the sine wave in Hz (A4 pitch)
duration = 5.0  # Duration in seconds

# Generate the sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
sine_wave = np.sin(2 * np.pi * frequency * t)

# Play the sine wave
sd.play(sine_wave, sample_rate)
sd.wait()  # Wait for the playback to finish
