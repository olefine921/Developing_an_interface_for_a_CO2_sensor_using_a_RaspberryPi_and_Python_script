from pymodbus.client.sync import ModbusSerialClient  # Import the pymodbus library part for syncronous master (=client)
from pymodbus.payload import BinaryPayloadDecoder
from time import time, ctime, sleep  # import the time library
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import csv  # Import the csv library

client = ModbusSerialClient(
    method='rtu',  # Modbus Modus = RTU = via USB & RS485
    port='/dev/ttyUSB0',  # Connected over ttyUSB0, not AMA0
    baudrate=19200,  # Baudrate was changed from 38400 to 19200
    timeout=3,  #
    parity='N',  # Parity = None
    stopbits=2,  # Bites was changed from 1 to 2
    bytesize=8  #
)
# Counter
counter1 = 0  # For getting the sum of 6 data points and getting the average after counter = 6
counter2 = 0
setCounter = 0

# Variables
t = 0

pCO2 = 0
temp = 0
mbar = 0
DLI = 0
calibration = 0

summePCO2 = []
summeTemp = []
summembar = []
summeDLI = []


avPCO2 = 0
avTemp = 0
avmbar = 0
avDLI = 0


first_reading = 0
second_reading = 0
third_reading = 0
fourth_reading = 0

# calibration Variables (specific)
calibrationPCO2 = [0,1]
calibrationX = [0,1]

# variables only for plotting
startTime = datetime.now()
loopedTime = 0
csvTimeCounter = 0

date = []
x = []
plotAvPCO2 = []
plotAvTemp = []





# calculate the slope
print('')
#print(calibrationPCO2)
#print(calibrationX)
print('')
print('The slope for this calibration is:')

slope, intercept = np.polyfit(calibrationX, calibrationPCO2,1)
print(slope)
print(intercept)

# calculate r^2
print('')
print('R^2 for this calibration is:')

x = np.array(calibrationX)
#print(x)
x = x.reshape(-1,1)
#print(x)

model = LinearRegression()
model.fit(x, calibrationPCO2)
rSq = model.score(x, calibrationPCO2)

print(rSq)
