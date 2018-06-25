# -*- coding:utf-8 -*-
import os


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize, 2)


if __name__ == '__main__':
    file_path_dir = "./data/code_notin_hs300/"
    for file_path in os.listdir(file_path_dir):
        if get_FileSize(os.path.join(file_path_dir, file_path)) < 2:
            print(file_path)
            os.remove(os.path.join(file_path_dir, file_path))