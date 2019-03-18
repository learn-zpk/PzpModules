import json
import re
from datetime import datetime
from time import sleep

import requests

sign_list = [',', '。', ';']

db_host = '192.168.100.41'
MODEL_REQ_URL = 'http://model.rxthinking.com/modelapi/api/req'
MODEL_RES_URL = 'http://model.rxthinking.com/modelapi/api/res'
re_pattern = re.compile(r'\d+$')


def replace_punctuations(text):
    text = text.replace('（', '(').replace('）', ')').replace('，', ',').replace('：', ':').replace('；', ';')
    if text[-1] == ',':
        text = text[0:-1] + '。'
    elif text[-1] not in ['。', ';']:
        text += '。'
    return text


def split_text(text, max_len=100):
    def continue_split(_begin, _txt, max_len):
        _arr = []
        if len(_txt) > max_len:
            idx = _txt.rfind(',', 0, max_len)
            if idx == -1:
                return [(_begin, _txt)]
            _arr.append((_begin, _txt[0:idx] + '。'))
            _arr.extend(continue_split(_begin + idx + 1, _txt[idx + 1:], max_len))
        else:
            _arr.append((_begin, _txt))
        return _arr

    begin, tmp = 0, []
    for cur_index, _chr in enumerate(text):
        if _chr in ['。', ';']:
            tmp.append((begin, text[begin:cur_index + 1]))
            begin = cur_index + 1
    if text[begin:]:
        tmp.append((begin, text[begin:]))
    results = []
    for start, _txt in tmp:
        if _txt[-1] not in ['。', ';']:
            _txt += '。'
        if len(_txt) > max_len:
            results.extend(continue_split(start, _txt, max_len))
        else:
            results.append((start, _txt))
    return [t[1] for t in results]


def split_text_with_punctuation(punc_list, text, tokens):
    result = []
    _text_puncs = []  # 记录标点的位置
    for i, t in enumerate(text + ' '):
        if t in punc_list:
            _text_puncs.append(i)
    _token_puncs = []  # 记录标点的位置
    for i, t in enumerate(tokens + [' ']):
        if t in punc_list:
            _token_puncs.append(i)
    if len(_text_puncs) != len(_token_puncs):
        print('原文和标注的标点不对齐')
        return []
    _text_parts = []
    s = 0
    for i in _text_puncs:
        _text_parts.append(text[s:i])
        s = i + 1
    s = 0
    _token_parts = []
    for i in _token_puncs:
        _token_parts.append(tokens[s:i])
        s = i + 1
    for t, k in zip(_text_parts, _token_parts):
        result.append((t, k))
    return result


def _load_content_from_response(_response, flag):
    if _response.status_code != 200:
        raise Exception("{flag}服务错误".format(flag=flag))
    _content = json.loads(_response.text)
    return _content


def deal_request(req_url, res_url, data="{}", flag="", time_out=60):
    try:
        first_content = _load_content_from_response(requests.post(req_url, data=data.encode('utf-8')), flag)
        if first_content.get('code') != 0:
            raise Exception("{flag}服务错误".format(flag=flag))
        request_id = first_content.get('requestId')
        sleep(0.4)
        start = datetime.now()
        next_url = "{}/{}".format(res_url, request_id)
        next_content = _load_content_from_response(requests.post(next_url), flag)
        while next_content.get('code') == 1 and (datetime.now() - start).seconds <= time_out:
            sleep(0.4)
            next_content = _load_content_from_response(requests.post(next_url), flag)
        if (datetime.now() - start).seconds > time_out:
            raise Exception("{flag}:{time_out}秒超时".format(flag=flag, time_out=time_out))
        elif next_content.get('code') != 0:
            raise Exception("服务端异常")
        return next_content.get('items')

    except Exception as e:
        raise Exception("{flag}错误，{error}".format(flag=flag, error=str(e)))
