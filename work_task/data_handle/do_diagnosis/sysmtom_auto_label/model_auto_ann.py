# encoding:utf-8
import copy
import json
import re
import traceback

from data_handle.do_diagnosis.sysmtom_auto_label.base import split_text, sign_list, split_text_with_punctuation, \
    re_pattern, \
    MODEL_REQ_URL, MODEL_RES_URL, deal_request
from data_handle.do_diagnosis.sysmtom_auto_label.vocab_auto_ann import vocab_auto_ann, get_vocab_dict


def _generate_relation_name(from_name, to_name, configure_relations):
    from_entity = re.split(re_pattern, from_name)[0]
    to_entity = re.split(re_pattern, to_name)[0]
    for configure_relation in configure_relations:
        if from_entity in configure_relation['from'] and to_entity in configure_relation['to']:
            return configure_relation['name']
    return None


def _to_entities(start, text, text_list, id_dict, configure_entities):
    sub_entities, convert_entity_dict = [], {'U': ''}
    i = 0
    _entity_from, _entity_to = 0, 0
    while i < len(text_list):
        if text_list[i] in convert_entity_dict:
            i += 1
            continue
        _entity_from = start + i
        j = 1
        while i + 1 < len(text_list) and text_list[i] == text_list[i + 1]:
            i += 1
            j += 1

        _entity_name = re.split(re_pattern, text_list[i])[0]
        if _entity_name not in configure_entities:
            i += 1
            continue
        _entity_id = "T{}".format(id_dict['T'])
        _entity_to = _entity_from + j
        id_dict['T'] += 1
        sub_entities.append({
            "t_id": _entity_id,
            "t_name": _entity_name,
            "text": text[_entity_from - start:_entity_to - start],
            "from": _entity_from,
            "to": _entity_to
        })
        convert_entity_dict[text_list[i]] = _entity_id
        i += 1
    return sub_entities, convert_entity_dict


def _to_relations(convert_entity_dict, relation_list, id_dict, configure_relations):
    sub_relations = []
    for _relation in relation_list:
        if len(_relation) < 1:
            continue
        if _relation[0] not in convert_entity_dict:
            continue
        relation_from = convert_entity_dict[_relation[0]]
        for relation_to_name in _relation[1:]:
            relation_name = _generate_relation_name(_relation[0], relation_to_name, configure_relations)
            if not relation_name:
                continue
            try:
                sub_relations.append({
                    "r_id": "R{}".format(id_dict['R']),
                    "from": relation_from,
                    "to": convert_entity_dict[relation_to_name],
                    "r_name": relation_name
                })
            except Exception as e:
                print(traceback.format_exc())
            id_dict['R'] += 1
    return sub_relations


def _split_pse(tokens):
    last_index = 0
    entities, relations = list(), list()
    for index, token in enumerate(tokens + ['PS']):
        if token == 'PS':
            entities.extend(tokens[last_index:index])
            last_index = index - 1
        if token == 'PE':
            relations.append([token for token in tokens[last_index:index + 1] if token not in ['PS', 'PE']])
            last_index = index + 1
    return entities, relations


def _guess_vocab_list(text, vocab_collection_name, model_token_list):
    vocab_entities = vocab_auto_ann(text, [], get_vocab_dict(vocab_collection_name))
    new_token_list = ['U' for _ in range(len(text))]
    for entity in vocab_entities:
        new_token_list[entity['from']:entity['to']] = [entity['t_name'] for _ in range(entity['from'], entity['to'])]
    _index = 0
    model_index = 0
    model_len = len(model_token_list)

    try:
        for _index, _entity in enumerate(new_token_list):
            if _entity == 'U':
                if text[_index] not in sign_list:
                    new_token_list[_index] = model_token_list[model_index]
                model_index += 1
            elif model_index < model_len and _entity in model_token_list[model_index]:
                new_token_list[_index] = model_token_list[model_index]
                model_index += 1
            elif model_index - 1 < model_len and _entity in model_token_list[model_index - 1]:
                new_token_list[_index] = model_token_list[model_index - 1]
            elif model_index + 1 < model_len and _entity in model_token_list[model_index + 1]:
                new_token_list[_index] = model_token_list[model_index + 1]
                model_index += 2
            else:
                new_token_list[_index] = 'U'
                model_index += 1
    except Exception as e:
        print(traceback.format_exc())
        new_token_list = []
    return new_token_list


