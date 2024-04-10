from spider_i2p.myutils.logger import logger
from spider_i2p.myutils.config import config
from spider_i2p.spider.index_spider import get_url_from_index
import random
import threading
from spider_i2p.traffic.capture import capture, stop_capture
from spider_i2p.traffic.handle_traffic import pcap2flowlog
from spider_i2p.spider.spider import consume
import os
from spider_i2p.traffic.align import align
import shutil
import queue


data_queue = queue.Queue()

def traffic(TASK_NAME, VPS_NAME):
    traffic_name = capture(TASK_NAME, VPS_NAME)
    pcap2flowlog(traffic_name)
    flow_log_dir = os.path.join(config["traffic"]["flow_log_dir"], "row")
    pcaps_dir = config["traffic"]["handled_traffic_dir"]
    dst_log_dir = os.path.join(config["traffic"]["flow_log_dir"], "handled")
    log_path = data_queue.get()
    align(log_path, flow_log_dir, dst_log_dir)
    if os.path.exists(flow_log_dir):
        # 删除非空目录及其所有内容
        shutil.rmtree(flow_log_dir)
    if os.path.exists(pcaps_dir):
        # 删除非空目录及其所有内容
        shutil.rmtree(pcaps_dir)
    data_queue.task_done()



def main():
    TASK_NAME = "packet_tagging"
    VPS_NAME = "VPS2"
    index_url = config["spider"]["index_url"]
    num = 3
    while (True):
        # 爬取导航网站，返回b32链接的列表
        # 给三次机会爬导航页
        while (num > 0):
            url_list = get_url_from_index(index_url)
            random.shuffle(url_list)  # 随机调换链接位置
            url_num = len(url_list)
            if url_num == 0:
                logger.error(f"获取url失败，还有{num-1}次机会")
                num -= 1
                continue
            else:
                logger.info(f"本次从{index_url}共获取{str(url_num)}个url链接")
                break
            return
        traffic_thread = threading.Thread(target=traffic,
                                              args=(TASK_NAME, VPS_NAME))
        traffic_thread.start()
        num = 0
        for url in url_list:
            consume(url)
            num += 1
            if num >= int(config["spider"]["website_num"]):
                num = 0
                log_path = stop_capture()
                data_queue.put(log_path)
                traffic_thread.join()
                traffic_thread = threading.Thread(target=traffic,
                                              args=(TASK_NAME, VPS_NAME))
                traffic_thread.start()
        log_path = stop_capture()
        data_queue.put(log_path)
        traffic_thread.join()


if __name__ == '__main__':
    main()
