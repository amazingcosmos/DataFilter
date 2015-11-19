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

holiday_date = ['20140906', '20140907', '20140908', 
            '20141001', '20141002', '20141003', 
            '20141004', '20141005', '20141006', 
            '20141007', '20150101', '20150102', '20150103']

work_date = ['20150104'] 

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


def analyse_data_date(file_path_read): 
    lables = 'date,what_day,hour,holiday,weekend'
    # lables = 'date,what_day,hour,holiday,num'
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
                # date, num = line.strip().split(',')
                date = line.strip()
                hour = date[-2:]
                date = date[:-2]
                temp = date
                temp += ',' + my_filter.what_day(date) + ',' + hour
                if date in holiday:
                    temp += ',' + '1'
                else:
                    temp += ',' + '0'
                # temp += ',' + num 
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
            # date, num = line.strip().split(',')
            date = line.strip()
            hour = date[-2:]
            date = date[:-2]
            temp = date 
            temp += ',' + my_filter.what_day(date) + ',' + hour
            if date in holiday_date:
                temp += ',' + '1'
            else:
                temp += ',' + '0'
            # temp += ',' + num 
            fp_write.write(temp+'\n')
        fp_read.close()
        fp_write.close()


def analyse_data(file_path_read, task_type = 1): 
    weather_dict = data_dict('./weather-analysed.csv', 'date')
    # task_type = train is 1, test is 2
    if task_type != 1 and task_type != 2:
        print 'wrong task_type, please input 1 for train, 2 for test.\n'
        return -1
    if task_type == 1:
        labels = 'date,what_day,hour,holiday,weekend,weather,num'
    else:
        labels = 'date,what_day,hour,holiday,weekend,weather'
    
    if os.path.isdir(file_path_read):
        file_path_read = my_filter.walk_dir(file_path_read, 'txt')
    else:
        file_path_read = [file_path_read]

    for path_read in file_path_read:
        file_path_write = path_read[:path_read.rfind('.')]
        file_path_write += '-analyse.csv'

        fp_read = open(path_read, 'r')
        fp_write = open(file_path_write, 'w')
        fp_write.write(labels+'\n')
        for line in fp_read:
            write_line = ''
            write_dict = {}

            line = line.strip().split(',')
            date_hour = line[0] 
            write_dict['date'] = date_hour[:-2]
            if task_type == 1:
                write_dict['num'] = line[1]
            write_dict['hour'] = date_hour[-2:]
            write_dict['what_day'] = my_filter.what_day(write_dict['date'])
            if write_dict['date'] in holiday_date:
                write_dict['holiday'] = '1'
            else:
                write_dict['holiday'] = '0'
            if int(write_dict['what_day']) >= 6 and write_dict['date'] not in work_date :
                write_dict['weekend'] = '1'
            elif write_dict['date'] in holiday_date:
                write_dict['weekend'] = '1'
            else:
                write_dict['weekend'] = '0'
            write_dict['weather'] = weather_dict[write_dict['date']]['weather']

            label_list = labels.strip().split(',')
            for l in label_list:
                write_line += write_dict[l] + ','
            write_line = write_line[:-1]
            # delete the last ','
            fp_write.write(write_line+'\n')
        fp_read.close()
        fp_write.close()

"""
def analyse_data_bak(file_path_read, type = 1): 
    # type = train is 1, test is 2
    if type != 1 and type != 2:
        print 'wrong type, please input 1 for train, 2 for test.\n'
        return -1
    if type == 1:
        lables = 'date,what_day,hour,holiday,weekend,num'
    else:
        lables = 'date,what_day,hour,holiday,weekend'
    
    if os.path.isdir(file_path_read):
        file_path_read = my_filter.walk_dir(file_path_read, 'txt')
    else:
        file_path_read = [file_path_read]

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
                what_day = my_filter.what_day(date)
                temp += ',' + what_day
                temp += ',' + hour
                if date in holiday_date:
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
"""

def analyse_weather_data(file_path_read):
    file_path_write = file_path_read[:file_path_read.rfind('.')]
    file_path_write += '-analysed.csv'
    fp_read = open(file_path_read, 'r')
    fp_write = open(file_path_write, 'w')
    labels = 'date,weather'

    fp_write.write(labels+'\n')

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
            kind_expand = '1'
        else:
            kind_expand = '0'

        fp_write.write(date_expand+','+kind_expand+'\n')

    fp_read.close()
    fp_write.close()
    print 'finish weather data analyse\n'


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


def data_dict(file_path_read, key_word):
    my_dict = {}
    fp_read = open(file_path_read, 'r')
    labels = fp_read.readline()
    labels = labels.strip().split(',')
    key_index = labels.index(key_word)
    for line in fp_read:
        line = line.strip().split(',')
        word_index = 0
        my_dict[line[key_index]] = {}
        while word_index < len(line):
            if key_index != word_index:
                my_dict[line[key_index]][labels[word_index]] = line[word_index]
            word_index += 1

        # value = line[:key_index] + line[key_index + 1:]
        # temp = ''
        # for i in value:
        #     temp += i + ','
        # temp = temp[:-1]
        # my_dict[line[key_index]] = temp
    fp_read.close()
    print 'data dict anaysed\n'
    return my_dict


if __name__ == '__main__':
    # analyse_data('d:/tianchi/line10/line10/split_by_card_holiday')
    print 'my_analyse\n'
