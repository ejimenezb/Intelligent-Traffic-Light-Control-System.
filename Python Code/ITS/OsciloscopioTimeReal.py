#Eladio Jimenez 13-10699
#Kheyter Chassaigne 13-10274
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
import serial
import time

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
    #print(Analogico)
    #Analogico = ((2 ** 7) * (a[0] & 31) + b[0])

    flotante = Analogico * 3.3 / ((2 ** 12) - 1)

    return flotante

def DecodificadorSerial(Paquete, Sensor):

    #"Paquete" es de 8 bytes, 1 byte por caracter
    if len(Paquete)== 2:
        f1 = DecodAnalog(Paquete[0], Paquete[1])
        Valor = str(f1)
        EscribirArchivo(Valor)
    else:
        if len(Paquete) == 4:
            f1 = DecodAnalog(Paquete[0], Paquete[1])
            f2 = DecodAnalog(Paquete[2], Paquete[3])
            Valor = str(f1)+" "+str(f2)
            EscribirArchivo(Valor)
        else:
            if len(Paquete) == 6:
                f1 = DecodAnalog(Paquete[0], Paquete[1])
                f2 = DecodAnalog(Paquete[2], Paquete[3])
                f3 = DecodAnalog(Paquete[4], Paquete[5])
                Valor = str(f1) + " " + str(f2) + " " + str(f3)
                EscribirArchivo(Valor)
            else:
                f1 = DecodAnalog(Paquete[0], Paquete[1])
                f2 = DecodAnalog(Paquete[2], Paquete[3])
                f3 = DecodAnalog(Paquete[4], Paquete[5])
                f4 = DecodAnalog(Paquete[6], Paquete[7])
                Valor = str(f1) + " " + str(f2) + " " + str(f3) + " " + str(f4)
                EscribirArchivo(Valor)

    d1 = DecodDig1(Paquete[0])
    d2 = DecodDig2(Paquete[0])

    #f2 = DecodAnalog(Paquete[2], Paquete[3])
    #f3 = DecodAnalog(Paquete[4], Paquete[5])
    #f4 = DecodAnalog(Paquete[6], Paquete[7])
    #Escribir en archivo
    #Escribir en un archivo todos los valores de los analogicos y digitales por columna
    #Columnas: f1 f2 f3 f4 d1 d2
    #, f2, f3, f4, d1, d2)

    list(Valor)
    Valores = Valor.split(" ")

    if Sensor == 1:
        SensorAnalog = Valores[0]
    else:
        if Sensor == 2:
            SensorAnalog = Valores[1]
        else:
            if Sensor == 3:
                SensorAnalog = Valores[2]
            else:
                if Sensor == 4:
                    SensorAnalog = Valores[3]

    return str(SensorAnalog) + " " +str(d1) + " " + str(d2)
#---------------------------------------------------------------------------------------
plt.ion()

#Inicializacion de vectores

#Vector que obtendra todos los datos del serial
contenido = np.zeros((0, 1), dtype=np.float)

#Vectores para leer las coordenadas del archivo
X = np.zeros((0, 1), dtype=np.float)
Y = np.zeros((0, 1), dtype=np.float)
#VectorGraficador = np.zeros((0, 1), dtype=np.float)
VectorGraficador = []

#Leer por serial
ruta = "SenalSensorSerial.txt"
excel_file = open("excel_File.txt","w")

