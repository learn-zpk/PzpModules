import codecs
import copy
import hashlib
import json
import os
import traceback
from collections import defaultdict
from functools import reduce

SIGN_LIST = """S程度
S等级
S范围大小
S方位
S否定
S活动度
S检查方法
S检查实体
S节律
S结果性质
S频率和次数
S气味
S趋势
S身体部位
S时期
S实体结果
S数目
S体液性质
S限定条件
S形态
S形状
S颜色
S医学耗材
S音色音调
S质地
E程度
E等级
E范围大小
E方位
E否定
E活动度
E检查方法
E检查实体
E节律
E结果性质
E频率和次数
E气味
E趋势
E身体部位
E时期
E实体结果
E数目
E体液性质
E限定条件
E形态
E形状
E颜色
E医学耗材
E音色音调
E质地
||""".split('\n')


def convert_relation2train(entities, relations, collection_name=None, group=None, indexing=None, sentence_part=None):
    """
    把数据库中的entities 和 relations 转换成 S@@@*** *** E@@@*** || S@@@*** *** E@@@*** 的格式
    :param entities:
    :param relations:
    :param collection_name:
    :param group:
    :param indexing:
    :param sentence_part:
    :return:
    """
    text_list = []
    try:
        id2name, to_from_dict = _generate_relation_dict(entities, relations)
        if not id2name:
            return None
        no_relation_entities = set(id2name.keys()) - (set(to_from_dict.keys()) | set(
            reduce(lambda x, y: x + y, to_from_dict.values(), [])))
        if no_relation_entities:
            for n in no_relation_entities:
                text_list.append('{a} //{a}'.format(a=n))
        root = defaultdict(list)
        leaf = defaultdict(list)
        from_to_dict = _reverse_dict(to_from_dict)
        _leaf_dfs(from_to_dict, root, leaf)
        root_result = _merge_root(root, leaf)
        # print('snapper: {} @@@ {}'.format(json.dumps(entities, ensure_ascii=False),
        #                                   json.dumps(relations, ensure_ascii=False)))
        for k, v in root_result.items():
            text_list.append('{} {} //{}'.format(k, _merge_list(v), k))
        text_enties = ' || '.join(sorted(text_list, key=lambda s: int(s.split()[0].replace('T', '')))).split()
        result = []
        for t in text_enties:
            if '//' in t:
                if t[2:] in id2name:
                    result.append('E{}'.format(id2name[t[2:]][0]))
                else:
                    raise ValueError('实体结尾有误: {}'.format(t[2:]))
            elif t in id2name:
                result.append('S{} {}'.format(id2name[t][0], id2name[t][1]))
            else:
                result.append(t)
        return ' '.join(result)
    except Exception as e:
        print(e, '@{} @{} @{} @{}'.format(collection_name, group, indexing, sentence_part))


def convert_train2node_list(train_list, key_words):
    result = []
    tmp = ' '.join([t.upper() for t in train_list])
    try:
        for t in tmp.split('||'):
            result.extend(_convert_single_train2node(t, key_words))
        return result
    except Exception as e:
        print(traceback.print_exc())


def convert_train2node(train_text, key_words):
    result = []
    try:
        for t in train_text.split('||'):
            result.extend(_convert_single_train2node(t, key_words))
        return result
    except Exception as e:
        print(traceback.print_exc())


def convert_node2json(node_list):
    """
    把 node 格式转成 key value children格式
    :param node_list:
    :return:
    """
    result = []
    if not node_list:
        return
    for n in node_list:
        labelId = n.get('labelId')
        word = n.get('word')
        att = n.get('att')
        if att:
            result.append({
                'key': labelId,
                'value': word,
                'children': convert_node2json(att)
            })
        else:
            result.append({
                'key': labelId,
                'value': word,
                'children': []
            })
    return result


def _convert_single_train2node(train_text, key_words):
    """
    把 不带 || 的 train 格式转换成 labelId, word att的格式
    :param train_text:
    :return:
    """
    words_list = train_text.split()
    if not words_list:
        return None
    entity_stack = []
    nodes_dict = defaultdict(list)
    entity_index = 0
    try:
        for idx, w in enumerate(words_list):
            if w.startswith('S') and w in key_words:
                if idx + 1 >= len(words_list):
                    # print(words_list)
                    continue
                    # raise ValueError('未找到 {} 对应的值'.format(w))
                if words_list[idx + 1].startswith('S') or words_list[idx + 1].startswith('E'):
                    continue
                entity_stack.append((w[1:], words_list[idx + 1], entity_index))
                entity_index += 1
            elif w.startswith('E') and w in key_words:
                if len(entity_stack) <= 0:
                    continue
                    # raise ValueError('节点结构错误')
                if w[1:] != entity_stack[-1][0]:
                    tmp = copy.deepcopy(entity_stack)
                    last = tmp[-1]
                    while len(tmp) > 0:
                        if tmp[-1][0] == w[1:]:
                            break
                        else:
                            last = tmp.pop()
                    if len(tmp) > 0:
                        entity_stack = tmp
                        if last in nodes_dict:
                            nodes_dict[entity_stack[-1]] = nodes_dict.pop(last)
                    else:
                        print(words_list)
                        continue
                        # raise ValueError('节点结构不匹配: 当前属性为: {}, 实际匹配结果为: {}'.format(w, entity_stack[-1][0]))
                key = entity_stack.pop()
                if len(entity_stack) <= 0:
                    if key not in nodes_dict:
                        # 没有属性的临床表现
                        nodes_dict[key] = []
                    continue
                if key in nodes_dict:
                    att = nodes_dict.pop(key)
                    nodes_dict[entity_stack[-1]].append({
                        'labelId': key[0],
                        'word': key[1],
                        'att': att
                    })
                else:
                    nodes_dict[entity_stack[-1]].append({
                        'labelId': key[0],
                        'word': key[1],
                        'att': []
                    })
            else:
                pass
        result = []
        for k, v in nodes_dict.items():
            result.append({
                'labelId': k[0],
                'word': k[1],
                'att': v
            })
        return result
    except Exception as e:
        print(traceback.print_exc())


