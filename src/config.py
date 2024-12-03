import json


def load_config(config_file="config.json"):
    """
    从配置文件加载配置
    """
    with open(config_file, "r") as file:
        config = json.load(file)
    return config
