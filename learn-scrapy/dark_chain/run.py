from scrapy import cmdline

cmdline.execute("scrapy crawl dark_chain -s LOG_FILE=all.log".split())
