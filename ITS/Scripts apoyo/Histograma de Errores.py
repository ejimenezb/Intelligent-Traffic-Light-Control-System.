#Eladio Jimenez 13-10699
#Kheyter Chassaigne 13-10274

import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
import numpy as np
#from matplotlib.pylab import hist, show
Y = np.zeros((0, 1), dtype=np.float)
Yhist = np.zeros((0, 1), dtype=np.float)
ruta= "SenalSensorSerial.txt"

try:
    with open(ruta, "r") as out_file:
        lines = out_file.readlines()

        for line in lines:
            Lectura = np.fromstring(line, dtype=float, sep=' ')
            Y = np.vstack([Y, Lectura[0]])

        Indmin=1.1
        Indmax=2
        Yhist = np.histogram(Y, bins=10, range=(int(Indmin),int(Indmax)))
        print(Yhist)
        #Analisis de caracteristicas para identificar si es carro o camioneta

        #plt.plot(Xhist, Ynew, marker='.')  # c='b')

        pyl.figure()
        pyl.title("Histograma de toda la señal completa")
        pyl.hist(Y)
        #pyl.show()
        pyl.waitforbuttonpress()

        plt.figure()
        plt.title("Histograma de toda la señal recortada")
        #plt.hist(Y)
        plt.hist(Y, bins=10, range=(int(Indmin),int(Indmax)))
        plt.xlim(1, 1.35)
        # pyl.show()
        plt.waitforbuttonpress()

except:
    print("Error al abrir el archivo")
    out_file.close()



