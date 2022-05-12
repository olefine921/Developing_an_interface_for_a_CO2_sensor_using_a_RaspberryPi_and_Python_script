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
counter1 = 0 #for median loop
counter2 = 1 #for counting the days -> 5760 = 4days
counter3 = 0 #for making and saving 5 plots for the diashow
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

#variables only for plotting
startTime = datetime.now()
loopedTime = 0
csvTimeCounter = 0

date = []
x =[]
plotAvPCO2 = []
plotAvTemp = []

csvRow = []

adresseTime = datetime.now().strftime('%Y.%m.%d')
adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/' + adresseTime

#create csv-file
with open(adresse + '.csv', 'w') as file:

    writer = csv.writer(file)

#get input from calibration
slope = float(input('Give the slope from the calibration as a float and confirm with Enter:   '))    
intercept = float(input('Give the intercept from the calibration as a float and confirm with Enter:    '))
rSq = float(input('Give the R^2 from the calibration as a float and confirm with Enter:    '))

#start endless loop
while counter1 < 8:

    if client.connect():  #trying to connect to Modbus Server/Slave
        #reading from a holding register
        #startregister = 100, registers to be read = 8, answer size = 1 byte
        res = client.read_holding_registers(address=100, count=8, unit=1)
        #creat decoder for res: '>' = Big Endian
        decoder = BinaryPayloadDecoder.fromRegisters(res.registers, byteorder='>', wordorder='>')
        #use decoder to get 32bit float big endian
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

            #after 1 min do this
            if counter1 == 6:
                #loop for plot names -> to get diashow
                if counter3 == 5:
                    counter3 = 1
                else:
                    counter3 +=1
                    
                #calculate median for 1 min
                avPCO2 = np.median(summePCO2)
                avTemp = np.median(summeTemp)
                avmbar = np.median(summembar)
                avDLI = np.median(summeDLI)

                #add calibration to pCO2
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

                with open(adresse +'.csv', 'a') as file:

                    writer = csv.writer(file)
                    
                    writer.writerow(csvRow)
                    
                csvTimeCounter = str(csvTimeCounter)
                x.append(csvTimeCounter)
                plotAvPCO2.append(avPCO2)
                plotAvTemp.append(avTemp)

                x = x[-20:]
                plotAvPCO2 = plotAvPCO2[-20:]
                plotAvTemp = plotAvTemp[-20:]

                fig, ax1 = plt.subplots(figsize=(23, 13))

                plt.suptitle('Average pCO2 and Temp starting at ' + adresseTime, fontsize = 20, fontweight='semibold')

                color = 'tab:red'
                ax1.set_xlabel('time (min)', fontsize = 18,fontweight='semibold')
                ax1.set_xticks(np.arange(0, len(x)+1, 5))
                plt.xticks(fontsize = 14)
                ax1.set_ylabel('pCO2 in %', color = color, fontsize = 18,fontweight='semibold')
                ax1.plot(x,plotAvPCO2, color = color, linewidth = 6)
                plt.xticks(rotation = 25, fontweight='semibold')
                plt.yticks(fontsize = 14, fontweight='semibold')

                ax2 = ax1.twinx()

                color = 'tab:blue'
                ax2.set_ylabel('avTemp in °C', color = color, fontsize = 18,fontweight='semibold')
                ax2.set_ylim(20,35)
                ax2.plot(plotAvTemp, color = color, linewidth = 4)
                plt.yticks(fontsize = 14, fontweight='semibold')

                fig.tight_layout()
                
                fig.savefig('/media/pi/boot/pCO2_Sensor_Data/Plots/TestPlot_' + str(counter3) + '.png')
                
                sleep(10)  # Stops Loop for 10sec
                
                plt.close('all')
                fig.clear()

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

                print('Code is running for ' + str(counter2) + ' minutes.')

                if counter2 == 5760: #check if 4 days are over
                    #set time variables for plot and csv-file back
                    
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
                    
                    startTime = datetime.now()
                    loopedTime = 0
                    csvTimeCounter = 0

                    date = []
                    x = []
                    plotAvPCO2 = []
                    plotAvTemp = []
                    csvRow = []

                    #set time for csv-filename back
                    adresseTime = datetime.now().strftime('%Y.%m.%d')
                    adresse = '/media/pi/boot/pCO2_Sensor_Data/CSV-Files/' + adresseTime

                else: #if 4 days aren't over, add 1 to counter
                    counter2 += 1

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
