# encoding=utf-8
import codecs
import collections
import json

import xlwt


def load_data(file_path):
    with codecs.open(file_path, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        while line:
            yield line
            line = f.readline().strip()


if __name__ == '__main__':
    y1 = collections.defaultdict(lambda: 0)
    y2 = collections.defaultdict(lambda: 0)
    for data in load_data('./sign_infer.result'):
        try:

            data_js = json.loads(data, encoding='utf8')
            for xx in data_js['infer_result']:
                label, word, att = xx['labelId'], xx['word'], xx['att']
                if label == u'检查实体' and not att:
                    y1[word] += 1
                if label == u'实体结果' and not att:
                    y2[word] += 1
                pass
        except Exception as e:
            continue
    print(y1)
    print(y2)

    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet(u"检查实体统计", cell_overwrite_ok=True)
    worksheet.write(0, 0, label=u"检查实体")
    worksheet.write(0, 1, label=u'频次')
    j = 1
    for _, freq in y1.items():
        worksheet.write(j, 0, label=_)
        worksheet.write(j, 1, label=freq)
        j += 1
    workbook.save(u'./检查实体统计结果2.xls')

    workbook2 = xlwt.Workbook(encoding='utf8')
    worksheet2 = workbook2.add_sheet(u"实体结果统计", cell_overwrite_ok=True)
    worksheet2.write(0, 0, label=u"实体结果")
    worksheet2.write(0, 1, label=u'频次')
    j = 1
    for __, freq in y2.items():
        worksheet2.write(j, 0, label=__)
        worksheet2.write(j, 1, label=freq)
        j += 1
    workbook2.save(u'./实体结果统计结果2.xls')
