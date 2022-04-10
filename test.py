import serial

hub = serial.Serial(port='COM5', baudrate=9600, timeout=1)

#hub.write(b'hello')
hub.write(b'\x01\x00\x01\x02\xe9\x01')