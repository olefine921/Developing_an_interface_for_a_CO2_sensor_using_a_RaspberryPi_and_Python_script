Code:

from pymodbus.client.sync import ModbusSerialClient  # Import the pymodbus library part for syncronous master (=client)
from time import time, ctime, sleep

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
counter1 = 0
counter2 = 1

# Variables
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

# Test Data


# Give date + time for csv-file




while counter1 < 8:
    t = time()
    dateForCSV = ctime(t)
    
    print(dateForCSV)
    print('')

    if client.connect():  # Trying to connect to Modbus Server/Slave
        # Reading from a holding register
        res = client.read_holding_registers(address=100, count=8,
                                            unit=1)  # Startregister = 100, Registers to be read = 8, Answer size = 1 byte

        if not res.isError():  # If Registers don't show Error
            print(res.registers)  # Print content of registers

            t = time()
            dateForCSV = ctime(t)

            print(dateForCSV)
            print('Start of loop')


            pCO2 = res.registers[0]
            temp = res.registers[2]
            mbar = res.registers[4]
            DLI = res.registers[6]

            print('')
            print('temp = ', temp)


            summePCO2 += pCO2
            summeTemp += temp
            summembar += mbar
            summeDLI += DLI

            t = time()
            dateForCSV = ctime(t)

            print(dateForCSV)

            print('summeTemp = ', summeTemp)

            counter1 += 1

            print(counter1)

            if counter1 == 6:
                # Calculate Average for 1 Min

                avPCO2 = summePCO2 / 6
                avTemp = summeTemp / 6
                avmbar = summembar / 6
                avDLI = summeDLI / 6
                print('')
                print('avTemp = ', avTemp)

                counter1 = 0
                print(counter1)
                print('End of Loop')
                sleep(10)  # Stops Loop for 10sec

            else:

                sleep(10)  # Stops Loop for 10sec

        else:
            print(res)  # Print Error Message, for meaning look at (insert git hub)

            sleep(10)  # Stops Loop for 10sec
            
    else:  # If not able to connect, do this
        print('Cannot connect to the Transmitter M80 SM and Sensor InPro 5000i.')
        print('----------------------------------------------------------------')
        print('Please check the following things:')
        print('Does the RS485-to-USB Adapter have power? Which LEDs are active?')
        print('Are the cables connected correctly?')

        print(counter1)
        sleep(10)  # Stops Loop for 10sec


Output:

Python 3.9.2 (/usr/bin/python3)
>>> %Run rtuloopaverage23.03.2022_11.30.py
Wed Mar 23 11:49:05 2022

Cannot connect to the Transmitter M80 SM and Sensor InPro 5000i.
----------------------------------------------------------------
Please check the following things:
Does the RS485-to-USB Adapter have power? Which LEDs are active?
Are the cables connected correctly?
0
Wed Mar 23 11:49:15 2022

Cannot connect to the Transmitter M80 SM and Sensor InPro 5000i.
----------------------------------------------------------------
Please check the following things:
Does the RS485-to-USB Adapter have power? Which LEDs are active?
Are the cables connected correctly?
0
Wed Mar 23 11:49:25 2022

Cannot connect to the Transmitter M80 SM and Sensor InPro 5000i.
----------------------------------------------------------------
Please check the following things:
Does the RS485-to-USB Adapter have power? Which LEDs are active?
Are the cables connected correctly?
0
Wed Mar 23 11:49:35 2022

[15888, 36579, 16841, 44564, 16302, 59158, 16372, 169]
Wed Mar 23 11:49:35 2022
Start of loop

temp =  16841
Wed Mar 23 11:49:35 2022
summeTemp =  16841
1
Wed Mar 23 11:49:45 2022

[15888, 30853, 16841, 34078, 16302, 52681, 16371, 64050]
Wed Mar 23 11:49:45 2022
Start of loop

temp =  16841
Wed Mar 23 11:49:45 2022
summeTemp =  33682
2
Wed Mar 23 11:49:55 2022

[15888, 22248, 16841, 18350, 16302, 42945, 16371, 61521]
Wed Mar 23 11:49:55 2022
Start of loop

temp =  16841
Wed Mar 23 11:49:55 2022
summeTemp =  50523
3
Wed Mar 23 11:50:05 2022

[15888, 48088, 16842, 0, 16303, 6640, 16372, 3548]
Wed Mar 23 11:50:05 2022
Start of loop

temp =  16842
Wed Mar 23 11:50:05 2022
summeTemp =  67365
4
Wed Mar 23 11:50:15 2022

[15889, 7574, 16845, 18350, 16303, 27490, 16370, 11867]
Wed Mar 23 11:50:15 2022
Start of loop

temp =  16845
Wed Mar 23 11:50:15 2022
summeTemp =  84210
5
Wed Mar 23 11:50:25 2022

[15889, 32543, 16849, 49807, 16303, 44444, 16367, 24224]
Wed Mar 23 11:50:25 2022
Start of loop

temp =  16849
Wed Mar 23 11:50:25 2022
summeTemp =  101059
6

avTemp =  16843.166666666668
0
End of Loop
Wed Mar 23 11:50:35 2022

[15890, 52587, 16854, 31457, 16305, 2219, 16365, 55882]
Wed Mar 23 11:50:35 2022
Start of loop

temp =  16854
Wed Mar 23 11:50:35 2022
summeTemp =  117913
1
Wed Mar 23 11:50:45 2022

[15892, 53613, 16859, 2621, 16307, 15833, 16365, 34621]
Wed Mar 23 11:50:45 2022
Start of loop

temp =  16859
Wed Mar 23 11:50:45 2022
summeTemp =  134772
2
Wed Mar 23 11:50:56 2022

[15894, 27270, 16862, 52428, 16308, 63930, 16365, 5665]
Wed Mar 23 11:50:56 2022
Start of loop

temp =  16862
Wed Mar 23 11:50:56 2022
summeTemp =  151634
3
Wed Mar 23 11:51:06 2022

[15895, 11502, 16864, 0, 16309, 54197, 16365, 21200]
Wed Mar 23 11:51:06 2022
Start of loop

temp =  16864
Wed Mar 23 11:51:06 2022
summeTemp =  168498
4
Wed Mar 23 11:51:16 2022

[15897, 31788, 16868, 47186, 16312, 23053, 16365, 7582]
Wed Mar 23 11:51:16 2022
Start of loop

temp =  16868
Wed Mar 23 11:51:16 2022
summeTemp =  185366
5
Wed Mar 23 11:51:26 2022

[15900, 18288, 16872, 57671, 16315, 31073, 16365, 65004]
Wed Mar 23 11:51:26 2022
Start of loop

temp =  16872
Wed Mar 23 11:51:26 2022
summeTemp =  202238
6

avTemp =  33706.333333333336
0
End of Loop
Wed Mar 23 11:51:36 2022

[15900, 25475, 16873, 2621, 16315, 39097, 16366, 1734]
Wed Mar 23 11:51:36 2022
Start of loop

temp =  16873
Wed Mar 23 11:51:36 2022
summeTemp =  219111
1
