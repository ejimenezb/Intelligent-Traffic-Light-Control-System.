import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
from scipy.fftpack import fft, fftfreq

"""
n = 2 ** 6  # Número de intervalos
f = 400.0  # Hz
dt = 1 / (f * 16)  # Espaciado, 16 puntos por período
t = np.linspace(0, (n - 1) * dt, n)  # Intervalo de tiempo en segundos
y = np.sin(2 * pi * f * t) - 0.5 * np.sin(2 * pi * 2 * f * t)  # Señal
plt.figure()
plt.plot(t, y)
plt.plot(t, y, 'ko')
plt.xlabel('Tiempo (s)')
plt.ylabel('$y(t)$')
#plt.show()
plt.waitforbuttonpress()

Y = fft(y) / n  # Normalizada
frq = fftfreq(n, dt)  # Recuperamos las frecuencias
plt.figure()
plt.vlines(frq, 0, Y.imag)  # Representamos la parte imaginaria
plt.annotate(s=u'f = 400 Hz', xy=(400.0, -0.5), xytext=(400.0 + 1000.0, -0.5 - 0.35), arrowprops=dict(arrowstyle = "->"))
plt.annotate(s=u'f = -400 Hz', xy=(-400.0, 0.5), xytext=(-400.0 - 2000.0, 0.5 + 0.15), arrowprops=dict(arrowstyle = "->"))
plt.annotate(s=u'f = 800 Hz', xy=(800.0, 0.25), xytext=(800.0 + 600.0, 0.25 + 0.35), arrowprops=dict(arrowstyle = "->"))
plt.annotate(s=u'f = -800 Hz', xy=(-800.0, -0.25), xytext=(-800.0 - 1000.0, -0.25 - 0.35), arrowprops=dict(arrowstyle = "->"))
plt.ylim(-1, 1)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Im($Y$)')
#plt.show()
plt.waitforbuttonpress()

n2 = 2 ** 5
t2 = np.linspace(0, 0.012, n2)  # Intervalo de tiempo en segundos
dt2 = t2[1] - t2[0]
y2 = np.sin(2 * pi * f * t2) - 0.5 * np.sin(2 * pi * 2 * f * t2)  # Señal
Y2 = fft(y2) / n2  # Transformada normalizada
frq2 = fftfreq(n2, dt2)
fig = plt.figure(figsize=(6, 8))
ax1 = fig.add_subplot(211)
ax1.plot(t2, y2)
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('$y_2(t)$')
ax2 = fig.add_subplot(212)
ax2.vlines(frq2, 0, Y2.imag)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Im($Y_2$)')
#plt.show()
plt.waitforbuttonpress()

t3 = np.linspace(0, 0.012 + 9 * dt2, 10 * n2)  # Intervalo de tiempo en segundos
y3 = np.append(y2, np.zeros(9 * n2))  # Señal
Y3 = fft(y3) / (10 * n2)  # Transformada normalizada
frq3 = fftfreq(10 * n2, dt2)
fig = plt.figure(figsize=(6, 8))
ax1 = fig.add_subplot(211)
ax1.plot(t3, y3)
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('$y_3(t)$')
ax2 = fig.add_subplot(212)
ax2.vlines(frq3, 0, Y3.imag)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Im($Y_3$)')
#plt.show()
plt.waitforbuttonpress()
"""

#ARCHIVO------------------------------------------------------------

Y = np.zeros((0, 1), dtype=np.float)
try:
    with open("SenalSensorSerial_ruido0.txt", "r") as out_file:
        lines = out_file.readlines()
        for line in lines:
            Lectura = np.fromstring(line, dtype=float, sep=' ')
            Y = np.vstack([Y, Lectura[1]])
except:
    print("Error al abrir el archivo")
    out_file.close()
