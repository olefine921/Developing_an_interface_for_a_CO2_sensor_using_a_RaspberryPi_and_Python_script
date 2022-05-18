from pymodbus.client.sync import ModbusSerialClient  #import the pymodbus library part for syncronous master (=client)
from pymodbus.payload import BinaryPayloadDecoder #import the BinaryPayloadDecoder to translate signals
from time import time, ctime, sleep #import the time  & datetime libraries
from datetime import datetime, date, timedelta
import numpy as np #import numpy for calculations, dash_usage.py uses pandas for calculation
import csv #import the csv library for documentation

client = ModbusSerialClient(
    method='rtu',  #Modbus Modus = RTU = via USB & RS485
    port='/dev/ttyUSB0',  #Connected over ttyUSB0, not AMA0
    baudrate=19200,  #Baudrate was changed from 38400 to 19200
    timeout=3,  #imeout after 3 sec of unanswered calls
    parity='N',  #Parity = None
    stopbits=2,  #Bites was changed from 1 to 2
    bytesize=8  #Register size is 8 bytes
)
#Counter
counter1 = 0 #for median loop
counter2 = 1 #for counting the days -> 5760 = 4days

#Variables
t = 0

pCO2 = 0
temp = 0
mbar = 0
DLI = 0 #fourth register reads now mg/l, for less mistakes during coding, the old name has been left

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

#variables only for time
startTime = datetime.now()
loopedTime = 0
csvTimeCounter = 0


#create list for line in csv & adresse of csv file, including path
csvRow = []

adresseTime = datetime.now().strftime('%Y.%m.%d')
adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/' + adresseTime

#create csv-file
with open(adresse + '.csv', 'w') as file:

    writer = csv.writer(file)

#get input from calibration
#important: use correct data type
slope = float(input('Give the slope from the calibration as a float and confirm with Enter:   '))    
intercept = float(input('Give the intercept from the calibration as a float and confirm with Enter:    '))
rSq = float(input('Give the R^2 from the calibration as a float and confirm with Enter:    '))

#start endless loop
while counter1 < 8:

    if client.connect():  #trying to connect to Modbus Server/Slave
        #reading from a holding register
        #startregister = 100, registers to be read = 8, answer size = 1 byte
        res = client.read_holding_registers(address=100, count=8, unit=1)
        
        #define decoder for res (registers to be read) to get the organisation for big endian
        #important: big endian = '>' 
        decoder = BinaryPayloadDecoder.fromRegisters(res.registers, byteorder='>', wordorder='>')
        #use decoder to get values in 32-bit float big endian
        first_reading = decoder.decode_32bit_float()
        second_reading = decoder.decode_32bit_float()
        third_reading = decoder.decode_32bit_float()
        fourth_reading = decoder.decode_32bit_float()                                            

        if not res.isError():  #if registers don't show Error

            summePCO2.append(first_reading) #summePCO2 is the array of the pCO2s a.k.a the readings from the 1st read register
            summeTemp.append(second_reading)
            summembar.append(third_reading)
            summeDLI.append(fourth_reading)
            
            #add 1 to counter for median loop
            counter1 += 1

            if counter1 == 6: #after 1 min do this
                    
                #calculate median for 1 min
                avPCO2 = np.median(summePCO2)
                avTemp = np.median(summeTemp)
                avmbar = np.median(summembar)
                avDLI = np.median(summeDLI)

                #add calibration to pCO2
                avPCO2 = avPCO2 * slope + intercept
                
                #get times to fill csv file
                t = time()
                dateForCSV = ctime(t)
                
                loopedTime = datetime.now()
                csvTimeCounter = loopedTime - startTime

                #add data to the list for writing into the csv file
                #important: if order of columns changes, this has to be updated in dash_usage.py & measurement.py
                csvRow.append(dateForCSV)
                csvRow.append(csvTimeCounter)
                csvRow.append(avPCO2)
                csvRow.append(avTemp)
                csvRow.append(avmbar)
                csvRow.append(avDLI)

                #write the data in the csv file
                with open(adresse +'.csv', 'a') as file:

                    writer = csv.writer(file)
                    
                    writer.writerow(csvRow)
                    


                sleep(7)  # Stops Loop for 7sec, changed from 10sec to 7sec to keep overall length at 60sec

                print('----------------------------------------------------------------')

                #set variables back to 0
                counter1 = 0
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
                
                #clear csvRow-List and variables
                csvRow = []

                loopedTime = 0
                csvTimeCounter = 0

                #print information for user, how long is the code running now, counter2 gets reset after 4 days
                print('Code is running for ' + str(counter2) + ' minutes.')

                if counter2 == 5760: #check if 4 days are over
                    #set time variables for plot and csv-file back                 
                    divider = []
                    #create lines to write calibration information at end of csv file
                    headerCalculations = ["Slope", "Intercept", "R^2"]
                    csvRow = []
                    csvRow.append(slope)
                    csvRow.append(intercept)
                    csvRow.append(rSq)
                    
                    #write calibration information at end of csv file
                    with open(adresse + '.csv', 'a') as file:

                        writer = csv.writer(file)
                        writer.writerow(divider)
                        writer.writerow(headerCalculations)
                        writer.writerow(csvRow)
                    
                    #set variables back
                    startTime = datetime.now()
                    loopedTime = 0
                    csvTimeCounter = 0

                    csvRow = []
                    counter2 = 0

                    #set time for csv-filename back
                    adresseTime = datetime.now().strftime('%Y.%m.%d')
                    adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/' + adresseTime

                else: #if 4 days aren't over, add 1 to counter
                    counter2 += 1

            else:

                sleep(10)  #Stops Loop for 10sec
                print('')

        else:
            print(res)  # Print Error Message, for meaning look at (insert git hub)
            counter1 = 0 #set counter1 = 0 to keep loop going
            sleep(10)  # Stops Loop for 10sec

    else:  # If not able to connect, do this
        #show in terminal to inform user
        print('Cannot connect to the Transmitter M80 SM and Sensor InPro 5000i.')
        print('----------------------------------------------------------------')
        print('Please check the following things:')
        print('Does the RS485-to-USB Adapter have power? Which LEDs are active?')
        print('Are the cables connected correctly?')

        counter1 = 0 #set counter1 = 0 to keep loop going
        sleep(10)  # Stops Loop for 10sec
