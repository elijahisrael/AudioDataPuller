from math import e
import numpy as np
import sounddevice as sd
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Sets the parametersfor the Sine wave
duration = 20.0 # seconds
sample_rate = 44100 # sample rate
frequency = 19000 # Hz

# Generate time values (x-axis)
time = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)

# Generate sine wave values (y-axis)
amplitude = np.sin(time)  # You can adjust the amplitude

sine_wave = amplitude * np.sin(2 * np.pi* frequency * time)

#play the sine wave
sd.play(sine_wave, sample_rate)
sd.wait()

# Plot the sine wave
plt.plot(time, amplitude)
plt.title('Sine Wave')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()