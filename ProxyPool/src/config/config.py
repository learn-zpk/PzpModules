import os

"""全局环境配置"""
global_config = {
    "env": os.getenv("env", "dev"),
    "name": "ip_proxy_pool",
    "version": "1.0",
    "host": os.getenv('host', "0.0.0.0"),
    "port": int(os.getenv('port', 8080)),
    "debug": os.getenv('debug', 'Y'),
}

"""redis操作配置"""
redis_config = {
    "host": os.getenv('redis_host', '192.168.100.19'),
    "port": int(os.getenv('redis_port', 56379)),
    "key_ttl": int(os.getenv('redis_key_ttl', 200))
}

"""mongo操作配置"""
mongo_config = {
    "host": os.getenv('mongo_host', '192.168.100.20'),
    "port": int(os.getenv('mongo_port', 57017)),
    "username": os.getenv('mongo_username', "platform"),
    "password": os.getenv('mongo_password', "platform"),
    "database": os.getenv('mongo_database', 'ai-platform'),
    "authentication_db": os.getenv('mongo_authentication_db', 'ai-platform')
}

