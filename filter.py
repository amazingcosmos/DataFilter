#!/usr/bin/python
#-*- coding:utf-8 -*-

import chardet
import os
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cf = ConfigParser.ConfigParser()
cf.read('./filter.ini')


prompt = {'choose' : 'Choose function:\
            \n0:exit.\
            \n1:save the first n lines data to file.\
            \n2:save the data between dates.\
            \n3:save the data by some key word.\
            \n4:convert the txt file into csv file.\n', 
            'save_k_line' : 'Enter the number of lines you want to save: ',
            'choose_date_from' : 'Enter the start date(e.g. 20140801): ',
            'choose_date_to' : 'Enter the end date(e.g. 20141231): ',
            'convert' : 'Convert txt to csv?(yes:1, no:0): ',
            'keyword' : 'Enter the keyword type(e.g. line): ',
            'file_path_read' : 'Enther the file path you want to handle: '}
keyword = dict(cf.items('keyword'))

def change_file_charset(file_name, file_type, charset):
    output_file_name = file_name[:file_name.rfind('.')] + file_type
    f = open(file_name)
    s = f.read()
    f.close()

    if file_name == output_file_name or output_file_name == "":
        remove(file_name)

    old_charset = chardet.detect(s)['encoding']
    u = s.decode(old_charset)

    if output_file_name == "":
        output_file_name = file_name
    f = open(output_file_name, 'w')
    s = u.encode(charset)
    f.write(s)
    f.close()
    print('convert done!')


def save_by_line(file_path_read, file_path_write, k):
    fp_read = open(file_path_read, 'r')
    fp_write = open(file_path_write, 'w')
    i = 1
    for line in fp_read:
        fp_write.write(line)
        i = i+1
        if i > max_line:
            break
    fp_read.close()
    fp_write.close()
    print('save k lines done!')


def save_by_date(date_from, date_to, file_path_read, file_path_write):
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
    fp_read = open(file_path_read, 'r')
    fp_write = open(file_path_write, 'w')
    for line in fp_read:
        word = line.split(',')[key_index]
        if word == key_word:
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


if __name__ == '__main__':
    # os.system('pip install chardet')
    # file_path_read = raw_input(prompt['file_path_read'])
    # file_path_read = '../origin/gd_train_data.txt'
    # file_path_read = '../train_data_filtered.txt'
    # file_path_write = '../train_data_filtered'
    # file_path_write = file_path_read[:file_path_read.rfind('.')]
    while(1):
        print('\n')
        func_num = raw_input(prompt['choose'])
        # file_path_read = raw_input(prompt['file_path_read'])
        # file_path_write = file_path_read[:file_path_read.rfind('.')]
        if func_num == '0':
            break

        elif func_num == '1':
            file_path_read = raw_input(prompt['file_path_read'])
            file_path_write = file_path_read[:file_path_read.rfind('.')]
            k = int(raw_input(prompt['save_k_line']))
            file_txt = file_path_write+'-save'+k+'lines.txt'
            save_by_line(file_path_read, file_txt, k)
            # convert(file_path_write, '.csv', 'gb2312')

        elif func_num == '2':
            file_path_read = raw_input(prompt['file_path_read'])
            file_path_write = file_path_read[:file_path_read.rfind('.')]
            date_from = raw_input(prompt['choose_date_from'])
            date_to = raw_input(prompt['choose_date_to'])
            file_txt = file_path_write+'-'+date_from+'-'+date_to+'.txt'
            save_by_date(date_from, date_to, file_path_read, file_txt)
            # convert(file_txt, '.csv', 'gb2312')

        elif func_num == '3':
            file_path_read = raw_input(prompt['file_path_read'])
            file_path_write = file_path_read[:file_path_read.rfind('.')]
            key_type = raw_input(prompt['keyword'])           
            key_words = list(eval(keyword[key_type]))
            key_index = int(key_words[0])
            key_words = key_words[1:]
            
            for key_word in key_words:
                file_txt = file_path_write+'-'+key_word+'.txt'
                file_txt.encode('utf-8')
                save_by_keyword(key_index, key_word, file_path_read, file_txt)

        elif func_num == '4':
            file_path_read = raw_input(prompt['file_path_read'])
            convert(file_path_read, '.csv', 'gb2312')


        else:
            continue
