import codecs
import os

import simplejson


def load_data(input_path):
    with codecs.open(input_path, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        while line:
            yield line
            line = f.readline().strip()


def parse_diagnosis(raw_diags):
    def _flatten_icds(diags, key):
        return [d for ds in diags if ds.get('type', '') == key for d in ds.get('icd10', [])]

    def gen_data():
        leave_hos_main = _flatten_icds(raw_diags, '出院主要诊断') + _flatten_icds(raw_diags, '出院诊断')
        pathologic_main = _flatten_icds(raw_diags, '病理诊断')
        rule1 = list(set(leave_hos_main) | set(pathologic_main))
        yield rule1
        yield leave_hos_main
        yield _flatten_icds(raw_diags, '主要诊断')
        yield _flatten_icds(raw_diags, '入院初诊')
        yield _flatten_icds(raw_diags, '门诊诊断')

    if raw_diags in [None, []]:
        return []
    for diagnosis in gen_data():
        if len(diagnosis) > 0:
            return diagnosis
    return [d for ds in raw_diags for d in ds['icd10']]


total = 0
cur_one = 0
new_one = 0


def process_data(input_path):
    global cur_one, new_one, total
    for idx, data in enumerate(load_data(input_path)):
        try:
            data_js = simplejson.loads(data)
        except Exception as e:
            print('error json loads, path: {}, idx: {}'.format(input_path, idx))
            continue
        total += 1
        if len(data_js['diagnosis']) == 1:
            cur_one += 1

        if len(parse_diagnosis(data_js['diagnosises'])) == 1:
            new_one += 1


if __name__ == '__main__':
    data_dir = '/data'
    filename_list = ['gd2h00', 'gyfy00', 'fsyy15', 'fsyy09', 'fsyy02', 'nfyy01', 'nfyy08', 'nfyy15', 'nfyy24', 'nfyy36']
    # filename_list = ['nfyy01']
    for filename in filename_list:
        process_data(os.path.join(data_dir, filename))
    print('采样: {}条'.format(total))
    print('原单诊断结果: {}条,'.format(cur_one))
    print('新单诊断结果: {}条,'.format(new_one))
