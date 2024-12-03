import struct
import math


# 1. 数据生成函数
def generate_data(channel_count, func_type="sin", t=0.0, step=0.1):
    """
    Generate floating-point data for the specified number of channels.

    Parameters:
        channel_count (int): Number of channels.
        func_type (str): 'sin' or 'cos' function to generate data.
        t (float): Current time or initial phase.
        step (float): Time step increment for each channel.

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


# 2. 浮点数矩阵构建函数
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


# 3. VOFA 数据流构建函数
def build_vofa_stream(float_matrix):
    """
    Build VOFA data stream by appending the frame tail to the float matrix.

    Parameters:
        float_matrix (bytes): Byte stream of floating-point data.

    Returns:
        bytes: Complete VOFA data stream.
    """
    frame_tail = struct.pack(
        "<f", float("+inf")
    )  # VOFA frame tail (00 00 80 7f for +Infinity)
    vofa_stream = float_matrix + frame_tail
    return vofa_stream


# 主程序示例
if __name__ == "__main__":
    # 用户输入参数
    channel_count = int(input("Enter the number of channels (N): "))
    func_type = input("Enter the function type ('sin' or 'cos'): ").strip().lower()
    t = float(input("Enter the time (t): "))
    step = float(input("Enter the time step (step): "))

    # 生成浮点数数据
    data = generate_data(channel_count, func_type, t, step)
    print("Generated Data:", data)

    # 构建浮点数矩阵
    float_matrix = build_float_matrix(data)
    print("Float Matrix (Hex):", float_matrix.hex(" "))

    # 构建 VOFA 数据流
    vofa_stream = build_vofa_stream(float_matrix)
    print("VOFA Data Stream (Hex):", vofa_stream.hex(" "))
