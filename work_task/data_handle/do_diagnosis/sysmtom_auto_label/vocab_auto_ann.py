# encoding:utf-8
from utils.pzp_utils import get_platform_collection

AUTO_ANN_TEXT_LEN_BEGIN = 1
AUTO_ANN_TEXT_LEN_END = 50


def get_vocab_dict(vocab_collection_name):
    vocab_dict = {}
    for _len in range(AUTO_ANN_TEXT_LEN_BEGIN, AUTO_ANN_TEXT_LEN_END + 1):
        vocab_dict[_len] = {}
    for data in get_platform_collection('192.168.100.41', vocab_collection_name).find({}, {"_id": 0}):
        cur_len = len(data.get('vocab'))
        if cur_len > AUTO_ANN_TEXT_LEN_END or cur_len < AUTO_ANN_TEXT_LEN_BEGIN:
            continue
        vocab_dict[cur_len][data.get('vocab')] = (data.get('unique_entity'), "") \
            if not data.get('unique_word') \
            else (data.get('unique_entity'), data.get('unique_word'))
    return vocab_dict


def _ann_result_to_entities(ann_result, root_entities, vocab_dict):
    final_result = []
    index = 1
    for result in ann_result:
        _from, _to, _vocab, _length = result.get('from'), result.get('to'), result.get('vocab'), result.get('length')
        entity, word = vocab_dict.get(_length).get(_vocab)
        tmp = {
            "t_id": "T{}".format(index),
            "t_name": entity,
            "from": _from,
            "to": _to,
            "text": _vocab,
            "word": word if word else ""
        }
        # if entity in root_entities:
        #     tmp['disabled'] = 'Y'
        final_result.append(tmp)
        index += 1

    return final_result


# @count_time
def _auto_ann(ann_vocab, vocab_dict):
    result = []
    start, stop = 0, len(ann_vocab)
    while start < stop:
        length = len(ann_vocab[start:])
        for size in range(AUTO_ANN_TEXT_LEN_END if length > AUTO_ANN_TEXT_LEN_END else length, 0, -1):
            cur_vocab = ann_vocab[start:start + size]
            if size not in vocab_dict:
                continue
            if cur_vocab in vocab_dict[size]:
                result.append({
                    "from": start,
                    "to": start + size,
                    "vocab": cur_vocab,
                    "length": size
                })
                start += size - 1
                break
        start += 1
    return result


def vocab_auto_ann(ann_vocab, root_entities, vocab_dict):
    ann_result = _auto_ann(ann_vocab, vocab_dict)
    return _ann_result_to_entities(ann_result, root_entities, vocab_dict)


if __name__ == '__main__':
    pass
    # ann_vocab = '19岁，有过性生活，女生妇科阴道分泌物，黄色，有味道，无痛无痒，小腹不痛，饮食比较辛辣，休息时间比较晚，'
    # root_entity_list = ['临床表现', '年龄段', '性别']
    #
    # print(auto_ann(ann_vocab, root_entity_list, 'word_XBLCBX_1'))
