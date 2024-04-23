from spider_i2p.myutils.logger import logger
from spider_i2p.myutils.config import config
from spider_i2p.spider.action import always_action, one_action


def main():
    mode = config["spider"]["mode"]
    logger.info(f"开始捕获流量，模式{mode}")
    if mode == "always":
        always_action()
    elif mode == "one":
        one_action()


if __name__ == "__main__":
    main()
