import pygame as pg
import random
from os import path
from sprites_serial import *  # import sprites
from settings import *
import time
import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
import serial

#Variales Globales
tpause = 0
tpause1 = 0
taux = 0
time_count = 2
clock_s1 = 0
clock_s2 = 0
time_count1 = 0
time_count2 = 0
estadoEspera = 0
start_time1 = 0
changeTime = 0
count_p = 0
estado = "000000"
STOP = 0
manual_Mode = 0

#Inicializacion de vectores

#Vector que obtendra todos los datos del serial
contenido = np.zeros((0, 1), dtype=np.float)

#Vectores para leer las coordenadas del archivo
X = np.zeros((0, 1), dtype=np.float)
Y = np.zeros((0, 1), dtype=np.float)
iden_veh = np.zeros((0, 1), dtype=np.float)
#VectorGraficador = np.zeros((0, 1), dtype=np.float)
VectorGraficador = []

#Leer por serial
ruta = "SenalSensorSerial.txt"
excel_file = open("excel_File.txt","w")

Calibracion = np.zeros((0, 1), dtype=np.float)
cont = 0
Time = 0
n = 500  # 0.7ms -> n=500 #1ms -> n=
Bytes = 9
Sensor = 2

#Variables de control

#Valor detectado por los digitales
d1 = 0
d2 = 0
flanco = 0

#Cantidad de carros (pasado)
veh1 = 0
veh2 = 0

#Distancia del ultrasonido a los vehiculos
cola1 = 0
cola2 = 0

#Tiempo por semaforo (pasado)
TIME_1P = 0
TIME_2P = 0

#Deteccion de veh
bandera = 0

#Funciones de recepcion por serial----------------------------------------------------------------------------------------------------------------------------------------------
def EscribirArchivo(Valor):#, f2, f3, f4, d1, d2):

    f1 = Valor

    list(Valor)
    Valores = Valor.split(" ")

    if len(Valores) == 1:
        #f1 = str(Valores[0])
        out_file.write(f1 + " " + "\n")

        list(f1)
        # f1.insert(1,',')
        coma = f1.split('.')
        # coma.insert(1,',')
        f1 = ",".join(coma)
        # print(f1)
        excel_file.write(f1 + " " + "\n")
    else:
        if len(Valores) == 2:

            f1 = Valores[0]
            f2 = Valores[1]
            out_file.write(str(f1) + " " + str(f2) + " " + "\n")

            list(str(f1))
            coma = f1.split('.')
            f1 = ",".join(coma)
            list(str(f2))
            coma = f2.split('.')
            f2 = ",".join(coma)
            excel_file.write(f1 + " " + f2 + " " + "\n")
        else:
            if len(Valores) == 3:
                f1 = Valores[0]
                f2 = Valores[1]
                f3 = Valores[2]
                out_file.write(str(f1) + " " + str(f2) + " " + str(f3) + " " + "\n")

                list(str(f1))
                coma = f1.split('.')
                f1 = ",".join(coma)
                list(str(f2))
                coma = f2.split('.')
                f2 = ",".join(coma)
                list(str(f3))
                coma = f3.split('.')
                f3 = ",".join(coma)

                excel_file.write(f1 + " " + f2 + " " + f3 + " " + "\n")
            else:
                f1 = Valores[0]
                f2 = Valores[1]
                f3 = Valores[2]
                f4 = Valores[3]
                out_file.write(str(f1) + " " + str(f2) + " " + str(f3) + " " + str(f4) + " " + "\n")

                list(str(f1))
                coma = f1.split('.')
                f1 = ",".join(coma)
                list(str(f2))
                coma = f2.split('.')
                f2 = ",".join(coma)
                list(str(f3))
                coma = f3.split('.')
                f3 = ",".join(coma)
                list(str(f4))
                coma = f4.split('.')
                f4 = ",".join(coma)
                excel_file.write(f1 + " " + f2 + " " + f3 + " " + f4 + " " + "\n")

    # Se escriben en el archivo los vectores X y Y formando las coordenadas por filas
    #out_file.write(f1 + " " + f2 + " " + f3 + " " + f4 + " " + d1 + " " + d2 + "\n")


def DecodDig1(V):
    #01000000 es 64
    V = int(V)
    d = V & 64
    return d >> 6 #Falta shiftear 6 valores a la derecha

def DecodDig2(V):
    #00100000 es 32
    V = int(V)
    d = V & 32
    return d >> 5 #Falta shiftear 5 valores a la derecha

def DecodAnalogD(V1,V2):
    a=int(V1)
    b=int(V2)

    a1 = a & 0x1F#31
    b1 = b << 1
    c = a1 << 8
    d = b1 & 0x00FF#255
    d = c | d

    Analogico = d >> 1
    flotante = Analogico/4.2#*10/58

    return flotante



def DecodAnalogV(V1,V2):
    a=int(V1)
    b=int(V2)

    a1 = a & 0x1F#31
    b1 = b << 1
    c = a1 << 8
    d = b1 & 0x00FF#255
    d = c | d

    Analogico = d >> 1
    flotante = Analogico * 3.3 / ((2 ** 12) - 1)

    return flotante