with open(ruta,"w") as out_file:
    with serial.Serial('COM5', 115200, timeout=1) as ser:
        print("El puerto serial usado es: ")
        print(ser)

        Calibracion = np.zeros((0, 1), dtype=np.float)

        start_time = time.time()
        cont=0
        Time = 0
        n=300 #0.7ms -> n=500 #1ms -> n=
        Bytes = 9
        Sensor = 1
        while( Time < 40  ):

            stop_time = time.time()
            Time = stop_time - start_time

            if ser.in_waiting > 1:

                Datos = ser.read(size = Bytes)#ser.in_waiting)

                while(Datos[0] < 244):
                    print("Esperando cabecera")
                    ser.reset_input_buffer()
                    Datos = ser.read(size=Bytes)

                if Bytes == 3:
                    aux = str(Datos[0])+" "+str(Datos[1])+" "+str(Datos[2])
                    #Cabecera = 241
                else:
                    if Bytes == 5:
                        aux = str(Datos[0]) + " " + str(Datos[1]) + " " + str(Datos[2]) + " " + str(Datos[3]) + " " + str(Datos[4])
                        #Cabecera = 242
                    else:
                        if Bytes == 7:
                            aux = str(Datos[0]) + " " + str(Datos[1]) + " " + str(Datos[2]) + " " + str(Datos[3]) + " " + str(Datos[4])+ " " + str(Datos[5]) + " " + str(Datos[6])
                            #Cabecera = 243
                        else:
                            aux = str(Datos[0]) + " " + str(Datos[1]) + " " + str(Datos[2]) + " " + str(Datos[3]) + " " + str(Datos[4])+ " " + str(Datos[5]) + " " + str(Datos[6])+ " " + str(Datos[7]) + " " + str(Datos[8])
                            #Cabecera = 244

                #header = 241 con un solo analogico F1
                Paquetes = aux.split(" ") #Cabecera ASCII 248
                Paquetes.pop(0)

                #print(type(Paquetes))
                ###print(Paquetes[0]+" "+Paquetes[1])
                Valor = DecodificadorSerial(Paquetes, Sensor)
                #print(Valor)

                list(Valor)
                valores = Valor.split(" ")

                #print(valores[0])
                valor = valores[0]
                print(valor)
                #Pila
                #VectorGraficador = np.vstack([VectorGraficador, valor])

                #Intentos de lista
                #VectorGraficador += [valor]
                #VectorGraficador = list()

                #Lista
                valor = float(valor)
                VectorGraficador.append(valor)
                if(Time<3):
                    Calibracion = np.vstack([Calibracion, valor])
                if(Time>3 and Time<3.2):
                    print("Calibracion lista")

                #print(type(VectorGraficador))
                #print(len(VectorGraficador))
                #print(VectorGraficador)


                if( len(VectorGraficador) > n):
                    Y=VectorGraficador[0:n]#[-9:]
                    nmedio=n/2
                    nmedio=int(nmedio)

                    #print(nmedio)
                    del VectorGraficador[0:nmedio]
                    #print(type(VectorGraficador))
                    #print(Y)
                    X=np.arange(0, len(Y))
                    #n=len(X)-1

                    #n=0; n = n+10

                # Graficar
                    plt.figure(1)
                    plt.clf()
                    plt.plot(X, Y, marker='.')  # c='b')
                    plt.axis('tight')
                    plt.title("Señal captada por los sensores")
                    plt.legend()
                    plt.ylim(-0.3, 3.3)
                    # plt.show()
                    plt.draw()
                    plt.waitforbuttonpress(0.02)

                #if(len(VectorGraficador))


#------

excel_file.close()
#Leer Archivo
#Vectores para leer las coordenadas del archivo
X = np.zeros((0, 1), dtype=np.float)
Y = np.zeros((0, 1), dtype=np.float)
Yaux = np.zeros((0, 1), dtype=np.float)
VectorSplit = np.zeros((0, 1), dtype=np.float)
#XSEP = np.zeros((0, 1), dtype=np.float)
#XSEP = np.vstack([XSEP, Valor a agregar])

