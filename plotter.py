import numpy as np
import matplotlib.pyplot as plt
import csv

SENSOR_SPACING = 71.2 # mm

def tempToVoltage(t):
    return 0.01*(t-25) + 0.75

def voltageToTemp(x):
    return 100*(x-0.75) + 25 

data = np.loadtxt('RunMay17-1.csv', delimiter=',')
time = data[:, 0] / 1000
t = np.array([voltageToTemp(data[:, i] * 5 / 1024) for i in range(1,6)])

plt.figure(1)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (degC)")

for i in range(len(t)):
    plt.plot(time, t[i])

plt.show()