import re

from src.core.util.HttpUtils import load_html_str
from src.free.abstract_ip_extract import AbstractIpExtract

proxy_compiler = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}")


class Proxy66(AbstractIpExtract):
    def __init__(self, url_list):
        AbstractIpExtract.__init__(self)
        self.url_list = url_list

    def extract(self, **kwargs):
        for url in self.url_list:
            url = url.format(count=kwargs.get('count'))
            html = load_html_str(url)
            ips = re.findall(proxy_compiler, html)
            for ip in ips:
                yield ip.strip()


if __name__ == '__main__':
    test = Proxy66([
        "http://www.66ip.cn/mo.php?sxb=&tqsl={count}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=",
        "http://www.66ip.cn/nmtq.php?getnum={count}"
        "&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip",
    ])

    for i in test.extract(count=20):
        print(i)
