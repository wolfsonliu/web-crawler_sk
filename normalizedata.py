# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 09:23:59 2018

@author: lib
"""
import pandas as pd
import numpy as np
import csv

with open('./data/good.csv', 'wb') as good:
    with open('./data/bad.csv', 'wb') as bad:
        with open('./data/sk.csv', 'rb') as f:
            for line in f:
                if len(line.decode('utf-8').split(',')) != 21:
                    bad.write(line)
                else:
                    good.write(line)

tmp = pd.read_csv('./data/good.csv', header=None, quoting=csv.QUOTE_ALL)
tmp.columns = [
    'num', '项目批准号','项目类别','学科分类','项目名称','立项时间','项目负责人','专业职务','工作单位','单位类别','所在省区市',
    '所属系统','成果名称','成果形式','成果等级','结项时间','结项证书号','出版社','出版时间','作者','获奖情况'
]
tmp.sort_values('项目批准号').to_csv('./data/good2.csv', index=False, encoding='utf-8')

tmp.loc[np.logical_not(tmp['项目类别'].isnull())].to_csv('./data/good2_rmempty', index=False, encoding='utf-8')

tmp2 = pd.read_csv('./data/good2_rmempty.csv', header=0, quoting=csv.QUOTE_ALL)

tmp2.loc[tmp2['项目批准号'].duplicated(keep=False)].sort_values('项目批准号').to_csv('./data/good2_rmempty_dup.csv', index=False, encoding='utf-8')

tmp3 = pd.read_csv('./data/good2_rmempty_g.csv', header=0, quoting=csv.QUOTE_ALL)

tmp3.sort_values('num').to_csv('./data/sheke.csv', index=False, encoding='utf-8')