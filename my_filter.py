#!/usr/bin/python
#-*- coding:utf-8 -*-

import chardet
import os
import ConfigParser
import types
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cf = ConfigParser.ConfigParser()
cf.read('./my_filter.ini')

holiday = ['20140906', '20140907', '20140908', 
            '20141001', '20141002', '20141003', 
            '20141004', '20141005', '20141006', 
            '20141007', '20150101', '20150102', '20150103']

prompt = {'choose' : 'Choose function:\
            \n0:exit.\
            \n1:save the first n lines data to file.\
            \n2:save the data between dates.\
            \n3:save the data by some key word.\
            \n4:convert the txt file into csv file.\
            \n5:count the date.\n', 
            'save_k_line' : 'Enter the number of lines you want to save: ',
            'choose_date_from' : 'Enter the start date yyyymmddhh(e.g. 2014080108): ',
            'choose_date_to' : 'Enter the end date yyyymmddhh(e.g. 2014123124): ',
            'convert' : 'Convert txt to csv?(yes:1, no:0): ',
            'keyword' : 'Enter the keyword type(e.g. line): ',
            'file_path_read' : 'Enther the file path you want to handle: ',
            'index' : 'Enter the index you want to count: '}
# keyword = dict(cf.items('keyword'))


def change_file_charset(file_path, file_type, charset):
    """change file type

    txt file into other type of file like .csv

    Args:
        file_path: the txt file path
        file_type: the file type you want to convert to(mostly .csv)
        charset: the charset convert to

    Returns:
        None
    """
    output_file_name = file_path[:file_path.rfind('.')] + file_type
    f = open(file_path)
    s = f.read()
    f.close()

    if file_path == output_file_name or output_file_name == "":
        remove(file_path)

    old_charset = chardet.detect(s)['encoding']
    u = s.decode(old_charset)

    if output_file_name == "":
        output_file_name = file_path
    f = open(output_file_name, 'w')
    s = u.encode(charset)
    f.write(s)
    f.close()
    print('convert done!')


def save_by_line(file_path_read, file_path_write, k):
    """save the first k lines of file

    the output file will be named by 'source_file_name-saveklines.txt'

    Args:
        file_path_read: the source file path
        file_path_write: the output file path 
        k: the lines you want to save

    Returns:
        None
    """
    fp_read = open(file_path_read, 'r')
    fp_write = open(file_path_write, 'w')
    i = 1
    for line in fp_read:
        fp_write.write(line)
        i = i+1
        if i > k:
            break
    fp_read.close()
    fp_write.close()
    print('save k lines done!')


def save_by_date(date_from, date_to, file_path_read, file_path_write):
    """save the data between some dates

    the output file will be named by 'source_file_name-date_from-date_to.txt'

    Args:
        date_from: the begin date
        date_to: the end date
        file_path_read: the source file path
        file_path_write: the output file path

    Returns:
        None 
    """
    fp_read = open(file_path_read, 'r')
    fp_write = open(file_path_write, 'w')
    for line in fp_read:
        date = line.split(',')[5]
        if date >= date_from and date <= date_to:
            fp_write.write(line)
    fp_read.close()
    fp_write.close()
    print('choose date done!')


def save_by_keyword(key_index, key_word, file_path_read, file_path_write):
    """save the data by keyword

    first write you own keyword into the filter.ini file!!!
    the output file will be named by 'source_file_name-keyword.txt'

    Args:
        key_index: the index of keyword
        key_word: the keyword 
        file_path_read: the source file path
        file_path_write: the output file path

    Returns:
        None 
    """
    fp_read = open(file_path_read, 'r')
    fp_write = open(file_path_write, 'w')
    if '2014' in key_word:
        file_path_write2 = file_path_write[:file_path_write.rfind('.')]
        file_path_write2 += '0.txt'
        fp_write2 = open(file_path_write2, 'w')
        for line in fp_read:
            word = line.strip().split(',')[key_index]
            word = word[:8]
            # print chardet.detect(word)['encoding'], chardet.detect(key_word)['encoding']
            # if word == key_word:
            if word in key_word:
                fp_write.write(line)
            else:
                fp_write2.write(line)
        fp_read.close()
        fp_write.close()
        fp_write2.close()
    else:
        for line in fp_read:
            word = line.strip().split(',')[key_index]
            # print chardet.detect(word)['encoding'], chardet.detect(key_word)['encoding']
            # if word == key_word:
            if word in key_word:
                fp_write.write(line)
        fp_read.close()
        fp_write.close()


def convert(file_name, file_type, charset):
    while(1):
        choise = raw_input(prompt['convert'])
        if choise == '1':
            change_file_charset(file_name, file_type, charset)
            break
        elif choise == '0':
            break
        else:
            continue


def data_counter(file_path_read, my_dict, key_index):
    fp_read = open(file_path_read, 'r')
    for line in fp_read:
        key = line.strip().split(',')[key_index]
        if key not in my_dict:
            my_dict[key] = 1
        else:
            my_dict[key] += 1
    return my_dict


