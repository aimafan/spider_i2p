import matplotlib.pyplot as plt
from spider_i2p.myutils.config import config
import os
image_dir = config["traffic"]["image_dir"]
file_name = os.path.join(image_dir, "range")
# 表中的数据，每个元素格式为（名称，起始点，范围）
data1 = """
TunnelData	265974	1037~1163
TunnelGateway	205250	67~1500
first	136200	64~286
second	136184	64~286
third	134588	71~1500
DatabaseStore	117161	520~1497
Termination	77536	9~49
DatabaseLookup	75053	81~312
ShortTunnelBuild	52406	882~1188
DatabaseSearchReply	22167	98~210
Garlic	18028	168~1262
Routerinfo	14615	773~1499
"""
# 解析数据
data = []
for line in data1:
    parts = line.strip().split('\t')
    if len(parts) == 3:
        data.append([parts[0], int(parts[1]), list(map(int, parts[2].split('~')))])

# 创建长条图
fig, ax = plt.subplots()

# 绘制每个条目的长条
for i, item in enumerate(data):
    range_start, range_end = item[2]
    ax.barh(i, range_end - range_start, left=range_start, align='center', label=item[0])

# 设置图表标题和标签
ax.set_xlabel('Range')
ax.set_ylabel('Items')
ax.set_title('Range of Items')
ax.set_yticks(range(len(data)))
ax.set_yticklabels([item[0] for item in data])
ax.legend()

# 显示图表
plt.grid(True)
plt.tight_layout()

# 显示图形
plt.savefig(file_name)
