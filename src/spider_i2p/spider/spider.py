import time
from selenium import webdriver
import requests
from spider_i2p.myutils.config import config
from spider_i2p.myutils.logger import logger
import re
import os

proxy_host_port = f"{config['proxy']['host']}:{config['proxy']['port']}"


def visit_website(url):
    timeout = int(config["spider"]["url_timeout"])
    sleep_time = int(config["spider"]["sleep_time"])

    # Set up Selenium WebDriver with the proxy
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server=http://{proxy_host_port}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(timeout)
    try:
        # Navigate to the URL
        logger.info(f"正在访问 {url}")
        driver.get(url)
        time.sleep(sleep_time)  # Wait for the page to load
        # save_page(driver.page_source, url)
        logger.info(f"成功访问 {url}")
        driver.quit()
        return True
    except Exception as e:
        logger.warning(f"访问 {url} 失败，失败原因 {str(e).split('Stacktrace')[0]}")
        driver.quit()
        return False


def save_page(page, url):
    filename = re.sub(r"^https?://", "", url)
    filename = re.sub(r"[^a-zA-Z0-9]", "_", filename)  # 替换非字母数字字符为下划线
    filename += ".html"  # 添加 .html 后缀
    filepath = os.path.join(config["spider"]["website_dir"], filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(page)


def consume(url):
    visit_website(url)


if __name__ == "__main__":
    visit_website("http://lhbd7ojcaiofbfku7ixh47qj537g572zmhdc4oilvugzxdpdghua.b32.i2p")