def gen_date_dict_bak(date_start, date_end):
    y_start = int(date_start[:4])
    m_start = int(date_start[4:6])
    d_start = int(date_start[6:8])
    h_start = int(date_start[8:])
    y_end = int(date_end[:4])
    m_end = int(date_end[4:6])
    d_end = int(date_end[6:8])
    h_end = int(date_end[8:])

    my_dict = {}
    yyyy = y_start
    while yyyy <= y_end:
        mm = 8
        while mm <= 12:
            date_m = str(yyyy)
            if mm < 10:
                date_m += '0'
            date_m += str(mm)
            dd = 1
            while dd <= 31:
                if mm % 2 == 1 and dd == 31:
                    break
                date_d = date_m 
                if dd < 10:
                    date_d += '0'
                date_d += str(dd)
                hh = 6
                while hh <= 21:
                    date_h = date_d 
                    if hh < 10:
                        date_h += '0'
                    date_h += str(hh)
                    print date_h
                    my_dict[date_h] = 0
                    hh += 1
                dd += 1
            mm += 1
        yyyy += 1
    return my_dict


def gen_date_dict():
    my_dict = []
    date_y = '2015'
    mm = 1
    while mm <= 1:
        date_m = date_y
        if mm < 10:
            date_m += '0'
        date_m += str(mm)
        dd = 1
        while dd <= 7:
            if mm % 2 == 1 and dd == 31:
                break
            date_d = date_m 
            if dd < 10:
                date_d += '0'
            date_d += str(dd)
            hh = 6
            while hh <= 21:
                date_h = date_d 
                if hh < 10:
                    date_h += '0'
                date_h += str(hh)
                # my_dict[date_h] = 0
                my_dict.append(date_h)
                hh += 1
            dd += 1
        mm += 1
    return my_dict


def what_day(yyyymmdd):
    # if yyyymmdd == '20140928' or yyyymmdd == '20141011':
    #     return False
    c=int(yyyymmdd[:2])
    y=int(yyyymmdd[2:4])
    m=int(yyyymmdd[4:6])
    d=int(yyyymmdd[6:8])
    #print(c,y,m,d)

    flag=0
    if (m==2 or d==31):
        if d==31 and (m in (4,6,9,11)):
            flag=1
        if m==2 and (d>29 or (d==29 and (y%4 !=0 or (y==0 and c%4 !=0)))):
            flag=1

    if m==1 or m==2:
        m=m+12
        y=y-1
        if y<0:
            y=99
            c=c-1

    w=y+(y//4)+(c//4)-2*c+26*(m+1)//10+d-1
    w = w % 7
    if w == 0:
        w = 7
    return str(w)
    # if w == 0 or w == 6:
    #     return True
    # else:
    #     return False


def walk_dir(dir_path, file_type):
    file_names = []
    if os.path.isdir(dir_path):
        for parent, dirnames, filenames in os.walk(dir_path):
            for file_name in filenames:
                if file_name.strip().split('.')[-1] == file_type:
                    temp = parent+'/'+file_name
                    file_names.append(temp)
    return file_names


def change_file_extensions(dir_path, old_type, new_type):
    file_names = walk_dir(dir_path, old_type)
    for file_name in file_names:
        old_name = file_name
        new_name = old_name[:old_name.rfind('.')]
        new_name += '.' + new_type
        os.rename(old_name, new_name)


if __name__ == '__main__':
    while(1):
        print('\n')
        func_num = raw_input(prompt['choose'])
        if func_num == '0':
            break

        elif func_num == '1':
            file_path_read = raw_input(prompt['file_path_read'])
            file_path_write = file_path_read[:file_path_read.rfind('.')]
            k = int(raw_input(prompt['save_k_line']))
            file_txt = file_path_write+'-save'+str(k)+'lines.txt'
            save_by_line(file_path_read, file_txt, k)

        elif func_num == '2':
            file_path_read = raw_input(prompt['file_path_read'])
            file_path_write = file_path_read[:file_path_read.rfind('.')]
            date_from = raw_input(prompt['choose_date_from'])
            date_to = raw_input(prompt['choose_date_to'])
            file_txt = file_path_write+'-'+date_from+'-'+date_to+'.txt'
            save_by_date(date_from, date_to, file_path_read, file_txt)

        elif func_num == '3':
            keyword = dict(cf.items('key_word'))
            keyindex = dict(cf.items('key_index'))
            filename = dict(cf.items('file_name'))
            file_path_read = raw_input(prompt['file_path_read'])
            file_path_write = file_path_read[:file_path_read.rfind('.')]
            key_type = raw_input(prompt['keyword'])           
            key_words = list(eval(keyword[key_type]))
            file_names = list(eval(filename[key_type]))
            # key_index = int(key_words[0])
            key_index = int(keyindex[key_type])
            # key_words = key_words[1:]
            
            for key_word in key_words:
                file_name = file_names[key_words.index(key_word)]
                file_txt = file_path_write+'-'+file_name+'.txt'
                file_txt.encode('utf-8')
                save_by_keyword(key_index, key_word, file_path_read, file_txt)

        elif func_num == '4':
            file_path_read = raw_input(prompt['file_path_read'])
            convert(file_path_read, '.csv', 'gb2312')

        elif func_num == '5':
            file_path_read = raw_input(prompt['file_path_read'])
            # key_index = int(raw_input(prompt['index']))
            key_index = 5

            if os.path.isdir(file_path_read):
                file_path_read = walk_dir(file_path_read, 'txt')
            else:
                file_path_read = [file_path_read]

            for path_read in file_path_read:
                file_path_write = path_read[:path_read.rfind('.')]
                file_path_write += '-date.txt'
                my_dict = gen_date_dict()
                my_dict = data_counter(path_read, my_dict, key_index)
                fp = open(file_path_write, 'w')
                for key in my_dict:
                    fp.write(str(key)+','+str(my_dict[key])+'\n')
                fp.close()
        else:
            continue
