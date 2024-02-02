import numpy as np
import sounddevice as sd
import threading
import queue
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

# Parameters for the Sine wave
duration = 20.0  # Total duration in seconds
sample_rate = 44100  # Sample rate in Hz
frequency = 19000  # Frequency of the sine wave in Hz
chunk_size = 1024  # Number of samples per chunk

# Queue to store recorded audio data
audio_queue = queue.Queue()

# Function to play the sine wave

def play_sine_wave():
    print("Starting sine wave playback")
    duration_seconds = int(duration * sample_rate)
    sine_wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, duration_seconds, endpoint=False))
    sine_wave *= 0.5  # Adjust the amplitude if necessary

    try:
        sd.play(sine_wave, sample_rate)
        sd.wait()  # You can try removing this line to see if it makes a difference
    except Exception as e:
        print(f"Error during playback: {e}")
    
    if stop_flag.is_set():
        print("Stopping sine wave playback")
    print("Finished sine wave playback")

# Callback function for recording audio
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

# Function to start audio recording
def record_audio():
    with sd.InputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
        while not stop_flag.is_set():
            sd.sleep(int(duration * 1000))

# Create a pyqtgraph application
app = QApplication([])

# Create the main window and layout
win = pg.GraphicsLayoutWidget(show=True, title="Real-time Audio Plot")
win.resize(1000,600)
win.setWindowTitle('Real-time Audio Plot')

# Create two plots
waveform_plot = win.addPlot(title="Waveform")
waveform_curve = waveform_plot.plot(pen='y')
win.nextRow()
spectrogram_plot = win.addPlot(title="Spectrogram")
spectrogram_curve = spectrogram_plot.plot(pen='y')

def update():
    if not audio_queue.empty():
        audio_data = audio_queue.get()
        num_samples = len(audio_data)

        # Update waveform plot
        waveform_curve.setData(audio_data[:, 0])

        # Update spectrogram plot
        X = np.fft.fft(audio_data[:, 0])
        X_mag = np.abs(X) / num_samples
        f_plot = np.linspace(0, sample_rate / 2, num_samples // 2)
        spectrogram_curve.setData(f_plot, X_mag[:num_samples // 2])

# Set the update function to run periodically
timer = QTimer()
timer.timeout.connect(update)
timer.start(100) # in milliseconds

# Flag to signal when to stop threads
stop_flag = threading.Event()

# Start the sine wave and recording in separate threads
playback_thread = threading.Thread(target=play_sine_wave)
recording_thread = threading.Thread(target=record_audio)
playback_thread.start()
recording_thread.start()

# Start Qt event loop
if __name__ == '__main__':
    app.exec_()
