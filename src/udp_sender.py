import socket


def send_udp_data(ip, port, vofa_stream):
    """
    通过 UDP 发送 VOFA 数据流
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(vofa_stream, (ip, port))
    finally:
        sock.close()
