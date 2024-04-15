import os
import csv
import click
from spider_i2p.myutils.config import config
import spider_i2p.handle.draw_image as draw_image
from spider_i2p.myutils.logger import logger



@click.group()
@click.pass_context
def statistic(ctx):
    """statistic traffic."""
    pass


@statistic.command(name="unknown-count")
@click.pass_context
@click.option(
    "--image",
    "-i",
    "image",
    help="是否保存为图像",
    # required=True,
    default=True,
    type=bool,
    show_default=True,
)
def count_unknowns_in_files(ctx, image):
    """统计所有文件中未知数据包的个数"""
    src_dir = os.path.join(config["traffic"]["flow_log_dir"], "handled")
    count_list = {}

    # 遍历目录下的所有文件
    for filename in os.listdir(src_dir):
        if filename.endswith(".csv"):
            count = 0
            csv_file_path = os.path.join(src_dir, filename)
            
            # 打开CSV文件并搜索包含"未知"的行
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row[2] == "未知":
                        count += 1
            if count not in count_list:
                count_list[count] = 1
            else:
                count_list[count] += 1
    count_list = {key: value for key, value in count_list.items() if value != 1}
    count_list = dict(sorted(count_list.items()))
    del count_list[0]
    if image:
        draw_image.draw_count_unknowns_in_files(count_list, "count_unknowns_in_files")
    logger.info(count_list)



@statistic.command(name="distribution")
@click.pass_context
@click.option(
    "--image",
    "-i",
    "image",
    help="是否保存为图像",
    # required=True,
    default=True,
    type=bool,
    show_default=True,
)
def length_distribution(ctx, image):
    """所有流中数据包数量的分布"""
    src_dir = os.path.join(config["traffic"]["flow_log_dir"])
    count_list = {}

    # 遍历目录下的所有文件
    for filename in os.listdir(src_dir):
        if filename.endswith(".csv"):
            count = 0
            csv_file_path = os.path.join(src_dir, filename)
            
            # 打开CSV文件并搜索包含"未知"的行
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for row in csv_reader:
                    count += 1
                if count not in count_list:
                    count_list[count] = 1
                else:
                    count_list[count] += 1
    count_list = {key: value for key, value in count_list.items() if value != 1}
    count_list = dict(sorted(count_list.items()))
    # if image:
    #     draw_image.draw_length_distribution(count_list, "length_distribution")
    logger.info(count_list)


@statistic.command(name="length_range")
@click.pass_context
@click.option(
    "--image",
    "-i",
    "image",
    help="是否保存为图像",
    # required=True,
    default=True,
    type=bool,
    show_default=True,
)
@click.option(
    "--type",
    "-t",
    "i2p_type",
    help="数据包类型",
    required=True,
    # default=True,
    type=str,
    # show_default=True,
)
def length_range(ctx, image, i2p_type):
    """某个类型的长度范围"""
    src_dir = os.path.join(config["traffic"]["flow_log_dir"])
    count_list = []

    # 遍历目录下的所有文件
    for filename in os.listdir(src_dir):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(src_dir, filename)
            
            # 打开CSV文件并搜索包含"未知"的行
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for row in csv_reader:
                    if row[2] == i2p_type:
                        count_list.append(int(row[1]))
                    if i2p_type == "未知":
                        if "+" in row[2]:
                            count_list.append(int(row[1]))
    if image:
        draw_image.draw_length_range(count_list, f"length_range_{i2p_type}")


