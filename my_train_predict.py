#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import pandas as pd
import numpy as np 
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
feature_cols = ['what_day', 'hour', 'holiday']
# y_test = ['2015010106', '2015010107', '2015010108', '2015010109', '2015010110', '2015010111', '2015010112', '2015010113', '2015010114', '2015010115', '2015010116', '2015010117', '2015010118', '2015010119', '2015010120', '2015010121', '2015010206', '2015010207', '2015010208', '2015010209', '2015010210', '2015010211', '2015010212', '2015010213', '2015010214', '2015010215', '2015010216', '2015010217', '2015010218', '2015010219', '2015010220', '2015010221', '2015010306', '2015010307', '2015010308', '2015010309', '2015010310', '2015010311', '2015010312', '2015010313', '2015010314', '2015010315', '2015010316', '2015010317', '2015010318', '2015010319', '2015010320', '2015010321', '2015010406', '2015010407', '2015010408', '2015010409', '2015010410', '2015010411', '2015010412', '2015010413', '2015010414', '2015010415', '2015010416', '2015010417', '2015010418', '2015010419', '2015010420', '2015010421', '2015010506', '2015010507', '2015010508', '2015010509', '2015010510', '2015010511', '2015010512', '2015010513', '2015010514', '2015010515', '2015010516', '2015010517', '2015010518', '2015010519', '2015010520', '2015010521', '2015010606', '2015010607', '2015010608', '2015010609', '2015010610', '2015010611', '2015010612', '2015010613', '2015010614', '2015010615', '2015010616', '2015010617', '2015010618', '2015010619', '2015010620', '2015010621', '2015010706', '2015010707', '2015010708', '2015010709', '2015010710', '2015010711', '2015010712', '2015010713', '2015010714', '2015010715', '2015010716', '2015010717', '2015010718', '2015010719', '2015010720', '2015010721']

if __name__ == '__main__':
    file_path_read = raw_input(prompt['file_path_read'])
    df_test = pd.read_csv('./date-7-analyse.csv')
    X_test = df_test[feature_cols]
    print X_test.head()

    if os.path.isdir(file_path_read):
        file_path_read = my_filter.walk_dir(file_path_read, 'csv')
    if type(file_path_read) == types.ListType:
        for path_read in file_path_read:
            file_path_write = path_read[:path_read.rfind('.')]
            file_path_write += '-predict.txt'

            df = pd.read_csv(path_read)
            X_train = df[feature_cols]
            print X_train.head()
            y_train = df.num
            print y_train.head()
            linreg = LinearRegression()
            linreg.fit(X_train, y_train)
            y_pred = linreg.predict(X_test)
            y_pred_list = y_pred.tolist()

            fp_write = open(file_path_write, 'w')
            for line in y_pred_list:
                fp_write.write(str(line)+'\n')
            fp_write.close()
            print 'done'
    else:
        file_path_write = file_path_read[:file_path_read.rfind('.')]
        file_path_write += '-predict.txt'

        df = pd.read_csv(file_path_read)
        X_train = df[feature_cols]
        print X_train.head()
        y_train = df.num
        print y_train.head()
        linreg = LinearRegression()
        linreg.fit(X_train, y_train)
        y_pred = linreg.predict(X_test)
        y_pred_list = y_pred.tolist()

        fp_write = open(file_path_write, 'w')
        for line in y_pred_list:
            fp_write.write(str(line)+'\n')
        fp_write.close()
        print 'done'





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