#--------------------------------------------------------------------
#Y=Y-2
#n4 = 2 ** 8
#t4 = np.linspace(0, 0.05, n4)
t4 = np.linspace(0, 14.110, len(Y))
print(len(Y))
dt4 = t4[1] - t4[0]
###y4 = np.sin(2 * pi * f * t4) - 0.5 * np.sin(2 * pi * 2 * f * t4)
##y5 = y4 * np.blackman(n4)
#y5 = Y * np.blackman(len(Y))
#t4 = np.linspace(0, 0.12 + 4 * dt4, 5 * n4)
t4 = np.linspace(0, 70.56 + 4*dt4, 5 * len(Y))
#y4 = np.append(y4, np.zeros(4 * n4))
y4 = np.append(Y, np.zeros(4*len(Y)))
##y5 = np.append(y5, np.zeros(4 * n4))
#y5 = np.append(y5, np.zeros(len(Y)))
#Y4 = fft(y4) / (5 * n4)
Y4 = fft(y4) / (5*len(Y))#(5 * n4)
##Y5 = fft(y5) / (5 * n4)
#Y5 = fft(y5) / (2 * len(Y))
#frq4 = fftfreq(5 * n4, dt4)
frq4 = fftfreq(5*len(Y), 1/4000)#dt4)
#frq4 = np.linspace(0, 5*len(Y), 1/1000)
fig = plt.figure(figsize=(6, 8))
ax1 = fig.add_subplot(411)
ax1.plot(t4, y4)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('$y_4(t)$')
ax2 = fig.add_subplot(412)
#ax2.vlines(frq4, 0, abs(Y4))  # Espectro de amplitud
ax2.plot(frq4, abs(Y4))  # Espectro de amplitud
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Abs($Y_4$)')
plt.xlim(-1000,1000)

ax3 = fig.add_subplot(413)
ax3.vlines(frq4, 0, abs(Y4))  # Espectro de amplitud
#ax2.plot(frq4, abs(Y4))  # Espectro de amplitud
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Abs($Y_4$)')
plt.xlim(-1000,1000)

#plt.xlim(-10, 10)
#ax3 = fig.add_subplot(413)
#ax3.plot(t4, y5)
#plt.xlabel('Frecuencia (Hz)')
#plt.ylabel('$y_5(t)$')
#ax4 = fig.add_subplot(414)
#ax4.vlines(frq4, 0, abs(Y5))  # Espectro de amplitud
#plt.xlabel('Frecuencia (Hz)')
#plt.ylabel('Abs($Y_5$)')
#plt.show()
plt.waitforbuttonpress()


#ARCHIVO------------------------------------------------------------

Y = np.zeros((0, 1), dtype=np.float)
try:
    with open("SenalSensorSerial_ruido1.txt", "r") as out_file:
        lines = out_file.readlines()
        for line in lines:
            Lectura = np.fromstring(line, dtype=float, sep=' ')
            Y = np.vstack([Y, Lectura[1]])
except:
    print("Error al abrir el archivo")
    out_file.close()
#--------------------------------------------------------------------
#Y=Y-2
#n4 = 2 ** 8
#t4 = np.linspace(0, 0.05, n4)
t4 = np.linspace(0, 130, len(Y))
print(len(Y))
dt4 = t4[1] - t4[0]
###y4 = np.sin(2 * pi * f * t4) - 0.5 * np.sin(2 * pi * 2 * f * t4)
##y5 = y4 * np.blackman(n4)
#y5 = Y * np.blackman(len(Y))
#t4 = np.linspace(0, 0.12 + 4 * dt4, 5 * n4)
t4 = np.linspace(0, 70.56 + 4*dt4, 5 * len(Y))
#y4 = np.append(y4, np.zeros(4 * n4))
y4 = np.append(Y, np.zeros(4*len(Y)))
##y5 = np.append(y5, np.zeros(4 * n4))
#y5 = np.append(y5, np.zeros(len(Y)))
#Y4 = fft(y4) / (5 * n4)
Y4 = fft(y4) / (5*len(Y))#(5 * n4)
##Y5 = fft(y5) / (5 * n4)
#Y5 = fft(y5) / (2 * len(Y))
#frq4 = fftfreq(5 * n4, dt4)
frq4 = fftfreq(5*len(Y), 1/4000)#dt4)
#frq4 = np.linspace(0, 5*len(Y), 1/1000)
fig = plt.figure(figsize=(6, 8))
ax1 = fig.add_subplot(411)
ax1.plot(t4, y4)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('$y_4(t)$')
ax2 = fig.add_subplot(412)
#ax2.vlines(frq4, 0, abs(Y4))  # Espectro de amplitud
ax2.plot(frq4, abs(Y4))  # Espectro de amplitud
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Abs($Y_4$)')
plt.xlim(-1000,1000)

