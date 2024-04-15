#-*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from spider_i2p.myutils.config import config
from spider_i2p.myutils.logger import logger
import os
from collections import Counter

os.makedirs(config["traffic"]["image_dir"], exist_ok=True)

font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SourceHanSansSC-Regular.otf")  # 替换为你的中文字体路径
prop = FontProperties(fname=font_path)

def draw_count_unknowns_in_files(data, title):
    # 提取字典的键和值
    labels = list(data.keys())
    values = list(data.values())
    image_dir = config["traffic"]["image_dir"]
    file_name = os.path.join(image_dir, title)

    # 创建柱状图
    plt.figure(figsize=(12, 6))
    # plt.hist(values, bins=50, edgecolor='black') 
    plt.bar(labels, values, color='skyblue')
    plt.xlabel('含有未知的个数', fontproperties=prop)
    plt.ylabel('含有这么多未知的流的个数', fontproperties=prop)
    plt.title('文件中未知的个数', fontproperties=prop)
    # 设置 x 轴和 y 轴的范围
    plt.xlim(0, 25)  # x 轴最大值为 200
    plt.ylim(0, 5000)  # y 轴最大值为 2000
    # plt.xticks(rotation=90)  # 旋转x轴标签，以免重叠
    plt.tight_layout()  # 自动调整布局，以防重叠
    # 保存图像到当前目录
    plt.savefig(file_name)

def draw_length_distribution(data, title):
    # 绘制直方图
    image_dir = config["traffic"]["image_dir"]
    file_name = os.path.join(image_dir, title)
    plt.hist(data, bins=30, edgecolor='black')  # 可以根据需要调整 bins 的数量
    plt.xlabel('数据包个数', fontproperties=prop)
    plt.ylabel('流的个数', fontproperties=prop)
    plt.title('所有流中数据包数量的分布', fontproperties=prop)
    plt.xlim(0, 50)  # x 轴最大值为 200
    plt.tight_layout()  # 自动调整布局，以防重叠

    # 保存图像到当前目录
    plt.savefig(file_name)


def draw_length_range(data, title):
    # 绘制直方图
    data = [x for x in data if (x <= 3000 and x >= -3000)]
    counter = Counter(data)
    logger.info(f"title: {title}, num: {counter}")
    image_dir = config["traffic"]["image_dir"]
    file_name = os.path.join(image_dir, title)
    plt.hist(data, bins=35, edgecolor='black')  # 可以根据需要调整 bins 的数量
    plt.xlabel('数据包个数', fontproperties=prop)
    plt.ylabel('流的个数', fontproperties=prop)
    plt.title(f'{title}长度分布', fontproperties=prop)
    plt.tight_layout()  # 自动调整布局，以防重叠
    # 标记最小值和最大值
    min_value = min(data)
    max_value = max(data)
    plt.axvline(min_value, color='r', linestyle='dashed', linewidth=1)  # 标记最小值为红色虚线
    plt.axvline(max_value, color='g', linestyle='dashed', linewidth=1)  # 标记最大值为绿色虚线
    
    # 在最小值和最大值处添加文本标签
    plt.text(min_value, -500, f'Min: {min_value}', color='r', ha='center', va='top')
    plt.text(max_value, -500, f'Max: {max_value}', color='g', ha='center', va='top')

    # 保存图像到当前目录
    plt.savefig(file_name)


def draw_all_type(data, title):
    # 提取字典的键和值
    labels = list(data.keys())
    values = list(data.values())
    image_dir = config["traffic"]["image_dir"]
    file_name = os.path.join(image_dir, title)

    # 创建柱状图
    plt.figure(figsize=(12, 6))
    # plt.hist(values, bins=50, edgecolor='black') 
    plt.bar(labels, values, color='skyblue')
    plt.xlabel('数据包类型', fontproperties=prop)
    plt.ylabel('数据包个数', fontproperties=prop)
    plt.title('统计各个类型数据包有多少个', fontproperties=prop)
    # 设置 x 轴和 y 轴的范围
    plt.xticks(rotation=90)  # 旋转x轴标签，以免重叠
    plt.tight_layout()  # 自动调整布局，以防重叠
    # 保存图像到当前目录
    plt.savefig(file_name)