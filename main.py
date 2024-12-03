import struct
import math
import socket
import time
import serial
import json


# 数据生成函数
def generate_data(channel_count, func_type="sin", t=0.0):
    """
    Generate floating-point data for the specified number of channels.

    Parameters:
        channel_count (int): Number of channels.
        func_type (str): 'sin' or 'cos' function to generate data.
        t (float): Current time or phase.

    Returns:
        list[float]: List of generated floating-point values.
    """
    data = []
    for i in range(1, channel_count + 1):
        if func_type == "sin":
            data.append(math.sin(i * t))
        elif func_type == "cos":
            data.append(math.cos(i * t))
        else:
            raise ValueError("func_type must be 'sin' or 'cos'")
    return data


# 从串口获取数据
def read_from_serial(port, baudrate=115200, channel_count=4):
    """
    Read data from a serial port and convert it to a float list.

    Parameters:
        port (str): Serial port name.
        baudrate (int): Baud rate for serial communication.
        channel_count (int): Number of channels to read from the serial port.

    Returns:
        list[float]: List of floating-point values read from the serial port.
    """
    ser = serial.Serial(port, baudrate, timeout=1)
    data = []
    for _ in range(channel_count):
        byte_data = ser.read(4)  # Read 4 bytes for a single float
        if len(byte_data) == 4:
            value = struct.unpack("<f", byte_data)[0]  # Convert bytes to float
            data.append(value)
    ser.close()
    return data


# 从UDP服务器获取数据
def read_from_udp(host, port, channel_count=4):
    """
    Read data from a UDP server.

    Parameters:
        host (str): UDP server host.
        port (int): UDP server port.
        channel_count (int): Number of channels to read from the UDP server.

    Returns:
        list[float]: List of floating-point values received from the UDP server.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    data = []
    while len(data) < channel_count:
        message, _ = sock.recvfrom(1024)  # Receive message from UDP server
        for i in range(0, len(message), 4):
            value = struct.unpack("<f", message[i : i + 4])[0]
            data.append(value)
    sock.close()
    return data


# 浮点数矩阵构建函数
def build_float_matrix(data_list):
    """
    Convert a list of floating-point numbers into a byte stream matrix.

    Parameters:
        data_list (list[float]): List of floating-point numbers.

    Returns:
        bytes: Byte stream representing the floating-point data.
    """
    float_matrix = b"".join(struct.pack("<f", value) for value in data_list)
    return float_matrix


# VOFA 数据流构建函数
def build_vofa_stream(float_matrix):
    """
    Build VOFA data stream by appending the frame tail to the float matrix.

    Parameters:
        float_matrix (bytes): Byte stream of floating-point data.

    Returns:
        bytes: Complete VOFA data stream.
    """
    frame_tail = struct.pack("<f", float("+inf"))  # VOFA frame tail (+Infinity)
    vofa_stream = float_matrix + frame_tail
    return vofa_stream


# 持续生成数据并通过 UDP 转发
def udp_send_vofa_stream(config):
    """
    Continuously generate VOFA data stream and send it via UDP.

    Parameters:
        config (dict): Configuration dictionary with keys:
            - 'ip' (str): Target IP address.
            - 'port' (int): Target port.
            - 'channel_count' (int): Number of channels.
            - 'func_type' (str): 'sin' or 'cos'.
            - 'interval' (float): Time interval between transmissions (in seconds).
            - 'data_source' (str): The source of the data ('generated', 'serial', 'udp').
            - 'serial_port' (str): Serial port name (required if 'data_source' is 'serial').
            - 'udp_host' (str): UDP host address (required if 'data_source' is 'udp').
            - 'udp_port' (int): UDP host port (required if 'data_source' is 'udp').
    """
    ip = config["ip"]
    port = config["port"]
    channel_count = config["channel_count"]
    func_type = config["func_type"]
    interval = config["interval"]
    data_source = config["data_source"]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t = 0.0  # Initial time/phase

    try:
        print(f"Sending VOFA data to {ip}:{port}...")
        while True:
            if data_source == "generated":
                # Generate data
                data = generate_data(channel_count, func_type, t)
            elif data_source == "serial":
                serial_port = config["serial_port"]
                data = read_from_serial(serial_port, channel_count=channel_count)
            elif data_source == "udp":
                udp_host = config["udp_host"]
                udp_port = config["udp_port"]
                data = read_from_udp(udp_host, udp_port, channel_count=channel_count)
            else:
                raise ValueError(
                    "Invalid data source. Choose 'generated', 'serial', or 'udp'."
                )

            # Build float matrix and VOFA stream
            float_matrix = build_float_matrix(data)
            vofa_stream = build_vofa_stream(float_matrix)

            # Send via UDP
            sock.sendto(vofa_stream, (ip, port))

            # Print debug info
            print(f"Sent VOFA Data Stream: {vofa_stream.hex(' ')}")

            # Increment time and wait for the next interval
            t += interval
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nTransmission stopped.")
    finally:
        sock.close()


# 主程序
if __name__ == "__main__":
    # 配置字典
    config = {
        "ip": "127.0.0.1",
        "port": 5000,
        "channel_count": 4,
        "func_type": "sin",  # or "cos"
        "interval": 0.1,  # Seconds
        "data_source": "generated",  # Options: 'generated', 'serial', 'udp'
        "serial_port": "/dev/ttyUSB0",  # Used if data_source is 'serial'
        "udp_host": "127.0.0.1",  # Used if data_source is 'udp'
        "udp_port": 5001,  # Used if data_source is 'udp'
    }

    # 启动数据发送
    udp_send_vofa_stream(config)