def _handle_entities_by_vocab(text, vocab_collection_name, model_entities, id_dict):
    new_entities = copy.deepcopy(model_entities)
    if not vocab_collection_name:
        return new_entities
    vocab_entities = vocab_auto_ann(text, [], get_vocab_dict(vocab_collection_name))
    _set = ()
    token_list = [0 for _ in range(len(text))]
    for model_entity in model_entities:
        for index in range(model_entity['from'], model_entity['to']):
            token_list[index] = 1
    for vocab_entity in vocab_entities:
        for index in range(vocab_entity['from'], vocab_entity['to']):
            if token_list[index] == 1:
                break
        else:
            new_entities.append({
                "t_id": "T{}".format(id_dict['T']),
                "t_name": vocab_entity['t_name'],
                "text": vocab_entity['text'],
                "from": vocab_entity['from'],
                "to": vocab_entity['to']
            })
            id_dict['T'] += 1

    return new_entities


def _convert_model_result(start, text, model_result, id_dict, configure_entities, configure_relations,
                          vocab_collection_name):
    if not model_result or model_result[0] in ['PS', 'PE']:
        return [], []
    token_list, relation_list = _split_pse(model_result)
    if len(token_list) != len(text):
        token_list = _guess_vocab_list(text, vocab_collection_name, token_list)
        if not token_list:
            return [], []
    try:
        sub_entities, convert_entity_dict = _to_entities(start, text, token_list, id_dict, configure_entities)
        sub_relations = _to_relations(convert_entity_dict, relation_list, id_dict, configure_relations)
    except Exception as e:
        print(traceback.format_exc())
        return [], []
    return sub_entities, sub_relations


def change_model_result(_text, model_result):
    xxx = []
    print(len(_text))
    print(len(model_result))
    for i, tmp in enumerate(model_result):
        if _text[i] in sign_list and tmp != 'U':
            xxx.append('U')
            xxx.append(tmp)
        else:
            xxx.append(tmp)
    print(len(_text))
    print(len(model_result))
    return xxx


def _label_relations(convert_entity_dict, relation_list, id_dict, configure_relations):
    try:
        sub_relations = _to_relations(convert_entity_dict, relation_list, id_dict, configure_relations)
    except Exception as e:
        print(traceback.format_exc())
        return []
    return sub_relations


def _label_entities(start, text, model_result, id_dict, configure_entities, vocab_collection_name):
    if not model_result or model_result[0] in ['PS', 'PE']:
        return [], [], []
    token_list, relation_list = _split_pse(model_result)
    if len(token_list) != len(text):
        token_list = _guess_vocab_list(text, vocab_collection_name, token_list)
        if not token_list:
            return [], [], []
    try:
        sub_entities, convert_entity_dict = _to_entities(start, text, token_list, id_dict, configure_entities)
    except Exception as e:
        print(traceback.format_exc())
        return [], [], []
    return sub_entities, relation_list, convert_entity_dict


def auto_ann_model(text, configure_entities, configure_relations, vocab_collection_name, service_queue):
    entities, relations, id_dict = list(), list(), {'T': 0, 'R': 0}
    model_result_list = deal_request(
        MODEL_REQ_URL + service_queue, MODEL_RES_URL,
        json.dumps({"input": split_text(text)}, ensure_ascii=False),
        '模型自动标注'
    )
    start = 0
    for (_text, model_result) in model_result_list:
        parts = split_text_with_punctuation(sign_list, _text, model_result)
        if not parts:
            start += len(_text)
            continue
        tmp_convert_dict = {}
        tmp_relations = []
        _entities = []
        for t, k in parts:
            if not t or not k:
                start += len(t) + 1
                continue
            sub_entities, sub_relations, con_dict = \
                _label_entities(start, t, k, id_dict, configure_entities, vocab_collection_name)
            _entities += sub_entities
            tmp_relations += sub_relations
            tmp_convert_dict.update(con_dict)
            start += len(t) + 1  # 跳过一个标点
        _relations = _label_relations(tmp_convert_dict, tmp_relations, id_dict, configure_relations)
        entities += _entities
        relations += _relations
    # 未标注出来的用词表标注
    # entities = _handle_entities_by_vocab(text, vocab_collection_name, entities, id_dict)
    return entities, relations
