import time
from config import load_config
from data_generator import generate_data
from data_builder import build_vofa_stream
from udp_sender import send_udp_data
import sys
import os

# 获取当前工作目录
current_directory = os.getcwd()

# 将当前工作目录添加到 sys.path
if current_directory not in sys.path:
    sys.path.append(current_directory)

import api.ch100_protocol


# device = CH100Device.CH100Device("COM32", 115200)

device = api.ch100_protocol.CH100Device("COM32", 115200)
device.open()


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

    try:
        print(f"开始发送 VOFA 数据到 {ip}:{port}...")
        while True:
            # 2. 获取数据（以生成数据为例）
            # data = generate_data(channel_count, func_type, t)
            frames = device.read_and_parse()
            # 4. 构建 VOFA 数据流
            if frames:
                for frame in frames:
                    roll = frame.get("roll", "N/A")
                    pitch = frame.get("pitch", "N/A")
                    yaw = frame.get("yaw", "N/A")
                    error = yaw - roll
                    data = [roll, pitch, yaw, error]
                    vofa_stream = build_vofa_stream(data)

                    # 5. 调用 UDP 发送
                    send_udp_data(ip, port, vofa_stream)

                    # 打印调试信息
                    print(f"已发送 VOFA 数据流: {vofa_stream.hex(' ')}")

    except KeyboardInterrupt:
        print("\n传输已停止。")


if __name__ == "__main__":
    main()
