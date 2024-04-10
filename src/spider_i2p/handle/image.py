import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 您提供的字典数据
data = {
    'type': 4980,
    '第一次握手': 4976,
    '第二次握手': 4975,
    '第三次握手': 4897,
    'DatabaseStore': 4411,
    'TunnelGateway': 6061,
    'ShortTunnelBuild': 2099,
    'DatabaseLookup': 2816,
    'Termination': 2823,
    'Garlic': 712,
    'DatabaseSearchReply': 920,
    '未知': 4808,
    'TunnelData': 15108,
    'Routerinfo': 509,
    'TunnelGateway+TunnelGateway': 103,
    'TunnelGateway+DatabaseSearchReply': 1,
    'VariableTunnelBuild': 10,
    'DateTime+Routerinfo': 31,
    'TunnelData+TunnelData': 137,
    'DatabaseSearchReply+DatabaseSearchReply': 1,
    'TunnelGateway+TunnelGateway+TunnelGateway': 6,
    'TunnelGateway+TunnelGateway+TunnelGateway+TunnelGateway': 8,
    'TunnelData+TunnelData+TunnelData+TunnelData': 3,
    'Padding': 4,
    'TunnelGateway+TunnelGateway+TunnelGateway+TunnelGateway+TunnelGateway+TunnelGateway': 1,
    'TunnelGateway+收的总+TunnelGateway': 1,
    'TunnelData+收的总+TunnelData': 1
}

# 提取字典的键和值
labels = list(data.keys())
values = list(data.values())

# 创建柱状图
plt.figure(figsize=(12, 6))
plt.bar(labels, values, color='skyblue')
plt.xlabel('类型')
plt.ylabel('数量')
plt.title('不同类型的数量柱状图')
plt.xticks(rotation=90)  # 旋转x轴标签，以免重叠
plt.tight_layout()  # 自动调整布局，以防重叠
# 保存图像到当前目录
plt.savefig('bar_chart.png')
plt.show()
