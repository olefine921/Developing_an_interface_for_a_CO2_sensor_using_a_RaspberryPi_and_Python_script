from pymodbus.client.sync import ModbusSerialClient  # Import the pymodbus library part for syncronous master (=client)
from pymodbus.payload import BinaryPayloadDecoder
from time import time, ctime, sleep #import the time library
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import csv #Import the csv library

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
x =[-20:]
plotAvPCO2 = [-20:]
plotAvTemp = [-20:]

# Header CSV File
#header = ["Timestamp", "pCo2", "Temp in C", "mbar", "DLI"]
csvRow = []

#adresse = '/media/pi/boot/pCO2_Sensor_Data/' + str(startTime)


with open('/home/pi/Desktop/Kalibration_1' + '.csv', 'w') as file:

    writer = csv.writer(file)
    
    #writer.writerow(header)

#get input for Temp
slope = float(input('Give the slope from the calibration as a float and confirm with Enter:   '))    
intercept = float(input('Give the intercept from the calibration as a float and confirm with Enter:    '))


while counter1 < 8:
    t = time()
    dateForCSV = ctime(t)
    print('Start of loop')
    print(dateForCSV)
    print('')

    if client.connect():  # Trying to connect to Modbus Server/Slave
        # Reading from a holding register
        res = client.read_holding_registers(address=100, count=8, unit=1)  # Startregister = 100, Registers to be read = 8, Answer size = 1 byte
                                            
        decoder = BinaryPayloadDecoder.fromRegisters(res.registers, byteorder='>', wordorder='>')
                                            
        first_reading = decoder.decode_32bit_float()
        second_reading = decoder.decode_32bit_float()
        third_reading = decoder.decode_32bit_float()
        fourth_reading = decoder.decode_32bit_float()                                            

        if not res.isError():  # If Registers don't show Error
            #print(res.registers)  # Print content of registers
            #print(first_reading)
            #print(second_reading)
            #print(third_reading)
            #print(fourth_reading)

            pCO2 = first_reading
            temp = second_reading
            mbar = third_reading
            DLI = fourth_reading
            
            calibration = res.registers[0]

            #print('')
            #print('temp = ', temp)

            summePCO2.append(pCO2) #summePCO2 is the array of the pCO2s
            summeTemp.append(temp)
            summembar.append(mbar)
            summeDLI.append(DLI)
            sumcalibratine.append(calibration)

            #print('summeTemp = ', summeTemp)

            counter1 += 1

            print(counter1)

            if counter1 == 6:
                # Calculate Average for 1 Min

                avPCO2 = np.median(summePCO2)

                print(summePCO2)
                print(avPCO2)
                avTemp = np.median(summeTemp)
                print(avTemp)
                avmbar = np.median(summembar)
                print(avmbar)
                avDLI = np.median(summeDLI)
                print(avDLI)
                
                avPCO2 = avPCO2 * slope + intercept

                
                t = time()
                dateForCSV = ctime(t)
                
                loopedTime = datetime.now()
                csvTimeCounter = loopedTime - startTime
                
                
                csvRow.append(dateForCSV)
                csvRow.append(csvTimeCounter)
                csvRow.append(avPCO2)
                csvRow.append(avTemp)
                csvRow.append(avmbar)
                csvRow.append(avDLI)
                
                print(csvRow)
                
                with open('/home/pi/Desktop/Kalibration_1'+'.csv', 'a') as file:

                    writer = csv.writer(file)
                    
                    writer.writerow(csvRow)
                    #writer.writerow(int(avCalibration))

                x.append(csvTimeCounter)
                plotAvPCO2.append(avPCO2)
                plotAvTemp.append(avTemp)

                """
                x =[-20:]
                plotAvPCO2 = [-20:]
                plotAvTemp = [-20:]
                """

                fig, ax1 = plt.subplots(figsize=(25, 15))

                plt.suptitle("Average pCO2 and Temp starting by " + date[0])

                color = 'tab:red'
                ax1.set_xlabel('time (min)')
                ax1.set_xticks(np.arange(0, len(x) + 1, 10))
                ax1.set_ylabel('pCO2 in %', color=color)
                ax1.plot(x, plotAvPCO2, color=color)
                plt.xticks(rotation=25)

                ax2 = ax1.twinx()

                color = 'tab:blue'
                ax2.set_ylabel('avTemp in °C', color=color)
                ax2.plot(plotAvTemp, color=color)

                fig.tight_layout()
                plt.show(block=False)

                print(avTemp)
                
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
                
                #clear csvRow-List
                csvRow.pop(0) #delete 1. element -> Timestamp
                csvRow.pop(0) #delete new 1. element -> avPCO2
                csvRow.pop(0) #delete new 1. element -> Temp
                csvRow.pop(0) #delete new 1. element -> mbar
                csvRow.pop(0)
                csvRow.pop(0) #delete last element
                avCalibration =0
                loopedTime = 0
                csvTimeCounter = 0
                
                x = []


            else:

                sleep(10)  # Stops Loop for 10sec
                print('')

        else:
            print(res)  # Print Error Message, for meaning look at (insert git hub)
            counter1 = 0
            sleep(10)  # Stops Loop for 10sec

    else:  # If not able to connect, do this
        print('Cannot connect to the Transmitter M80 SM and Sensor InPro 5000i.')
        print('----------------------------------------------------------------')
        print('Please check the following things:')
        print('Does the RS485-to-USB Adapter have power? Which LEDs are active?')
        print('Are the cables connected correctly?')

        counter1 = 0
        sleep(10)  # Stops Loop for 10sec
