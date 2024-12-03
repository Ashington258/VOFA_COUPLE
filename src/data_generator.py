import math


def generate_data(channel_count, func_type="sin", t=0.0):
    """
    生成浮点数数据
    """
    data = []
    for i in range(1, channel_count + 1):
        if func_type == "sin":
            data.append(math.sin(i * t))
        elif func_type == "cos":
            data.append(math.cos(i * t))
        else:
            raise ValueError("func_type 必须是 'sin' 或 'cos'")
    return data
