import collections
import json

import xlrd

from utils.pzp_utils import get_platform_collection


def merge_child(children_icd10_list, other_list):
    return_list = []
    _set = set()
    for xxx in children_icd10_list + other_list:
        if xxx.get('children_icd10') in _set:
            continue
        _set.add(xxx.get('children_icd10'))
        return_list.append(xxx)
    # print(len(return_list) == len(children_icd10_list + other_list))
    return return_list


if __name__ == '__main__':
    # workbook = xlrd.open_workbook('./补充icd结果统计(1).xlsx')
    # sheet = workbook.sheet_by_name('脑图过滤后丢弃的icd10')
    # _dict = collections.defaultdict(lambda: [])
    # for i in range(1, sheet.nrows):
    #     children_icd10 = str(sheet.cell(i, 0).value).strip()
    #     children_icd10_name = str(sheet.cell(i, 1).value).strip()
    #     unify_icd10 = str(sheet.cell(i, 4).value).strip()
    #     unify_icd10_name = str(sheet.cell(i, 3).value).strip()
    #
    #     if unify_icd10 in ['', '？']:
    #         continue
    #     # print(unify_icd10, unify_icd10_name)
    #     _dict[unify_icd10].append({
    #         "children_icd10": children_icd10,
    #         "children_icd10_name": children_icd10_name
    #     })
    _coll = get_platform_collection('192.168.100.41', 'disease_mind_map')

    # print(_dict.keys() - _coll.distinct('unify_icd10', {'unify_icd10': {'$in': list(_dict.keys())}}))
    # for data in _coll.find({'unify_icd10': {'$in': list(_dict.keys())}}):
    #     data['children_icd10_list']['new'] = merge_child(data['children_icd10_list']['new'], _dict[data['unify_icd10']])
    #     data['children_icd10_list']['old'] = merge_child(data['children_icd10_list']['old'], _dict[data['unify_icd10']])
    # _coll.save(data)

    _dict = {}
    for data in _coll.find():
        unify_icd10 = data['unify_icd10'].strip()

        for xx in data['children_icd10_list']['new']:
            children_icd10 = xx["children_icd10"].strip()
            _dict[children_icd10] = unify_icd10
    print(json.dumps(_dict, ensure_ascii=False))
