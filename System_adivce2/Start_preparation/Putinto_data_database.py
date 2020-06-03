import tkinter as tk
import warnings
import Relative_path
import Database_connect
import pymysql

def inputdata():
    warnings.filters
    conn,cur = Database_connect.Connect_sql()
    print('连接成功')

    sql_createDatabase = ["drop database if exists Advice_Database;",
                          "create database Advice_Database;",
                          "use Advice_Database;",
                          ]

    # sql_createDatabase= ["drop database if exists Movie;",
    #                      "create database Movie;",
    #                      "use Movie;",
    #                      ]
    for sql in sql_createDatabase:
        cur.execute(sql)

    print("成功创建")
    sql_inpulinks = ["create table links(movieId int, imdbId int, tmdbId int);",
                     r'''load data infile '{}' into table links fields terminated by ',' lines terminated by '\r\n'  ignore 1 lines;'''.format(Relative_path.pathlinks),

                     ]

    for sql in sql_inpulinks:
        cur.execute(sql)

    sql_inputmovies = ["create table movies(movieId int,title varchar(200),genres varchar(100));",
                       r'''load data infile "{}" into table movies fields terminated by ',' optionally enclosed by '"' escaped by '"' lines terminated by '\n' ignore 1 lines;'''.format(
                           Relative_path.pathmovie),
                       ]
    for sql in sql_inputmovies:
        cur.execute(sql)

    sql_inputratings = ["create table ratings(userId int,movieId int,rating float,timestamp int)",
                        r'''load data infile "{}" into table ratings fields terminated by ',' lines terminated by '\n' ignore 1 lines'''.format(
                            Relative_path.pathrating),
                        ]
    for sql in sql_inputratings:
        cur.execute(sql)

    conn.commit()

    sql_inputmovie_similar_svd = ["create table movie_similar_svd(movieId int,similarId int,similarDegree float)",
                                  r'''load data infile "{}" into table movie_similar_svd fields terminated by',' lines terminated by '\n' ignore 1 lines'''.format(
                                      Relative_path.pathmovie_similar_svd)]
    for sql in sql_inputmovie_similar_svd:
        cur.execute(sql)
    conn.commit()

    sql_inputusers = ['create table users (userid int,password varchar(10))',
                      r'''load data infile "{}" into table users fields terminated by ',' lines terminated by '\n' ignore 1 lines'''.format(
                          Relative_path.pathusers)]
    for sql in sql_inputusers:
        cur.execute(sql)
    conn.commit()

    sql_inputoffline_recommend_svd = [
        "create table offline_recommend_svd(userId int,recommendId int,predictScore float)",
        r'''load data infile "{}" into table offline_recommend_svd fields terminated by',' lines terminated by '\n' ignore 1 lines'''.format(
            Relative_path.pathusers_svd)]
    for sql in sql_inputoffline_recommend_svd:
        cur.execute(sql)
    conn.commit()

    sql_input_average_rating = [
        "create table average_rating(userId int,rating float)",
        r'''load data infile "{}" into table average_rating fields terminated by',' lines terminated by '\n' ignore 1 lines'''.format(
            Relative_path.pathusers_average_rating)]
    for sql in sql_input_average_rating:
        cur.execute(sql)
    conn.commit()

    sql_inputonline_recommend = [
        "create table online_recommend (userId int,movieId int);",
        r'''load data infile "{}" into table online_recommend fields terminated by ',' lines terminated by '\n' ignore 1 lines'''.format(
           Relative_path.pathusers_onlinerecommend)
    ]
    for sql in sql_inputonline_recommend:
        cur.execute(sql)
    conn.commit()

    Database_connect.Close_sql(conn,cur)
def Create_newtable():
    warnings.filters
    conn,cur=Database_connect.Connect_sql()
    sqll=["use Advice_Database;",
           "create table movie_score_info select movieId,avg(rating) score,count(*) times from ratings group by movieId;"]
    for sql in sqll:
        cur.execute(sql)
    conn.commit()

    Database_connect.Close_sql(conn,cur)




if __name__=='__main__':
    inputdata()
    Create_newtable()
