from pymodbus.client.sync import ModbusSerialClient  # Import the pymodbus library part for syncronous master (=client)
from pymodbus.payload import BinaryPayloadDecoder #import BinaryPayloadDecoder for translation
from time import time, ctime, sleep #import the time library
from datetime import datetime, date, timedelta #import the datetime library
import matplotlib.pyplot as plt #import matplotlib and numpy for plotting
import matplotlib.animation as animation
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
counter1 = 0 #For getting the sum of 6 data points and getting the average after counter = 6 => get the average of 1 minute
counter2 = 0
counter3 = 0

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

csvRow = []

now = datetime.now()
adresseDate = now.strftime("%d.%m.%Y")
adresse = '/home/pi/Desktop/CSV_' + adresseDate  #trying to outsource the naming of the saved documents


with open(adresse + '.csv', 'w') as file: #creating & defining the csv-file

    writer = csv.writer(file)


fig, (ax1, ax2) = plt.subplots(2)



date = []
x =[] #holds numbers for x axis -> the difference of each datapoint time to the start time
plotAvPCO2 = []
plotAvTemp = []

def animate(i, x, plotAvPCO2, plotAvTemp):
    global counter1, summePCO2, summeTemp, summembar, summeDLI, csvRow
    while counter1 < 6:
        t = time()
        dateForCSV = ctime(t)

        if client.connect():  # Trying to connect to Modbus Server/Slave
            # Reading from a holding register
            res = client.read_holding_registers(address=100, count=8,
                                                unit=1)  # Startregister = 100, Registers to be read = 8, Answer size = 1 byte

            decoder = BinaryPayloadDecoder.fromRegisters(res.registers, byteorder='>',
                                                         wordorder='>')  # decode with BinaryPayloadDecoder, ! Big.Endian = '>' !

            first_reading = decoder.decode_32bit_float()  # reads & translates the 1. chanel => pCO2 in %
            second_reading = decoder.decode_32bit_float()  # reads & translates the 2. chanel => Temp in °C
            third_reading = decoder.decode_32bit_float()  # reads & translates the 3. chanel => mbar
            fourth_reading = decoder.decode_32bit_float()  # reads & translates the 4. chanel =>

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

                    #print(csvRow)

                    with open(adresse +'.csv', 'a') as file:

                        writer = csv.writer(file)

                        writer.writerow(csvRow)
                    # sleep(10)  # Stops Loop for 10sec

                    x.append(datetime.now().strftime('%H:%M:%S.%f'))
                    plotAvPCO2.append(avPCO2)
                    plotAvTemp.append(avTemp)

                    x = x[-20:]
                    plotAvPCO2 = plotAvPCO2[-20:]
                    plotAvTemp = plotAvTemp[-20:]

                    ax1.clear()

                    color = 'tab:red'
                    ax1.set_xlabel('time (min)')
                    ax1.set_xticks(np.arange(0, len(x) + 1, 10))
                    ax1.set_ylabel('pCO2 in %', color=color)
                    ax1.plot(x, plotAvPCO2, color=color)
                    plt.xticks(rotation=25)

                    ax2.clear()

                    color = 'tab:blue'
                    ax2.set_xlabel('time (min)')
                    ax2.set_xticks(np.arange(0, len(x) + 1, 10))
                    ax2.set_ylabel('avTemp in °C', color=color)
                    ax2.plot(x, plotAvTemp, color=color)
                    plt.xticks(rotation=45)

                    fig.tight_layout()

                    

                    print(plotAvPCO2)
                    print(plotAvTemp)

                    print('----------------------------------------------------------------')

                    # set every variable back to 0

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

                    # clear csvRow-List
                    csvRow = []

                    # clear time variables for difference
                    loopedTime = 0
                    csvTimeCounter = 0

                    # clear arrays for plotting


                else:
                    print('---')

                    # sleep(10)  # Stops Loop for 10sec"""

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


    


while counter3 <1440:
    

    ani = animation.FuncAnimation(fig, animate, fargs=(x, plotAvPCO2, plotAvTemp),
                                                  interval=60000)  # 60000 = 1Min
    plt.show(block=False)
    print(counter3)
    counter1 = 0
    counter3 +=1
