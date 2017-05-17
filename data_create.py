# -*-coding: utf-8 -*-

import pandas as pd
dataset = pd.read_csv("/Users/wuqiwei/Data/nba/NBA.csv", parse_dates=["Date"])#文件名的扩展名也需要给上
#dataset = pd.read_csv("/Users/wuqiwei/Data/nba/NBA_data.csv")
dataset.columns = ["Date","Visitor Team","VisitorPts","Home Team","HomePts","Score Type","OT?","Notes","HomeLastWin","VisitorLastWin"]
#print dataset.ix[:5]  #显示前5行   ix 显示每一行的数据情况  若给出具体值那就是在具体的那一行数据显示

dataset["HomeWin"] = dataset["VisitorPts"] < dataset["HomePts"]

y_true = dataset["HomeWin"].values

#print dataset.ix[:10]
#print  y_true[:4]

from collections import defaultdict

won_last = defaultdict(int)   #这个字典默认值为int类型，{key:0}


for index,row in dataset.iterrows(): # 遍历数据集的 index是行号  row是行信息
    #print row["Home Team"]   #给出那一列的所有数据，也就是给出Home Team列的所有球队
    home_team = row["Home Team"]  #字典的键为球队
    visitor_team = row["Visitor Team"]
    #print home_team
    #print row  #给出每一行
    #print won_last[home_team]

    row["HomeLastWin"] = won_last[home_team]  #由于采用了默认字典，所以初始值都是0，也就是我们默认球队上一场都输
    row["VisitorLastWin"] = won_last[visitor_team]
    #print row
    #print index
    dataset.ix[index] = row #更新
    #print dataset.ix[index]

    won_last[home_team] = row["HomeWin"]  #该结果留到下次遇到该球队时使用
    won_last[visitor_team] = not row["HomeWin"]

#print dataset.ix[20:25]

