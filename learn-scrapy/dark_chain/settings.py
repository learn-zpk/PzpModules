# Scrapy settings for dark_chain project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'dark_chain'

SPIDER_MODULES = ['dark_chain.spiders']
NEWSPIDER_MODULE = 'dark_chain.spiders'

MONGO_URI = 'mongodb://USERNAME:PASSWORD@HOST:PORT/books'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'dark_chain (+http://www.yourdomain.com)'
LOG_LEVEL = 'INFO'  # 日志级别
FEED_EXPORT_ENCODING = 'utf-8'  # 解决unicode中文乱码问题
# RETRY_ENABLED = False #禁止重试
DOWNLOAD_TIMEOUT = 10  # 减少下载超时
# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # 不遵守robots协议
REDIRECT_ENABLED = True  # 开启重定向，一般建议关闭此选项，根据状态位进一步发起请求
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100  # 设置并发的request请求
CONCURRENT_REQUESTS_PER_DOMAIN = 10  # 任何单个域执行的并发（即同时）请求的最大数量
CONCURRENT_REQUESTS_PER_IP = 10  # 对任何单个IP执行的并发（即同时）请求的最大数量
COOKIES_ENABLED = False  # 禁用cookies
HTTPERROR_ALLOWED_CODES = [403, 404]  # 默认只处理200-300之间的response,通过此参数配置其他处理的响应
# DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter' # 自定义url去重，一般分布式爬虫时指定scrapy_redis.dupefilter.RFPDupeFilter

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0 # 下载延时，不怕被拦截，就设置为0(可以自配ip代理池)

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'dark_chain.middlewares.DarkChainSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'dark_chain.middlewares.DarkChainDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

ITEM_PIPELINES = {
    'dark_chain.pipelines.mongo_pipeline.ItemWritePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