def DecodificadorSerial(Paquete, Sensor):

    global d1,d2,cola1,cola2
    #"Paquete" es de 8 bytes, 1 byte por caracter
    if len(Paquete)== 2:
        f1 = DecodAnalogV(Paquete[0], Paquete[1])
        Valor = str(f1)
        EscribirArchivo(Valor)
    else:
        if len(Paquete) == 4:
            f1 = DecodAnalogV(Paquete[0], Paquete[1])
            f2 = DecodAnalogV(Paquete[2], Paquete[3])
            Valor = str(f1)+" "+str(f2)
            EscribirArchivo(Valor)
        else:
            if len(Paquete) == 6:
                f1 = DecodAnalogV(Paquete[0], Paquete[1])
                f2 = DecodAnalogV(Paquete[2], Paquete[3])
                #Distancia
                f3 = DecodAnalogD(Paquete[4], Paquete[5])
                Valor = str(f1) + " " + str(f2) + " " + str(int(f3))
                EscribirArchivo(Valor)
            else:
                f1 = DecodAnalogV(Paquete[0], Paquete[1])
                f2 = DecodAnalogV(Paquete[2], Paquete[3])
                #Distancia
                f3 = DecodAnalogD(Paquete[4], Paquete[5])
                f4 = DecodAnalogD(Paquete[6], Paquete[7])
                Valor = str(f1) + " " + str(f2) + " " + str(int(f3)) + " " + str(int(f4))
                EscribirArchivo(Valor)

    d1 = DecodDig1(Paquete[0])
    d2 = DecodDig2(Paquete[0])


    list(Valor)
    Valores = Valor.split(" ")
    cola1 = int(Valores[2])
    cola2 = int(Valores[3])
    if Sensor == 1:
        SensorAnalog = Valores[0]
    else:
        if Sensor == 2:
            SensorAnalog = Valores[1]
        else:
            if Sensor == 3:
                SensorAnalog = Valores[2]
                #cola1 = int(SensorAnalog)
            else:
                if Sensor == 4:
                    SensorAnalog = Valores[3]
                    #cola2 = int(SensorAnalog)

    return str(SensorAnalog) + " " +str(d1) + " " + str(d2)