ax3 = fig.add_subplot(413)
ax3.vlines(frq4, 0, abs(Y4))  # Espectro de amplitud
#ax2.plot(frq4, abs(Y4))  # Espectro de amplitud
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Abs($Y_4$)')
plt.xlim(-1000,1000)

#plt.xlim(-10, 10)
#ax3 = fig.add_subplot(413)
#ax3.plot(t4, y5)
#plt.xlabel('Frecuencia (Hz)')
#plt.ylabel('$y_5(t)$')
#ax4 = fig.add_subplot(414)
#ax4.vlines(frq4, 0, abs(Y5))  # Espectro de amplitud
#plt.xlabel('Frecuencia (Hz)')
#plt.ylabel('Abs($Y_5$)')
#plt.show()
plt.waitforbuttonpress()


#ARCHIVO------------------------------------------------------------

Y = np.zeros((0, 1), dtype=np.float)
try:
    with open("SenalSensorSerial_ruido2.txt", "r") as out_file:
        lines = out_file.readlines()
        for line in lines:
            Lectura = np.fromstring(line, dtype=float, sep=' ')
            Y = np.vstack([Y, Lectura[1]])
except:
    print("Error al abrir el archivo")
    out_file.close()
#--------------------------------------------------------------------
#Y=Y-2
#n4 = 2 ** 8
#t4 = np.linspace(0, 0.05, n4)
t4 = np.linspace(0, 1996, len(Y))
print(len(Y))
dt4 = t4[1] - t4[0]
###y4 = np.sin(2 * pi * f * t4) - 0.5 * np.sin(2 * pi * 2 * f * t4)
##y5 = y4 * np.blackman(n4)
#y5 = Y * np.blackman(len(Y))
#t4 = np.linspace(0, 0.12 + 4 * dt4, 5 * n4)
t4 = np.linspace(0, 70.56 + 4*dt4, 5 * len(Y))
#y4 = np.append(y4, np.zeros(4 * n4))
y4 = np.append(Y, np.zeros(4*len(Y)))
##y5 = np.append(y5, np.zeros(4 * n4))
#y5 = np.append(y5, np.zeros(len(Y)))
#Y4 = fft(y4) / (5 * n4)
Y4 = fft(y4) / (5*len(Y))#(5 * n4)
##Y5 = fft(y5) / (5 * n4)
#Y5 = fft(y5) / (2 * len(Y))
#frq4 = fftfreq(5 * n4, dt4)
frq4 = fftfreq(5*len(Y), 1/4000)#dt4)
#frq4 = np.linspace(0, 5*len(Y), 1/1000)
fig = plt.figure(figsize=(6, 8))
ax1 = fig.add_subplot(411)
ax1.plot(t4, y4)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('$y_4(t)$')
ax2 = fig.add_subplot(412)
#ax2.vlines(frq4, 0, abs(Y4))  # Espectro de amplitud
ax2.plot(frq4, abs(Y4))  # Espectro de amplitud
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Abs($Y_4$)')
plt.xlim(-1000,1000)

ax3 = fig.add_subplot(413)
ax3.vlines(frq4, 0, abs(Y4))  # Espectro de amplitud
#ax2.plot(frq4, abs(Y4))  # Espectro de amplitud
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Abs($Y_4$)')
plt.xlim(-1000,1000)

#plt.xlim(-10, 10)
#ax3 = fig.add_subplot(413)
#ax3.plot(t4, y5)
#plt.xlabel('Frecuencia (Hz)')
#plt.ylabel('$y_5(t)$')
#ax4 = fig.add_subplot(414)
#ax4.vlines(frq4, 0, abs(Y5))  # Espectro de amplitud
#plt.xlabel('Frecuencia (Hz)')
#plt.ylabel('Abs($Y_5$)')
plt.show()
#plt.waitforbuttonpress()