import re

import scrapy
from scrapy import Request
from scrapy.selector import Selector

from dark_chain.items import DarkChainDomainNameItem
from tld import get_tld
from urllib.parse import urlparse, urljoin

ALL_DOMAINNAME={'www.ujs.edu.cn'}

"""自定义的爬虫类，用来解析response，提前item/发送下一请求"""
class MainSpider(scrapy.Spider):
    name = "dark_chain"

    start_urls = ['http://' + _ for _ in ALL_DOMAINNAME]

    def parse(self, response):
        selector = Selector(response)

        tmp_obj = urlparse(response.url)
        # url_prefix = tmp_obj.scheme + '://' + tmp_obj.netloc
        print("url:{}, response status: {}".format(response.url, response.status))
        if response.status == 404:
            print(response.status)
        if response.status not in [200]:
            # 响应非200，回头记录数据库，分析原因
            return
        if not response.text:
            return
        # 正则提取网址
        # response.encoding = 'utf-8'
        t = '((http(s)?:\/\/)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:[0-9]{1,5})?[-a-zA-Z0-9()@:%_\\\+\.~#?//=])'
        # print('text: ', response.text)
        for _ in re.findall(t, response.text):
            next_url = _[0]
            if any(_ in next_url for _ in [
                '.edu.cn', '.gov.cn', '.org.cn', '.qq.com', '.163.com', '.microsoft.com',
                '.adobe.com', '.google.com', '.baidu.com', '.foxitsoftware.cn', '.ujsde.com',
                'weibo.com', '.ieee.org', '.sunning.com', '.jd.com', '.springer.com', '.people.com.cn',
                '.12306.com', '.cnki.net', '.w3.org', '.sina.com.cn', '.cctv.com', '.hao123.com', '.youku.com',
                '.sohu.com', '.zol.com.cn'
            ]):
                continue
            if not urlparse(next_url).netloc.strip():
                continue
            domain_item = DarkChainDomainNameItem()
            domain_item['domainname'] = urlparse(next_url).netloc
            domain_item['origin_url'] = response.url
            domain_item['typo'] = 're'
            yield domain_item
        tmp_set = set()
        for _ in selector.xpath('//a/@href'):
            next_url = _.extract()
            if next_url in tmp_set:
                continue
            tmp_set.add(next_url)
            if 'javascript' in next_url or next_url.startswith('#') or \
                    'linkurl' in next_url or 'download' in next_url or '@' in next_url:
                continue
            if any(next_url.endswith(_) for _ in ['doc', 'pdf', 'xls', 'xlsx', 'docx', 'tar', 'tar.gz', 'zip', '7z']):
                continue
            if next_url.startswith('http'):
                if urlparse(next_url).netloc in ALL_DOMAINNAME:
                    yield Request(url=next_url, meta={'num': response.meta.get('num', 0) + 1}, callback=self.parse)
                else:
                    if any(_ in next_url for _ in [
                        '.edu.cn', '.gov.cn', '.org.cn', '.qq.com', '.163.com', '.microsoft.com',
                        '.adobe.com', '.google.com', '.baidu.com', '.foxitsoftware.cn', '.ujsde.com',
                        'weibo.com', '.ieee.org', '.sunning.com', '.jd.com', '.springer.com', '.people.com.cn',
                        '.12306.com', '.cnki.net', '.w3.org', '.sina.com.cn', '.cctv.com', '.hao123.com', '.youku.com',
                        '.sohu.com', '.zol.com.cn'
                    ]):
                        continue
                    if not urlparse(next_url).netloc.strip():
                        continue
                    domain_item = DarkChainDomainNameItem()
                    domain_item['domainname'] = urlparse(next_url).netloc
                    domain_item['origin_url'] = response.url
                    domain_item['typo'] = 'href'
                    yield domain_item
            else:
                # yield Request(url=urljoin(url_prefix, next_url), callback=self.parse)
                yield Request(url=urljoin(response.url, next_url), meta={'num': response.meta.get('num', 0) + 1},
                              callback=self.parse)