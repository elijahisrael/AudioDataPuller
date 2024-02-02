import numpy as np
import matplotlib.pyplot as plt

# making time signal
fs = 2000
tstep = 1 / fs
f0 = 100

N = int(10 * fs / f0)

t = np.linspace(0, (N-1) * tstep, N)
fstep = fs / N
f = np.linspace(0, (N-1) * fstep, N)

y = 1 * np.sin(2 * np.pi * f0 * t) + 4 * np.sin(2 * np.pi * 2 * f0 * t)

# making spectrogram
X = np.fft.fft(y)
X_mag = np.abs(X) / N

f_plot = f[0:int(N/2+1)]
X_mag_plot = X_mag[0:int(N/2+1)]
X_mag_plot[0] = X_mag_plot[0] / 2

# plot
fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
ax1.plot(t, y, '.-')
ax2.plot(f_plot, X_mag_plot, '.-')
ax1.set_xlabel('Time [s]')
ax2.set_xlabel('Freq [Hz]')
ax1.grid()
ax2.grid()
plt.show()