@statistic.command(name="all_type")
@click.pass_context
@click.option(
    "--image",
    "-i",
    "image",
    help="是否保存为图像",
    # required=True,
    default=True,
    type=bool,
    show_default=True,
)
def all_type(ctx, image):
    """统计所有流中有哪些种类的数据包，每个种类的数据包都有多少"""
    src_dir = os.path.join(config["traffic"]["flow_log_dir"], "handled")
    count_list = {}

    # 遍历目录下的所有文件
    for filename in os.listdir(src_dir):
        if filename.endswith(".csv"):
            count = 0
            csv_file_path = os.path.join(src_dir, filename)
            
            # 打开CSV文件并搜索包含"未知"的行
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for row in csv_reader:
                    if "+" not in row[2]:
                        if row[2] == "未知":
                            row[2] = "unknown"
                        if row[2] == "第一次握手":
                            row[2] = "first"
                        if row[2] == "第二次握手":
                            row[2] = "second"
                        if row[2] == "第三次握手":
                            row[2] = "third"
                        if row[2] not in count_list:
                            count_list[row[2]] = 1
                        else:
                            count_list[row[2]] += 1
    count_list = {key: value for key, value in count_list.items() if value >= 10}
    count_list = dict(sorted(count_list.items(), key=lambda item: item[1], reverse=True))
    if image:
        draw_image.draw_all_type(count_list, "all_type")
    logger.info(count_list)



@statistic.command(name="yichang")
@click.pass_context
def yichang(ctx):
    """统计数据集中异常的流和数据包有多少"""
    src_dir = config["traffic"]["flow_log_dir"]
    packet_list = {}
    packet_list["all"] = 0
    packet_list["合"] = 0
    packet_list["未知"] = 0
    packet_list["收的总"] = 0

    flow_list = {}
    flow_list["all"] = 0
    flow_list["未知"] = 0

    # 遍历目录下的所有文件
    for filename in os.listdir(src_dir):
        if filename.endswith(".csv"):
            flag = 0
            csv_file_path = os.path.join(src_dir, filename)
            
            # 打开CSV文件并搜索包含"未知"的行
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                flow_list["all"] += 1
                header = next(csv_reader)
                for row in csv_reader:
                    packet_list["all"] += 1
                    if "收的总" in row[2]:
                        flag = 1
                        packet_list["收的总"] += 1
                    if "+" in row[2]:
                        flag = 1
                        packet_list["合"] += 1
                    elif row[2] == "未知":
                        flag = 1
                        packet_list["未知"] += 1
            if flag == 1:
                flow_list["未知"] += 1

    logger.info(packet_list)
    logger.info(flow_list)



@statistic.command(name="short_all_type")
@click.pass_context
@click.option(
    "--image",
    "-i",
    "image",
    help="是否保存为图像",
    # required=True,
    default=True,
    type=bool,
    show_default=True,
)
@click.option(
    "--length",
    "-l",
    "length",
    help="少于多少算短流",
    required=True,
    default=10,
    type=int,
    show_default=True,
)
def short_all_type(ctx, image, length):
    """统计短流中有哪些种类的数据包，每个种类的数据包都有多少"""
    src_dir = os.path.join(config["traffic"]["flow_log_dir"], "handled")
    count_list = {}

    # 遍历目录下的所有文件
    for filename in os.listdir(src_dir):
        if filename.endswith(".csv"):
            count = 0
            csv_file_path = os.path.join(src_dir, filename)
            
            # 打开CSV文件并搜索包含"未知"的行
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for row in csv_reader:
                    count += 1
            if count > length:
                continue
            else:
                with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    header = next(csv_reader)
                    for row in csv_reader:
                        if "+" not in row[2]:
                            if row[2] == "未知":
                                row[2] = "unknown"
                            if row[2] == "第一次握手":
                                row[2] = "first"
                            if row[2] == "第二次握手":
                                row[2] = "second"
                            if row[2] == "第三次握手":
                                row[2] = "third"
                            if row[2] not in count_list:
                                count_list[row[2]] = 1
                            else:
                                count_list[row[2]] += 1
    count_list = {key: value for key, value in count_list.items() if value >= 10}
    count_list = dict(sorted(count_list.items(), key=lambda item: item[1], reverse=True))
    if image:
        draw_image.draw_all_type(count_list, f"all_type_shorter_{str(length)}")
    logger.info(count_list)