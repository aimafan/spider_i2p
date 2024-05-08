from spider_i2p.myutils import project_path
import os
import json
import random
from spider_i2p.myutils.config import config
from spider_i2p.myutils.logger import logger
import threading
from spider_i2p.traffic.capture import capture, stop_capture
from spider_i2p.traffic.handle_traffic import pcap2flowlog
from spider_i2p.traffic.align import align
import shutil
import subprocess
import time
from spider_i2p.spider.spider import consume
import queue
from datetime import datetime


log_path_queue = queue.Queue()
time_name = queue.Queue()


def traffic_test(traffic_name, TASK_NAME, log_path):
    flow_log_dir = pcap2flowlog(traffic_name, TASK_NAME)

    dst_log_dir = os.path.join(project_path, "data", TASK_NAME, "flowlog", "handled")

    if config["traffic"]["align"] == "True" and config["traffic"]["protocal"] == "tcp":
        logger.info(f"对{flow_log_dir}中的流日志进行对齐")
        align(log_path, flow_log_dir, dst_log_dir)


def traffic(TASK_NAME, VPS_NAME, protocal):
    # 获取当前时间
    current_time = datetime.now()
    # 格式化输出
    formatted_time = current_time.strftime("%Y%m%d%H%M%S")
    time_name.put(formatted_time)
    logger.info("流量采集开始")

    traffic_name = capture(TASK_NAME, VPS_NAME, formatted_time, protocal)
    log_path = log_path_queue.get()
    flow_log_dir = pcap2flowlog(traffic_name, TASK_NAME)

    dst_log_dir = os.path.join(project_path, "data", TASK_NAME, "flowlog", "handled")

    if config["traffic"]["align"] == "True":
        logger.info(f"对{flow_log_dir}中的流日志进行对齐")
        align(log_path, flow_log_dir, dst_log_dir)


def browser_action():
    TASK_NAME = "browser"
    VPS_NAME = "VPS2"
    protocal = config["traffic"]["protocal"]
    while True:
        url_path = os.path.join(project_path, "config", "my_list.json")
        with open(url_path, "r") as json_file:
            json_data = json_file.read()
            url_list = json.loads(json_data)
        logger.info(f"已从{url_path}中获取i2p网站列表")
        i2pd_path = os.path.join(config["spider"]["i2pd_path"], "build", "i2pd")

        # 开流量收集
        traffic_thread = threading.Thread(
            target=traffic, args=(TASK_NAME, VPS_NAME, protocal)
        )
        traffic_thread.start()
        time.sleep(1)

        # 开i2p结点
        process = subprocess.Popen([i2pd_path], stdout=subprocess.PIPE)
        time.sleep(1)
        logger.info(f"成功开启i2pd结点 {process}")

        # 浏览网页
        num = 0
        while True:
            random.shuffle(url_list)  # 洗牌url列表

            consume(url_list)

            num += 1
            if num >= int(config["spider"]["website_num"]):
                num = 0
                formatted_time = time_name.get()
                # 关i2pd结点
                process.kill()
                time.sleep(0.5)
                # 关流量收集
                log_path = stop_capture(formatted_time, TASK_NAME)
                log_path_queue.put(log_path)
                traffic_thread.join()

                time.sleep(1)

                # 开流量收集
                traffic_thread = threading.Thread(
                    target=traffic, args=(TASK_NAME, VPS_NAME, protocal)
                )
                traffic_thread.start()

                # 开i2pd结点
                process = subprocess.Popen([i2pd_path], stdout=subprocess.PIPE)
                time.sleep(1)
                logger.info(f"成功开启i2pd结点 {process}")


if __name__ == "__main__":
    traffic_test(
        "/home/aimafan/Documents/mycode/spider_i2p/data/browser/row_pcap/20240508105601.pcap",
        "browser",
        "/home/aimafan/Documents/mycode/spider_i2p/data/browser/log_file/20240508105601.log",
    )
