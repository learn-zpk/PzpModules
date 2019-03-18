import codecs
import os

import simplejson


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


def load_data(input_path):
    with codecs.open(input_path, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        while line:
            yield line
            line = f.readline().strip()


def process_data(input_path):
    print("cur_path:", input_path)
    with codecs.open('{}.data'.format(input_path), 'w+', encoding='utf-8') as fw:
        for idx, data in enumerate(load_data(input_path)):
            try:
                data_js = simplejson.loads(data)
                data_js['diagnosis'] = parse_diagnosis(data_js['diagnosises'])
                fw.write('{}\n'.format(simplejson.dumps(data_js, ensure_ascii=False)))
            except Exception as e:
                print('error json loads, path: {}, idx: {}'.format(input_path, idx))
                continue
    os.remove(input_path)


if __name__ == '__main__':
    data_dir = '/data'
    path_list=os.listdir(data_dir)
    print(path_list)
    for filename in path_list:
        if not any([_ in filename for _ in ['nfyy', 'gyfy', 'fsyy', 'gd2h']]):
            continue

        process_data(os.path.join(data_dir, filename))
