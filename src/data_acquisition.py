import struct
import serial
import socket


def read_from_serial(port, baudrate=115200, channel_count=4):
    ser = serial.Serial(port, baudrate, timeout=1)
    data = [
        struct.unpack("<f", ser.read(4))[0]
        for _ in range(channel_count)
        if len(ser.read(4)) == 4
    ]
    ser.close()
    return data


def read_from_udp(host, port, channel_count=4):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    data = []
    while len(data) < channel_count:
        message, _ = sock.recvfrom(1024)
        data.extend(
            struct.unpack("<f", message[i : i + 4])[0]
            for i in range(0, len(message), 4)
        )
    sock.close()
    return data
