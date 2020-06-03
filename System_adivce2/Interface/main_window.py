import tkinter as tk
import Database_connect
import threading
import Interface.Single_frame
import Interface.changge_Buttons
global Images
import tkinter.font as tkFont
from PIL import Image,ImageTk
import Relative_path
import schedule
import time
Images=[]

class Main_window():

    def __init__(self,root,window,moviedid,userid):
        self.movie_id=moviedid
        self.user_id=userid
        self.window=window
        self.root=root
        self.count = 0


        navbar_Frame = tk.Frame(self.window, width=800, height=20)
        navbar_Frame.pack_propagate(False)
        navbar_Frame.place(x=0,y=0,anchor="nw")
        Interface.changge_Buttons.Navigation_Bar(self.root,self.window,navbar_Frame,self.movie_id,self.user_id,type="M")

        ft1 = tkFont.Font(family='Fixdsys',size =20)


        if self.user_id is None:
            # tk.Label(self.window,text="Master",font=ft1).place(x=230, y=130,anchor='nw')
            tk.Label(self.window,text='Classic Movies:',font=ft1).place(x=40,y=440,anchor='nw')

            load = Image.open(Relative_path.pathusers_image_main_tourist)
            w, h = load.size
            f1 = 1.0 * 600 / w
            f2 = 1.0 * 400 / h
            factor = min(f1, f2)
            width = int(w * f1)
            height = int(h * f2)
            load = load.resize((width, height), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(load)
            Images.append(photo)
            img = tk.Label(self.window,image=photo,font=ft1,compound = tk.CENTER,fg="white")
            img.place(x=10, y=30, anchor="nw")

            load1 = Image.open(Relative_path.pathusers_image_main_tourist2)
            w, h = load1.size
            f1 = 1.0 * 200 / w
            f2 = 1.0 * 400 / h
            factor = min(f1, f2)
            width = int(w * f1)
            height = int(h * f2)
            load1 = load1.resize((width, height), Image.ANTIALIAS)
            photo1 = ImageTk.PhotoImage(load1)
            Images.append(photo1)
            tk.Label(self.window, image=photo1, font=ft1, compound=tk.CENTER, fg="white").place(x=600, y=30, anchor="nw")

            self.hotmovie_Frame = tk.Frame(self.window,bg='white',height=150,width=1000)
            self.hotmovie_Frame.place(x=15,y=480, anchor='nw')
            self.hotmovie()
            button1 = tk.Button(self.window,text="Next_Page",command=self.countmovies)
            button1.place(x=350,y=650,anchor="nw")


            # self.window.after(10000,self.countmovies())


        else:
             conn, cur = Database_connect.Connect_sql()
             cur.execute(
                    'select rating from Advice_Database.average_rating where userId = {};'.format(self.user_id))
             data = cur.fetchall()
             Database_connect.Close_sql(conn, cur)
             number_suer = 1800

             load1 = Image.open(Relative_path.pathusers_image_main_users)
             w, h = load1.size
             f1 = 1.0 * 600 / w
             f2 = 1.0 * 300 / h
             factor = min(f1, f2)
             width = int(w * f1)
             height = int(h * f2)
             load1 = load1.resize((width, height), Image.ANTIALIAS)
             photo1 = ImageTk.PhotoImage(load1)
             Images.append(photo1)
             tk.Label(self.window, image=photo1, font=ft1, compound=tk.CENTER, fg="white").place(x=100, y=450,
                                                                                                 anchor="nw")

             if self.user_id <=number_suer:
                button1 = tk.Button(self.window, text="Next_Page", command=self.countmovies)
                button1.place(x=700, y=260, anchor="nw")
                tk.Label(self.window, text="Welcome User: {}.  Your average rating is {} ".format(self.user_id,round(data[0][0],4))).place(x=20, y=15, anchor='nw')
             else:
                 tk.Label(self.window, text="Welcome User: {},  ".format(self.user_id)).place( x=20, y=15, anchor='nw')

             tk.Label(self.window,text="RECOMMENDATION OF SVD Offline: ",font=ft1).place(x=45,y=242,anchor='nw')
             self.users_svd_Frame = tk.Frame(self.window,width=800,height=150)
             self.users_svd_Frame.pack_propagate(False)
             self.users_svd_Frame.place(x=15,y=282,anchor='nw')

             t = threading.Thread(target=self.users_svd())
             t.start()

             tk.Label(self.window,text="Real Time:",font=ft1).place(x=45,y=40,anchor='nw')
             tk.Button(self.window,text="Next Page",command = self.next_page_online).place(x=700,y=40,anchor='nw')
             self.online_Frame = tk.Frame(self.window)
             self.online_Frame.place(x=15,y=70,anchor='nw')
             self.online_movie()

    def online_movie(self):
        conn, cur = Database_connect.Connect_sql()
        cur.execute('select movieid from Advice_Database.online_recommend where userid = {}'.format(self.user_id))
        data = cur.fetchall()  # 拿到离线用户推荐信息
        Database_connect.Close_sql(conn, cur)
        print(data)
        self.data3 = data
        self.count_online_movie = 0
        for tup in data[:5]:
            t = threading.Thread(target=self.single_frame, args=(self.online_Frame, tup[0]))
            t.start()

        self.count_online_movie += 5
    def next_page_online(self):
        self.online_Frame.destroy()
        self.online_Frame = tk.Frame(self.window)
        self.online_Frame.place(x=15, y=70, anchor='nw')
        start = self.count_online_movie
        end = self.count_online_movie+5
        data = self.data3[start:end]
        print("haha")
        print(self.count_online_movie)
        for tup in data:
            t = threading.Thread(target=self.single_frame, args=(self.online_Frame, tup[0]))
            t.start()
        self.count_online_movie+=5
        if self.count_online_movie//5==4:
            self.count_online_movie=0






    def hotmovie(self):

        conn,cur = Database_connect.Connect_sql()
        k='select movieid from Advice_Database.movie_score_info order by times desc limit 50;'
        t='select movieid,count(1) from Advice_Database.ratings group by movieid order by count(1) desc limit 20;'
        cur.execute(t)
        self.data = cur.fetchall()
        Database_connect.Close_sql(conn,cur)
        self.count = 0
        self.showmovie()

    def showmovie(self):

        start = self.count
        print(start)
        end = self.count + 5
        if self.user_id is None:
          data2 = self.data[start:end]
        else:
          data2 = self.data2[start:end]
        for single in data2:
            if self.user_id is None:
                t = threading.Thread(target=self.single_frame, args=(self.hotmovie_Frame, single[0]))
            else:
                t = threading.Thread(target=self.single_frame, args=(self.users_svd_Frame, single[0]))
            print(single[0])
            t.setDaemon(True)
            t.start()
        self.count +=5

    def countmovies(self):
        if self.user_id is None:
            self.hotmovie_Frame.destroy()
            self.hotmovie_Frame = tk.Frame(self.window, bg='white', height=150, width=1000)
            self.hotmovie_Frame.place(x=15, y=480, anchor='nw')
        else:
            self.users_svd_Frame.destroy()
            self.users_svd_Frame = tk.Frame(self.window, width=800, height=150)
            self.users_svd_Frame.pack_propagate(False)
            self.users_svd_Frame.place(x=15, y=282, anchor='nw')
        if self.count %5==0:
            if self.count == 20:
                if self.user_id is None:
                    self.hotmovie()
                else:
                    self.users_svd()
                     # if self.user_id is None:
                     #
                     # else:
                     #     self.users_svd()
                     # self.window.after(8000, self.countmovies())
            else:
                    self.showmovie()
            # schedule.every(5).seconds.do(self.countmovies())
           



            # if self.count % 5==0:
            #      if self.count==30:
            #          self.hotmovie()
            #          # self.window.after(5000, self.countmovies())
            #      else:
            #          self.showmovie()
            #          self.window.after(5000,self.countmovies())




        # self.canvas.move(self.hotmovie_Frame,-15,0)
        # for single in data:
        #      if(i%5==0 and i<=15):
        #          time.sleep(5)
        #          self.hotmovie_Frame.destroy()
        #          self.hotmovie_Frame = tk.Frame(self.window,bg='blue')
        #      t = threading.Thread(target=self.single_frame, args=(self.hotmovie_Frame, single[0]))
        #      t.start()
        #      i += 1
        # if(i==20):
        #     time.sleep(2)


    def single_frame(self,frame, movieid):
        tem = Interface.Single_frame.single_frame(movieid,self.user_id,frame,self.window,self.root)
        Images.append(tem.tk_image)
        tem.frm.pack(side='left')

    def users_svd(self):

        conn,cur = Database_connect.Connect_sql()
        cur.execute('select recommendid from Advice_Database.offline_recommend_svd where userid={} order by predictScore desc limit 20;'.format(self.user_id))
        data= cur.fetchall()
        self.data2 = data
        Database_connect.Close_sql(conn,cur)
        print(data)
        self.count = 0
        if(len(data)==0):
              tk.Label(self.users_svd_Frame,text="Sorry, we don't find good recommendation for U",font=('',20)).pack(side='bottom')
        else:
               self.showmovie()