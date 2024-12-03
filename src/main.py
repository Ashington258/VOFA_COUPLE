from udp_handler import udp_send_vofa_stream


def main():
    config = {
        "ip": "127.0.0.1",
        "port": 5000,
        "channel_count": 4,
        "func_type": "sin",
        "interval": 0.1,
        "data_source": "generated",
        "serial_port": "/dev/ttyUSB0",
        "udp_host": "127.0.0.1",
        "udp_port": 5001,
    }
    udp_send_vofa_stream(config)


if __name__ == "__main__":
    main()
