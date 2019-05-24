import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as colormap
from mpl_toolkits.mplot3d import Axes3D as plt3d
import csv

sensorLocations = [0.013, 0.083, 0.153, 0.223, 0.293]

def tempToVoltage(t):
    return 0.01*(t-25) + 0.75

def voltageToTemp(x):
    return 100*(x-0.75) + 25 + 273.15

data = np.loadtxt('RunMay17-1.csv', delimiter=',')
data[:, 1] -= 1
data[:, 2] -= 1
data[:, 3] += 1
data[:, 4] -= 1
data[:, 5] += 1
time = data[:, 0] / 1000
temp = np.array([voltageToTemp(data[:, i] * 5 / 1024) for i in range(1,6)])
x = np.array(sensorLocations)

# fig2 = plt.figure(2)
# ax2 = fig2.add_subplot(111, projection = '3d')

# ax2.set_xlabel("Position along rod (mm)")
# ax2.set_ylabel("Time (s)")
# ax2.set_zlabel("Temperature (degC)")

#time, x = np.meshgrid(time, x)

print(x.shape)
print(time.shape)

print(temp.shape)

# ax2.plot_surface(x, time, temp, cmap = colormap.viridis)
# plt.show()

plt.figure(1, figsize = (10.0,6.0), dpi = 125)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")

for i in range(len(temp)):
    error = 0.569
    plt.plot(time, temp[i], '.', color = 'C' + str(i), ms = 1, label = "Sensor at {} m".format(sensorLocations[i]))
    plt.fill_between(time, temp[i] - error, temp[i] + error, alpha = 0.25)

plt.legend()
plt.show()


