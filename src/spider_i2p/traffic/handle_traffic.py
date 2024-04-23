from spider_i2p.myutils.config import config
from spider_i2p.myutils.logger import logger
from spider_i2p.myutils import project_path
import os
from tqdm import tqdm
from spider_i2p.traffic.cut_flow_dpkt import cut
from spider_i2p.traffic.pcap2flowlog import pcap2flowlog_dpkt


def pcap2flowlog(filename, TASK_NAME):
    pcaps_dir = os.path.join(project_path, "data", TASK_NAME, "handled_pcap")
    flow_log_dir = os.path.join(project_path, "data", TASK_NAME, "flowlog", "row")
    pcap_list = cut(filename, pcaps_dir)
    for pcap_file in pcap_list:
        logger.info(f"开始处理{pcap_file}")
        pcap2flowlog_dpkt(pcap_file, flow_log_dir)
    return flow_log_dir


if __name__ == "__main__":
    # pcap2flowlog(
    #     "/home/aimafan/Documents/mycode/spider_i2p/data/traffic/packet_tagging_VPS2_atlkfvuwwpgvnw24dkwyyxf5psrueozxb3i6zgebymjuquuquvqq.b32.i2p_20240403164426.pcap"
    # )
    pcap2flowlog("/home/aimafan/Documents/mycode/spider_i2p/data/output.pcap", "always")
