import socket
import time
from data_processing import generate_data, build_float_matrix, build_vofa_stream
from data_acquisition import read_from_serial, read_from_udp


def udp_send_vofa_stream(config):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t = 0.0
    try:
        while True:
            if config["data_source"] == "generated":
                data = generate_data(config["channel_count"], config["func_type"], t)
            elif config["data_source"] == "serial":
                data = read_from_serial(
                    config["serial_port"], channel_count=config["channel_count"]
                )
            elif config["data_source"] == "udp":
                data = read_from_udp(
                    config["udp_host"],
                    config["udp_port"],
                    channel_count=config["channel_count"],
                )
            else:
                raise ValueError(
                    "Invalid data source. Choose 'generated', 'serial', or 'udp'."
                )

            float_matrix = build_float_matrix(data)
            vofa_stream = build_vofa_stream(float_matrix)
            sock.sendto(vofa_stream, (config["ip"], config["port"]))

            print(f"Sent VOFA Data Stream: {vofa_stream.hex(' ')}")
            t += config["interval"]
            time.sleep(config["interval"])
    except KeyboardInterrupt:
        print("\nTransmission stopped.")
    finally:
        sock.close()
