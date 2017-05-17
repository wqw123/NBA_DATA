# -*-coding: utf-8 -*-

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=14)
from data_create import *
from sklearn.cross_validation import cross_val_score
import numpy as np

X_previouswins = dataset[["HomeLastWin", "VisitorLastWin"]].values
scores = cross_val_score(clf,X_previouswins,y_true,scoring="accuracy")
#print "Accuracy:{0:.1f}%".format(np.mean(scores)*100)
standings = pd.read_csv("/users/wuqiwei/Data/NBA/standings.csv",skiprows=[0,]) #不读取第0行  skiprow：传入一个列表，列表里面的元素代表着要显示跳过的行数（内存中数据集不带这几行）
#print standings

dataset["HomeTeamRankHigher"]=0
for index,row in dataset.iterrows():   #遍历数据集的行号和行情况
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    if home_team == "New Orleans Pelicans":
        home_team = "New Orleans Hornets"
    elif visitor_team == "New Orleans Pelicans":
        visitor_team = "New Orleans Hornets"

    home_rank = standings[standings["Team"] == home_team]["Rk"].values[0]  #取主队的上赛季rank   #这里也是对于数据集的部分抽取
    visitor_rank = standings[standings["Team"]==visitor_team]["Rk"].values[0] #取客队的上赛季rank
    #print home_rank     #注意前面的standings数据集 skiprow的时候，Team的条目我们不能给它省略掉

    row["HomeTeamRankHigher"] = int(home_rank > visitor_rank)
    dataset.ix[index] = row

X_homehigher = dataset[["HomeLastWin","VisitorLastWin","HomeTeamRankHigher"]].values  #用来训练分类器的每个球队的三个特征

clf = DecisionTreeClassifier(random_state=14)   #实例化决策树分类器对象   注意状态参数，一般来说随机种子我们就选14吧
scores = cross_val_score(clf,X_homehigher,y_true,scoring="accuracy")
#print "Accuracy: {0:.1f}%".format(np.mean(scores)*100)



#为了使得决策树的分类效果更佳，我们需要再向决策树中加入更有用的特征信息 （信息增益）

last_match_winner = defaultdict(int)
dataset["HomeTeamWonLast"] = 0

for index,row in dataset.iterrows():
    home_team = row["Home Team"]  #从数据集中得到所有球队
    visitor_team = row["Visitor Team"]

    teams = tuple(sorted([home_team,visitor_team]))  #元组是不可变的
    row["HomeTeamWonLast"] =1 if last_match_winner[teams] == row["Home Team"] else 0
    dataset.ix[index] = row   #其实就是对这一行新的条目进行更新

    winner = row["Home Team"] if row["HomeWin"] else row["Visitor Team"]
    last_match_winner[teams] = winner

X_lastwinner = dataset[["HomeTeamRankHigher","HomeTeamWonLast"]].values
clf = DecisionTreeClassifier(random_state=14)

scores = cross_val_score(clf,X_lastwinner,y_true,scoring="accuracy")  #使用决策树分类器进行交叉验证

print scores
#print np.mean(scores)*100
