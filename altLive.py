from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy_garden.graph import Graph
from kivy_garden.graph import MeshLinePlot
from kivy.core.window import Window
import numpy as np
import sounddevice as sd
import threading
import queue

# Parameters for the Sine wave
sample_rate = 44100  # Sample rate in Hz
frequency = 1000  # Frequency of the sine wave in Hz
chunk_size = 1024  # Number of samples per chunk
phase = 0.0
# Queue to store recorded audio data
audio_queue = queue.Queue()

# Flag to signal when to stop threads
stop_flag = threading.Event()

class AudioPlotterApp(App):

    def build(self):
        self.main_layout = BoxLayout(orientation='vertical')
        self.waveform_graph = Graph(xlabel='Sample', ylabel='Amplitude', x_ticks_minor=5,
                                    x_ticks_major=25, y_ticks_major=0.25,
                                    y_grid_label=True, x_grid_label=True, padding=5,
                                    x_grid=True, y_grid=True, xmin=0, xmax=chunk_size, ymin=-1, ymax=1)
        self.spectrogram_graph = Graph(xlabel='Frequency', ylabel='Magnitude', x_ticks_minor=5,
                                       x_ticks_major=5000, y_ticks_major=1,
                                       y_grid_label=True, x_grid_label=True, padding=5,
                                       x_grid=True, y_grid=True, xmin=0, xmax=sample_rate//2, ymin=0, ymax=100)
        
        self.waveform_plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.spectrogram_plot = MeshLinePlot(color=[0, 1, 0, 1])
        
        self.waveform_graph.add_plot(self.waveform_plot)
        self.spectrogram_graph.add_plot(self.spectrogram_plot)

        self.main_layout.add_widget(self.waveform_graph)
        self.main_layout.add_widget(self.spectrogram_graph)

        Clock.schedule_interval(self.update, 0.01)  # Update at 10 Hz
        return self.main_layout

    def update(self, dt):
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            num_samples = len(audio_data)

            # Update waveform plot
            self.waveform_plot.points = [(i, audio_data[i][0]) for i in range(num_samples)]

            # Update spectrogram plot
            X = np.fft.fft(audio_data[:, 0])
            X_mag = np.abs(X) / num_samples
            f_plot = np.linspace(0, sample_rate / 2, num_samples // 2)
            self.spectrogram_plot.points = [(f_plot[i], X_mag[i]) for i in range(num_samples // 2)]

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
                sd.sleep(100)  # Sleep for a short period to prevent high CPU usage
    except Exception as e:
        print(f"Error during continuous playback: {e}")
    finally:
        print("Finished continuous sine wave playback.")

def record_audio():
    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        audio_queue.put(indata.copy())

    with sd.InputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
        while not stop_flag.is_set():
            sd.sleep(100)

if __name__ == '__main__':
    playback_thread = threading.Thread(target=play_sine_wave_continuous)
    recording_thread = threading.Thread(target=record_audio)
    playback_thread.start()
    recording_thread.start()
    
    AudioPlotterApp().run()
    
    stop_flag.set()
    playback_thread.join()
    recording_thread.join()