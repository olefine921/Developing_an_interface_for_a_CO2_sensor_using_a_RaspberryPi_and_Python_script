from pymodbus.client.sync import ModbusSerialClient  #import the pymodbus library part for syncronous master (=client)
from pymodbus.payload import BinaryPayloadDecoder #import the BinaryPayloadDecoder to translate signals
from time import time, ctime, sleep  #import the time & datetime libraries
from datetime import datetime, date, timedelta
import numpy as np #import numpy for all calculations
from sklearn.linear_model import LinearRegression  #import to calculate slope, intercept & R^2
import csv  #import the csv library for documentation

client = ModbusSerialClient(
    method='rtu',  #Modbus Modus = RTU = via USB & RS485
    port='/dev/ttyUSB0',  #connected over ttyUSB0, not AMA0
    baudrate=19200,  #Baudrate was changed from 38400 to 19200
    timeout=3,  #Timeout after 3 sec of unanswered calls
    parity='N',  #Parity = None
    stopbits=2,  #Bites was changed from 1 to 2
    bytesize=8  #Register size is 8 bytes
)
# Counter
counter1 = 0  #for doing X samples
counter2 = 0 #for getting the median of X data points 
setCounter = 0 #will be filled with the number of samples
counterMeasurement = 0 #will be filled with the length of the measurement
realSample = 0 #will be filled with the value of the sample 

# Variables
t = 0

pCO2 = 0
temp = 0
mbar = 0
DLI = 0

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

#calibration variables (specific)
calibrationPCO2 = []
calibrationX = []

#variables for getting time
startTime = datetime.now()
loopedTime = 0
csvTimeCounter = 0

#Header & lines for csv file
header = ["Timestamp", "Time since start", "Sample", "pCo2", "Temp in C", "mbar", "mgl", "Measurement Length in Minutes"]
csvRow = []

#creating of the file name & path
adresseTime = datetime.now().strftime('%Y.%m.%d')
adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/Calibration_' + adresseTime

#creating csv file & writing header
with open(adresse + '.csv', 'w') as file:
    writer = csv.writer(file)

    writer.writerow(header)

#explanation for user, will be printed in terminal
print('Please prepare the following samples:') #Probes should be on a brought spectrum
print('1. 0.1 mbar')
print('2. 1.0 mbar')
print('3. 5.0 mbar')
print('4. 10.0 mbar')
print('')
print('If wanted, the samples an be adjusted in value and number. The correct mbar for the samples has to be given as user input.')
print('The code will ask for one sample too much. Please give any float as input for the last asked user input.')
print('')
#prompting user input
#important: sample has to be in position before measurement length is confirmed, measurement starts immediately after confirmation
setCounter = int(input('Please enter how many samples will be used for this calibration and confirm with Enter:    '))
print('')
realSample = float(input('Please give the mbar of the first sample as a float and confirm with Enter:   '))
counterMeasurement = 6* int(input('Please give how long this sample should be measured for this calibration in X minutes and confirm with Enter:    '))


while counter1 < 1200: #counter1 will be set to 1201 after all samples & the calculations have been done, the code will end
    while counter2 < setCounter: #loop will repeated until all samples have been measured

        print('')

        if client.connect():  #trying to connect to Modbus Server/Slave
            #reading from a holding register
            res = client.read_holding_registers(address=100, count=8,
                                                unit=1)  #Startregister = 100, Registers to be read = 8, Answer size = 1 byte
            
            #define decoder for res (registers to be read) to get the organisation for big endian
            #important: big endian = '>' 
            decoder = BinaryPayloadDecoder.fromRegisters(res.registers, byteorder='>', wordorder='>')

            #use decoder to get values in 32-bit float big endian
            first_reading = decoder.decode_32bit_float()
            second_reading = decoder.decode_32bit_float()
            third_reading = decoder.decode_32bit_float()
            fourth_reading = decoder.decode_32bit_float()

            if not res.isError():  #If Registers don't show Error
                #save translated values as specific variables (not necessary but helpfull for logic)
                pCO2 = first_reading
                temp = second_reading
                mbar = third_reading
                DLI = fourth_reading #fourth register reads now mg/l, for less mistakes during coding, the old name has been left

                summePCO2.append(pCO2)  # summePCO2 is the array of the pCO2s
                summeTemp.append(temp)
                summembar.append(mbar)
                summeDLI.append(DLI)

                counter1 += 1 #add after each measurement to reach the right measurement length

                if counter1 == counterMeasurement: #if right measurement length is reached
                    
                    # Calculate Median over X Min
                    avPCO2 = np.median(summePCO2)
                    avTemp = np.median(summeTemp)
                    avmbar = np.median(summembar)
                    avDLI = np.median(summeDLI)

                    #get times to fill csv file
                    t = time()
                    dateForCSV = ctime(t)

                    loopedTime = datetime.now()
                    csvTimeCounter = loopedTime - startTime

                    #add data to the list for writing into the csv file
                    #importan: keep order as in header declared
                    csvRow.append(dateForCSV)
                    csvRow.append(csvTimeCounter)
                    csvRow.append(realSample)
                    csvRow.append(avPCO2)
                    csvRow.append(avTemp)
                    csvRow.append(avmbar)
                    csvRow.append(avDLI)
                    csvRow.append(counterMeasurement)

                    #add the calculated median to a list for the calculation of slope, intercept & r^2
                    calibrationPCO2.append(avPCO2)
                    calibrationX.append(realSample)


                    #show the median in the terminal
                    print('pCO2 = ' + str(avPCO2))
                    print('')
                    
                    #write the data in the csv file
                    with open(adresse + '.csv', 'a') as file:

                        writer = csv.writer(file)

                        writer.writerow(csvRow)

                    counter2 += 1 #add to counter2 for each sample done

                    #set every variable back to 0
                    counter1 = 0
                    pCO2 = 0
                    temp = 0
                    mbar = 0
                    DLI = 0
                    realSample = 0

                    summePCO2 = []
                    summeTemp = []
                    summembar = []
                    summeDLI = []

                    avPCO2 = 0
                    avTemp = 0
                    avmbar = 0
                    avDLI = 0
                    
                    loopedTime = 0
                    csvTimeCounter = 0
                    
                    #clear csvRow-List
                    csvRow = []
                    
                    #prompt user input for next sample
                    #important: sample has to be in position before measurement length is confirmed, measurement starts immediately after confirmation
                    print('If this was your last sample, give (now) any float') #maybe need to write more specific instruction
                    realSample = float(input('Please give the mbar of the next sample as a float and confirm with Enter:   '))
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
    
    counter1 = 1201
