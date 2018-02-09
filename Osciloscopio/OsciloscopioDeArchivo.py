#Eladio Jimenez 13-10699
#Kheyter Chassaigne 13-10274
import cv2
import numpy as np
import matplotlib.pyplot as plt
import serial
import time

#Escribe Señal en archivo y la lee para ser graficada

def EscribirArchivo(f1):#, f2, f3, f4, d1, d2):

    f1 = str(f1)#, 'UTF-8')
    #f2 = str(f2)#, 'UTF-8')
    #f3 = str(f3)#, 'UTF-8')
    #f4 = str(f4)#, 'UTF-8')
    #d1 = str(d1)#, 'UTF-8')
    #d2 = str(d2)#, 'UTF-8')

    out_file.write(f1 + " " + "\n")

    # Se escriben en el archivo los vectores X y Y formando las coordenadas por filas
    #out_file.write(f1 + " " + f2 + " " + f3 + " " + f4 + " " + d1 + " " + d2 + "\n")


def DecodDig1(V):
    #01000000 es 64

    V = np.fromstring(V, dtype=np.int8)

    d = V[0] & 64
    return d >> 6 #Falta shiftear 6 valores a la derecha

def DecodDig2(V):
    #00100000 es 32

    V = np.fromstring(V, dtype=np.int8)

    d = V[0] & 32
    return d >> 5 #Falta shiftear 5 valores a la derecha


def DecodAnalog(V1,V2):

    #print('V1'+" = "+str(V1)+"  Su tipo es: ")
    #print(type(V1))

    a=int(V1)
    b=int(V2)
    #print(type(a_))
    #a = np.fromstring(V1, dtype=np.uint8)
    #print('a = ' + str(a)+ " "+ str(a[0]))
    #b = np.fromstring(V2, dtype=np.int8)
    #print('b = '+str(b[0]))

    a1 = a & 0x1F#31
    b1 = b << 1
    c = a1 << 8
    d = b1 & 0x00FF#255
    d = c | d

    Analogico = d >> 1
    print(Analogico)
    #Analogico = ((2 ** 7) * (a[0] & 31) + b[0])

    flotante = Analogico * 3.3 / ((2 ** 12) - 1)

    return flotante

def DecodificadorSerial(Paquete):

    #"Paquete" es de 8 bytes, 1 byte por caracter

    f1 = DecodAnalog(Paquete[0], Paquete[1])
    #f2 = DecodAnalog(Paquete[2], Paquete[3])
    #f3 = DecodAnalog(Paquete[4], Paquete[5])
    #f4 = DecodAnalog(Paquete[6], Paquete[7])

    #d1 = DecodDig1(Paquete[0])
    #d2 = DecodDig2(Paquete[1])

    #Escribir en archivo
    #Escribir en un archivo todos los valores de los analogicos y digitales por columna
    #Columnas: f1 f2 f3 f4 d1 d2
    EscribirArchivo(f1)#, f2, f3, f4, d1, d2)

#---------------------------------------------------------------------------------------
plt.ion()

#Inicializacion de vectores

#Vector que obtendra todos los datos del serial
contenido = np.zeros((0, 1), dtype=np.float)

#Vectores para leer las coordenadas del archivo
X = np.zeros((0, 1), dtype=np.float)
Y = np.zeros((0, 1), dtype=np.float)

#Leer por serial
ruta = "SenalSensorSerial.txt"

with open(ruta,"w") as out_file:
    with serial.Serial('COM5', 115200, timeout=1) as ser:
        print("El puerto serial usado es: ")
        print(ser)
        start_time = time.time()
        cont=0
        Time = 0
        while( Time < 10 ):

            stop_time = time.time()
            Time = stop_time - start_time

            if( ser.in_waiting > 1):

                Datos = ser.read(size=3)#ser.in_waiting)
                aux = str(Datos[0])+" "+str(Datos[1])+" "+str(Datos[2])
                #print(type(Datos))
                #StringDatos = str(Datos)
                #print(type(StringDatos))
                ##v_ = StringDatos.encode('utf-8')

                #print(aux)
                #print(Datos)

                #header = 241 con un solo analogico
                Paquetes = aux.split(" ") #Cabecera ASCII 248
                Paquetes.pop(0)
                #print(Paquetes[0])+" "+Paquetes[1])
                DecodificadorSerial(Paquetes)
                #for i in range(len(Paquetes)):
                    ##X = np.vstack([X, cont])
                    #print("Paquete:" + str(i))
                    #print(Paquetes[i])
                    #print("Decodificacion:")
                    #DecodificadorSerial(Paquetes[i])


                    #cont = cont + 1
#------------------------------------------

#Leer Archivo

try:
    with open("SenalSensorSerial.txt", "r") as out_file:
        lines = out_file.readlines()

        for line in lines:
            Lectura = np.fromstring(line, dtype=float, sep=' ')
            Y = np.vstack([Y, Lectura[0]])


except:
    print("Error al abrir el archivo")
    out_file.close()

X=np.arange(0, len(Y))
print(len(X))
print(len(Y))

#Graficar
plt.figure(1)
plt.clf()
plt.plot(X, Y, marker = '.')# c='b')
plt.axis('tight')
plt.title("Señal captada por los sensores")
plt.legend()
#plt.show()
plt.draw()
plt.waitforbuttonpress()