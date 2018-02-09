#Eladio Jimenez 13-10699
#Kheyter Chassaigne 13-10274
import cv2
import numpy as np
import matplotlib.pyplot as plt
import serial

#Ciclo{
#Recibir por serial contenido
#Decodificar
#Graficar
#Guardar en archivo
#}

def Graficar(X, Y):

    plt.plot(X, Y, c='b')  # plt.plot(X, Y, marker='.', c='b', linewidth=0)#, label="Señal captada")
    plt.axis('tight')  # equal')
    plt.title("Señal captada por los sensores")
    plt.legend()
    plt.draw()
    plt.waitforbuttonpress()

def EscribirArchivo(f1, f2, f3, f4, d1, d2):

    f1 = str(f1, 'UTF-8')
    f2 = str(f2, 'UTF-8')
    f3 = str(f3, 'UTF-8')
    f4 = str(f4, 'UTF-8')
    d1 = str(d1, 'UTF-8')
    d2 = str(d2, 'UTF-8')

    # Se escriben en el archivo los vectores X y Y formando las coordenadas por filas
    out_file.write(f1 + " " + f2 + " " + f3 + " " + f4 + " " + d1 + " " + d2 + "\n")


def DecodDig1(V):
    #01000000 es 64
    d = V & 64
    return d >> 6 #Falta shiftear 6 valores a la derecha

def DecodDig2(V):
    #00100000 es 32
    d = V & 32
    return d >> 5 #Falta shiftear 5 valores a la derecha


def DecodAnalog(V1,V2):

    a = np.fromstring(V1, dtype=np.int)
    b = np.fromstring(V2, dtype=np.int)
    Analogico = ((2 ** 7) * (a & 31) + b)

    flotante = Analogico * 3.3 / ((2 ** 12) - 1)

    return flotante

def DecodificadorSerial(Paquete, cont):

    #"Paquete" es de 8 bytes, 1 byte por caracter

    f1 = DecodAnalog(Paquete[0], Paquete[1])
    f2 = DecodAnalog(Paquete[2], Paquete[3])
    f3 = DecodAnalog(Paquete[4], Paquete[5])
    f4 = DecodAnalog(Paquete[6], Paquete[7])

    d1 = DecodDig1(Paquete[0])
    d2 = DecodDig2(Paquete[1])

    #Escribir en archivo
    EscribirArchivo(f1, f2, f3, f4, d1, d2)

    X = cont
    Y = f1 #Asigno el que quiera graficar

    #Graficar
    Graficar(X, Y)

    #Escribir en un archivo todos los valores de los analogicos y digitales por columna
    #Columnas: f1 f2 f3 f4 d1 d2




plt.ion()
plt.figure(1)
plt.clf()

cont = 0

ser = serial.Serial('COM5')     # open serial port
print(ser.name)                 # check which port was really used
with open("SenalSensorSerial.txt","w") as out_file:
    with serial.Serial('COM5', 115200, timeout=1) as ser:

        start_time = time.time()

        while( time < 5 ):

            stop_time = time.time()
            time = stop_time - start_time

            if( ser.in_waiting > 1):

                Datos = ser.read(ser.in_waiting)
                StringDatos = str(Datos, 'UTF-8')
                Paquetes = StringDatos.split("º")#Cabecera
                for i in range(Paquetes):
                    DecodificadorSerial(Paquetes[i], cont)
                    cont++

                #plt.waitforbuttonpress()
