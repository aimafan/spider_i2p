from scapy.all import sniff, wrpcap
from spider_i2p.myutils.config import config
import os
from datetime import datetime
import time
import shutil
from spider_i2p.myutils import project_path

should_stop_capture = False


def capture(TASK_NAME, VPS_NAME, formatted_time):
    global should_stop_capture
    should_stop_capture = False

    traffic_dir = os.path.join(project_path, "data", TASK_NAME, "row_pcap")
    os.makedirs(traffic_dir, exist_ok=True)

    traffic_name = os.path.join(traffic_dir, f"{formatted_time}.pcap")
    log_path = os.path.join(config["spider"]["i2pd_path"], "aimafan.log")
    if os.path.exists(log_path):
        # 删除文件
        os.remove(log_path)
    packets = sniff(
        filter=f"not port 22 and not port 443 and not port 80 and host {config["spider"]["host"]}",
        stop_filter=stop_filter,
    )
    wrpcap(traffic_name, packets)
    return traffic_name


def stop_capture(formatted_time, TASK_NAME):
    global should_stop_capture
    should_stop_capture = True
    log_path = os.path.join(config["spider"]["i2pd_path"], "aimafan.log")
    dst_dir = os.path.join(project_path, "data", TASK_NAME, "log_file")
    dst_name = os.path.join(dst_dir, f"{formatted_time}.log")
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
