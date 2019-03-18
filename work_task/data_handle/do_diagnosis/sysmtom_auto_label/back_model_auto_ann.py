# encoding:utf-8


from data_handle.do_diagnosis.sysmtom_auto_label.base import replace_punctuations, db_host
from data_handle.do_diagnosis.sysmtom_auto_label.model_auto_ann import auto_ann_model
from utils.pzp_utils import get_platform_collection

complete_set = set()


def back_auto_ann(task_name, configure_id):
    configure = get_platform_collection(db_host, 'ann_configure_relation').find_one(
        {'id': configure_id, 'deleted': 'N'}, {'_id': 0, 'deleted': 0}
    )
    configure_entities = [x.get('name') for x in configure.get("entities")]
    configure_relations = configure.get("relations")
    if not configure.get('auto_ann') or not configure.get('auto_ann').get('is_auto'):
        raise Exception("{}未开启自动标注".format(configure.get('name')))
    queue_name = "/{version}/{service}".format(
        service=configure.get('auto_ann').get('service'),
        version=configure.get('auto_ann').get('version')
    )
    vocab_collection_name = configure.get('vocab_collection')
    task_collection = get_platform_collection(db_host, task_name)
    i = 0
    # for data in task_collection.find({'status': {"$in": ["已创建", "已分配"]}, configure_id: {"$exists": False}}):
    try:
        for data in task_collection.find({'status': {"$in": ["已创建", "已分配"]}}):
            # for data in task_collection.find({'status': {"$in": ["已创建"]}}):
            if int(data['group']) < 507:
                continue
            try:
                text = replace_punctuations(data['chunks'][0]['chunk'][0]['chunk_text'])
                entities, relations = auto_ann_model(
                    text, configure_entities, configure_relations, vocab_collection_name, queue_name
                )
            except Exception as e:
                entities, relations = [], []
            if configure_id not in data:
                data[configure_id] = [{}]
            data[configure_id][0]['entities'] = entities
            data[configure_id][0]['relations'] = relations
            data[configure_id][0]['remarks'] = []
            data[configure_id][0]['text_tips'] = ""
            data[configure_id][0]['text'] = data['chunks'][0]['chunk'][0]['chunk_text']
            data[configure_id][0]['chunk_md5'] = data['chunks'][0]['chunk'][0]['md5']
            i += 1
            print(i, data['group'], data['indexing'])
            complete_set.add(data['group'])
            task_collection.update_one(
                {"_id": data["_id"], "status": {"$in": ["已创建", "已分配"]}},
                {"$set": {configure_id: data[configure_id]}}
            )
            # task_collection.update_one(
            #     {"_id": data["_id"]},
            #     {"$set": {configure_id: data[configure_id]}}
            # )
    except Exception:
        print(i, data['group'], data['indexing'])
        print(complete_set)


if __name__ == '__main__':
    _configure_id = '1191cf9a-e2fd-11e8-bd36-6a00038f2a30'
    # _task_name = 'task_relation_TGJCGX_4'
    _task_name = 'task_relation_CWZZJGH_14'
    back_auto_ann(_task_name, _configure_id)
