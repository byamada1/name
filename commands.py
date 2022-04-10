# Importing Libraries
import serial
import time

OPCODES = {
    "get health" : b'\x00\x00',
    "set health" : b'\x00\x01',
    "get skillpoints" : b'\x01\x00',
    "set skillpoints" : b'\x01\x01',
    "gain item" : b'\x02',
    "lose item" : b'\x03',
    "get inventory" : b'\x04\x00',
    "set inventory" : b'\x04\x01',
    "get playername" : b'\x05\x00',
    "set playername" : b'\x05\x01',
    "get stats" : b'\x06\x00',
    "set stats" : b'\x06\x01',
    "get exiting player" : b'\x07',
    "send done" : b'\x08'
}

hub = serial.Serial(port='COM13', baudrate=9600, timeout=0.05)

def write_commands(player, command, data, reply_expected=False):
    reply = []

    packet = bytearray()
    packet += bytes((player,))
    packet += OPCODES[command]

    if not reply_expected:
        if type(data) == str:
            transformed_data = data.encode()
        elif type(data) == list:
            transformed_data = serial.to_bytes(data)
        else:
            transformed_data = data.to_bytes(2, "little")
        packet += serial.to_bytes((len(transformed_data),))
        packet += transformed_data
    
    hub.write(packet)
    time.sleep(0.05)
    if reply_expected:
        reply_len = hub.read(1)

        reply = hub.read(reply_len)
    return reply

write_commands(0, "set health", 300)