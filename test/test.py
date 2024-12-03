import struct
import math
import socket
import time


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
def udp_send_vofa_stream(ip, port, channel_count, func_type="sin", interval=0.1):
    """
    Continuously generate VOFA data stream and send it via UDP.

    Parameters:
        ip (str): Target IP address.
        port (int): Target port.
        channel_count (int): Number of channels.
        func_type (str): 'sin' or 'cos'.
        interval (float): Time interval between transmissions (in seconds).
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t = 0.0  # Initial time/phase

    try:
        print(f"Sending VOFA data to {ip}:{port}...")
        while True:
            # Generate data
            data = generate_data(channel_count, func_type, t)

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
    # 用户设置参数
    target_ip = input("Enter target IP address: ").strip()
    target_port = int(input("Enter target port: "))
    channel_count = int(input("Enter the number of channels (N): "))
    func_type = input("Enter the function type ('sin' or 'cos'): ").strip().lower()
    interval = float(input("Enter the interval between transmissions (seconds): "))

    # 启动数据发送
    udp_send_vofa_stream(target_ip, target_port, channel_count, func_type, interval)