#Interfaz-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Game():
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.ventana = pg.display.set_mode((ancho, largo))
        pg.display.set_caption(NAME)
        self.Clock = pg.time.Clock()
        self.running = True

    def new(self):
        # inicia un nuevo juego

        self.playing = True

        self.canal1=0
        self.canal2=0
        self.tiempos = ""
        #Ultima distancia del ultrasonido para detectar cola
        self.COLA_1 = 0
        self.COLA_2 = 0
        #Indicia el nivel de cola segun la distancia con el ultrasonido
        self.nivel_cola_1 = 0
        self.nivel_cola_2 = 0
        self.count = 0

        self.all_sprites = pg.sprite.Group()
        self.all_Buttons = pg.sprite.Group()
        self.all_LEDS1 = pg.sprite.Group()
        self.all_LEDS2 = pg.sprite.Group()
        self.all_Veh = pg.sprite.Group()

        self.inf_font = pg.font.Font(pg.font.match_font("times new roman"), 20)
        self.message_font = pg.font.Font(pg.font.match_font("times new roman"), 25)
        self.subTitle_font = pg.font.Font(pg.font.match_font("times new roman"), 30)
        self.title_font = pg.font.Font(pg.font.match_font("times new roman"), 40)

        self.Buttons = {"B0": Button(self, 800, 225, "Modo Manual", self.PRUEBA, 1, 1, 0,"red"),
                        "B1": Button(self, 700, 400, "Semaforo 1", self.PRUEBA, 0, 0, 1,"red"),
                        "B2": Button(self, 900, 400, "Semaforo 2", self.PRUEBA, 0, 0, 2,"red"),
                        "B_On_Off": Button(self, 800, 115, "", self.PRUEBA, 0, 1, 0,"blue")}

        self.semaforos = {"S1": Semaforo(self, "Semaforo 1", 225-100, 220, 1), #148,180
                          "S2": Semaforo(self, "Semaforo 2", 225+100, 220, 2)} #336,180

        self.maquina = MaquinaEstados(self, self.semaforos["S1"], self.semaforos["S2"], self.Buttons["B1"],
                                      self.Buttons["B2"])

        #Vehicle(self, 65, 400, "car", "Carro", num_s1[0])
        #Vehicle(self, 160, 400, "truck", "Camioneta", num_s1[1])

        #Vehicle(self, 270, 400, "car", "Carro", num_s2[0])
        #Vehicle(self, 375, 400, "truck", "Camioneta", num_s2[1])

    def run(self, start_time, TIME_1, TIME_2, Periodo):
        # game loop
        global changeTime, time_count2, time_count1, veh1, veh2, iden_veh, bandera
        while self.playing:
            self.Clock.tick(FPS)
            self.events(start_time)
            self.serial_data(start_time)
            self.countVeh()

            self.COLA_1 = int(cola1)
            self.COLA_2 = int(cola2)
            colas = self.cola()

            list(colas)
            c = colas.split(" ")

            self.nivel_cola_1 = c[0]
            self.nivel_cola_2 = c[1]


            if changeTime == 1:
                #Archivos por canal

                self.count += 1
                if estado == "100001":
                    bandera = 0
                elif estado == "001100":
                    bandera = 1

                if veh1 > 0 or veh2 > 0:
                    self.tiempos = self.controlSystem(TIME_1, TIME_2)

                else:
                    self.tiempos = str(TIME_1)+" "+str(TIME_2)
                    veh1 = self.canal1
                    veh2 = self.canal2

                    self.canal1 = 0
                    self.canal2 = 0
                #-----------------

                list(self.tiempos)
                T = self.tiempos.split(" ")

                TIME_1 = int(T[0])
                time_count1 = TIME_1
                TIME_2 = int(T[1])
                time_count2 = TIME_1

                Periodo = TIME_1 + TIME_2
                changeTime = 0

            self.update(start_time)
            self.drawing(start_time, TIME_1, TIME_2, Periodo)

    def controlSystem(self, TIME_1, TIME_2):
        global veh1,veh2,TIME_1P,TIME_2P
        #d1,d2,cola1,cola2
        #d1,cola2->self.canal1,self.COLA_2
        #d2,cola1->self.canal2,self.COLA_1
        time_1 = 0
        time_2 = 0
        Pquit = 0
        n = 2 #valor de division del tiempo agregado
        estado1 = "Mantenemos"
        estado2 = "Mantenemos"
        c1v = veh1
        c2v = veh2
        veh1 = veh1/TIME_1P
        veh2 = veh2/TIME_2P
        c1 = self.canal1
        c2 = self.canal2
        self.canal1 = self.canal1/TIME_1
        self.canal2 = self.canal2/TIME_2

        #Comparacion pasado
        if veh2 == self.canal2:
            estado2 = "Mantenemos"
        elif veh2 > self.canal2:
            estado2 = "Disminuimos"
        elif veh2 < self.canal2:
            estado2 = "Aumentamos"

        if veh1 == self.canal1:
            estado1 = "Mantenemos"
        elif veh1 > self.canal1:
            estado1 = "Disminuimos"
        elif veh1 < self.canal1:
            estado1 = "Aumentamos"

        if estado1 == "Mantenemos" and estado2 == "Mantenemos":

            #NO IMPORTA cual sea el caso, tiene el mismo tiempo del pasado, por haber pasado la misma cantidad de vehiculos
            tiempos = self.controlCola(estado1, estado2, TIME_1, TIME_2)
            list(tiempos)
            t = tiempos.split(" ")
            print("Tiempo queda igual")
            time_plus1 = 0
            time_plus2 = 0
            time_1 = int(t[0])
            time_2 = int(t[1])

        elif estado1 == "Disminuimos" and estado2 == "Disminuimos":
            if veh1 > 0:
                Pquit = abs(((veh1 - self.canal1) * 1) / veh1)
                time_plus1 = Pquit * TIME_1
            else:
                time_plus1 = 0

            if veh2 > 0:
                Pquit = abs(((veh2 - self.canal2) * 1) / veh2)
                time_plus2 = Pquit * TIME_2
            else:
                time_plus2 = 0

            tiempos = self.controlCola(estado1, estado2, time_plus1, time_plus2)
            list(tiempos)
            t = tiempos.split(" ")

            time_plus1 = int(t[0])
            time_plus2 = int(t[1])

            time_1 = TIME_1 - time_plus1/n
            time_2 = TIME_2 - time_plus2/n

        elif estado1 == "Disminuimos" and estado2 == "Aumentamos":

            if veh1 > 0:
                Pquit = abs(((veh1-self.canal1) * 1)/veh1)
                time_plus1 = Pquit * TIME_1
            else:
                time_plus1 = 0

            if veh2 > 0:
                Pquit = abs(((veh2 - self.canal2) * 1) / veh2)
                time_plus2 = Pquit * TIME_2
            else:
                time_plus2 = 0

            tiempos = self.controlCola(estado1, estado2, time_plus1, time_plus2)
            list(tiempos)
            t = tiempos.split(" ")

            time_plus1 = int(t[0])
            time_plus2 = int(t[1])

            time_1 = TIME_1 - time_plus1/n
            time_2 = TIME_2 + time_plus2/n

        elif estado1 == "Aumentamos" and estado2 == "Disminuimos":
            if veh1 > 0:
                Pquit = abs(((veh1-self.canal1) * 1)/veh1)
                time_plus1 = Pquit * TIME_1
            else:
                time_plus1 = 0

            if veh2 > 0:
                Pquit = abs(((veh2 - self.canal2) * 1) / veh2)
                time_plus2 = Pquit * TIME_2
            else:
                time_plus2 = 0

            tiempos = self.controlCola(estado1, estado2, time_plus1, time_plus2)
            list(tiempos)
            t = tiempos.split(" ")

            time_plus1 = int(t[0])
            time_plus2 = int(t[1])

            time_1 = TIME_1 + time_plus1/n
            time_2 = TIME_2 - time_plus2/n

        elif estado1 == "Aumentamos" and estado2 == "Aumentamos":
            if veh1 > 0:
                Pquit = abs(((veh1-self.canal1) * 1)/veh1)
                time_plus1 = Pquit * TIME_1
            else:
                time_plus1 = 0

            if veh2 > 0:
                Pquit = abs(((veh2 - self.canal2) * 1) / veh2)
                time_plus2 = Pquit * TIME_2
            else:
                time_plus2 = 0

            tiempos = self.controlCola(estado1, estado2, time_plus1, time_plus2)
            list(tiempos)
            t = tiempos.split(" ")

            time_plus1 = int(t[0])
            time_plus2 = int(t[1])

            time_1 = TIME_1 + time_plus1/n
            time_2 = TIME_2 + time_plus2/n

        elif estado1 == "Mantenemos" and estado2 == "Disminuimos":
            if veh2 > 0:
                Pquit = abs(((veh2 - self.canal2) * 1) / veh2)
                time_plus2 = Pquit * TIME_2
            else:
                time_plus2 = 0

            tiempos = self.controlCola(estado1, estado2, TIME_1, time_plus2)
            list(tiempos)
            t = tiempos.split(" ")

            time_plus1 = int(t[0])
            time_plus2 = int(t[1])

            time_1 = time_plus1
            time_2 = TIME_2 - time_plus2/n


        elif estado1 == "Mantenemos" and estado2 == "Aumentamos":
            if veh2 > 0:
                Pquit = abs(((veh2 - self.canal2) * 1) / veh2)
                time_plus2 = Pquit * TIME_2
            else:
                time_plus2 = 0
            print("time_plus2 antes de controlCola: "+str(time_plus2))
            tiempos = self.controlCola(estado1, estado2, TIME_1, time_plus2)
            list(tiempos)
            t = tiempos.split(" ")

            time_plus1 = int(t[0])
            time_plus2 = int(t[1])

            time_1 = time_plus1
            time_2 = TIME_2 + time_plus2/n

        elif estado1 == "Disminuimos" and estado2 == "Mantenemos":
            if veh1 > 0:
                Pquit = abs(((veh1-self.canal1) * 1)/veh1)
                time_plus1 = Pquit * TIME_1
            else:
                time_plus1 = 0
            tiempos = self.controlCola(estado1, estado2, time_plus1, TIME_2)
            list(tiempos)
            t = tiempos.split(" ")

            time_plus1 = int(t[0])
            time_plus2 = int(t[1])

            time_1 = TIME_1 - time_plus1/n
            time_2 = time_plus2

        elif estado1 == "Aumentamos" and estado2 == "Mantenemos":
            if veh1 > 0:
                Pquit = abs(((veh1-self.canal1) * 1)/veh1)
                time_plus1 = Pquit * TIME_1
            else:
                time_plus1 = 0

            tiempos = self.controlCola(estado1, estado2, time_plus1, TIME_2)
            list(tiempos)
            t = tiempos.split(" ")

            time_plus1 = int(t[0])
            time_plus2 = int(t[1])

            time_1 = TIME_1 + time_plus1/n
            time_2 = time_plus2

        if time_1 < 5:
            time_1 = 5
        if time_2 < 5:
            time_2 = 5

        TIME_1P = TIME_1
        TIME_2P = TIME_2
        veh1=c1
        veh2=c2
        self.canal1=0
        self.canal2=0
        self.COLA_1=0
        self.COLA_2=0

        return str(int(time_1))+" "+str(int(time_2))

    def controlCola(self,estado1, estado2, time_1, time_2):
        #Afecta al tiempo que se va a agregar
        time_1 = time_1
        time_2 = time_2

        colas = self.cola()
        list(colas)
        C = colas.split(" ")
        cola_1 = int(C[0])
        cola_2 = int(C[1])

        #Se alteran los estados agregar, excepto en el estado "Mantenemos" donde se altera el tiempo asignado

        if cola_2 == 0:
            time_1 = time_1

        elif cola_2 == 1:
            if estado1 == "Aumentamos":
                time_1 = 0.75 * time_1
            elif estado1 == "Mantenemos":
                time_1 = time_1
            elif estado1 == "Disminuimos":
                time_1 = 1 * time_1

        elif cola_2 == 2:
            if estado1 == "Aumentamos":
                time_1 = 0.5 * time_1
            elif estado1 == "Mantenemos":
                time_1 = time_1
            elif estado1 == "Disminuimos":
                time_1 = 1 * time_1

        elif cola_2 == 3:
            if estado1 == "Aumentamos":
                time_1 = 0.25 * time_1
            elif estado1 == "Mantenemos":
                time_1 = 0.8 * time_1
            elif estado1 == "Disminuimos":
                time_1 = 1.2 * time_1

        elif cola_2 == 4:
            if estado1 == "Aumentamos":
                time_1 = 0.0 * time_1
            elif estado1 == "Mantenemos":
                time_1 = 0.8 * time_1
            elif estado1 == "Disminuimos":
                time_1 = 1.3 * time_1

        if cola_1 == 0:
            time_2 = time_2

        elif cola_1 == 1:
            if estado2 == "Aumentamos":
                time_2 = 0.75 * time_2
            elif estado2 == "Mantenemos":
                time_2 = time_2
            elif estado2 == "Disminuimos":
                time_2 = 1 * time_2

        elif cola_1 == 2:
            if estado2 == "Aumentamos":
                time_2 = 0.5 * time_2
            elif estado2 == "Mantenemos":
                time_2 = time_2
            elif estado2 == "Disminuimos":
                time_2 = 1 * time_2

        elif cola_1 == 3:
            if estado2 == "Aumentamos":
                time_2 = 0.25 * time_2
            elif estado2 == "Mantenemos":
                time_2 = 0.8 * time_2
            elif estado2 == "Disminuimos":
                time_2 = 1.2 * time_2

        elif cola_1 == 4:
            if estado2 == "Aumentamos":
                time_2 = 0.0 * time_2
            elif estado2 == "Mantenemos":
                time_2 = 0.8 * time_2
            elif estado2 == "Disminuimos":
                time_2 = 1.3 * time_2


        return str(int(time_1)) + " " + str(int(time_2))

    def cola(self):
        #n=6
        #global nivel_1, nivel_2
        nivel_1 = 0
        nivel_2 = 0

        if self.COLA_1 < 27:
            nivel_1 = 1
            if self.COLA_1 < 21:
                nivel_1 = 2
                if self.COLA_1 < 15:
                    nivel_1 = 3
                    if self.COLA_1 < 8:
                        nivel_1 = 4
        elif self.COLA_1 >= 27:
            nivel_1 = 0

        if self.COLA_2 < 27:
            nivel_2 = 1
            if self.COLA_2 < 21:
                nivel_2 = 2
                if self.COLA_2 < 15:
                    nivel_2 = 3
                    if self.COLA_2 < 8:
                        nivel_2 = 4
        elif self.COLA_2 >= 27:
            nivel_2 = 0

        return str(nivel_1)+" "+str(nivel_2)


    def countVeh(self):
        global flanco, d1, d2
        if d1 == 1:
            if flanco == 0:
                self.canal1 += 1
                flanco = 1
        elif d2 == 0:
            flanco = 0

        if d2 == 1:
            if flanco == 0:
                self.canal2 += 1
                flanco = 1
        elif d1 == 0:
            flanco = 0

    def ESTADO(self,estado):
        ESTADO = 0
        if estado == "000000":
            ESTADO = 0  #0 en hexadecimal
        elif estado == "100001":
            ESTADO = 33 #21 en hexadecimal
        elif estado == "001100":
            ESTADO = 12 #C en hexadecimal
        elif estado == "010001":
            ESTADO = 17 #11 en hexadecimal
        elif estado == "001010":
            ESTADO = 10 #A en hexadecimal
        elif estado == "001001":
            ESTADO = 9  #9 en hexadecimal

        return ESTADO


    def serial_data(self,start_time):
        global contenido,VectorGraficador,X,Y,Calibracion,cont,n,Time,Bytes,Sensor, estado

        stop_time = time.time()
        Time = stop_time - start_time

        if ser.in_waiting > 1:

            Datos = ser.read(size=Bytes)

            while (Datos[0] < 244):
                print("Esperando cabecera")
                ser.reset_input_buffer()
                Datos = ser.read(size=Bytes)

            if Bytes == 3:
                aux = str(Datos[0]) + " " + str(Datos[1]) + " " + str(Datos[2])
                # Cabecera = 241
            else:
                if Bytes == 5:
                    aux = str(Datos[0]) + " " + str(Datos[1]) + " " + str(Datos[2]) + " " + str(Datos[3]) + " " + str(Datos[4])
                    # Cabecera = 242
                else:
                    if Bytes == 7:
                        aux = str(Datos[0]) + " " + str(Datos[1]) + " " + str(Datos[2]) + " " + str(Datos[3]) + " " + str(Datos[4]) + " " + str(Datos[5]) + " " + str(Datos[6])
                        # Cabecera = 243
                    else:
                        aux = str(Datos[0]) + " " + str(Datos[1]) + " " + str(Datos[2]) + " " + str(Datos[3]) + " " + str(Datos[4]) + " " + str(Datos[5]) + " " + str(Datos[6]) + " " + str(Datos[7]) + " " + str(Datos[8])
                        # Cabecera = 244

            # header = 241 con un solo analogico F1
            Paquetes = aux.split(" ")  # Cabecera ASCII 248
            Paquetes.pop(0)
            Valor = DecodificadorSerial(Paquetes, Sensor)
            list(Valor)
            valores = Valor.split(" ")
            valor = valores[0]

            # Lista
            valor = float(valor)

            VectorGraficador.append(valor)
            if (Time < 3):
                Calibracion = np.vstack([Calibracion, valor])
            elif (Time > 3 and Time < 3.2):
                print("Calibracion lista")
            #Envio del estado actual
            dat = self.ESTADO(estado)
            #print(type(dat))
            ser.write(bytearray([dat]))

    def events(self,start_time):
        # game loop events
        self.serial_data(start_time)
        global manual_Mode, estado, STOP, estadoEspera, tpause1, tpause, start_time1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing == True:
                    self.playing = False
                self.running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for button in self.all_Buttons:
                    button.checkClick(mouse_pos)
                    if button.activo == 1 and button.manual == 1:
                        manual_Mode = button.manualMode


            if self.Buttons["B_On_Off"].estado == "OFF":
                self.playing = False
                self.running = False

            if manual_Mode == 1:
                for button in self.all_Buttons:
                    button.setActivo()

                if estado == "000000":
                    if self.Buttons["B1"].estado == "ON":
                        estado = "100001"
                    elif self.Buttons["B2"].estado == "ON":
                        estado = "001100"

                elif estado == "100001":
                    if self.Buttons["B1"].estado == "OFF" or self.Buttons["B2"].estado == "ON":
                        estado = "010001"
                        STOP = 0
                        estadoEspera = 1
                        tpause1 = tpause
                        if self.Buttons["B1"].estado == "OFF":
                            STOP = 1
                    elif self.Buttons["B1"].estado == "ON" or self.Buttons["B2"].estado == "OFF":
                        estado = "100001"

                elif estado == "001100":
                    if self.Buttons["B1"].estado == "ON" or self.Buttons["B2"].estado == "OFF":
                        estado = "001010"
                        STOP = 0
                        estadoEspera = 1
                        tpause1 = tpause
                        if self.Buttons["B2"].estado == "OFF":
                            STOP = 1
                    elif self.Buttons["B2"].estado == "ON" or self.Buttons["B1"].estado == "OFF":
                        estado = "001100"

                elif estado == "001001":
                    if self.Buttons["B1"].estado == "ON":
                        estado = "100001"
                    elif self.Buttons["B2"].estado == "ON":
                        estado = "001100"
                    elif self.Buttons["B1"].estado == "OFF" or self.Buttons["B2"].estado == "OFF":
                        estado = "001001"

            else:
                for button in self.all_Buttons:
                    if button.manual != 1:
                        if button.control != 1:
                            button.setDesactivo()

            # Control automatico se hace en draw

            if event.type == pg.MOUSEBUTTONUP:
                # mouse_pos = pg.mouse.get_pos()

                for button in self.all_Buttons:
                    button.Onpull()

    def update(self,start_time):
        # game loop update
        self.serial_data(start_time)
        self.all_sprites.update()

    def drawing(self, start_time, TIME_1, TIME_2, Periodo):
        self.serial_data(start_time)

        global manual_Mode, estado, STOP, tpause1, tpause, estadoEspera, clock_s1, clock_s2, time_count1, time_count2, time_count, changeTime, cola1, cola2, Sensor#, nivel_2, nivel_1  # , taux

        pg.display.set_caption("{:.0f}".format(self.Clock.get_fps()))
        self.ventana.fill(BLACK)
        self.all_sprites.draw(self.ventana)
        self.draw_text(self.ventana, "Sistema de Monitoreo y Control de Vialidad", 550, 50, self.title_font, BLUE)#550, 50
        self.draw_text(self.ventana, "Semaforos", 225, 110, self.title_font, WHITE)#110
        self.draw_text(self.ventana, "Vehiculos por canal", 225, 320, self.title_font, WHITE)

        self.draw_text(self.ventana, self.semaforos["S1"].name, self.semaforos["S1"].posX, self.semaforos["S1"].posY - 50, self.message_font, WHITE)
        self.draw_text(self.ventana, self.semaforos["S2"].name, self.semaforos["S2"].posX, self.semaforos["S2"].posY - 50, self.message_font, WHITE)

        for button in self.all_Buttons:
            if button.activo == 1 or button.manual == 1:
                self.draw_text(self.ventana, button.description, button.rect.centerx, button.rect.centery - 50,
                               self.subTitle_font, WHITE)
                self.draw_text(self.ventana, button.estado, button.rect.centerx + 50, button.rect.centery,
                               self.inf_font, WHITE)
            else:
                button.setOFF()

        self.draw_text(self.ventana, "Canal 1", 225-70, 375, self.subTitle_font, WHITE)#subTitle_font
        self.draw_text(self.ventana, str(self.canal1), 225-70, 415, self.subTitle_font, WHITE)
        self.draw_text(self.ventana, "Canal 2", 225+70, 375, self.subTitle_font, WHITE)
        self.draw_text(self.ventana, str(self.canal2), 225+70, 415, self.subTitle_font, WHITE)
        self.draw_text(self.ventana, "Cola:", 225 - 170, 460, self.subTitle_font, WHITE)
        self.draw_text(self.ventana, str(self.nivel_cola_2), 225 + 70, 460, self.subTitle_font, WHITE)
        self.draw_text(self.ventana, str(self.nivel_cola_1), 225 - 70, 460, self.subTitle_font, WHITE)

        #for veh in self.all_Veh:
            #self.draw_text(self.ventana, veh.description, veh.rect.centerx, veh.rect.centery - 40, self.message_font, WHITE)
            #self.draw_text(self.ventana, veh.num, veh.rect.centerx, veh.rect.centery + 40, self.inf_font, WHITE)

        if manual_Mode == 1:
            self.draw_text(self.ventana, "Habilitar Semaforo por emergencia", 800, 290, self.message_font, WHITE)

        # if manual_Mode == 0 and estado!="000000":
        self.clock_semaforos(start_time, TIME_1, TIME_2, Periodo)

        # Modo automatico
        if manual_Mode == 0:
            if estado == "100001":

                if clock_s1 == 0:  # Marca el tiempo de entrada
                    clock_s1 = 1
                    tpause1 = tpause
                    time_count2 = TIME_1
                    time_count1 = TIME_1

                elif clock_s1 == 1:  # Mantiene en estado actual
                    estado = "100001"
                    clock_s1 = 1
                elif clock_s1 == 2:  # Estado siguiente
                    estado = "010001"
                    STOP = 0
                    estadoEspera = 1  # analogo de clock_s1
                    tpause1 = tpause
                    self.COLA_2 = int(cola2)
                    clock_s1 = 0

            elif estado == "001100":

                if clock_s2 == 0:  # Marca el tiempo de entrada
                    clock_s2 = 1
                    tpause1 = tpause
                    time_count1 = TIME_2
                    time_count2 = TIME_2

                elif clock_s2 == 1:  # Mantiene en estado actual
                    estado = "001100"
                    clock_s2 = 1
                elif clock_s2 == 2:  # Estado siguiente
                    estado = "001010"
                    STOP = 0
                    estadoEspera = 1
                    tpause1 = tpause
                    self.COLA_1 = int(cola1)
                    clock_s2 = 0

        if estado == "001010":

            if estadoEspera != 1:

                if STOP == 1:
                    estado = "001001"
                    STOP = 0

                elif STOP == 0:
                    estado = "100001"


        elif estado == "010001":

            if estadoEspera != 1:

                if STOP == 1:
                    estado = "001001"
                    STOP = 0

                elif STOP == 0:
                    estado = "001100"

        if estado == "100001":
            self.maquina.estado10()
        elif estado == "001100":
            self.maquina.estado01()
        elif estado == "001010":
            self.maquina.estadoT10()
        elif estado == "010001":
            self.maquina.estadoT01()
        elif estado == "001001":
            self.maquina.estadoOff()
        else:
            estado = "000000"

        pg.display.flip()


    def clock_semaforos(self, start_time, TIME_1, TIME_2, Periodo):

        global tpause, time_count1, time_count2, time_count, start_time1, estadoEspera, estado, tpause1, clock_s1, clock_s2, manual_Mode, changeTime, count_p
        stop_time = time.time()
        Time = stop_time - start_time
        reference = Time - tpause1

        if clock_s1 == 1:

            if reference > TIME_1 - time_count:
                clock_s1 = 2

        elif clock_s2 == 1:
            if reference > TIME_2 - time_count:
                clock_s2 = 2

        if reference > time_count + 1:
            estadoEspera = 0

        if Time > 1 and Time < 1.15:
            tpause = Time

        taux = Time - tpause

        if taux > 1 and taux < 1.2:
            if manual_Mode == 0 and estado != "000000":
                count_p += 1
            else:
                count_p = 0

            tpause = Time
            time_count1 = time_count1 - 1
            time_count2 = time_count2 - 1

        if time_count1 <= 0:
            time_count1 = 0

        if time_count2 <= 0:
            time_count2 = 0

        if Periodo == count_p:
            changeTime = 1
            count_p = 0

        if manual_Mode == 0 and estado != "000000":
            self.draw_time(time_count1, 225-100, 270)
            self.draw_time(time_count2, 225+100, 270)

    def draw_new_game_screen(self):
        # draw the new game screen
        pass

    def draw_game_over_screen(self):
        # draw the game over screen
        pass

    RED = (255, 0, 0)

    def draw_text(self, surface, value, x, y, font, color):
        # draw text in the screen
        text_image = font.render(value, True, color)
        rect = text_image.get_rect()
        rect.center = (x, y)
        surface.blit(text_image, rect)

    def draw_time(self, t, x, y):
        if t >= 0:
            num = str(t)
        else:
            num = "0"
            print("Error Tiempo negativo: " + str(t))
        self.draw_text(self.ventana, num, x, y, self.subTitle_font, WHITE)



    def PRUEBA(self):
        print("Estoy probando... Quien lea esto es marico")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

