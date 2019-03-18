import codecs
import os
import re

import simplejson

re_compiler = re.compile(r"([。 ])(\1+)")
html_compiler = re.compile(r'<[^>]+>', re.S)
blank_back_compiler = re.compile(r"([.。，,:：；;()（）、\\/+-]) ")
blank_front_compiler = re.compile(r" ([.。，,:：；;()（）、\\/+-])")

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


def replace_character(txt):
    def deal(s):
        return s.group().strip()

    # 替换换行、table
    tmp = txt.replace('\\t', '。').replace('\\r', '。').replace('\\n', '。')
    tmp = tmp.replace('\t', '。').replace('\r', '。').replace('\n', '。')
    tmp = html_compiler.sub(' ', tmp)
    tmp = tmp.replace('\\xa0', ' ').replace('\xa0', ' ').replace(' ', ' ').replace('　', ' ')
    tmp = re_compiler.sub(r"\1", tmp)

    tmp = blank_back_compiler.sub(deal, tmp)
    return blank_front_compiler.sub(deal, tmp)


def good_xbs(xbs):
    if len(xbs) > 30:
        return True
    ch_len = 0
    for x in xbs:
        if u'\u4e00' <= x <= u'\u9fff':
            ch_len += 1
            # print(x)
        if ch_len >= 10:
            return True
    return False


def handler_emrs(data):
    xbs_list, zhusu_list, contents_new = [], [], []
    for idx, emr in enumerate(data):
        for doc in emr['data']:
            if doc['doc_type'] not in ['入院记录']:
                continue
            for content in doc['contents']:  # a list
                content_title, content_text = content['title'], content['text']
                if not content_title or not content_text:
                    continue
                content_text = replace_character(content_text)
                if re.match(".*主.*诉.*", content_title):
                    zhusu_list.append(content_text)
                elif re.match(".*现.*病.*史.*", content_title):
                    xbs_list.append(content_text)
                elif re.match(".*体.*格.*检.*查.*", content_title):
                    continue
                elif re.match(".*专.*科.*检.*查.*", content_title):
                    continue
                elif re.match(".*查.*体.*", content_title):
                    continue
                elif len(content_text) > 20:
                    contents_new.append({'title': content_title, 'text': content_text})
                    pass
    if xbs_list:
        flag = 0
        for xbs in xbs_list:
            if good_xbs(xbs):
                flag = 0
            else:
                contents_new.append({'title': '现病史', 'text': xbs})
                flag = 1
        if flag == 1:
            return '现病史少于10个汉字', contents_new
    elif zhusu_list:
        flag = 0
        for zhusu in zhusu_list:
            if good_xbs(zhusu):
                flag = 0
            else:
                contents_new.append({'title': '主诉', 'text': zhusu})
                flag = 1
        if flag == 1:
            return '主诉少于10个汉字', contents_new
    else:
        return '无现病史主诉', contents_new
    return None, None


def process_data(input_path):
    xxx = 0
    inp_xxx, outp_xxx = 0, 0
    print('# 来源医院{}'.format(input_path.split('/')[2][0:4]))
    for idx, data in enumerate(load_data(input_path)):
        try:
            if idx > 30000 or (inp_xxx > 80 and outp_xxx > 80):
                break
            data_js = simplejson.loads(data)
            if data_js['type'] == '@住院' and inp_xxx > 80:
                continue
            if data_js['type'] in ['@门诊', '@急诊'] and outp_xxx > 80:
                continue
            tag, contents = handler_emrs(data_js['emrs'])
            if not contents:
                continue

            xxx += 1
            if data_js['type'] == '@住院':
                inp_xxx += 1
            else:
                outp_xxx += 1
            print('## {}. {}'.format(xxx, tag))
            print('- **类型** {}'.format(data_js['type']))
            print('- **诊断结果** ')
            for ds in data_js['diagnosises']:
                print(' - **{}** {}'.format(ds['type'], ds['diagnosis']))

            print('- **入院记录** ')
            for content in contents:
                print(' - **{}** {}'.format(content['title'], content['text']))
        except Exception as e:
            # print('error json loads, path: {}, idx: {}'.format(input_path, idx))
            continue


if __name__ == '__main__':
    data_dir = '/data'
    filename_list = ['gd2h00', 'gyfy00', 'fsyy15', 'nfyy01']
    # data_dir = './'
    # filename_list = ['nfyy01']
    for filename in filename_list:
        process_data(os.path.join(data_dir, filename))
