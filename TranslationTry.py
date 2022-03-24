from pymodbus.client.sync import ModbusSerialClient # Import the pymodbus library part for syncronous master (=client)

client = ModbusSerialClient(
    method='rtu', #Modbus Modus = RTU = via USB & RS485
    port='/dev/ttyUSB0', #Connected over ttyUSB0, not AMA0
    baudrate=19200, #Baudrate was changed from 38400 to 19200
    timeout=3, #
    parity='N', #Parity = None
    stopbits=2, #Bites was changed from 1 to 2
    bytesize=8 #
)

if client.connect():  # Trying to connect to Modbus Server/Slave
    #Reading from a holding register
    res = client.read_holding_registers(address=100, count=8, unit=1) #Startregister = 100, Registers to be read = 8, Answer size = 1 byte




    if not res.isError(): #If Registers don't show Error

        decoder = BinaryPailoadDecoder.fromRegisters(res.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        active_power_w = decoder.decode_32bit_int()
        print(res.registers) #Print content of registers
    else:
        print(res) #Print Error Message, for meaning look at (insert git hub)

else: #If not able to connect, do this
    print('Cannot connect to the Transmitter M80 SM and Sensor InPro 5000i.')
    print('Please check the following things:')
    print('Does the RS485-to-USB Adapter have power? Which LEDs are active?')
    print('Are the cables connected correctly?')