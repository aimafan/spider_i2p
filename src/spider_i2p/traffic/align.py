import re
import os
from spider_i2p.myutils.logger import logger, logger_log
from spider_i2p.myutils.config import config
import shutil
import csv
import glob


message_types = {
    0: "DummyMsg",
    1: "DatabaseStore",
    2: "DatabaseLookup",
    3: "DatabaseSearchReply",
    10: "DeliveryStatus",
    11: "Garlic",
    18: "TunnelData",
    19: "TunnelGateway",
    20: "I2NPData",
    21: "TunnelBuild",
    22: "TunnelBuildReply",
    23: "VariableTunnelBuild",
    24: "VariableTunnelBuildReply",
    25: "ShortTunnelBuild",
    26: "ShortTunnelBuildReply",
    231: "TunnelTest",
    500: "第一次握手",
    501: "第二次握手",
    502: "第三次握手",
    600: "Routerinfo",
    700: "DateTime",
    800: "Options",
    900: "Padding",
    999: "Termination",
    -1: "收的总",
}


def align(log_file, src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    log_dic = read_log_file(log_file)
    for host_port in log_dic:
        for filename in os.listdir(src_dir):
            if filename.endswith("csv"):
                if host_port in filename:
                    # shutil.move(os.path.join(src_dir, filename), dst_dir)
                    result_path = os.path.join(dst_dir, filename)
                    file_path = os.path.join(src_dir, filename)
                    result = conbine(log_dic[host_port], file_path)
                    save_csv(result, result_path)
                    break
        # break


def conbine(log_list, file_path):
    flowlog = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            time, length = row
            flowlog.append([time, int(length)])
    logger.info(file_path)
    flowlog1 = handle_flowlog(log_list, flowlog, file_path)
    return flowlog1


def handle_flowlog(log_list, flowlog, file_name):
    flowlog1 = []

    for i in range(0, len(log_list)):
        if log_list[i][1] == "收":
            log_list[i][-1] = -log_list[i][-1]
        if log_list[i][1] == "发" and log_list[i][2] == "Routerinfo":
            log_list[i][-1] += 18

    logger_log.info(file_name)
    logger_log.info(log_list)
    logger_log.info(flowlog)
    logger_log.info("========")
    n = 0
    while n < len(flowlog):
        if log_list == None or log_list == []:
            break
        if len(flowlog[n]) >= 3:
            flowlog1.append(flowlog[n])
            n += 1
            continue
        for i in range(0, len(log_list)):
            if i >= 50:
                flowlog[n].append("未知")
                break
            if log_list[i][-1] == flowlog[n][-1]:
                log_list[i][0] = "N"
                if log_list[i][-2] == "收的总":
                    get_type = []
                    for j in range(i + 1, len(log_list)):
                        if log_list[j][-2] == "Padding":
                            log_list[j][0] = "N"
                            break
                        get_type.append(log_list[j][-2])
                    packet_type = "+".join(get_type)
                    flowlog[n].append(packet_type)
                else:
                    flowlog[n].append(log_list[i][-2])
                break

        log_list = del_item(log_list)
        flowlog1.append(flowlog[n])
        n += 1
    return flowlog1


def del_item(log_list):
    new_log_list = []
    for log in log_list:
        if log[0] != "N":
            new_log_list.append(log)
    return new_log_list


def same_sign(a, b):
    if a > 0 and b > 0:
        return True
    elif a < 0 and b < 0:
        return True
    elif a == 0 and b == 0:
        return True
    else:
        return False


def save_csv(result, file_name):
    # 定义 CSV 文件路径
    csv_file = file_name
    for i in range(len(result)):
        if len(result[i]) < 3:
            result[i].append("未知")
    # 定义 CSV 文件的表头
    header = ["time", "length", "type"]

    # 将数据写入 CSV 文件
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        # 写入表头
        writer.writerow(header)
        # 写入数据行
        writer.writerows(result)


def read_log_file(log_file):
    log_dic = {}
    with open(log_file, "r") as file:
        for line in file:
            time, direction, host, port, msgtype, size = line.split(" ; ")
            if f"{host}_{port}" not in log_dic:
                log_dic[f"{host}_{port}"] = []
            log_dic[f"{host}_{port}"].append(
                [time, direction, message_types[int(msgtype)], int(size.split("\n")[0])]
            )

    return log_dic


def get_datetime_from_filename(file):
    # 假设文件名格式为：YYYYMMDDHHMM.log
    filename = os.path.basename(file)
    datetime_str = filename[:-4]  # 去掉后缀 .log
    return datetime_str


def offline_align():
    # 使用glob获取目录下所有的log文件
    log_dir = config["spider"]["new_log_dir"]
    log_files = glob.glob(os.path.join(log_dir, "*.log"))
    # 解析文件名中的日期时间信息
    flowlog_row = os.path.join(config["traffic"]["flow_log_dir"], "row")
    dst_dir = os.path.join(config["traffic"]["flow_log_dir"], "handled")
    # 获取目标目录下的所有项目（包括文件和目录）
    all_items = os.listdir(flowlog_row)

    # 筛选出是目录的项目
    directories = [
        item for item in all_items if os.path.isdir(os.path.join(flowlog_row, item))
    ]
    for director in directories:
        for log_file in log_files:
            if director == os.path.basename(log_file)[:-4]:
                align(log_file, os.path.join(flowlog_row, director), dst_dir)

    # print(log_files)


if __name__ == "__main__":
    # align("/home/aimafan/Documents/mycode/spider_i2p/data/test/aimafan.log", "/home/aimafan/Documents/mycode/spider_i2p/data/flowlog/row", "/home/aimafan/Documents/mycode/spider_i2p/data/flowlog/handled")
    offline_align()
