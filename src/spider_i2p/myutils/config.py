import configparser
import os

# 创建一个配置解析器

# 读取配置文件
config_path = os.path.join(
    *os.path.dirname(os.path.abspath(__file__)).split("/")[:-3])
config_defult_path = os.path.join("/" + config_path, "config", "config.ini")
config_dataset_path = os.path.join("/" + config_path, "config", "datasets.ini")
config_algorithm_path = os.path.join("/" + config_path, "config",
                                     "algorithm.ini")

config = configparser.ConfigParser()
config.read(config_defult_path)

# 可以在这里添加一些函数来获取特定的配置项
# def get_database_config():
#     return {
#         'host': config['database']['host'],
#         'user': config['database']['user'],
#         'password': config['database']['password'],
#         'database': config['database']['database']
#     }
