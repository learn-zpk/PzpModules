# encoding:utf-8
import collections
import csv
import re

from data_handle.do_diagnosis.sysmtom_auto_label.base import replace_punctuations, sign_list, split_text
from utils.pzp_utils import get_platform_collection


def generate_train_text_dict(begin, end, entities):
    suffix_dict = collections.defaultdict(lambda: 0)
    tid2train_name_dict = dict()
    text_dict = dict()
    for entity in entities:
        _from, _to, t_name = entity.get('from'), entity.get('to'), entity['t_name']
        if not (begin <= _from <= _to <= end):
            continue
        train_name = "{}{}".format(t_name, suffix_dict[t_name])
        suffix_dict[t_name] += 1
        tid2train_name_dict[entity.get('t_id')] = train_name
        for pos in range(_from, _to):
            text_dict[pos] = train_name
    return text_dict, tid2train_name_dict


def generate_relation_dict(tid2train_name_dict, relations):
    relation_dict = collections.defaultdict(set)
    for tid in tid2train_name_dict:
        for relation in relations:
            if relation.get('from') == tid and relation.get('to') in tid2train_name_dict:
                relation_dict[tid2train_name_dict[tid]].add(tid2train_name_dict[relation.get('to')])
                relation['flag'] = True
    return relation_dict


re_pattern = re.compile(r'\d+$')


def generate_convert_no_dict(_list):
    _dict = collections.defaultdict(list)
    for data in _list:
        if data == 'U':
            continue
        xxx = re.split(re_pattern, data)
        if data not in _dict[xxx[0]]:
            _dict[xxx[0]].append(data)
    # print(_dict)
    return _dict


def convert_result(result_list, convert_no_dict):
    tmp = []
    for data in result_list:
        if data in ['U', 'PS', 'PE'] + sign_list:
            tmp.append(data)
            continue
        xxx = re.split(re_pattern, data)
        if not xxx or xxx[0] not in convert_no_dict or data not in convert_no_dict[xxx[0]]:
            tmp.append(data)
            continue
        tmp.append('{}{}'.format(xxx[0], convert_no_dict[xxx[0]].index(data)))
    return tmp


repeat_dict = set()
space_idx = 0
idx = 0


def generate_data(text, entities, relations, train_fw, test_fw):
    global idx, space_idx
    _set = set()
    for data in relations:
        x1, x2 = "", ""
        for entity in entities:
            if entity['t_id'] == data.get('from'):
                x1 = "{}_{}".format(entity['from'], entity['to'])
        for entity in entities:
            if entity['t_id'] == data.get('to'):
                x2 = "{}_{}".format(entity['from'], entity['to'])
        # if '{}_{}'.format(x1, x2) in _set:
        #     pass
        _set.add('{}_{}'.format(x1, x2))
    for begin, _text in split_text(text):
        if not _text:
            continue
        # if _text in repeat_dict:
        #     continue
        repeat_dict.add(_text)
        end = begin + len(_text)
        text_dict, tid2train_name_dict = generate_train_text_dict(begin, end, entities)

        _list = []
        for _chr in _text:
            if _chr in sign_list:
                _list.append(_chr)
            else:
                _list.append('U')
        for _index, _chr in enumerate(_text):
            i = _index + begin
            if i in text_dict:
                _list[_index] = text_dict[i]
        relation_dict = generate_relation_dict(tid2train_name_dict, relations)

        result_list = [_list[0]]
        j = 1
        while j < len(_list):
            if _list[j - 1] in relation_dict and _list[j] != _list[j - 1]:
                result_list.append('PS')
                for train_name in relation_dict[_list[j - 1]]:
                    result_list.append(train_name)
                result_list.append('PE')
            result_list.append(_list[j])
            j += 1

        convert_no_dict = generate_convert_no_dict(_list)
        _result = [_text, ' '.join(convert_result(_list, convert_no_dict)),
                   ' '.join(convert_result(result_list, convert_no_dict))]
        if set(_result[1].split(' ')).issubset(set(sign_list + ['U'])):
            space_idx += 1
            if space_idx % 6 != 0:
                continue
        idx += 1
        if idx % 11 == 0:
            test_fw.writerow(_result)
        else:
            train_fw.writerow(_result)


def generate_data_set(relation_task_name_list, configure_id):
    train_out = open('./train.csv', 'w+')
    train_fw = csv.writer(train_out, dialect='excel')
    train_fw.writerow(["text", "label_no_relation", "label_relation"])

    test_out = open('./test.csv', 'w+')
    test_fw = csv.writer(test_out, dialect='excel')
    test_fw.writerow(["text", "label_no_relation", "label_relation"])

    for relation_task_name in relation_task_name_list:
        _collection = get_platform_collection("192.168.100.41", relation_task_name)
        for _data in _collection.find({'status': {"$in": ['已标注', '审核通过']}}):
            tmp = _data[configure_id][0]
            text = replace_punctuations(tmp['text'])
            generate_data(text, tmp.get('entities', []), tmp.get('relations', []), train_fw, test_fw)
    train_out.close()
    test_out.close()


if __name__ == '__main__':
    generate_data_set(
        ['task_relation_XBS_NEW', 'task_relation_CWZZJGH_14'],
        '1191cf9a-e2fd-11e8-bd36-6a00038f2a30'
    )
    # _txt = '12345678901234567890,012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678,90。'
    # print(continue_split(0, _txt, 100))
    # print(_txt[99:])
