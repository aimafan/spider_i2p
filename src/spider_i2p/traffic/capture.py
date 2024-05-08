from scapy.all import sniff, wrpcap
from spider_i2p.myutils.config import config
from spider_i2p.myutils.logger import logger
import os
from datetime import datetime
import time
import shutil
from spider_i2p.myutils import project_path
import subprocess

should_stop_capture = False


def capture(TASK_NAME, VPS_NAME, formatted_time, protocal):
    traffic_dir = os.path.join(project_path, "data", TASK_NAME, "row_pcap")
    os.makedirs(traffic_dir, exist_ok=True)

    traffic_name = os.path.join(traffic_dir, f"{formatted_time}.pcap")

    # 设置tcpdump命令的参数
    tcpdump_command = [
        "tcpdump",
        "-n",
        protocal,
        "and",
        "not",
        "port",
        "22",
        "and",
        "not",
        "port",
        "443",
        "and",
        "not",
        "port",
        "80",
        "-w",
        traffic_name,  # 输出文件的路径
    ]

    log_path = os.path.join(config["spider"]["i2pd_path"], "aimafan.log")
    if os.path.exists(log_path):
        # 删除文件
        os.remove(log_path)
    global process
    # 开流量收集
    process = subprocess.Popen(tcpdump_command)

    logger.info("开始捕获流量")
    return traffic_name


def stop_capture(formatted_time, TASK_NAME):
    global process
    process.terminate()
    log_path = os.path.join(config["spider"]["i2pd_path"], "aimafan.log")
    dst_dir = os.path.join(project_path, "data", TASK_NAME, "log_file")
    dst_name = os.path.join(dst_dir, f"{formatted_time}.log")
    try:
        move_log(log_path, dst_name)
    except Exception as e:
        logger.error(f"无法将log文件{log_path}移动到指定位置：{e}")
    return dst_name


def move_log(log_path, dst_path):
    if not os.path.exists(os.path.dirname(dst_path)):
        os.makedirs(os.path.dirname(dst_path))
    shutil.move(log_path, dst_path)


if __name__ == "__main__":
    capture("www.baidu.com", "TEST", "1111111", "tcp")
    time.sleep(9)
    stop_capture("11111", "test")
