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
import json
from spider_i2p.myutils import project_path
import subprocess
import time
from spider_i2p.spider.action import always_action, one_action


def main():
    mode = config["spider"]["mode"]
    if mode == "always":
        always_action()
    elif mode == "one":
        one_action()


if __name__ == "__main__":
    main()
