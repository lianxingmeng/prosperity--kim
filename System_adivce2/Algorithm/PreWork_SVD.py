# -*- coding: utf-8 -*-
#preWork_SVD中包括/ this file includes：
#根据ratings.csv文件得到协同过滤矩阵/ read file ratings.csv and then convert into matrix.
#数据归一化 /normalize data
#SVD进行分解，保留5个纬度，基于item进行协同过滤 / SVD runs, then reduce dimensionality of useful information
#得到余弦相似度矩阵 / calculate useful information to get similarity between movies.
# 得到movie_similar_svd矩阵，将相似度大于0.88的电影存入/ sort similarity file to show most closing movies for each movie
#得到offline_recommend_svd矩阵，根据预测后的评分，每个用户保留前100个电影/ use formula to predict favor value of movies that users like
#这篇文档中的工作应该在程序启动前完成/ this code runs before this system run.
#实际运行程序时，会将处理好的数据直接导入mysql中/ when this system runs, all data required had stored into database.


import pandas as pd
import numpy as np
import pickle
import Relative_path

#根据rating.csv得到协同过滤矩阵
# read file ratings.csv.
ratings = pd.read_csv("{}".format(Relative_path.pathrating))
rating_dict = {}

# convert data into matrix
for i in range(ratings.shape[0]):
    line = ratings.iloc[i,:]
    if line.userId in rating_dict:
        rating_dict[line.userId][line.movieId] = line.rating
    else:
        rating_dict[line.userId] = {line.movieId:line.rating}
#visible matrix
rating_matrix = pd.DataFrame(rating_dict).T

# outcome of average_rating.csv for users' mean ratings.
x=rating_matrix.mean(1)
userlist = rating_matrix.index
Average_rating = pd.DataFrame()
users_rating=pd.DataFrame()
Average_rating = pd.concat([Average_rating,pd.DataFrame({'userId':userlist,"averragerating":x})])
Average_rating.to_csv(Relative_path.pathusers_average_rating,index=False,sep=',')
# outcome of users.csv for users'login
a = [i+1 for i in range(1800)]
users = pd.concat([users_rating,pd.DataFrame({'userId':userlist,"password":a})])
users.to_csv(Relative_path.pathusers,index=False,sep=',')


# normalization of data to eliminate error
rating_matrix3 = ((rating_matrix.T - rating_matrix.T.mean(axis=0))/(rating_matrix.T.max(axis=0)-rating_matrix.T.min(axis=0))).T
rating_matrix_fillzero = rating_matrix3.fillna(0)

#使用SVD进行分解
#SVD runs
U,sigma,Vt = np.linalg.svd(rating_matrix_fillzero)


#对数据进行降维
# reduce dimensionality of useful data to calculate conveniently
reduced_matrix = (U[:,:5].dot(np.eye(5)*sigma[:5])).T.dot(rating_matrix_fillzero)

# normilize data to speed up preocess of calculation of data
# std_matrix1 = ((reduced_matrix.T - reduced_matrix.T.mean(axis=0))/(reduced_matrix.T.max(axis=0)-reduced_matrix.T.min(axis=0))).T
std_matrix2 = ((reduced_matrix.T - reduced_matrix.T.mean(axis=0))/reduced_matrix.T.std(axis=0)).T
# 2 is for speed up the calculation of Similarity
std_matrix = std_matrix2

#计算余弦相似度矩阵
# calculate similarity
upfactor = std_matrix.T.dot(std_matrix)#分子
downfactor = (np.linalg.norm(std_matrix,axis=0).reshape(-1,1)).dot(np.linalg.norm(std_matrix,axis=0).reshape(1,-1))
cosSim = (upfactor/downfactor + 1)/2#在原本余弦相似度的基础上进行小小修改，将值定在0～1之间

#  similarity of movies,cosSim.csv
with open(Relative_path.pathusers_CosSim,"wb") as file:
    pickle.dump(cosSim,file)
movieIdList = rating_matrix.columns
# name of movies, movieslist.csv
with open(Relative_path.pathusers_movielist,'wb') as file:
    pickle.dump(movieIdList,file)

#把相似度大于0.88的电影，以movieId,similarId,similarDegree的格式进行保存，数字过小，信息量太大
# sort similarity file to show most closing movies for each movie, then store it into file. movie_similar_svd.csv
movieIdList = rating_matrix.columns
movie_similar_svd = pd.DataFrame()

for i in range(cosSim.shape[0]):
    movieId = movieIdList[i]
    similarlist = movieIdList[cosSim[i,:]>=0.88]
    similardegreelist = cosSim[i,:][cosSim[i,:]>=0.88]
    index = np.argsort(similardegreelist)[::-1]
    if len(similardegreelist)>26:
        index = index[:26]
    similarlist = similarlist[index]
    similardegreelist = similardegreelist[index]
    movie_similar_svd = pd.concat([movie_similar_svd,pd.DataFrame({'movieId':movieId,'similarId':similarlist,'similarDegree':similardegreelist})])


movie_similar_svd = movie_similar_svd.loc[movie_similar_svd.movieId != movie_similar_svd.similarId,:]#删除自己与自己的相似度
movie_similar_svd.to_csv(Relative_path.pathmovie_similar_svd,index=False)
print("made closing file of movies")



#离线推荐系统
#预测用户未评分的电影评分
#对于每个用户取预测评分最高的50部电影，存入predict_matrix中
# use formulas to predict favor value of movies that users like, then store data into file. offline_recommend_svd.csv
predict_matrix = pd.DataFrame()
userIdlist = rating_matrix.index
movieIdList = rating_matrix.columns
for user in range(rating_matrix.shape[0]):
    userId = userIdlist[user]
    unrate = np.isnan(rating_matrix.values[user,:])
    haverated = ~unrate
    recommendId = movieIdList[unrate]
    similar_movie_rated = (cosSim[unrate, :][:, haverated]) * (cosSim[unrate, :][:, haverated] > 0.4)  # martix of
    ratedmovie = (rating_matrix.values[user, :][haverated])
    print(userIdlist[user])
    sum_rated_cos = np.sum(similar_movie_rated, axis=1)
    for i in range(sum_rated_cos.shape[0]):
        if sum_rated_cos[i] == 0:
            sum_rated_cos[i] = 1
    predict_Val = similar_movie_rated.dot(ratedmovie.T)/sum_rated_cos
    index = np.argsort(predict_Val)[::-1]
    if len(predict_Val>100):
        index = index[:100]
    predict_Val = predict_Val[index]
    recommendId = recommendId[index]
    predict_matrix = pd.concat([predict_matrix,pd.DataFrame({'userId':userId,'recommendId':recommendId,'predictScore':predict_Val})])


predict_matrix.to_csv(Relative_path.pathusers_svd,index=False)




