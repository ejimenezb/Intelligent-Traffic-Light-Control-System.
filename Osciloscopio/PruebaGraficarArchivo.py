#Eladio Jimenez 13-10699
#Kheyter Chassaigne 13-10274
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

#Prueba para escribir y leer archivo

plt.ion()
n=100

#------------------------------------------
#Inicializacion de vectores

#Vector que obtendra todos los datos del serial
contenido = np.zeros((0, 1), dtype=np.float)

#Vectores para leer las coordenadas del archivo
X = np.zeros((0, 1), dtype=np.float)
Y = np.zeros((0, 1), dtype=np.float)

#Simulacion de recepcion del serial (Se llena un vector)

#Revertir Protocolo
#0xFF 0xDDAAAAA

#Llenado de vector de coordenadas
for i in range(0,n):
    contenido = np.vstack([contenido, i])

#Pasamos el vector "contenido" a bytes
ts = contenido.tostring()#En bytes

#Pasamos "ts" que esta en bytes a una lista de floats
cont= np.fromstring(ts,dtype=np.float) #En floats

#Pasamos la lista de floats a una lista de strings
TS = [str(elem) for elem in cont]
#La funcion TS=" ".join(TS) #Necesita que el contenido de la lista sean strings y asi los concatena
#print(TS)

#------------------------------------------

#Nombre del archivo
ruta = "SenalSensor.txt"

#Escribir archivo

f=open(ruta, "w")

print(ts)
print(TS)
print(contenido)
print(cont)

for i in range(0,n):
    #Se escriben en el archivo los vectores X y Y formando las coordenadas por filas
    f.write(TS[i]+" "+TS[i]+"\n")
f.close()

#Leer Archivo

try:
    f=open(ruta,"r")
except:
    print("Error al abrir el archivo")
    f.close()

lines = f.readlines()

for line in lines:
    Lectura = np.fromstring(line, dtype=float, sep=' ')
    #print ('Leyendo')
    #print(Lectura)
    X = np.vstack([X, Lectura[0]])
    Y = np.vstack([Y, Lectura[1]])
    #coord=line.split() para esto se deberia leer la linea en vez de el vector
f.close()

#Graficar
plt.figure(1)
plt.clf()

#v= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#v = np.vstack([v,v])
v=np.arange(0,10000)

aux=np.arange(0, len(Y))


print(aux)
print(Y)


y=np.sin(v)
plt.plot(X, Y, c='b')#, label="Señal captada")
#plt.plot(X, Y, marker='.', c='b', linewidth=0)#, label="Señal captada")
plt.axis('tight')#equal')
plt.title("Señal captada por los sensores")
plt.legend()
#plt.show()
plt.draw()
plt.waitforbuttonpress()