import struct


def build_float_matrix(data_list):
    """
    构建浮点数矩阵
    """
    float_matrix = b"".join(struct.pack("<f", value) for value in data_list)
    return float_matrix


def build_vofa_stream(float_matrix):
    """
    构建 VOFA 数据流
    """
    frame_tail = struct.pack("<f", float("+inf"))  # VOFA帧尾(+Infinity)
    vofa_stream = float_matrix + frame_tail
    return vofa_stream
