# noinspection PyPep8Naming
import random

import chardet
import requests
import time
from lxml import etree


def load_default_header():
    return {'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            }


def random_agent():
    ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    ]
    return random.choice(ua_list)


def get_content(url, headers=None, data="{}", retry_time=5, time_out=30, retry_flag=None, retry_interval=0):
    if not headers:
        headers = load_default_header()
    if retry_flag is None:
        retry_flag = []
    while retry_time > 0:
        try:
            html = requests.get(url, headers=headers, params=data, timeout=time_out)
            # print(html.encoding)
            # html.encoding = 'utf8'
            if any(f in html.content for f in retry_flag):
                raise Exception
            return html.content
        except Exception as e:
            print(e)
            retry_time -= 1
            time.sleep(retry_interval if retry_interval != 0 else random.randint(2, 10))
    else:
        print("not found")
        return ""


def load_html_tree(url, headers=None):
    # todo 取代理服务器用做代理服务器访问
    if not headers:
        headers = load_default_header()
    time.sleep(random.randint(2, 4))
    html = get_content(url=url, headers=headers)
    return etree.HTML(html)


def load_html_str(url, headers=None):
    if not headers:
        headers = load_default_header()
    time.sleep(random.randint(2, 4))
    html_bytes = get_content(url=url, headers=headers)
    ret = chardet.detect(html_bytes)
    print(ret)
    return html_bytes.decode()


if __name__ == '__main__':
    pass
