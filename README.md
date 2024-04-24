# i2p流量自动收集和标记程序

主要包括两方面内容，一是i2p网络中流量进行自动收集：
1. 浏览网页
2. bt种子
3. 即时通信


二是对流量中每一个数据包进行类别的标记
1. 对数据包进行未知
2. 将数据包转为流日志
3. 通过两个日志对比来对数据包进行标记


这两个方面的内容没必要分开来做，可以做一起，搞个定时器，每隔一段时间停止采集，然后整理一下之前的数据，然后继续采集

爬虫方面，首先爬取网站，然后访问网站


## How to use

### 准备

1. 因为需要捕获流量，所以要使用sudo指令执行代码，为了保证环境不受到变化，所以

```
sudo vim /etc/sudoers
```

找到

```
Defaults env_reset
Defaults mail_badpass
Defaults secure_path=“/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin”
```

修改为

```
Defaults !env_reset
Defaults mail_badpass
#Defaults secure_path=“/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin”
```

2. 安装chrome和chromedriver

```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt -f install
```

可能遇到问题
```
dpkg: 警告: 在 PATH 环境变量中找不到 ldconfig 或没有可执行权限
dpkg: 警告: 在 PATH 环境变量中找不到 start-stop-daemon 或没有可执行权限
dpkg: 错误: 2 在环境变量 PATH 中找不到该程序，或不可执行
提示：root 的 PATH 环境变量通常应当包含 /usr/local/sbin、/usr/sbin 和 /sbin
```

此时
```
sudo -i
export PATH=$PATH:/usr/local/sbin:/usr/sbin:/sbin
dpkg -i google-chrome-stable_current_amd64.deb
apt -f install
exit
```

之后查看chrome版本
```
google-chrome --version
```

version == 124.0.6367.78

在 https://chromedriver.chromium.org/downloads 选择一样的版本下载，如
```
https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chromedriver-linux64.zip
```

> warning：需要翻墙

将下载下来的zip文件解压 `unzip chromedriver-linux64.zip`

然后将目录中的chromedriver文件放入/usr/bin/
```
sudo mv chromedriver-linux64/chromedriver /usr/bin/
```





## 其他说明

i2pd结点输出日志的格式为“时间戳 ; 发/收 ; IP地址 ; 端口 ; 类型 ; 大小”

关于类型

|类型|编号|
|:---:|:---:|
|DummyMsg|0|
|DatabaseStore|1|
|DatabaseLookup|2|
|DatabaseSearchReply|3|
|DeliveryStatus|10|
|Garlic|11|
|TunnelData|18|
|TunnelGateway|19|
|I2NPData|20|
|TunnelBuild|21|
|TunnelBuildReply|22|
|VariableTunnelBuild|23|
|VariableTunnelBuildReply|24|
|ShortTunnelBuild|25|
|ShortTunnelBuildReply|26|
|TunnelTest|231|
|第一次握手|500|
|第二次握手|501|
|第三次握手|502|
|Routerinfo|600|
|DateTime|700|
|Options|800|
|Padding|900|
|Termination|999|
|收的总|-1|





## 重构一下代码

这个代码实现的流量捕获主要有几个方面
1. 每次捕获都要重新开启和关闭i2pd结点
2. 针对一条隧道进行捕获，看看这条隧道从建立到过期的所有流量


主要有两种收集流量的方法：
1. i2pd结点一直开着，每隔几个网页收集一次流量（always）
2. 收集一次流量，访问一个网页，打开一次结点（one）

对齐方式：
- 对齐
- 不对齐

流是否完整
- 完整
- 不完整



## 容器使用方式

进入容器之后，首先运行 `sudo ethtool -K eth0 tso off gso off gro off`