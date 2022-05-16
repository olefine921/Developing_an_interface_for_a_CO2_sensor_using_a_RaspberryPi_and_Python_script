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
counterMeasurement = 0

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
calibrationPCO2 = []
calibrationX = []

# variables only for plotting
startTime = datetime.now()
loopedTime = 0
csvTimeCounter = 0

date = []
x = []
plotAvPCO2 = []
plotAvTemp = []

# Header CSV File
header = ["Timestamp", "Time since start", "Sample", "pCo2", "Temp in C", "mbar", "DLI", "Measurement Length in Minutes"]
csvRow = []

adresseTime = datetime.now().strftime('%Y.%m.%d')
adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/Calibration_' + adresseTime

with open(adresse + '.csv', 'w') as file:
    writer = csv.writer(file)

    writer.writerow(header)

print('Please prepare the following samples:') #Probes should be on a brought spectrum
print('1. 0.1 mbar')
print('2. 1.0 mbar')
print('3. 5.0 mbar')
print('4. 10.0 mbar')
print('')
print('If wanted, the samples an be adjusted in value and number. The correct mbar for the samples has to be given as user input.')
print('The code will ask for one sample too much. Please give any float as input for the last asked user input.')
print('')
setCounter = int(input('Please enter how many samples will be used for this calibration and confirm with Enter:    '))
print('')
realProbe = float(input('Please give the mbar of the first sample as a float and confirm with Enter:   '))
counterMeasurement = 6* int(input('Please give how long this sample should be measured for this calibration in X minutes and confirm with Enter:    '))

while counter1 < 1200:
    while counter2 < setCounter:
        t = time()
        dateForCSV = ctime(t)

        print('')

        if client.connect():  # Trying to connect to Modbus Server/Slave
            # Reading from a holding register
            res = client.read_holding_registers(address=100, count=8,
                                                unit=1)  # Startregister = 100, Registers to be read = 8, Answer size = 1 byte

            decoder = BinaryPayloadDecoder.fromRegisters(res.registers, byteorder='>', wordorder='>')

            first_reading = decoder.decode_32bit_float()
            second_reading = decoder.decode_32bit_float()
            third_reading = decoder.decode_32bit_float()
            fourth_reading = decoder.decode_32bit_float()

            if not res.isError():  # If Registers don't show Error
                # print(res.registers)  # Print content of registers
                # print(first_reading)
                # print(second_reading)
                # print(third_reading)
                # print(fourth_reading)

                pCO2 = first_reading
                temp = second_reading
                mbar = third_reading
                DLI = fourth_reading


                # print('')
                # print('temp = ', temp)

                summePCO2.append(pCO2)  # summePCO2 is the array of the pCO2s
                summeTemp.append(temp)
                summembar.append(mbar)
                summeDLI.append(DLI)

                # print('summeTemp = ', summeTemp)

                counter1 += 1

                #print(counter1)

                if counter1 == counterMeasurement:
                    # Calculate Median over 1 Min

                    avPCO2 = np.median(summePCO2)
                    avTemp = np.median(summeTemp)
                    avmbar = np.median(summembar)
                    avDLI = np.median(summeDLI)

                    t = time()
                    dateForCSV = ctime(t)

                    loopedTime = datetime.now()
                    csvTimeCounter = loopedTime - startTime

                    csvRow.append(dateForCSV)
                    csvRow.append(csvTimeCounter)
                    csvRow.append(realTemp)
                    csvRow.append(avPCO2)
                    csvRow.append(avTemp)
                    csvRow.append(avmbar)
                    csvRow.append(avDLI)
                    csvRow.append(counterMeasurement)

                    calibrationPCO2.append(avPCO2)
                    calibrationX.append(realProbe)


                    print('pCO2 = ' + str(avPCO2))
                    print('')
                    with open(adresse + '.csv', 'a') as file:

                        writer = csv.writer(file)

                        writer.writerow(csvRow)
                        # writer.writerow(int(avCalibration))

                    counter2 += 1
                    sleep(10)

                    # set every variable back to 0
                    counter1 = 0
                    pCO2 = 0
                    temp = 0
                    mbar = 0
                    DLI = 0
                    realProbe = 0

                    summePCO2 = []
                    summeTemp = []
                    summembar = []
                    summeDLI = []

                    avPCO2 = 0
                    avTemp = 0
                    avmbar = 0
                    avDLI = 0

                    # clear csvRow-List
                    csvRow.pop(0)  # delete 1. element -> Timestamp
                    csvRow.pop(0)  # delete new 1. element -> avPCO2
                    csvRow.pop(0)  # delete new 1. element -> Temp
                    csvRow.pop(0)  # delete new 1. element -> mbar
                    csvRow.pop(0)
                    csvRow.pop(0)
                    csvRow.pop(0)
                    csvRow.pop(0)  # delete last element
                    avCalibration = 0
                    loopedTime = 0
                    csvTimeCounter = 0

                    x = []
                    plotAvPCO2 = []
                    plotAvTemp = []
                    
                    print('If this was your last sample, give (now) any float') #maybe need to write more specific instruction
                    realProbe = float(input('Please give the mbar of the next sample as a float and confirm with Enter:   '))
                    counterMeasurement = int(input('Please give how long this sample should be measured for this calibration in X minutes and confirm with Enter:    '))


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

    # calculate the slope & intercept
    print('')
    #print(calibrationPCO2)
    #print(calibrationX)
    print('')
    print('The slope for this calibration is:')
    
    slope, intercept = np.polyfit(calibrationX, calibrationPCO2,1)
    print(slope)
    
    print('')
    print('The intercept for this calibration is:')
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
    
    divider = []
    headerCalculations = ["Slope", "Intercept", "R^2"]
    csvRow = []
    csvRow.append(slope)
    csvRow.append(intercept)
    csvRow.append(rSq)
    
    with open(adresse + '.csv', 'a') as file:

                        writer = csv.writer(file)
                        writer.writerow(divider)
                        writer.writerow(headerCalculations)
                        writer.writerow(csvRow)
                        # writer.writerow(int(avCalibration))
    
    counter1 = 9