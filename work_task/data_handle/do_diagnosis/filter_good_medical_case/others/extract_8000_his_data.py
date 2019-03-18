import codecs
import json
import os
import re


def good_xbs(xbs):
    if len(xbs) > 30:
        return True
    ch_len = 0
    for x in xbs:
        if u'\u4e00' <= x <= u'\u9fff':
            ch_len += 1
            print(x)
        if ch_len >= 12:
            return True
    return False


blank_back_compiler = re.compile(r"([.。，,:：；;()（）、\\/+-]) ")
blank_front_compiler = re.compile(r" ([.。，,:：；;()（）、\\/+-])")


def replace_blank(_str):
    def deal(s):
        return s.group().strip()

    tmp = blank_back_compiler.sub(deal, _str)
    return blank_front_compiler.sub(deal, tmp)


def load_data(input_path):
    with codecs.open(input_path, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        while line:
            yield line
            line = f.readline().strip()


def handle_emrs(emrs):
    tmp = {
        'xbs': [],
        'jiancha': []
    }
    xbs_count = 0
    for xbs in emrs['现病史/主诉']:
        if not good_xbs(xbs):
            continue
        tmp['xbs'].append(replace_blank(xbs))
        xbs_count += 1
    if xbs_count == 0:
        raise Exception('bad xbs')
    for jiancha in emrs['检查']:
        tmp['jiancha'].append(replace_blank(jiancha))

    return tmp


def process_data(input_dir, output_fw):
    inp_total = 0
    inp_path = os.path.join(input_dir, '住院')
    for idx, data in enumerate(load_data(inp_path)):
        if inp_total > 5600:
            break
        try:
            data_js = json.loads(data)
            data_js['emrs'] = handle_emrs(data_js['emrs'])
            output_fw.write('{}\n'.format(json.dumps(data_js, ensure_ascii=False)))
            inp_total += 1
        except Exception as e:
            print(e, ':', inp_path)
            continue
    outp_path = os.path.join(input_dir, '门急诊')
    outp_total = 0
    for idx, data in enumerate(load_data(outp_path)):
        if outp_total > 8000 - inp_total:
            break
        try:
            data_js = json.loads(data)
            data_js['emrs'] = handle_emrs(data_js['emrs'])
            outp_total += 1
            output_fw.write('{}\n'.format(json.dumps(data_js, ensure_ascii=False)))
        except Exception as e:
            print(e, ':', outp_path)
            continue
    print('@@{} 住院: {},门急诊: {}'.format(input_dir.split('/')[3], inp_total, outp_total))


if __name__ == '__main__':
    data_dir = './6000case/'
    output_dir = './8000data2his'
    for _dir in os.listdir(data_dir):
        first_dir = os.path.join(data_dir, _dir)
        for __dir in os.listdir(first_dir):
            second_dir = os.path.join(first_dir, __dir)

            key = second_dir.split('/')[3]
            fw = codecs.open(os.path.join(output_dir, '{}.json'.format(key)), 'w+', encoding='utf8')
            process_data(second_dir, fw)
            fw.close()
