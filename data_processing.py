# -*- coding: utf-8 -*-

from sklearn.preprocessing import LabelEncoder  #将字符串类型特征转换为整型
from data_create import *
import numpy as np


#sklearn的决策树，要求特征数值化,特征不能使用 "高" "矮"，而应该转化为 0， 1   所以使用LabelEncoder

encoding = LabelEncoder()

encoding.fit(dataset["Home Team"].values)   #将所有主队名称转换为数字，比方说公牛队就是用数字 12

home_teams = encoding.transform(dataset["Home Team"].values)
visitor_teams =  encoding.transform(dataset["Visitor Team"].values)

X_teams = np.vstack([home_teams,visitor_teams]).T  #将两个向量组成矩阵

#print  X_teams

from sklearn.preprocessing import OneHotEncoder   #再将特征由数字转化为二进制

onehot = OneHotEncoder()
X_teams_expanded = onehot.fit_transform(X_teams).todense()

