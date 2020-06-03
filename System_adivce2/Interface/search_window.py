import tkinter as tk
import Interface.changge_Buttons
import Database_connect
import threading
import Interface.Single_frame

global Images
import tkinter.font as tkFont
from PIL import Image,ImageTk
import Relative_path
global Images
Images=[]

class Search_window():

    def __init__(self, root, window, movieid, userid):
        self.movieid = movieid
        self.userid = userid
        self.window = window
        self.root = root

        navbar_Frame = tk.Frame(self.window, width=800, height=20)
        navbar_Frame.pack_propagate(False)
        navbar_Frame.place(x=0, y=0, anchor="nw")
        Interface.changge_Buttons.Navigation_Bar(self.root,self.window,navbar_Frame,self.movieid, self.userid, type="S")


        self.searchcontent =  tk.StringVar()
        # tk.Entry(self.window,textvariable=self.searchcontent).place(x=58,y=48,anchor='nw')
        # tk.Button(self.window,text="search",command=self.get_search).place(x=249,y=48)

        self.Entry = tk.Entry(self.window,textvariable=self.searchcontent,cursor="cross",font=("",20))
        self.Entry.place(x=220,y=430,anchor='nw')
        self.button = tk.Button(self.window,text="Search",command=self.get_search)
        self.button.place(x=500,y=440)

        load1 = Image.open(Relative_path.pathusers_image_search1)
        w, h = load1.size
        f1 = 1.0 * 600 / w
        f2 = 1.0 * 350 / h
        factor = min(f1, f2)
        width = int(w * f1)
        height = int(h * f2)
        load1 = load1.resize((width, height), Image.ANTIALIAS)
        photo1 = ImageTk.PhotoImage(load1)
        Images.append(photo1)
        self.image = tk.Label(self.window, image=photo1, font=('',20), compound=tk.CENTER, fg="white")
        self.image.place(x=100, y=50,anchor="nw")

        self.result_Frame = tk.Frame(self.window,width=800,height=700)
        self.result_Frame.pack_propagate(False)

        print("userid:",self.userid)

    def get_search(self):
        self.result_Frame.destroy()
        self.result_Frame = tk.Frame(self.window, width=800, height=700)
        self.result_Frame.pack_propagate(False)
        self.result_Frame.place(x=0, y=90, anchor='nw')

        searchcontent = self.searchcontent.get()

        self.Entry.place(x=58,y=48,anchor='nw')
        self.button.place(x=350,y=55)
        self.image.destroy()

        conn, cur = Database_connect.Connect_sql()
        sql = "select movieid from Advice_Database.movies where title like '%{}%';".format(searchcontent)
        cur.execute(sql)
        data = cur.fetchall()  # 记录用户的打分情况
        Database_connect.Close_sql(conn,cur)

        # 显示搜索结果

        # 电影展示页面
        if len(data) == 0:
            tk.Label(self.result_Frame, text="Sorry,we didn't find any similar movies about it", font=('', 20)).place(x=200, y=60,
                                                                                                        anchor="nw")
        if len(data) > 0:
            tk.Label(self.result_Frame,
                     text="We have found {} movies,but only show the recent 15 movies".format(len(data))).place(x=58,
                                                                                                                y=0,
                                                                                                                anchor='nw')
            # 只显示一行
            list1_Frame = tk.Frame(self.result_Frame)
            list1_Frame.place(x=15, y=50)
            movielist1 = data[:5]
            for tup in movielist1:
                t = threading.Thread(target=self.job, args=(list1_Frame, tup[0]))
                t.start()

        if len(data) > 5:
            list2_Frame = tk.Frame(self.result_Frame)
            list2_Frame.place(x=15, y=258)
            movielist2 = data[5:10]
            for tup in movielist2:
                t = threading.Thread(target=self.job, args=(list2_Frame, tup[0]))
                t.start()

        if len(data) > 10:
            # 再显示一行
            list3_Frame = tk.Frame(self.result_Frame)
            list3_Frame.place(x=15, y=465)
            movielist3 = data[10:15]
            for tup in movielist3:
                t = threading.Thread(target=self.job, args=(list3_Frame, tup[0]))
                t.start()

    def job(self, Frame, movieid):
        temp = Interface.Single_frame.single_frame(movieid, self.userid, Frame, self.window, self.root)
        Images.append(temp.tk_image)
        temp.frm.pack(side='left')

if __name__ == "__main__":
    Root =tk.Tk()
    Root.geometry('800x900')
    Frame = tk.Frame(Root,width=800, height=900, bg='black')
    Frame.place(x=0, anchor='nw', y=0)
    movieid='1'
    userid='1'
    Search_window(Root,Frame,movieid,userid)

    Root.mainloop()