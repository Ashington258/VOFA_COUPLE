import time
from config import load_config
from data_generator import generate_data
from data_builder import build_float_matrix, build_vofa_stream
from udp_sender import send_udp_data
import sys
import os

# 获取当前工作目录
current_directory = os.getcwd()

# 将当前工作目录添加到 sys.path
if current_directory not in sys.path:
    sys.path.append(current_directory)


def main():
    """
    主程序入口
    """
    # 1. 初始化：加载配置
    config = load_config("src/config.json")

    # 提取配置参数
    ip = config["ip"]
    port = config["port"]
    channel_count = config["channel_count"]
    func_type = config["func_type"]
    interval = config["interval"]

    t = 0.0  # 初始时间/相位

    try:
        print(f"开始发送 VOFA 数据到 {ip}:{port}...")
        while True:
            # 2. 获取数据（以生成数据为例）
            data = generate_data(channel_count, func_type, t)

            # 3. 构建浮点数矩阵
            float_matrix = build_float_matrix(data)

            # 4. 构建 VOFA 数据流
            vofa_stream = build_vofa_stream(float_matrix)

            # 5. 调用 UDP 发送
            send_udp_data(ip, port, vofa_stream)

            # 打印调试信息
            print(f"已发送 VOFA 数据流: {vofa_stream.hex(' ')}")

            # 增加时间并等待下一个间隔
            t += interval
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n传输已停止。")


if __name__ == "__main__":
    main()
