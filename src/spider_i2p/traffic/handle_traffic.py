from spider_i2p.myutils.config import config
from spider_i2p.myutils.logger import logger
import os
from tqdm import tqdm
from spider_i2p.traffic.cut_flow_dpkt import cut
from spider_i2p.traffic.pcap2flowlog import pcap2flowlog_dpkt


def pcap2flowlog(filename):
    pcaps_dir = config["traffic"]["handled_traffic_dir"]
    flow_log_dir = os.path.join(config["traffic"]["flow_log_dir"], "row")
    pcap_list = cut(filename, pcaps_dir)
    for pcap_file in pcap_list:
        pcap2flowlog_dpkt(pcap_file, flow_log_dir)


if __name__ == "__main__":
    # pcap2flowlog(
    #     "/home/aimafan/Documents/mycode/spider_i2p/data/traffic/packet_tagging_VPS2_atlkfvuwwpgvnw24dkwyyxf5psrueozxb3i6zgebymjuquuquvqq.b32.i2p_20240403164426.pcap"
    # )
    pcap2flowlog("/home/aimafan/Documents/mycode/spider_i2p/data/test/output.pcap")
