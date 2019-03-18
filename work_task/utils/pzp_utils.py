import codecs

import pymongo


def load_data(file_path):
    with codecs.open(file_path, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        while line:
            yield line
            line = f.readline().strip()


def get_platform_collection(host, task_collection_name,port=27017):
    host = host
    username = u'platform'
    password = u'platform'
    db_name = u'ai-platform'
    uri = u"mongodb://{host}:{port}".format(host=host, port=port)
    db = pymongo.MongoClient(uri)[db_name]
    db.authenticate(username, password)
    return db[task_collection_name]


if __name__ == '__main__':
    pass
