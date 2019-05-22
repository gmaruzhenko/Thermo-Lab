from math import pi
import numpy as np
from matplotlib import pyplot as plt

C = 900 # J/(kg*K)
RHO = 2700 # kg/m^3
SIGMA = 5.67*10**(-8) #W/m^2/K^4

def calculateStep(T, Tamb, radius, dx, dt, K, Kc, epsilon, powerIn):
    Parr = -2*pi*radius*dx* ( Kc*(T[1:-1] - Tamb) + epsilon*SIGMA*((T[1:-1])**4 - Tamb**4))
    T[1:-1] = T[1:-1] + (
            # effect of surrounding segment
            ((T[0:-2] - 2*T[1:-1] + T[2:])/dx**2) * K/(C*RHO) 
            # losses to convection and radiation
            + Parr / (C*RHO*pi*radius**2*dx)
        ) * dt
    T[0] = T[0] + (
            # effect of surrounding segment
            -1*K*(T[0]-T[1]) / (C*RHO*dx**2) 
            # losses to convection and radiation
            - (2*pi*radius*dx + pi*radius**2) * ( Kc*(T[0] - Tamb) + epsilon*SIGMA*((T[0])**4 - Tamb**4)) / (C*RHO*pi*radius**2*dx)
            # input from heat source
            + powerIn / (C*RHO*pi*radius**2*dx)
        ) * dt
    T[-1] = T[-1] + (
            # effect of surrounding segment
            K*(T[-2]-T[-1]) / (C*RHO*dx**2) 
            # losses to convection and radiation
            - (2*pi*radius*dx + pi*radius**2) * ( Kc*(T[-1] - Tamb) + epsilon*SIGMA*((T[-1])**4 - Tamb**4)) / (C*RHO*pi*radius**2*dx)
        ) * dt
    return T

def diffTwoArrays(A, B):
    return np.sum((A-B)**2)


ROD_LENGTH = 0.3045 # m
NUM_POINTS = 100
xRange = np.linspace(0, ROD_LENGTH, NUM_POINTS)
sensorLocations = [0.013, 0.083, 0.153, 0.223, 0.293]
sensorIndices = [np.argmax(xRange >= sensorLocation) for sensorLocation in sensorLocations]
print([xRange[index] for index in sensorIndices])

def simulateThroughTime(numSteps, Tamb, radius, dx, dt, K, Kc, epsilon, powerIn):
    Tarr = np.full((numSteps, NUM_POINTS), Tamb)
    for i in range(numSteps - 1):
        Tarr[i+1] = calculateStep(Tarr[i], Tamb, radius, dx, dt, K, Kc, epsilon, powerIn)
    return Tarr

    #return np.sum((modelTemps - Tarr) ** 2)



def voltageToTemp(x):
    return 100*(x-0.75) + 25 + 273 

data = np.loadtxt('RunMay17-1.csv', delimiter=',')
time = data[:, 0] / 1000
averageTimeStep = np.mean([time[i] - time[i-1] for i in range(1, len(time))])
temp = np.array([voltageToTemp(data[:, i] * 5 / 1024) for i in range(1,6)])
# print(temp.shape)

numTimeSteps = 150000
Tamb = 293.15 # K
radius = 0.0254/2
dx = ROD_LENGTH/NUM_POINTS
K = 200 # J/(s*m*K)
Kc = 12 # W/m^2/K
powerIn = 15 # W
epsilon = 0.09
Tarr = simulateThroughTime(numTimeSteps, Tamb, radius, dx, averageTimeStep/100, K, Kc, epsilon, powerIn)

#plt.plot(xRange, Tarr.transpose())
modelTimes = np.arange(numTimeSteps) * averageTimeStep/100
modelTemps = np.array([Tarr[:, index] for index in sensorIndices]).transpose()
plt.plot(modelTimes, np.array([Tarr[:, index] for index in sensorIndices]).transpose())
plt.plot(time - 90, temp.transpose())
plt.show()