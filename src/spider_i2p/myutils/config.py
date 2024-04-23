import configparser
import os
from spider_i2p.myutils import project_path

# 创建一个配置解析器

# 读取配置文件
config_defult_path = os.path.join(project_path, "config", "config.ini")


config = configparser.ConfigParser()
config.read(config_defult_path)
