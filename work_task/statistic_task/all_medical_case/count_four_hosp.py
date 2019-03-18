import codecs
import collections
import json

import simplejson
import os


def load_data(file_path):
    with codecs.open(file_path, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        while line:
            yield line
            line = f.readline().strip()


if __name__ == '__main__':
    xxx_dict = collections.defaultdict(lambda: collections.defaultdict(lambda: {
        'count': 0,
        'labs': 0,
        'one_icd10': 0,
        'more_icd10': 0
    }))
    for filename in os.listdir('./'):
        # if not filename.endswith('.data'):
        #     continue
        # if 'gd2h' in filename:
        #     continue
        if filename != 'fsyy.data':
            continue
        hosp = filename.split('.data')[0]

        for idx, data in enumerate(load_data('./{}'.format(filename))):
            try:
                if idx % 20000 == 0:
                    print(hosp, idx)
                if len(data) >= 100000 * 10000:
                    print(idx)
                    continue
                data_js = simplejson.loads(data)
                typo = data_js['type']
                if len(data_js['diagnosis']) == 1:
                    xxx_dict[hosp][typo]['one_icd10'] += 1
                elif len(data_js['diagnosis']) > 1:
                    xxx_dict[hosp][typo]['more_icd10'] += 1
                xxx_dict[hosp][typo]['count'] += 1
                if data_js['labs']:
                    xxx_dict[hosp][typo]['labs'] += 1
            except Exception as e:
                continue
        print(json.dumps(xxx_dict, ensure_ascii=False))
