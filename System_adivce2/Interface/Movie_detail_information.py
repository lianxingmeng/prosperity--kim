import tkinter as tk
import threading
import Relative_path
import Get_url
global Images
import Database_connect
import Interface
from Algorithm import online_recommendation

Images=[]


class Movie_detail_show():

    def __init__(self,root,window,movieid,userid):
         self.movieid=movieid
         self.userid=userid
         self.window=window
         self.root=root
         self.predice_score = 0

         navbar_Frame = tk.Frame(self.window, width=800, height=20)
         navbar_Frame.pack_propagate(False)
         navbar_Frame.place(x=0, y=0, anchor="nw")
         Interface.changge_Buttons.Navigation_Bar(self.root, self.window, navbar_Frame, self.movieid, self.userid,
                                                  type="I")

         self.frm_content = tk.Frame(self.window,width=800,height=500,bg="white")
         self.frm_content.place(x=0,y=20)
         self.url_imbid = Get_url.get_movie_url(movieid=self.movieid)
         self.src,self.title,self.date,self.genres,self.briefinfo = Get_url.get_detail_movie(self.url_imbid,self.movieid)
         self.tk_image=Get_url.get_image(self.src,w_box=300,h_box=300)  #call this
         Images.append(self.tk_image)

         self.frm_content_left = tk.Frame(self.frm_content,width=375, height=500,bg="white")
         self.frm_content_left.place(x=0,y=0,anchor="nw")
         tk.Label(self.frm_content_left,borderwidth=2,relief="flat",image=self.tk_image).place(x=130,y=17,anchor="nw")

         self.score, self.times = self.get_score()
         if userid != None :
             self.button1 = tk.Button(self.window,text="Fun",command=self.love_movie,font=("",15))
             self.button1.place(x=190,y=370,anchor="nw")
             conn, cur = Database_connect.Connect_sql()
             sql = "select  predictScore from Advice_Database.offline_recommend_svd where userid={} and recommendId={};".format(
                 self.userid, self.movieid)
             q = cur.execute(sql)
             if(q>0):
                     data2 = cur.fetchall()
                     self.predice_score = data2[0][0]
                     tk.Label(self.frm_content_left,text="score:{:.2f} Predict:{} ".format(self.score, self.predice_score,
                                                                     )).place(x=125, y=330, anchor="nw")

             else:
                 tk.Label(self.frm_content_left, text="score:{:.2f} ".format(self.score, )).place(
                     x=125, y=330, anchor="nw")
             Database_connect.Close_sql(conn, cur)
         else:
             tk.Label(self.frm_content_left,text="score:{:.2f} ".format(self.score)).place( x=125, y=330, anchor="nw")

         self.frm_content_right = tk.Frame(self.frm_content,bg="white", height=500,width=500)
         self.frm_content_right.place(x=380,y=0,anchor="nw")
         tk.Label(self.frm_content_right, text="Title:{}".format(self.title),font=("",15),height=1).place(x=0,y=17)
         tk.Label(self.frm_content_right,text="Date:{}".format(self.date), font=("",15), height=1).place(x=0,y=50)
         self.genres = self.genres.strip('""').replace(",", "").replace('"', "").replace(" ", '')
         tk.Label(self.frm_content_right,text="Genres:\n" + self.genres,font=("",15)).place(x=0,y=85)
         tk.Label(self.frm_content_right,text="Description:\n" +self.briefinfo.replace('\\u0027','\''),
                  font=("",15), wraplength=300, justify="left",height=10).place(x=0,y=220)


         tk.Label(self.window,text="Recommendations with SVD algorithm:").place(x=25, y=445,anchor="nw")
         self.data_svd =Get_url.get_similar_movie_list(self.movieid,type="SVD")

         print (self.movieid)
         print(self.data_svd)
         if len(self.data_svd) == 0:
             tk.Label(self.window, text="Sorry,we didn't find any similar movies about it", font=('', 20)).place(
                 x=25, y=500,
                 anchor="nw")
             if userid != None:
                self.button1.destroy()
         else:
             self.count = 0
             self.frm_svd = tk.Frame(self.window, bg="white")
             self.frm_svd.place(x=25, y=470, anchor="nw")
             button1 = tk.Button(self.window, text="Next_Page", command=self.countmovies)
             button1.place(x=700, y=450, anchor="nw")
             self.showmovie()
    def countmovies(self):
            self.frm_svd.destroy()
            self.frm_svd = tk.Frame(self.window, bg='white', height=150, width=1000)
            self.frm_svd.place(x=25, y=470, anchor='nw')

            if self.count %5==0:
                if self.count == 20:
                    self.count=0
                    self.showmovie()
                else:
                  self.showmovie()
    def love_movie(self):
         print(self.userid,"sss",self.movieid)
         online_recommendation.updataonline(self.userid,self.movieid)

    def showmovie(self):
        start = self.count
        print(start)
        end = self.count + 5
        data2 = self.data_svd[start:end]
        for tup in data2:
            t = threading.Thread(target=self.job, args=(tup[0], tup[1], self.frm_svd))
            t.start()
        self.count +=5



    def get_score(self):
        conn,cur = Database_connect.Connect_sql()
        sql= "select score,times from Advice_Database.movie_score_info where movieid={};".format(self.movieid)
        cur.execute(sql)
        data = cur.fetchall()
        score = 0
        times = 0
        if (len(data)>0):
            score = data[0][0]
            times = data[0][1]
        Database_connect.Close_sql(conn, cur)

        return score, times


    def job(self,movieid,similarDegree,frm):
        temp = Interface.Single_frame.single_frame(movieid,self.userid,frm,self.window,self.root,type="similarDegree",SimilarDegree=similarDegree)
        Images.append(temp.tk_image)
        temp.frm.pack(side='left')