try:
    with open("SenalSensorSerial.txt", "r") as out_file:

        #print("HOLA")
        #print("Aqui toy")
        lines = out_file.readlines()

        for line in lines:
            Lectura = np.fromstring(line, dtype=float, sep=' ')

            if Sensor == 1:
                Y = np.vstack([Y, Lectura[0]])
                #print(Lectura[0])
            else:
                if Sensor == 2:
                    Y = np.vstack([Y, Lectura[1]])
                else:
                    if Sensor == 3:
                        Y = np.vstack([Y, Lectura[2]])
                    else:
                        Y = np.vstack([Y, Lectura[3]])
        #print("Aqui toy")
        print(Calibracion)
        ##vector = np.arange(0, 4)
        #print(Calibracion)
        Ref = np.mean(Calibracion)
        #print("Aqui toy 3")
        #prom = np.mean(Y)
        print("Valor referencia: " + str(Ref))
        Indmax = np.argmax(Y)
        Vmax=Y[Indmax]
        #print("Vmax: "+str(Vmax))
        Vresta = (Vmax - Ref)/2
        #print("Vresta: "+str(Vresta))
        ##print(type(prom))
        ##print(type(Vresta))
        Vcorte = Ref + Vresta
        #print("El valor de corte sera: " + str(Vcorte))
        #print("La longitud del vector original es: "+str(len(Y)))

        #Todos los valores del vector que sean mayores al voltaje de corte
        Yaux = Y > Vcorte
        Ynew = Y[Yaux]

        #print(Y)
        print("Yaux:")
        #print(type(Yaux))
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

        ##Ynew=np.nonzero(Yaux)
        #print("La longitud del nuevo vector es: "+str(len(Ynew)))
        #print("Ynew_ind: ")
        #print(Ynew_ind)
        #print("Y[Ynew_ind]: ")
        #print(Y[Ynew_ind[0]])
        #print("Zeros: Y[Ynew_ind[1]] ")
        #print(Y[Ynew_ind[1]])
        #print("Ynew: ")
        #print(Ynew)

        #Separacion de picos
        Indmin = np.argmin(Ynew)
        Vmin=Ynew[Indmin]
        print("Vmin: " + str(Vmin))

        Ysepi = Ynew < (Vmin + 0.1)
        Ysepv = Ynew[Ysepi]
        Ysep_ind = np.where(Ysepi > 0)

        Xsep = Xnew[Ysep_ind[0]]#Ynew[Ysep_ind[0]] #Valores minimos en "x"
        print(Xsep)

        s=[]
        saux=[]
        s.append(0)

        for i in range(len(Xsep)-1):
            DifX = Xsep[i+1]-Xsep[i]
            if(DifX > 30):
                #s.append(i)
                s.append(i+1)
        #179 espacios entre min
        #227 espacios entre min

        #170 estapacion entre min (Bien)
        #



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
        #--------

        #print("Vamos bien")

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

        print("Vamos bien")
        print("CantVeh: "+str(CanVeh))
        i=0
        print("CanVeh en entero es: ")
        print(int(CanVeh))

        print("Vamos bien: " + str(i) + " Hasta: " + str(int(CanVeh)))

        print("Xisep: " + str(Xisep))
        print("Xisepaux: " + str(Xisepaux))

        print("XSep: " + str(XSep))
        print("Su longitud es: " + str(len(XSep)))

        print("XSepM: " + str(XSepM))
        print("Su longitud es: " + str(len(XSepM)))

        #print(type(Xnew))
        #print(type(VectorSplit))
        #imin = int(XSep[i])
        #imax = int(XSep[i+1])
        #print("Indices: min es "+str(imin)+" max es "+str(imax))
        #VectorSplit = Xnew[imin:imax]
        #print("VectorSplit de prueba: "+str(VectorSplit))

        #s=saux
        while(i<int(len(XSepM))):

            #print("El valor "+str(i)+" es: "+str(int(XSep[i])))

            #XSEP = np.vstack([XSEP, Xnew[int(XSep[i]):int(XSep[i+1])]])
            XSEP.append(Xnew[int(XSepM[i]):int(XSepM[i+1])])#XSepM es XSep modificado
            YSEP.append(Ynew[int(XSepM[i]):int(XSepM[i+1])])

            i=i+2
            #print("i= "+str(i))

        #print("Vamos bien")
        #print("XSep: "+str(XSep))
        #print("XSEP: "+str(XSEP))

        #XSEP contiene en sus posiciones los arreglos en X que se van a graficar
        #YSEP contiene los valores en Y que se van a graficar

        #print("Ysepi:")
        #print(Ysepi)
        #print("Ysepv:")
        #print(Ysepv)
        #print("Xsep:")
        #print(Xsep)

        #print("La longitud del vector de discriminacion es: "+str(len(Ysepv)))
        #print("Longitud de XSEP: "+str(len(XSEP)))
        print("Han pasado "+str(len(XSEP))+" vehiculos")
        Amplitud=[]
        for i in range(len(YSEP)):
            Amplitud.append(np.mean(YSEP[i]))

        print(Amplitud)
except:
    print("Error al abrir el archivo")
    out_file.close()

X=np.arange(0, len(Y))
#Xnew=np.arange(0, len(Ynew))

with open("EjeTiempoX.txt", "w") as file:
    for i in range(len(X)):
        file.write(str(i) + " " + "\n")

#print(len(X))
#print(len(Y))

#Graficar
plt.figure()
plt.clf()
plt.plot(X, Y, marker = '.')# c='b')
plt.axis('tight')
plt.title("Señal captada por los sensores")
plt.legend()
#plt.ylim(1.5, 3)
#plt.show()
plt.draw()
plt.waitforbuttonpress()

#Histograma
pyl.figure()
pyl.hist(Y)
pyl.show()
pyl.title("Histograma de toda la señal")
pyl.waitforbuttonpress()

#Graficar
plt.figure()
plt.clf()
plt.plot(Xnew, Ynew, marker = '.')# c='b')
plt.axis('tight')
plt.title("Señal filtrada captada por los sensores")
plt.legend()
#plt.show()
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
plt.plot(Xsep, Ysepv, marker='*')#, marker = '.')# c='b')
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
    # plt.clf()
    plt.plot(XSEP[i], YSEP[i], marker='.')  # c='b')
    plt.axis('tight')
    plt.title("Vehiculo numero: " + str(i+1))
    # plt.legend()
    plt.ylim((Vmin-0.1), (Vmax+0.1))
    # plt.show()
    plt.draw()
    plt.waitforbuttonpress()

# Graficar iterativamente
for i in range(len(XSEP)):
    plt.figure()
    # plt.clf()
    plt.hist(YSEP[i], bins=50)
    plt.title("Histograma del Vehiculo numero: " + str(i+1))
    plt.draw()
    plt.waitforbuttonpress()

