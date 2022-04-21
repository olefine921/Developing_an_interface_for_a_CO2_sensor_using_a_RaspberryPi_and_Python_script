from pymodbus.client.sync import ModbusSerialClient  # Import the pymodbus library part for syncronous master (=client)
from pymodbus.payload import BinaryPayloadDecoder
from time import time, ctime, sleep #import the time library
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import csv #Import the csv library
import random

plt.ion()

# Counter
counter1 = 0 #For getting the sum of 6 data points and getting the average after counter = 6
counter2 = 0

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
sumcalibratine = []

avPCO2 = 0
avTemp = 0
avmbar = 0
avDLI = 0
avCalibration = 0

first_reading = 0
second_reading = 0
third_reading = 0
fourth_reading = 0

#variables only for plotting
startTime = datetime.now()
loopedTime = 0
csvTimeCounter = 0

date = []
x =[]
plotAvPCO2 = []
plotAvTemp = []
i = 0

# Header CSV File
#header = ["Timestamp", "pCo2", "Temp in C", "mbar", "DLI"]
csvRow = []

#adresse = '/media/pi/boot/pCO2_Sensor_Data/' + str(startTime)


with open('/home/pi/Desktop/Test20.04.2022_1' + '.csv', 'w') as file:

    writer = csv.writer(file)
    
    #writer.writerow(header)

#get input for Temp
slope = float(input('Give the slope from the calibration as a float and confirm with Enter:   '))    
intercept = float(input('Give the intercept from the calibration as a float and confirm with Enter:    '))


while counter1 < 20:
    t = time()
    dateForCSV = ctime(t)
    print('Start of loop')
    print(dateForCSV)
    print('')



    pCO2 = random.randint(0,2)
    temp = random.randint(20,34)


    #print('')
    #print('temp = ', temp)

    summePCO2.append(float(pCO2)) #summePCO2 is the array of the pCO2s
    summeTemp.append(float(temp))


    #print('summeTemp = ', summeTemp)

    counter1 += 1

    print(counter1)
    """
    if counter1 == 5:
        plt.close()
    else:
        print("----") """

    if counter1 == 6:
        # Calculate Average for 1 Min
        
        

        avPCO2 = np.median(summePCO2)

        print(summePCO2)
        print(avPCO2)
        avTemp = np.median(summeTemp)
        print(avTemp)

        
        t = time()
        dateForCSV = ctime(t)
        
        loopedTime = datetime.now()
        csvTimeCounter = loopedTime - startTime
        

        csvTimeCounter = str(csvTimeCounter)
        x.append(csvTimeCounter)
        plotAvPCO2.append(avPCO2)
        plotAvTemp.append(avTemp)
        
        print(x)
        print(plotAvPCO2)
        

        x = x[-20:]
        plotAvPCO2 = plotAvPCO2[-20:]
        plotAvTemp = plotAvTemp[-20:]
        

        fig, ax1 = plt.subplots(figsize=(20, 12))
        ax2 = ax1.twinx()

        plt.suptitle("Average pCO2 and Temp")
        
        
        for i in range(len(x)):
            


            ax1.clear()

            color = 'tab:red'
            ax1.set_xlabel('time (min)')
            ax1.set_xticks(np.arange(0, len(x) + 1, 10))
            ax1.set_ylabel('pCO2 in %', color=color)
            #plt.hold(True)
            ax1.plot(x, plotAvPCO2, color=color)
            plt.xticks(rotation=25)

            
            ax2.clear()

            color = 'tab:blue'
            ax2.set_ylabel('avTemp in °C', color=color)
            ax2.set_ylim(20,35)
            #plt.hold(True)
            ax2.plot(plotAvTemp, color=color)

            fig.tight_layout()
            fig.canvas.draw()
            #fig.canvas.flush_events()



        print(plotAvTemp)
        
        sleep(10)  # Stops Loop for 10sec

        print('----------------------------------------------------------------')
        
        #set every variable back to 0
        counter1 = 0
        pCO2 = 0
        temp = 0
        mbar = 0
        DLI = 0

        summePCO2 = []
        summeTemp = []
        summembar = []
        summeDLI = []
        sumcalibatine =[]

        avPCO2 = 0
        avTemp = 0
        avmbar = 0
        avDLI = 0
        


        loopedTime = 0
        csvTimeCounter = 0
        


    else:

        sleep(10)  # Stops Loop for 10sec
        print('')


