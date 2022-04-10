# Importing Libraries
import serial
import time

OPCODES = {
    "get health" : b'00',
    "set health" : b'01',
    "get skillpoints" : b'10',
    "set skillpoints" : b'11',
    "gain item" : b'2',
    "lose item" : b'3',
    "get inventory" : b'40',
    "set inventory" : b'41',
    "get playername" : b'50',
    "set playername" : b'51',
    "get stats" : b'60',
    "set stats" : b'61',
    "get exiting_player" : b'7',
    "send done" : b'8'
}

hub = serial.Serial(port='COM13', baudrate=9600, timeout=0.05)

def write_commands(player, command, data, reply_expected=False):
    reply = []

    packet = bytes()
    packet += serial.to_bytes(player)
    packet += OPCODES[command]

    if not reply_expected:
        transformed_data = serial.to_bytes(data)
        packet += serial.to_bytes(len(transformed_data))
        packet += serial.to_bytes(transformed_data)

    hub.write(packet)
    time.sleep(0.05)
    if reply_expected:
        reply_len = hub.read(1)

        reply = hub.read(reply_len)
    return reply