from src.core.util.HttpUtils import load_html_tree
from src.free.abstract_ip_extract import AbstractIpExtract


class Data5U(AbstractIpExtract):
    def __init__(self, url_list):
        AbstractIpExtract.__init__(self)
        self.url_list = url_list

    def extract(self, **kwargs):
        for url in self.url_list:
            html_tree = load_html_tree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    yield ':'.join(ul.xpath('.//li/text()')[0:2])
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    test = Data5U([
        'http://www.data5u.com/',
        'http://www.data5u.com/free/gngn/index.shtml',
        'http://www.data5u.com/free/gnpt/index.shtml'
    ])

    for i in test.extract():
        print(i)