def _reverse_dict(to_from_dict):
    from_to_dict = defaultdict(list)
    tmp_dict = copy.deepcopy(to_from_dict)
    for k, v in tmp_dict.items():
        for d in v:
            from_to_dict[d].append(k)
    return from_to_dict


def _generate_relation_dict(entities, relations):
    """
    :param entities:
    :param relations:
    :return:
    """
    if not entities:
        return None, None
    id2name = {}
    for en in entities:
        t_id = en.get('t_id')
        t_name = en.get('t_name')
        text = en.get('text')
        id2name[t_id] = (t_name, text)
    to_from_dict = defaultdict(list)
    for rl in relations:
        _from = rl.get('from')
        _to = rl.get('to')
        # 检查是否存在双向关系
        if _from in to_from_dict and _to in to_from_dict[_from]:
            raise ValueError('{}<->{}存在双向关系'.format(id2name[_from], id2name[_to]))
        # 检查是否存在自己到自己的关系
        if _from == _to:
            raise ValueError('{}<->{}存在自己到自己的关系'.format(id2name[_from], id2name[_to]))
        to_from_dict[_to].append(_from)
    return id2name, to_from_dict


def _leaf_dfs(from_to_dict, root_dict, leaf_dict):
    if not from_to_dict:
        return root_dict, leaf_dict
    fs = set()
    ts = set()
    for k, v in from_to_dict.items():
        fs.add(k)
        ts.update(set(v))
    leaf = fs - ts
    if leaf:
        for f in leaf:
            t = from_to_dict.pop(f)
            if f in root_dict:
                att = root_dict.pop(f)
                leaf_dict[f].extend(att)
                for idx, i in enumerate(leaf_dict[f]):
                    if i in leaf_dict:
                        att[idx] = {i: leaf_dict[i]}
                leaf_dict[f] = att
                for m in t:
                    root_dict[m].append(f)
            else:
                leaf_dict[f] = []
                for a in t:
                    root_dict[a].append(f)
    else:
        pass
    _leaf_dfs(from_to_dict, root_dict, leaf_dict)


def _merge_root(root, leaf):
    tmp = {}
    for k, v in root.items():
        if not v:
            tmp[k] = v
            continue
        for idx, d in enumerate(v):
            if d in leaf:
                v[idx] = {d: copy.deepcopy(leaf[d])}
        tmp[k] = v
    return tmp


def _merge_list(relation_dict):
    data = copy.deepcopy(relation_dict)
    try:
        tmp = ''
        if not data:
            return ''
        for d in data:
            k, v = d.popitem()
            tmp += ' {a} {b} //{a}'.format(a=k, b=_merge_list(v))
        return tmp
    except Exception as e:
        print(e)


def load_data(file_path):
    with codecs.open(file_path, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        while line:
            yield line
            line = f.readline().strip()


def cut_y(y):
    index = [i for i, iy in enumerate(y) if iy == '||']
    # print index
    tmp_list = []
    if index == []:
        tmp_list = [y]
    else:
        for ii in range(len(index)):
            if ii == 0:
                tmp_list.append(y[:index[ii]])
            else:
                tmp_list.append(y[index[ii - 1] + 1:index[ii]])
        tmp_list.append(y[index[ii] + 1:])
    return tmp_list


if __name__ == '__main__':
    repeat_set = set()
    with open('./sign_infer.result', 'w+', encoding='utf8') as fw:
        for filename in os.listdir('./'):
            if not filename.endswith('.json'):
                continue
            for idx, data in enumerate(load_data('./{}'.format(filename))):
                if 'all' in filename and idx < 50000:
                    continue

                data_js = json.loads(data)
                text = data_js['x']
                text_md5 = hashlib.md5(text.encode('utf8')).hexdigest()
                if text_md5 in repeat_set:
                    continue
                repeat_set.add(text_md5)
                tmp = []
                for xxx in cut_y(data_js['y']):
                    try:
                        tmp += convert_train2node_list(xxx, SIGN_LIST)
                    except Exception as e:
                        # print(data)
                        pass
                fw.write('{}\n'.format(json.dumps({"text": text, "infer_result": tmp}, ensure_ascii=False)))
