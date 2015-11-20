#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import pandas as pd
import numpy as np 
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import my_filter
import chardet
import ConfigParser
import types
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# import seaborn as sns 
# import matplotlib as inline

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
# feature_cols = ['weekend', 'hour', 'holiday', 'weather']
feature_cols = ['weekend', 'weather', 'temp_high', 'temp_low', 'temp_mean', 'temp_predict']
if __name__ == '__main__':
    file_path_read = raw_input(prompt['file_path_read'])
    line_num = int(raw_input('what the line number: '))
    df_test = pd.read_csv('./date-7-analysed.csv')
    # X_test = df_test[feature_cols]
    # X_test = preprocessing.normalize(X_test)
    # print X_test.head()

    if os.path.isdir(file_path_read):
        file_path_read = my_filter.walk_dir(file_path_read, 'csv')
    else:
        file_path_read = [file_path_read]
    result = {}
    i = 6
    while i <= 21:
        result[i] = []
        i += 1
    for path_read in file_path_read:
        df = pd.read_csv(path_read)
        scaler = preprocessing.StandardScaler().fit(df[feature_cols])
        i = 6
        while i <= 21:
            df_hour = df[df.hour == i][df.date > 20141030]
            X_train = df_hour[feature_cols]
            X_train = scaler.transform(X_train)
            # print X_train.head()
            y_train = df_hour.num
            X_test = df_test[df_test.hour == i][feature_cols]
            X_test = scaler.transform(X_test)

            # print y_train.head()
            linreg = LinearRegression()
            linreg.fit(X_train, y_train)
            # print linreg.intercept_
            # print linreg.coef_
            y_pred = linreg.predict(X_test)
            y_pred_list = y_pred.tolist()
            if file_path_read.index(path_read) == 0:
                for y in y_pred_list:
                    result[i].append(int(y))
            else:
                j = 0
                for y in y_pred_list:
                    result[i][j] += int(y) 
                    j += 1
            print 'done'
            i += 1
    file_path_write = 'predict' + str(line_num) + '.txt'
    fp_write = open(file_path_write, 'w')
    my_date = df_test.date.tolist()
    my_hour = df_test.hour.tolist()
    # print zip(my_date, my_hour)
    i = 0
    for date in my_date:
        value = '线路' + str(line_num) + ','
        value += str(my_date[i]) + ','
        value += str(my_hour[i]) + ','

        num = int(result[int(my_hour[i])][i/16])
        if my_hour[i] == 12:
            if line_num == 10:
                if my_date[i] <= 20150103:
                    num += 740
                else:
                    num += 3000
            if line_num == 15:
                if my_date[i] <= 20150103:
                    num += 370
                else:
                    num += 1500

        value += str(num)
        fp_write.write(str(value)+'\n')
        i += 1
    fp_write.close()




    # df = pd.read_csv('../line10/line10/train_data_filtered-line10-student-date-analyse.csv')
    # print df.head()
    # df.info()
    # print df.shape


    # # %matplotlib inline
    # # sns.pairplot(df, x_vars=['what_day', 'hour', 'holiday'], y_vars = 'num',
    # #                 size = 7, aspect = 0.8)

    # feature_cols = ['what_day', 'hour', 'holiday']
    # X = df[feature_cols]
    # print X.head()

    # y = df.num 
    # print y.head()

    # X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1)
    # print X_train.shape
    # print y_train.shape
    # print X_test.shape
    # print y_test.shape

    # linreg = LinearRegression()

    # linreg.fit(X_train, y_train)

    # print linreg.intercept_
    # print linreg.coef_

    # y_pred = linreg.predict(X_test)
    # print y_pred

    # print "MAE:",metrics.mean_absolute_error(y_test, y_pred)

    # # s = cross_val_score(linreg, X_test, y_test, cv=5)
    # # print s
    # print 'lalala'