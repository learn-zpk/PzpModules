import collections

import pymongo
import xlrd

SIGN_ENTITY_LIST = [
    "检查实体",
    "实体结果",
    "身体部位",
    "检查方法",
    "限定条件",
    "等级",
    "颜色",
    "时期",
    "音色音调",
    "质地",
    "形态",
    "范围大小",
    "数目",
    "形状",
    "程度",
    "活动度",
    "气味",
    "趋势",
    "节律",
    "频率和次数",
    "结果性质",
    "体液性质",
    "方位",
    "医学耗材",
    "否定"
]


def get_collection(task_collection_name):
    host = '192.168.100.41'
    port = 27017
    username = u'platform'
    password = u'platform'
    db_name = u'ai-platform'
    uri = u"mongodb://{host}:{port}".format(host=host, port=port)
    db = pymongo.MongoClient(uri)[db_name]
    db.authenticate(username, password)
    return db[task_collection_name]


def read_sign_unify_dict(_path):
    unify_dict = collections.defaultdict(lambda: {})
    workbook = xlrd.open_workbook(_path)
    for sheet in workbook.sheets():
        key = sheet.name.split('-')[0]
        # if key not in SIGN_ENTITY_LIST:
        #     print(key)
        # if sheet.cell(0, 1).value.strip() == '归一词':
        #     print(1, key)
        # elif sheet.cell(0, 2).value.strip() == '归一词':
        #     print(2, key)
        # else:
        #     print(3, key)
        for i in range(1, sheet.nrows):
            word = str(sheet.cell(i, 0).value).strip()
            unify_word = str(sheet.cell(i, 2).value).strip()
            if word and unify_word:
                unify_dict[key][word] = unify_word
    return unify_dict


unify_dict = read_sign_unify_dict('/Users/learnzpk/Myspace/pzp_module/work_task/data/dicts/体征标准词表-v1.0.xls')


def handle_data(entities, relations, no_unify_dict, relation_dict):
    entity_dict = {}
    for entity in entities:
        text, t_name, t_id = entity['text'], entity['t_name'], entity['t_id']
        if not text:
            continue
        if t_name not in unify_dict or text not in unify_dict[t_name]:
            no_unify_dict[t_name][text] += 1
            continue
        entity_dict[t_id] = (t_name, unify_dict[t_name][text])
    for relation in relations:
        _from, _to = relation['from'], relation['to']
        if _from not in entity_dict or _to not in entity_dict:
            continue
        xxx = '{}@@@{}@@@{}@@@{}'.format(entity_dict[_to][0], entity_dict[_to][1], entity_dict[_from][0],
                                         entity_dict[_from][1])
        relation_dict[xxx] += 1


if __name__ == '__main__':
    pass
    # configure_id = '76379b42-f945-11e8-927c-0242ac130009'
    # i = 0
    # no_unify_dict = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    # relation_dict = collections.defaultdict(lambda: 0)
    # for relation_task_name in ['task_relation_TGJC&ZKJCJGHXG_11', 'task_relation_TGJCGX_4', 'task_relation_ZKJCGX_9']:
    #     query = {'status': {"$in": ['已标注', '审核通过']}}
    #     if relation_task_name != 'task_relation_TGJC&ZKJCJGHXG_11':
    #         query['annotator'] = {}
    #         query['annotator']['$in'] = ['杨玉莹', '富佳妮', '吴婕']
    #
    #     for _data in get_collection(relation_task_name).find({}):
    #         i += 1
    #         if configure_id not in _data:
    #             continue
    #         entities, relations = _data[configure_id][0]['entities'], _data[configure_id][0]['relations']
    #         try:
    #             handle_data(entities, relations, no_unify_dict, relation_dict)
    #         except Exception:
    #             print(relation_task_name, _data['group'], _data['indexing'])
    # print(i)
    # import openpyxl
    #
    # workbook = openpyxl.Workbook()
    # for key, freq_dict in no_unify_dict.items():
    #     worksheet = workbook.create_sheet(index=0, title=key)
    #     worksheet.cell(1, 1).value = '实体'
    #     worksheet.cell(1, 2).value = '频次'
    #     j = 2
    #     for xx, xxx in freq_dict.items():
    #         worksheet.cell(j, 1).value = xx
    #         worksheet.cell(j, 2).value = xxx
    #         j += 1
    # workbook.save('体征未归一实体统计.xlsx')
    #
    # workbook2 = openpyxl.Workbook()
    # worksheet2 = workbook2.create_sheet(index=0, title="关系统计结果")
    # worksheet2.cell(1, 1).value = '实体'
    # worksheet2.cell(1, 2).value = '实体值'
    # worksheet2.cell(1, 3).value = '属性'
    # worksheet2.cell(1, 4).value = '属性值'
    # worksheet2.cell(1, 5).value = '频次'
    # k = 2
    # for xx, freq in relation_dict.items():
    #     worksheet2.cell(k, 1).value = xx.split('@@@')[0]
    #     worksheet2.cell(k, 2).value = xx.split('@@@')[1]
    #     worksheet2.cell(k, 3).value = xx.split('@@@')[2]
    #     worksheet2.cell(k, 4).value = xx.split('@@@')[3]
    #     worksheet2.cell(k, 5).value = freq
    #     k += 1
    # workbook2.save('体征关系统计结果.xlsx')
