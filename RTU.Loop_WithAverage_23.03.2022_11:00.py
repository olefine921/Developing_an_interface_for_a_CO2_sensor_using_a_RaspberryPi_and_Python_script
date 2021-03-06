from pymodbus.client.sync import ModbusSerialClient # Import the pymodbus library part for syncronous master (=client)
from time import time, ctime, sleep


client = ModbusSerialClient(
    method='rtu', #Modbus Modus = RTU = via USB & RS485
    port='/dev/ttyUSB0', #Connected over ttyUSB0, not AMA0
    baudrate=19200, #Baudrate was changed from 38400 to 19200
    timeout=3, #
    parity='N', #Parity = None
    stopbits=2, #Bites was changed from 1 to 2
    bytesize=8 #
)
#Counter
counter1 = 0
counter2 = 1

#Variables
t = 0

pCO2 = 0
temp = 0
mbar = 0
DLI = 0

summePCO2 = 0
summeTemp = 0
summembar = 0
summeDLI = 0

avPCO2 = 0
avTemp = 0
avmbar = 0
avDLI = 0

#Test Data



#Give date + time for csv-file

t = time()
dateForCSV = ctime(t)

print(dateForCSV)
print('')

if client.connect():  # Trying to connect to Modbus Server/Slave
    #Reading from a holding register
    res = client.read_holding_registers(address=100, count=8, unit=1) #Startregister = 100, Registers to be read = 8, Answer size = 1 byte



    if not res.isError(): #If Registers don't show Error
        print(res.registers) #Print content of registers
        
        t = time()
        dateForCSV = ctime(t)

        print(dateForCSV)
        print('Start of loop')

        while counter1 < 8:
         

            pCO2 = res.registers[0]
            temp = res.registers[3]
            mbar = res.registers[5]
            DLI =  res.registers[7]


            print('')
            print('pCO2 = ', pCO2)
            print(mbar)

            summePCO2 += pCO2
            summeTemp += temp
            summembar += mbar
            summeDLI += DLI

            t = time()
            dateForCSV = ctime(t)

            print(dateForCSV)


            print('summePCO2 = ', summePCO2)
            print(summembar)

            counter1 += 1

            print(counter1)

            if counter1 == 6:
                #Calculate Average for 1 Min

                avPCO2 = summePCO2 / 6
                avTemp = summeTemp / 6
                avmbar = summembar / 6
                avDLI = summeDLI / 6
                print('')
                print('avPCO2 = ', avPCO2)
                print(avmbar)

                counter1 = 0
                print(counter1)        
                print('End of Loop')

            else:

                sleep(10)  # Stops Loop for 10sec
        
    else:
        print(res) #Print Error Message, for meaning look at (insert git hub)

else: #If not able to connect, do this
    print('Cannot connect to the Transmitter M80 SM and Sensor InPro 5000i.')
    print('----------------------------------------------------------------')
    print('Please check the following things:')
    print('Does the RS485-to-USB Adapter have power? Which LEDs are active?')
    print('Are the cables connected correctly?')