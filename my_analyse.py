#!/usr/bin/python
#-*- coding:utf-8 -*-

import my_filter
import chardet
import os
import ConfigParser
import types
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

holiday = ['20140906', '20140907', '20140908', 
            '20141001', '20141002', '20141003', 
            '20141004', '20141005', '20141006', 
            '20141007', '20150101', '20150102', '20150103']

def make_result(file_path_read, line_name):
    fp_read = open('./date-7.txt', 'r')
    date_list = []
    hour_list = []
    for line in fp_read:
        line = line.strip()
        date_list.append(line[:8])
        hour_list.append(line[8:])
    fp_read.close()
    
    file_path_write = file_path_read[:file_path_read.rfind('.')]
    file_path_write += '-full.txt'
    fp_read = open(file_path_read, 'r')
    fp_write = open(file_path_write, 'w')
    i = 0
    for line in fp_read:
        
        num = int(float(line))
        if num < 0:
            num = 0
        temp = line_name + ',' + date_list[i] + ',' + hour_list[i] + ',' + str(num)
        fp_write.write(temp+'\n')
        i += 1
    fp_read.close()
    fp_write.close()


def analyse_data(file_path_read): 
    # lables = 'what_day,hour,holiday'
    lables = 'date,what_day,hour,holiday,num'
    if os.path.isdir(file_path_read):
        file_path_read = my_filter.walk_dir(file_path_read, 'txt')

    if type(file_path_read) == types.ListType:
        for path_read in file_path_read:
            file_path_write = path_read[:path_read.rfind('.')]
            file_path_write += '-analyse.csv'

            fp_read = open(path_read, 'r')
            fp_write = open(file_path_write, 'w')
            fp_write.write(lables+'\n')
            for line in fp_read:
                date, num = line.strip().split(',')
                # date = line.strip()
                hour = date[-2:]
                date = date[:-2]
                temp = date
                temp += ',' + my_filter.what_day(date) + ',' + hour
                if date in holiday:
                    temp += ',' + '1'
                else:
                    temp += ',' + '0'
                temp += ',' + num 
                fp_write.write(temp+'\n')
            fp_read.close()
            fp_write.close()
    else:
        file_path_write = file_path_read[:file_path_read.rfind('.')]
        file_path_write += '-analyse.csv'

        fp_read = open(file_path_read, 'r')
        fp_write = open(file_path_write, 'w')
        fp_write.write(lables+'\n')
        for line in fp_read:
            date, num = line.strip().split(',')
            # date = line.strip()
            hour = date[-2:]
            date = date[:-2]
            temp = date 
            temp += ',' + my_filter.what_day(date) + ',' + hour
            if date in holiday:
                temp += ',' + '1'
            else:
                temp += ',' + '0'
            temp += ',' + num 
            fp_write.write(temp+'\n')
        fp_read.close()
        fp_write.close()


def analyse_weather_data(file_path_read):
    file_path_write = file_path_read[:file_path_read.rfind('.')]
    file_path_write += '-analysed.txt'
    fp_read = open(file_path_read, 'r')
    fp_write = open(file_path_write, 'w')

    for line in fp_read:
        if '\n' == line:
            continue
        line = line.strip().split(',')
        if len(line) != 4:
            continue
        date, kind, tem, wind = line

        date = date.split('/')
        date_expand = date[0]
        if int(date[1]) < 10:
            date_expand += '0'
        date_expand += date[1]
        if int(date[2]) < 10:
            date_expand += '0'
        date_expand += date[2]

        # kind = kind.split('/')
        if '雨' in kind:
            kind_expand = 'rain'
        else:
            kind_expand = 'norain'

        fp_write.write(date_expand+','+kind_expand+'\n')

    fp_read.close()
    fp_write.close()


def file_join(file_from, file_to, key_word):
    if os.path.isdir(file_to):
        file_to = my_filter.walk_dir(file_to, 'csv')

    fp_from = open(file_from, 'r')
    lable_from = fp_from.readline().strip().split(',')
    index_from = lable_from.index(key_word)
    dict_from = {}
    for line in fp_from:
        line = line.strip().split(',')
        temp = line[:index_from] + line[index_from+1:]
        value = ''
        for i in temp:
            value += i + ','
        value = value[:-1]
        dict_from[line[index_from]] = value

    if type(file_to) == types.ListType:
        for f in file_to:
            fp_to = open(f, 'r')
            lable_to = fp_to.readline().strip().split(',')
            index_to = lable_to.index(key_word)

            file_new = f[:f.rfind('.')] + '-joined.csv'
            fp_write = open(file_new, 'w')
            lable_new = lable_to
            for word in lable_from:
                if key_word != word:
                    lable_new.append(word)
            value = ''
            for i in lable_new:
                value += i + ','
            value = value[:-1]
            fp_write.write(value+'\n')

            for line in fp_to:
                temp = line.strip().split(',')
                line_new = line.strip() + ',' + dict_from[temp[index_to]]
                fp_write.write(line_new+'\n')
    else:
        fp_to = open(file_to, 'r')
        lable_to = fp_to.readline().strip().split(',')
        index_to = lable_to.index(key_word)

        file_new = file_to[:file_to.rfind('.')] + '-joined.csv'
        fp_write = open(file_new, 'w')
        lable_new = lable_to
        for word in lable_from:
            if key_word != word:
                lable_new.append(word)
        value = ''
        for i in lable_new:
            value += i + ','
        value = value[:-1]
        fp_write.write(value+'\n')

        for line in fp_to:
            temp = line.strip().split(',')
            line_new = line.strip() + ',' + dict_from[temp[index_to]]
            fp_write.write(line_new+'\n')

    


if __name__ == '__main__':
    # analyse_data('d:/tianchi/line10/line10/split_by_card_holiday')
    print 'my_analyse\n'
