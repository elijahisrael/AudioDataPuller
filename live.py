import numpy as np
import sounddevice as sd
import threading
import queue
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

# Parameters for the Sine wave
duration = 20.0  # Total duration in seconds, used for modulo in continuous playback
sample_rate = 44100  # Sample rate in Hz
block_duration = 50 # length of block in ms
frequency = 1000  # Frequency of the sine wave in Hz
chunk_size = 256  # Number of samples per chunk
phase = 0.0
# Queue to store recorded audio data
audio_queue = queue.Queue()

# Continuous sine wave playback function

def play_sine_wave_continuous():
    global phase

    def callback(outdata, frames, time, status):
        global phase
        if status:
            print(status)
        t = np.arange(frames) / sample_rate
        outdata[:, 0] = np.sin(2 * np.pi * frequency * t + phase) * 0.5
        phase += 2 * np.pi * frequency * frames / sample_rate
        phase %= 2 * np.pi  # Keep phase in the [0, 2*pi] interval

    try:
        with sd.OutputStream(samplerate=sample_rate, channels=1, callback=callback):
            print("Starting continuous sine wave playback.")
            while not stop_flag.is_set():
                sd.sleep(block_duration)  # Sleep for a short period to prevent high CPU usage
    except Exception as e:
        print(f"Error during continuous playback: {e}")
    finally:
        print("Finished continuous sine wave playback.")

# Callback function for recording audio
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

# Function to start audio recording
def record_audio():
    with sd.InputStream(samplerate=sample_rate, blocksize=int(sample_rate * block_duration / 1000), channels=1, callback=audio_callback):
        while not stop_flag.is_set():
            sd.sleep(block_duration)

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
spectrogram_plot.setYRange(0,.02) # This changes the y axis range
spectrogram_curve = spectrogram_plot.plot(pen='y')

def update():
    if not audio_queue.empty():
        audio_data = audio_queue.get()
        num_samples = len(audio_data)
        # Update waveform plot
        waveform_curve.setData(audio_data[:, 0])

        # Update spectrogram plot
        X = np.fft.rfft(audio_data[:, 0])
        X_mag = np.abs(X) / num_samples
        f_plot = np.linspace(0, sample_rate / 2, num_samples // 2)
        spectrogram_curve.setData(f_plot, X_mag[:num_samples // 2])

# Set the update function to run periodically
timer = QTimer()
timer.timeout.connect(update)
timer.start(block_duration) # in milliseconds

# Flag to signal when to stop threads
stop_flag = threading.Event()

# Start the sine wave and recording in separate threads
playback_thread = threading.Thread(target=play_sine_wave_continuous)
recording_thread = threading.Thread(target=record_audio)
playback_thread.start()
recording_thread.start()

# Start Qt event loop
if __name__ == '__main__':
    app.exec_()
    stop_flag.set()
    playback_thread.join()
    recording_thread.join()
