# encoding=utf-8
import os

if __name__ == '__main__':
    data_dir = '/data/share/all_data/filter_corpus'
    output_dir = '/home/zhangpei/emrs/600'
    for dir_name in os.listdir(data_dir):
        _dir = os.path.join(data_dir, dir_name)
        odir = os.path.join(output_dir, dir_name)
        if not os.path.exists(odir):
            os.makedirs(odir)
        for filename in os.listdir(_dir):
            os.system('head -600 {} > {}'.format( os.path.join(_dir, filename),  os.path.join(odir, filename)))
