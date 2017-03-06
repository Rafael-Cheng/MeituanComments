#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import jieba


reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    prename = 'File'
    with open('mydict.txt', 'r') as file_name:
        jieba.load_userdict(file_name)
        index = 1
        key_frequency = {}
        while index < 180:
            filename = prename + str(index)
            with open(filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if len(line) > 17:
                        line = line.strip()
                        seg_list = jieba.cut(line, cut_all=True, HMM=False)
                        for key in seg_list:
                            if len(key) == 0:
                                continue
                            if False == key_frequency.has_key(key):
                                key_frequency[key] = 1
                            else:
                                key_frequency[key] += 1
            index += 1
    sorteddic = sorted(key_frequency.items(), key=lambda x:x[1], reverse=True)
    for i in sorteddic:
        print i[0] + ': ' + str(i[1])
