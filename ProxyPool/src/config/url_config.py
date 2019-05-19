
"""免费代理网站"""
from src.free.impl import data5u_impl, proxy66_impl

default_free_list = {
    "data5u": {
        "desc": "无忧代理",
        "impl": data5u_impl,
        "url_list": [
            'http://www.data5u.com/',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml'
        ]
    },
    "proxy66": {
        "desc": "66代理",
        "impl": proxy66_impl,
        "url_list": [
            "http://www.66ip.cn/mo.php?sxb=&tqsl={count}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=",
            "http://www.66ip.cn/nmtq.php?getnum={count}"
            "&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip",
        ]
    }
}