game = Game()
game.draw_new_game_screen()
start_time = time.time()

plt.ion()

#Tiempo inicial
TIME_1 = 15
TIME_1P = TIME_1
time_count1 = TIME_1
TIME_2 = 15
TIME_2P = TIME_2
time_count2 = TIME_2
Periodo = TIME_1 + TIME_2

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with open(ruta,"w") as out_file:
    with serial.Serial('COM5', 115200, timeout=1) as ser:
        print("El puerto serial usado es: ")
        print(ser)

        while game.running:
            game.Clock.tick(FPS)
            game.new()
            game.run(start_time, TIME_1, TIME_2, Periodo)  # ,tpause,taux)
            game.draw_game_over_screen()

excel_file.close()
pg.quit()

print("Finalice")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Leer Archivo
#Vectores para leer las coordenadas del archivo
X = np.zeros((0, 1), dtype=np.float)
Y = np.zeros((0, 1), dtype=np.float)
Yaux = np.zeros((0, 1), dtype=np.float)
VectorSplit = np.zeros((0, 1), dtype=np.float)

Vmin = 0
Vmax = 0

try:
    with open("SenalSensorSerial.txt", "r") as out_file:

        lines = out_file.readlines()

        for line in lines:
            Lectura = np.fromstring(line, dtype=float, sep=' ')

            if Sensor == 1:
                Y = np.vstack([Y, Lectura[0]])

            else:
                if Sensor == 2:
                    Y = np.vstack([Y, Lectura[1]])
                else:
                    if Sensor == 3:
                        Y = np.vstack([Y, Lectura[2]])
                    else:
                        Y = np.vstack([Y, Lectura[3]])

        if Sensor == 1 or Sensor == 2:

            print(Calibracion)
            Ref = np.mean(Calibracion)
            print("Valor referencia: " + str(Ref))
            Indmax = np.argmax(Y)
            Vmax=Y[Indmax]
            Vresta = (Vmax - Ref)/2
            Vcorte = Ref + Vresta

            #Todos los valores del vector que sean mayores al voltaje de corte
            Yaux = Y > Vcorte
            Ynew = Y[Yaux]

            #print(Y)
            print("Yaux:")
            print(Yaux)

            Ynew_ind = np.where(Yaux > 0)
            Xnew = Ynew_ind[0] #Ynew=Y[new_ind[0]]

            #-------Extra
            Yauxd = Y < Vcorte
            Xd = np.where(Yauxd > 0)
            Xdeteccion = Xd[0]
            #----------------
            print("Xdeteccion: "+str(Xdeteccion))
            print("Xnew: " + str(Xnew))

            #Separacion de picos
            Indmin = np.argmin(Ynew)
            Vmin=Ynew[Indmin]
            print("Vmin: " + str(Vmin))

            Ysepi = Ynew < (Vmin + 0.1)
            Ysepv = Ynew[Ysepi]
            Ysep_ind = np.where(Ysepi > 0)

            Xsep = Xnew[Ysep_ind[0]]
            print(Xsep)

            s=[]
            saux=[]
            s.append(0)

            for i in range(len(Xsep)-1):
                DifX = Xsep[i+1]-Xsep[i]
                if(DifX > 30):

                    s.append(i+1)

            #-------------Extra
            for i in range(len(Xdeteccion)-1):
                DifX = Xdeteccion[i + 1] - Xdeteccion[i]
                if (DifX > 10):
                    saux.append(i)
                    saux.append(i + 1)
            #--------------------------

            print("Longitud de saux: "+str(len(saux)))
            print("saux: "+str(saux))

            print("Longitud de s: "+str(len(s)))
            print("s: "+str(s))
            CanVeh = len(s)/2

            Xisep = []
            XSep = []
            XSepM = []
            XSEP = []
            YSEP = []

            #Extra
            Xisepaux=[]

            #El vector "s" contiene los valores limitrofes (indices de Xsep) de los minimos en el eje "x"

            for i in range(len(s)):
                Xisep.append(Xsep[s[i]]) #Valores de Xisep son los valores de los indices de Xsep respectivos (pares de minimos)

            #-----------Extra
            for i in range(len(saux)):
                Xisepaux.append(Xdeteccion[saux[i]])  # Valores de Xisep son los valores de los indices de Xsep respectivos (pares de minimos)

            #----------------------Extra
            listAux=[]
            for i in range(len(Xisepaux)):
                if i % 2 == 0:
                    listAux.append(Xisepaux[i]+1)
                else: listAux.append(Xisepaux[i]-1)
            #----------

            #Xisepaux=Xisep para la prueba
            for i in range(len(Xisepaux)):
                ind = np.where(Xnew == listAux[i])#(Xisepaux[i]))
                XSep.append(ind[0])

            for i in range(len(XSep)):
                if i % 2 != 0:
                    Dif = XSep[i] - XSep[i - 1]
                    if Dif > 35:
                        XSepM.append(XSep[i-1])
                        XSepM.append(XSep[i])
            i=0
            while(i<int(len(XSepM))):

                #print("El valor "+str(i)+" es: "+str(int(XSep[i])))

                XSEP.append(Xnew[int(XSepM[i]):int(XSepM[i+1])])#XSepM es XSep modificado
                YSEP.append(Ynew[int(XSepM[i]):int(XSepM[i+1])])

                i=i+2

            print("Han pasado "+str(len(XSEP))+" vehiculos")
            Media=[]
            Ind_max = []
            V_max = []
            vehiculos = []
            #-----------
            Media_Camioneta = 0 #Valor medio de las camionetas
            Media_Carro = 0 #Valor medio de los carros
            V_max_camioneta = 0 #Valor maximo de camioneta
            V_max_carro = 0 #Valor maximo de camioneta
            #-----------
            carro = 0
            camioneta = 0

            for i in range(len(YSEP)):
                Media.append(np.mean(YSEP[i]))
                Ind_max.append(np.argmax(YSEP[i]))
                V_max.append(YSEP[i][Ind_max[i]])
            print("Media: "+str(Media))
            print("Indice maximo: "+str(Ind_max))
            print("Valor maximo: "+str(V_max))

