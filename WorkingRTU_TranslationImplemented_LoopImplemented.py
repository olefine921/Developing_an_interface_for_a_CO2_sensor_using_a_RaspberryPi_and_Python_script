from pymodbus.client.sync import ModbusSerialClient
from time import time, sleep


client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyUSB0',
    baudrate=19200,
    timeout=3,
    parity='N',
    stopbits=2,
    bytesize=8
)


counter = 1


while counter < 5000:
    

    
    while counter < 4900:
        counter += 1
    else:
        counter == 1 #counter is way too fast -> timed loop needed!
        
        if client.connect():  # Trying for connect to Modbus Server/Slave
            '''Reading from a holding register with the below content.'''
            res = client.read_holding_registers(address=100, count=8, unit=1)

            '''Reading from a discrete register with the below content.'''
            # res = client.read_discrete_inputs(address=100, count=8, unit=1)

            if not res.isError():
                print(res.registers)
                
                #translate data to 32-bit float big endian
                
                #decodeData = res.decode word_order = little byte_order = little formatters = float32
                
                #floatData = data_to_float32(res.registers)
                #print(floatData)
            else:
                print(res)

        else:
            print('Cannot connect to the Modbus Server/Slave')
        
        


