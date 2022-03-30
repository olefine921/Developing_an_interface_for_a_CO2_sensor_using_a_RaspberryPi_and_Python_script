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


result = [15873, 15774, 16831, 2621, 16284, 50208, 16355, 13656]


#translate data to 32-bit float big endian
        
decodeData = result.decode(word_order=big, byte_order=big, formatters=float32)
print(decodeData)


floatData = data_to_float32(res.registers)
print(floatData)


print(res)
