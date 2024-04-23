FROM debian:bullseye

# 设置工作目录
WORKDIR /app

# 安装基本工具和依赖
RUN apt-get update && apt-get install -y \
    vim \
    sudo \
    python3.10 \
    python3-pip \
    python3.10-venv \
    net-tools \
    wget    \
    curl    \
    build-essential \
    gcc \
    make \
    inetutils-ping \
    python-is-python3

# 将vim设为默认编辑器
RUN update-alternatives --set editor /usr/bin/vim.basic

ADD . .
RUN pip3 install --no-cache-dir -r mycode/requirements.txt

RUN cd i2pd_paper/build; cmake .; make

# 默认命令，打开vim
CMD ["bash"]