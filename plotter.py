import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as colormap
from mpl_toolkits.mplot3d import Axes3D as plt3d
import csv

SENSOR_SPACING = 71.2 # mm

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
x = np.array([i * SENSOR_SPACING for i in range(5)])

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

plt.figure(1)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")

for i in range(len(temp)):
    plt.plot(time, temp[i])

plt.show()