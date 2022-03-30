from pymodbus.client.sync import ModbusSerialClient

client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyUSB0',
    baudrate=19200,
    timeout=3,
    parity='N',
    stopbits=2,
    bytesize=8
)



if client.connect():  # Trying for connect to Modbus Server/Slave
    '''Reading from a holding register with the below content.'''
    res = client.read_holding_registers(address=100, count=8, unit=1)

    '''Reading from a discrete register with the below content.'''
    # res = client.read_discrete_inputs(address=100, count=8, unit=1)

    if not res.isError():
        print(res.registers)
        
        #translate data to 32-bit float big endian
                
        decodeData = res.decode(word_order=big, byte_order=big, formatters=float32)
        print(decodeData)
        
        
        #floatData = data_to_float32(res.registers)
        #print(floatData)
        
    else:
        print(res)

else:
    print('Cannot connect to the Modbus Server/Slave')