except:
    print("Error al abrir el archivo")
    out_file.close()

X=np.arange(0, len(Y))


with open("EjeTiempoX.txt", "w") as file:
    for i in range(len(X)):
        file.write(str(i) + " " + "\n")

TipoSensor = ""
Valor_Sensor = ""

if Sensor == 1 or Sensor == 2:
    TipoSensor = "Infrarrojo"
    Valor_Sensor = "Voltaje"
elif Sensor == 3 or Sensor == 4:
    TipoSensor = "Ultrasonido"
    Valor_Sensor = "Distancia"

#Graficar
plt.figure()
plt.clf()
plt.plot(X, Y, marker = '.')# c='b')
plt.axis('tight')
plt.title("Señal captada por sensor " + TipoSensor)
plt.legend()
plt.xlabel("Tiempo")
plt.ylabel(Valor_Sensor)
plt.draw()
plt.waitforbuttonpress()

#Histograma
pyl.figure()
pyl.hist(Y)
pyl.show()
pyl.title("Histograma de toda la señal")
pyl.waitforbuttonpress()

if Sensor == 1 or Sensor == 2:
    #Graficar
    plt.figure()
    plt.clf()
    plt.plot(Xnew, Ynew, marker = '.')# c='b')
    plt.axis('tight')
    plt.title("Señal filtrada captada por sensor infrarrojo")
    plt.legend()
    plt.draw()
    plt.waitforbuttonpress()

    #Histograma
    pyl.figure()
    pyl.hist(Ynew)
    pyl.show()
    pyl.title("Histograma de la señal de interes")
    pyl.waitforbuttonpress()

    #Graficar
    plt.figure()
    plt.clf()
    plt.plot(Xsep, Ysepv, marker='*')
    plt.axis('tight')
    plt.title("Valores minimos")
    plt.legend()
    #plt.show()
    plt.draw()
    plt.waitforbuttonpress()

    #Histograma
    pyl.figure()
    pyl.hist(Xsep, bins=100)
    pyl.show()
    pyl.title("Histograma de la señal de Valores minimos")
    pyl.waitforbuttonpress()

    # Graficar iterativamente
    for i in range(len(XSEP)):
        plt.figure()
        plt.plot(XSEP[i], YSEP[i], marker='.')  # c='b')
        plt.axis('tight')
        plt.title("Vehiculo numero: " + str(i+1))
        plt.ylim((Vmin-0.1), (Vmax+0.1))
        plt.draw()
        plt.waitforbuttonpress()

    # Graficar iterativamente
    for i in range(len(XSEP)):
        plt.figure()
        plt.hist(YSEP[i], bins=50)
        plt.title("Histograma del Vehiculo numero: " + str(i+1))
        plt.draw()
        plt.waitforbuttonpress()


