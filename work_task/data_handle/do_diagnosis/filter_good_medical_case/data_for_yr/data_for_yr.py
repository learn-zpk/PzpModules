import codecs
import json
import os
import zlib


def load_data(file_path):
    with codecs.open(file_path, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        while line:
            yield line
            line = f.readline().strip()


def compress(result):
    bytes_message = str.encode(json.dumps(result))
    return zlib.compress(bytes_message, zlib.Z_BEST_COMPRESSION)


if __name__ == '__main__':
    # dict_path = '/script/graph_filtered.json'
    # corpus_dir = '/data/filter_corpus'
    # output_path = '/script/all_info.json'
    # _dict = {}
    # # 加载字典
    # for line in load_data(dict_path):
    #     data_js = {}
    #     try:
    #         data_js = json.loads(line)
    #     except Exception as e:
    #         pass
    #     _dict[data_js['vid']] = {
    #         'dh_visit': data_js['dh_visit'],
    #         'relation_infer_result': compress(data_js['relation_infer_result'])
    #     }
    #
    # idx = 0
    # with open(output_path, 'w+') as fw:
    #     for system in os.listdir(corpus_dir):
    #         system_dir = os.path.join(corpus_dir, system)
    #         for filename in os.listdir(system_dir):
    #             detail_path = os.path.join(system_dir, filename)
    #             for data in load_data(detail_path):
    #                 try:
    #                     info = json.loads(data)
    #                     vid = info.get('vid')
    #                     if info.get('vid') not in _dict:
    #                         continue
    #                     xxx = _dict.pop(vid)
    #                     dh_visit = xxx.get('dh_visit')
    #                     # icd10 = xxx.get('icd10')
    #                     symptom_infer_result = xxx.get('relation_infer_result')
    #                     icd10 = info.get('诊断').get('icd10')
    #                     if not info.get('入院记录'):
    #                         continue
    #                     signs = []
    #                     # for records in info.get('入院记录'):
    #                     signs += info.get('入院记录').get('体格检查', [])
    #                     signs += info.get('入院记录').get('专科检查', [])
    #                     signs += info.get('入院记录').get('专科情况', [])
    #                     signs += info.get('入院记录').get('查体', [])
    #                     labs = {}
    #                     for item, details in info['化验项目'].items():
    #                         if not details:
    #                             continue
    #                         labs[item] = {}
    #                         for detail_item, value in details.items():
    #                             labs[item][detail_item[0:detail_item.rindex('_')]] = value
    #                     idx += 1
    #                     print(idx)
    #                     fw.write('{}\n'.format(json.dumps({
    #                         'vid': vid,
    #                         'icd10': icd10,
    #                         'dh_visit': dh_visit,
    #                         'symptom_infer_result': zlib.decompress(symptom_infer_result).decode(),
    #                         'signs': signs,
    #                         'labs': labs
    #                     }, ensure_ascii=False)))
    #                 except Exception as e:
    #                     pass
    _dict = {}
    input_path = '/script/140w'
    corpus_dir = '/data/filter_corpus'
    output_path = '/script/all_info.json'
    for filename in os.listdir(input_path):
        for line in load_data(os.path.join(input_path, filename)):
            data_js = {}
            try:
                data_js = json.loads(line)
            except Exception as e:
                pass
            _dict[data_js['vid']] = {
                'icd10': data_js['diagnosis'],
                'visit': data_js['visit'],
                'symptom_infer_result': data_js.get('xbs_infer_result', []),
                'sign_infer_result': data_js.get('jiancha_infer_result', [])
            }
    print('begin: {}'.format(len(_dict)))
    idx = 0
    with open(output_path, 'w+') as fw:
        for system in os.listdir(corpus_dir):
            system_dir = os.path.join(corpus_dir, system)
            for filename in os.listdir(system_dir):
                detail_path = os.path.join(system_dir, filename)
                for data in load_data(detail_path):
                    try:
                        info = json.loads(data)
                        vid = info.get('vid')
                        if info.get('vid') not in _dict:
                            continue
                        emr = _dict.pop(vid)

                        labs = {}
                        if '化验项目' in info:
                            for item, details in info['化验项目'].items():
                                if not details:
                                    continue
                                labs[item] = {}
                                for detail_item, value in details.items():
                                    labs[item][detail_item[0:detail_item.rindex('_')]] = value
                        idx += 1
                        print(idx)
                        fw.write('{}\n'.format(json.dumps({
                            'vid': vid,
                            'icd10': emr.get('icd10'),
                            'visit': emr.get('visit'),
                            'symptom_infer_result': emr.get('symptom_infer_result'),
                            'signs_infer_result': emr.get('sign_infer_result'),
                            'labs': labs
                        }, ensure_ascii=False)))
                    except Exception as e:
                        pass
    print('end: {}'.format(len(_dict)))