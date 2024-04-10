from scapy.all import *
from spider_i2p.myutils.config import config
import os
from datetime import datetime
import time
import shutil

should_stop_capture = False


def capture(TASK_NAME, VPS_NAME):
    global should_stop_capture
    should_stop_capture = False
    # 获取当前时间
    current_time = datetime.now()

    # 格式化输出
    formatted_time = current_time.strftime("%Y%m%d%H%M")

    # host = config["spider"]["host"]
    # port = config["spider"]["port"]
    traffic_dir = config["spider"]["traffic_dir"]
    os.makedirs(traffic_dir, exist_ok=True)
    # url = url.replace("http://", "").replace("https://", "")[:6]
    traffic_name = os.path.join(
        traffic_dir, f"{TASK_NAME}_{VPS_NAME}_{formatted_time}.pcap")
    log_path = config["spider"]["log_dir"]
    if os.path.exists(log_path):
    # 删除文件
        os.remove(log_path)
    packets = sniff(filter=f"tcp and not port 22 and not port 443 and not port 80", stop_filter=stop_filter)
    # packets = sniff(filter=f"tcp and not port 22",
                    # stop_filter=stop_filter)  # 测试用
    wrpcap(traffic_name, packets)
    return traffic_name


def stop_capture():
    # 获取当前时间
    current_time = datetime.now()
    # 格式化输出
    formatted_time = current_time.strftime("%Y%m%d%H%M")
    global should_stop_capture
    should_stop_capture = True
    log_path = config["spider"]["log_dir"]
    dst_path = config["spider"]["new_log_dir"]
    dst_name = os.path.join(
        dst_path, f"{formatted_time}.log")
    move_log(log_path, dst_name)
    return dst_name


def stop_filter(packets):
    global should_stop_capture
    return should_stop_capture


def move_log(log_path, dst_path):
    if not os.path.exists(os.path.dirname(dst_path)):
        os.makedirs(os.path.dirname(dst_path))
    shutil.move(log_path, dst_path)

if __name__ == "__main__":
    capture("www.baidu.com", "TEST", "a100")
