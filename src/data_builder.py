import struct


def build_vofa_stream(data_list):
    """
    构建 VOFA 数据流

    该函数接受一个float型数据列表，将其转换为特定格式的数据流，用于VOFA（Voice over Frame Analysis）处理。
    [<class 'float'>, <class 'float'>, <class 'float'>, <class 'float'>]
    它首先将列表中的数据转换为浮点数矩阵，然后添加一个特殊的帧尾标记，表示数据流的结束。

    参数:
    - data_list: 一个包含数据值的列表，这些数据值将被转换为VOFA数据流。

    返回值:
    - vofa_stream: 转换后的VOFA数据流，格式为字节字符串，包含所有数据值和帧尾标记。
    """
    # 构建浮点数矩阵
    float_matrix = b"".join(struct.pack("<f", value) for value in data_list)
    # 构建 VOFA 帧尾 (+Infinity)
    frame_tail = struct.pack("<f", float("+inf"))
    # 返回完整的 VOFA 数据流
    vofa_stream = float_matrix + frame_tail
    return vofa_stream
