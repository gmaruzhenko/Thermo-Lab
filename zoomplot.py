import numpy as np
from matplotlib import pyplot as plt


sensorLocations = [0.013, 0.083, 0.153, 0.223, 0.293]
error = 0.569

def voltageToTemp(x):
    return 100*(x-0.75) + 25 + 273 

dataRaw = np.loadtxt('RunMay17-1.csv', delimiter=',')
numTimeSteps = 2655
dataTruncStart = 89
#truncating data
data = dataRaw[dataTruncStart:dataTruncStart + numTimeSteps]

#calibrations for sensors that are slightly off
data[:, 1] -= 1
data[:, 2] -= 1
data[:, 3] += 1
data[:, 4] -= 1
data[:, 5] += 1

time = (data[:, 0] - data[0][0]) / 1000
dt = np.mean([time[i] - time[i-1] for i in range(1, len(time))])
modelTimes = np.arange(numTimeSteps) * dt
temp = np.array([voltageToTemp(data[:, i] * 5 / 1024) for i in range(1,6)]).transpose()



arrowStartX = 1360
arrowStartYs = [338, 329.5, 326.5, 322, 317.5]
arrowDeltaX = 70
arrowDeltaYs = [-8, -3, -1, 0.3, 1]

plt.figure(figsize = (10.0,6.0), dpi = 125)

for i in range(5):
    plt.plot(
        modelTimes, 
        temp[:, i], 
        '.', 
        color = 'C' + str(i), 
        ms = 0.5,
        label = "Sensor at {} m".format(sensorLocations[i])
    )
    plt.fill_between(
        modelTimes, 
        temp[:, i] - error, temp[:, i] + error, 
        color = 'C' + str(i), 
        alpha = 0.25
    )
    plt.arrow(
        arrowStartX, arrowStartYs[i], arrowDeltaX, arrowDeltaYs[i],
        color = "C0" if arrowDeltaYs[i] < 0 else "C3",
        width = 0.05, head_width=0.5, head_length=10
    )

plt.text(1400,334.5,"Cooling", color="C0")
plt.text(1400,317,"Heating", color="C3")
plt.xlim(1200,1700)
plt.ylim(315,340)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.legend()
plt.show()