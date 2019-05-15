
# info source = https://arduino.stackexchange.com/questions/55941/serial-communication-between-python-and-arduino
import serial
import collections
from datetime import datetime
import csv
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

ser = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 9600,
    timeout = 10
)

window = pg.GraphicsWindow()
window.setWindowTitle("Temperature Monitor")

data = np.random.normal(size = 5)

plotItem = window.addPlot()
datasets = [collections.deque(maxlen = 1000) for _ in range(len(data))]
plotDataItems = [plotItem.plot(datasets[i], pen = (i, 3)) for i in range(len(data))]

filename = str(datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S.csv"))

def update():
    global plotDataItems, filename
    data = ser.readline().decode().strip().split(',')
    #data = np.random.normal(size = 5)
    print(data)
    for i in range(len(data)):
        datasets[i].append(data[i])
        plotDataItems[i].setData(datasets[i])

    with open(filename, "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
