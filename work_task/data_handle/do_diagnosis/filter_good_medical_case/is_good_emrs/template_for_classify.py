import codecs
import copy
import json
import os
import random
from datetime import datetime

import simplejson

from utils.pzp_utils import get_platform_collection


def gene_text(emr):
    # print(emr['诊断'])
    text_str = ""
    if '诊断' in emr:
        diag = emr['诊断']
        text_str += '<p style="color:green">诊断结果: {}_{}</p></br>'.format(diag['诊断名'], diag['icd10'])
    if '来源医院' in emr:
        text_str += '<p class="text"><b>来源医院:</b> {}</p>'.format(emr['来源医院'])
    if '就诊类型' in emr:
        text_str += '<p class="text"><b>就诊类型:</b> {}</p>'.format(emr['就诊类型'])
    if '基本信息' in emr:
        text_str += '</br><b>基本信息:</b></br>'
        base = emr['基本信息']
        if '年龄' in base:
            text_str += '<p class="textIndent w25"><b>年龄:</b> {}</p>'.format(base['年龄'])
        if '性别' in base:
            text_str += '<p class="textIndent w25"><b>性别:</b> {}</p>'.format(base['性别'])
        if '身高' in base:
            text_str += '<p class="textIndent w25"><b>身高:</b> {}</p>'.format(base['身高'])
        if '体重' in base:
            text_str += '<p class="textIndent w25"><b>体重:</b> {}</p>'.format(base['体重'])
    if '入院记录' in emr:
        admit = emr['入院记录']
        if '现病史' in admit:
            text_str += '</br></br><b>入院记录-现病史:</b></br>'
            for tmp in admit['现病史']:
                text_str += '<p class="textIndent">{}</p>'.format(tmp)
        if '主诉' in admit:
            text_str += '</br></br><b>入院记录-主诉:</b></br>'
            for tmp in admit['主诉']:
                text_str += '<p class="textIndent">{}</p>'.format(tmp)
        if '入院情况' in admit:
            text_str += '</br></br><b>入院记录-入院情况:</b></br>'
            for tmp in admit['入院情况']:
                text_str += '<p class="textIndent">{}</p>'.format(tmp)
        if '体格检查' in admit:
            text_str += '</br></br><b>入院记录-体格检查:</b></br>'
            for tmp in admit['体格检查']:
                text_str += '<p class="textIndent">{}</p>'.format(tmp)
        if '专科检查' in admit:
            text_str += '</br></br><b>入院记录-专科检查:</b></br>'
            for tmp in admit['专科检查']:
                text_str += '<p class="textIndent">{}</p>'.format(tmp)
        if '专科情况' in admit:
            text_str += '</br></br><b>入院记录-专科情况:</b></br>'
            for tmp in admit['专科情况']:
                text_str += '<p class="textIndent">{}</p>'.format(tmp)
        if '查体' in admit:
            text_str += '</br></br><b>入院记录-查体:</b></br>'
            for tmp in admit['查体']:
                text_str += '<p class="textIndent">{}</p>'.format(tmp)
        if '辅助检查' in admit:
            text_str += '</br></br><b>入院记录-辅助检查:</b></br>'
            for tmp in admit['辅助检查']:
                text_str += '<p class="textIndent">{}</p>'.format(tmp)
    if '首次病程记录' in emr and not (
            emr.get('入院记录').get('现病史', []) + emr.get('入院记录').get('主诉', []) + emr.get('入院记录').get('入院情况', [])):
        text_str += '</br></br><b>首次病程记录:</b></br>'
        for tmp in emr['首次病程记录']:
            text_str += '<p class="textIndent">{}</p>'.format(tmp)
    if '化验项目' in emr:
        text_str += '</br></br><b>化验项目:</b>'
        for item, details in emr['化验项目'].items():
            if not details:
                continue
            text_str += '</br></br><p class="textIndent"><b>化验项目: {}</b></p></br>'.format(item)
            for detail_item, value in details.items():
                text_str += '<p class="text textIndent">{}: {}</p>'.format(detail_item, value)
    return text_str


def gene_doc(emr, idx):
    return {
        "vid": emr.get('vid'),
        "group": emr.get('诊断').get('诊断名'),
        "indexing": "{:03d}".format(idx),
        "status": "已分配",
        "text": gene_text(emr),
        "creator": "robot",
        "annotator": "杨旭",
        "show_html": "Y",
        "auditor": "",
        "create_time": datetime.now(),
    }


def load_data(input_path):
    with codecs.open(input_path, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        while line:
            yield line
            line = f.readline().strip()


if __name__ == '__main__':
    _list = []
    data_dir = '/Users/learnzpk/Myspace/pzp_module/work_task/data_handle/do_diagnosis/filter_good_medical_case/is_good_emrs/nfyy'
    coll = get_platform_collection('192.168.100.41', 'ann_task_classification_BLSXFLRW_18', 27017)

    for filename in os.listdir(data_dir):
        if '_' not in filename:
            continue
        icd10, icd10_name = filename.split('_')
        idx = 225
        if icd10_name != '女性盆腔炎':
            continue
        with codecs.open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # idx_list = random.sample(range(0, len(lines)), 500)
            # print(idx_list)
            xxx = coll.distinct('vid', {'group': '女性盆腔炎'})

            for cur_idx, txt in enumerate(lines):
                try:
                    # if cur_idx not in idx_list:
                    #     continue
                    emr = simplejson.loads(txt)
                    if emr.get('vid') in xxx:
                        continue
                    #     coll.update_one({'vid': emr.get('vid')}, {'$set': {'text': gene_text(emr)}})
                    _list.append(gene_doc(emr, idx))
                    idx += 1
                    if idx >= 500:
                        break
                except Exception as e:
                    pass

            #coll.insert_many(_list, ordered=False)
            print(_list)

