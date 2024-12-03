import struct
import math


def generate_data(channel_count, func_type="sin", t=0.0):
    return [
        math.sin(i * t) if func_type == "sin" else math.cos(i * t)
        for i in range(1, channel_count + 1)
    ]


def build_float_matrix(data_list):
    return b"".join(struct.pack("<f", value) for value in data_list)


def build_vofa_stream(float_matrix):
    frame_tail = struct.pack("<f", float("+inf"))
    return float_matrix + frame_tail
