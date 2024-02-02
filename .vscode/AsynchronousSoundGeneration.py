import asyncio
import numpy as np
import sounddevice as sd

async def generate_sine_wave(duration, sample_rate, frequency):
    # Generate the time values
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Generate the sine wave
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

    return sine_wave

async def play_sound(sine_wave, sample_rate):
    sd.play(sine_wave, sample_rate, blocking=True)

async def main():
    duration = 3.0  # in seconds
    sample_rate = 44100  # typical audio sample rate
    frequency = 6000  # in Hertz

    sine_wave = await generate_sine_wave(duration, sample_rate, frequency)
    await play_sound(sine_wave, sample_rate)

if __name__ == "__main__":
    asyncio.run(main())
