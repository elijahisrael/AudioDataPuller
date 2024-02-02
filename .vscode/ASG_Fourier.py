import asyncio
import numpy as np
import sounddevice as sd
import librosa
import librosa.display
import matplotlib.pyplot as plt

async def generate_sine_wave(duration, sample_rate, frequency):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return sine_wave

async def play_and_record(sine_wave, sample_rate, duration):
    # Create an array to store recorded audio
    recorded_audio = np.zeros(int(sample_rate * duration))

    # Define the callback function for recording
    def callback(indata, frames, time, status):
        if status:
            print(f"Error in recording: {status}")
        recorded_audio[:frames] = indata[:, 0]

    # Start recording in the background
    stream = sd.InputStream(callback=callback, channels=1, samplerate=sample_rate)
    with stream:
        # Play the sine wave while recording
        sd.play(sine_wave, sample_rate, blocking=True)

    return recorded_audio

def plot_fourier_transform(signal, sample_rate):
    X_T = librosa.stft(signal)
    audio_db = librosa.amplitude_to_db(np.abs(X_T), ref=np.max)

    fig, ax = plt.subplots(figsize=(10, 5))
    img = librosa.display.specshow(audio_db, x_axis="time", y_axis="log", ax=ax)

    # Adjust the color scale (vmin and vmax) for better visualization
    img.set_clim(vmin=-80, vmax=0)

    ax.set_title("Fourier Spectrogram", fontsize=20)
    fig.colorbar(img, ax=ax, format='%0.2f')
    plt.show()

async def main():
    duration = 5.0  # in seconds
    sample_rate = 44100  # typical audio sample rate
    frequency = 6000  # in Hertz

    sine_wave = await generate_sine_wave(duration, sample_rate, frequency)
    recorded_audio = await play_and_record(sine_wave, sample_rate, duration)

    # Plot the Fourier transform of the recorded audio
    plot_fourier_transform(recorded_audio, sample_rate)

if __name__ == "__main__":
    asyncio.run(main())
