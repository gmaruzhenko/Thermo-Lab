from math import pi
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import minimize
from scipy.ndimage import gaussian_filter1d as smooth
import pickle

C = 900 # J/(kg*K)
RHO = 2700 # kg/m^3
SIGMA = 5.67*10**(-8) #W/m^2/K^4

ROD_LENGTH = 0.3045 # m
NUM_POINTS = 23
xRange = np.linspace(0, ROD_LENGTH, NUM_POINTS)
sensorLocations = [0.013, 0.083, 0.153, 0.223, 0.293]
#sensorIndices = [np.argmax(np.abs(xRange >= sensorLocation)) for sensorLocation in sensorLocations]
sensorIndices = [np.argmin(np.abs(xRange - sensorLocation)) for sensorLocation in sensorLocations]
print([xRange[index] for index in sensorIndices])



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
    
def simulateThroughTime(K, Kc, epsilon, powerIn, numSteps, Tamb, radius, dx, dt):
    Tarr = np.full((numSteps, NUM_POINTS), Tamb)
    for i in range(numSteps - 1):
        Tarr[i+1] = calculateStep(Tarr[i], Tamb, radius, dx, dt, K, Kc, epsilon, powerIn)
    return Tarr

def pickSensorModelTemps(Tarr, sensorIndices):
    return np.array([Tarr[:, index] for index in sensorIndices]).transpose()

def voltageToTemp(x):
    return 100*(x-0.75) + 25 + 273 

def compare(params, *otherArgs):
    K = params[0]
    Kc = params[1]
    epsilon = params[2]
    powerIn = params[3]
    model = simulateThroughTime(K, Kc, epsilon, powerIn, numTimeSteps, Tamb, radius, dx, dt)
    modelTemps = pickSensorModelTemps(model, sensorIndices)

    return diffTwoArrays(modelTemps, smoothTemp)


numTimeSteps = 1350
dataTruncStart = 89
dataRaw = np.loadtxt('RunMay17-1.csv', delimiter=',')

#truncating data
data = dataRaw[dataTruncStart:dataTruncStart + numTimeSteps]

#calibrations for sensors that are slightly off
data[:, 1] -= 1
data[:, 2] -= 1
data[:, 3] += 1
data[:, 4] -= 1
data[:, 5] += 1

time = (data[:, 0] - data[0][0]) / 1000
averageTimeStep = np.mean([time[i] - time[i-1] for i in range(1, len(time))])
temp = np.array([voltageToTemp(data[:, i] * 5 / 1024) for i in range(1,6)])
smoothTemp = np.array( [ smooth(temp[i], 6) for i in range(len(temp)) ])
smoothTemp = smoothTemp.transpose()
temp = temp.transpose()
# print(temp.shape)

Tamb = np.mean(temp[0]) # K
radius = 0.0254/2
dx = ROD_LENGTH/(NUM_POINTS)
dt = averageTimeStep
K = 200 # J/(s*m*K)
Kc = 12 # W/m^2/K
epsilon = 0.1
powerIn = 13 # W

# residual, observed, model = compare(temp.transpose(), K, Kc, epsilon, powerIn)

# print(residual)

results = minimize(
    compare, 
    np.array([K, Kc, epsilon, powerIn]),
    #method = "TNC",
    bounds = (
        (150,300),
        (1, 20),
        (0, 1),
        (10,19)
    ),
    options = {
        'maxiter': 1000, 
        'disp': True
    }
)

# with open("PDE_fit_results.pickle", "wb") as f:
#     pickle.dump(results, f)

fP = results.x

print(fP)

# plt.plot(xRange, Tarr.transpose())
modelTimes = np.arange(numTimeSteps) * dt
model = pickSensorModelTemps(
    simulateThroughTime(fP[0], fP[1], fP[2], fP[3], numTimeSteps, Tamb, radius, dx, dt), 
    sensorIndices
)
# # modelTemps = pickSensorModelTemps(Tarr, sensorIndices)
# # print(modelTemps.shape)
# # print(temp.transpose().shape)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.plot(modelTimes, model)
plt.plot(modelTimes, temp, '.')
# plt.plot(modelTimes, smoothTemp)
plt.show()