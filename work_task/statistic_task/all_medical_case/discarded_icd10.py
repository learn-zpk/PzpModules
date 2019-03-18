import codecs
import collections
import json

import pymongo
import xlwt

from data.dicts.medical_case_dict import ICD10_UNIFY_DICT


def load_icd10_dict():
    db = pymongo.MongoClient(u"mongodb://{host}:{port}".format(host='192.168.100.19', port=27017))[u'dataplatform']
    disease_collection = db['entity.disease.version']
    _dict = {}
    for data in disease_collection.find({}, {'content.icd10s.code': 1, 'content.name.name': 1, "_id": 0}):
        _dict[data['content']['icd10s'][0]['code']] = data['content']['name']['name']
    return _dict


all_icd10 = load_icd10_dict()


def load_data(input_path):
    with codecs.open(input_path, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        while line:
            yield line
            line = f.readline().strip()


def process_data(input_path):
    no_unify_dict = collections.defaultdict(lambda: 0)
    for idx, line in enumerate(load_data(input_path)):
        try:
            medical_record = json.loads(line)
        except Exception as e:
            continue
        for icd10 in medical_record['diagnosis']:
            if icd10 in ICD10_UNIFY_DICT:
                continue
            no_unify_dict[icd10] += 1
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet("脑图过滤后丢弃的icd10", cell_overwrite_ok=True)
    worksheet.write(0, 0, label='icd10')
    worksheet.write(0, 1, label='icd10_name')
    worksheet.write(0, 2, label='icd10_name')
    j = 1
    for icd10, count in no_unify_dict.items():
        worksheet.write(j, 0, label=icd10)
        worksheet.write(j, 1, label=all_icd10.get(icd10, None))
        worksheet.write(j, 2, label=count)
        j += 1
    workbook.save('./脑图过滤后丢弃的icd10统计结果.xls')


if __name__ == '__main__':
    # _input_path = '/Users/learnzpk/Myspace/pyproject/do_diagnose/data/origin/nfyy_test2w.data'

    _input_path = '/data/nfyy.data'

    process_data(_input_path)
    # print(content_title_set)
