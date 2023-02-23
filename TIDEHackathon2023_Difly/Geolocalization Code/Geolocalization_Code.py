import math
import numpy as np
import cv2
import pandas as pd
from matplotlib import pyplot as plt

#From pixels coordinates on screen to direction versor in camera frame


'''

From direction cosine matrix to Euler angles

'''
def dcm2euler(dcm):
    euler = [0, 0, 0]  # inizializza il vettore degli angoli di Eulero

    # Calcola la matrice trasposta del DCM
    rmat_ib = [dcm [0], dcm [3], dcm [6],
               dcm [1], dcm [4], dcm [7],
               dcm [2], dcm [5], dcm [8]]

    # Calcola l'angolo di pitch (-asin(rmat31))
    euler [1] = -math.asin (rmat_ib [6])  # Usa math.asin per sicurezza

    # Se siamo lontani dalla singolarità, calcola roll e yaw
    if abs (rmat_ib [6]) < 0.9999:
        # Calcola l'angolo di yaw (atan2(rmat21,rmat11))
        euler [2] = math.atan2 (rmat_ib [3], rmat_ib [0])

        # Calcola l'angolo di roll (atan2(rmat32,rmat33))
        euler [0] = math.atan2 (rmat_ib [7], rmat_ib [8])
    else:
        if rmat_ib [6] < 0:
            # In questo caso, sin(pitch) = 1
            # Calcola (roll - yaw) = atan2(rmat12,rmat13)
            c = math.atan2 (rmat_ib [1], rmat_ib [2])

            # Risolve il problema di ottimizzazione per evitare salti in roll e yaw
            sum_old = euler [0] + euler [2]  # roll_old + yaw_old
            euler [0] = 0.5 * (c + sum_old)  # roll
            euler [2] = 0.5 * (-c + sum_old)  # yaw
        else:
            # In questo caso, sin(pitch) = -1
            # Calcola (roll + yaw) = atan2(-rmat12,rmat22)
            c = math.atan2 (-rmat_ib [1], rmat_ib [4])

            # Risolve il problema di ottimizzazione per evitare salti in roll e yaw
            sum_old = euler [0] - euler [2]  # roll_old - yaw_old
            euler [0] = 0.5 * (c + sum_old)  # roll
            euler [2] = 0.5 * (c - sum_old)  # yaw

    return euler


'''

From Euler angles to direction cosine matrix 

'''
def euler2dcm(roll, pitch, yaw):
    Tbi = [0] * 9  # inizializza la matrice di direzioni coseni

    #roll, pitch, yaw = eul  # estrai gli angoli di Eulero

    cosRoll = math.cos (roll)
    sinRoll = math.sin (roll)
    cosPitch = math.cos (pitch)
    sinPitch = math.sin (pitch)
    cosYaw = math.cos (yaw)
    sinYaw = math.sin (yaw)

    # Calcola la matrice di direzioni coseni
    Tbi [0] = cosPitch * cosYaw
    Tbi [1] = -cosRoll * sinYaw + sinRoll * sinPitch * cosYaw
    Tbi [2] = sinRoll * sinYaw + cosRoll * sinPitch * cosYaw
    Tbi [3] = cosPitch * sinYaw
    Tbi [4] = cosRoll * cosYaw + sinRoll * sinPitch * sinYaw
    Tbi [5] = -sinRoll * cosYaw + cosRoll * sinPitch * sinYaw
    Tbi [6] = -sinPitch
    Tbi [7] = sinRoll * cosPitch
    Tbi [8] = cosRoll * cosPitch

    return Tbi


def zoom(Zoom=1):
    FOV = 63.7
    return FOV/Zoom

telemetria = pd.read_csv ('TUTTOBELLO_2.csv', sep = ',')

Versore = (1,0,1)
NorthX = []
EastY = []

#Script to compute geolocalization of targets detected on camera screen

for i in range(0,len(telemetria)):

    #From Camera frame to Body frame

    VersoreUAV = euler2dcm (math.radians(telemetria['Roll'][i]*0.9), math.radians(telemetria['Pitch'][i]*0.9), math.radians(telemetria['Yaw'][i]*0.9))

    print (VersoreUAV)
    ele1 = [(VersoreUAV [0] * Versore [0]) + (VersoreUAV [1] * Versore [1]) + (VersoreUAV [2] * Versore [2])]
    ele2 = [(VersoreUAV [3] * Versore [0]) + (VersoreUAV [4] * Versore [1]) + (VersoreUAV [5] * Versore [2])]
    ele3 = [(VersoreUAV [6] * Versore [0]) + (VersoreUAV [7] * Versore [1]) + (VersoreUAV [8] * Versore [2])]

    #Frome Body frame to inertial MED

    MUAV = euler2dcm(telemetria['roll'][i],telemetria['pitch'][i],telemetria['yaw'][i])

    ele1 = [(MUAV[0]*ele1[0]) + (MUAV[1]*ele2[0]) + (MUAV[2]*ele3[0])]
    ele2 = [(MUAV[3]*ele1[0]) + (MUAV[4]*ele2[0]) + (MUAV[5]*ele3[0])]
    ele3 = [(MUAV[6]*ele1[0]) + (MUAV[7]*ele2[0]) + (MUAV[8]*ele3[0])]

    #Projection of image axis

    NorthX.append(((ele1[0]/ele3[0])*telemetria['quota'][i]))
    EastY.append(((ele2[0]/ele3[0])*telemetria['quota'][i]))


telemetria['NorthX'] = NorthX
telemetria['EastY'] = EastY

telemetria.to_csv('DATAFRAME_FLY_LOG.CSV')


'''plt.plot(EastY, NorthX)
# Impostazione delle etichette degli assi e del titolo
plt.xlabel('Valori X')
plt.ylabel('Valori Y')
plt.title('Grafico a linea con valori XY')
plt.axis('equal')
# Visualizzazione del grafico
plt.show()'''
