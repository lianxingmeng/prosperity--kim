import  pandas as pd
import numpy as np
import tkinter as tk
import Relative_path
import Database_connect
import pickle
import tkinter.messagebox
import random
def prework():
    # create recommendation online file before system works. onlinerecomend.csv
    res_svd = pd.read_csv(Relative_path.pathusers_svd)
    # mix = res_svd.sort_values(by=['userId', 'predictScore'], ascending=[True, False])
    mix=res_svd
    useridlist = mix.userId.unique()

    mix_svd_als = pd.DataFrame()
    i=0
    for userid in useridlist:
        i+=1
        temp = mix.loc[mix.userId == userid, :]
        if(temp.shape[0]>50):
            # temp = temp.sort_values(by='predictScore', ascending=False)[:50]
            temp =temp[:50]
        else:
            temp = temp.sort_values(by='predictScore', ascending=False)[:35]
        mix_svd_als = pd.concat([mix_svd_als, temp])
        print(i)
    pd.DataFrame({'userId':mix_svd_als['userId'],'recommendId':mix_svd_als['recommendId']}).to_csv(Relative_path.pathusers_onlinerecommend,index=False)

def updataonline(userid,nowmovieid):
    # algorithm of recommendation online works, when this system runs
    try:
            conn,cur=Database_connect.Connect_sql()
            cur.execute('select movieid from Advice_Database.online_recommend where userid = {}'.format(userid))
            optionallist = cur.fetchall()
            cur.execute('select similarid from Advice_Database.movie_similar_svd where movieid = {}'.format(nowmovieid))
            similarlist = cur.fetchall()

            oldlist = set(optionallist).difference(set(similarlist))
            oldlist = np.array([mix[0] for mix in oldlist])
            mix_list = set(optionallist).union(set(similarlist))
            # for new users
            rand_list_new = random.sample(mix_list,50)
            rand_list_new = np.array([mix[0] for mix in rand_list_new])
            #
            mix_list = np.array([mix[0] for mix in mix_list])
            number_user = 1800
            if userid <= number_user:
                cur.execute("select * from Advice_Database.ratings where userid = {}".format(userid))
                ratingdata = cur.fetchall()
                ratingdata = np.array(ratingdata)
                recentmovie = ratingdata[np.argsort(ratingdata[:, -1])[::-1][:10], :]
                mix_list = np.array(list(set(mix_list) - set(ratingdata[:, 1])))


            movieList = pickle.load(open(Relative_path.pathusers_movielist, 'rb')).values
            movieList = [*map(int, movieList)]
            CosSim = pickle.load(open(Relative_path.pathusers_CosSim, 'rb'))
            CosSim = pd.DataFrame(CosSim, columns=movieList, index=movieList, copy=True)
            if userid<=number_user:
                similar_movie_rated = (CosSim.loc[mix_list, recentmovie[:, 1]]) * (CosSim.loc[mix_list, recentmovie[:, 1]] > 0.3)

                ratedmovie = (recentmovie[:, 2])
                sum_rated_cos = np.sum(similar_movie_rated, axis=1)
                for u in mix_list:
                    if sum_rated_cos[u] == 0:
                        sum_rated_cos[u] = 1
                predict_Val = similar_movie_rated.dot(ratedmovie.T) / sum_rated_cos
                predict_Val[oldlist] *= 0.75
                newrecommend = mix_list[np.argsort(predict_Val)[::-1][:50]]
            else:
                newrecommend = rand_list_new


            useridlist = np.array([userid] * len(newrecommend))

            newrecommendValue = ','.join(map(str, [*zip(useridlist, newrecommend)]))
            sqls = ['delete from Advice_Database.online_recommend where userid = {}'.format(userid),
                    'insert into Advice_Database.online_recommend values {}'.format(newrecommendValue)]
            for sql in sqls:
                cur.execute(sql)
                conn.commit()
            Database_connect.Close_sql(conn,cur)
            tk.messagebox.showerror(message="Thanks, You chose me !")
    except:
            tk.messagebox.showerror(message="You can't do it, Try another")
    print('online well done!!!')

def insertnew_user(userid):

    conn,cur = Database_connect.Connect_sql()
    cur.execute( 'insert into Advice_Database.online_recommend select {}, movieid from Advice_Database.movie_score_info  order by times desc limit 50;'.format(userid))
    # data = cur.fetchall()
    # newmovie = ([mix[1] for mix in data])
    # useidlist = np.array([userid]*50)
    # newuser_movies_suggest = ','.join(map(str,[*zip(useidlist,newmovie)]))
    #
    # sql = 'insert into Advice_Database.online_recommend  values {}'.format(newuser_movies_suggest)
    # cur.execute(sql)
    conn.commit()
    Database_connect.Close_sql(conn, cur)

if __name__ == "__main__":
    prework()
    # insertnew_user(770)
