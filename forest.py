# -*-coding: utf-8 -*-

#随机森林 :创建多个决策树  （几乎是随机选取的特征） 多个决策树组成随机森林

from sklearn.ensemble import RandomForestClassifier  #导入随机森林分类器
from data_processing import *
from sklearn.cross_validation import cross_val_score
from sklearn.model_selection import GridSearchCV  #参数选择
from tree import X_homehigher

#clf = RandomForestClassifier(random_state=14)  #随机森林分类器

#scores = cross_val_score(clf,X_teams_expanded,y_true,scoring="accuracy")
#print "Accuracy : {0:.1f}%".format(np.mean(scores)*100)

X_all = np.hstack([X_homehigher,X_teams_expanded])
#为随机森林选取最佳参数
parameter_space ={"max_features":[2,10,"auto"],"n_estimators":[100,],"criterion":["gini","entropy"],"min_samples_leaf":[2,4,6],}

clf = RandomForestClassifier(random_state=14)
grid = GridSearchCV(clf,parameter_space) #将每个参数装入分类器训练,其实要进行多次运算
grid.fit(X_all,y_true)
print "Accuracy : {0:.1f}%".format(grid.best_score_*100)  #65%  #py的格式化输出{0}.format(表达式）
