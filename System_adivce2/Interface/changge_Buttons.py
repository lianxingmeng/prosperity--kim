import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk
import Interface.main_window
import Interface.Movie_detail_information
import Database_connect
import Interface.search_window
import Relative_path
from Get_url import resize
global image
image = []
from Algorithm import online_recommendation
class Login_bt():
    def __init__(self,root,window,navibar,movieid, userid,type="M"):
          self.movie_id = movieid
          self.userid = userid
          self.navi_bar = navibar
          self.root = root
          self.window = window
          self.type = type
          s=tk.StringVar()
          if self.userid is None:
              s.set('Login|sign up')
          else:
              s.set('Logout')

          self.Button = tk.Button(self.navi_bar,textvariable=s,command=self.retire)

    def retire(self):
            if self.userid is None:
                 self.login()
            else:
                print("I am retiring from this ")
                print("Preparing to create a new main_window")
                self.userid = None
                self.update()
                print("well done")

    def login(self):
           self.window_signup = tk.Toplevel(self.root)

           screen_width = self.window_signup.winfo_screenwidth()
           screen_height = self.window_signup.winfo_screenheight()
           self.window_signup.geometry("500x300+%d+%d"%((screen_width-500)/2,(screen_height-400)/2))
           self.window_signup.title('Login | Register')
           self.frm = tk.Frame(self.window_signup, width=500, height=300, bg='white')
           self.frm.place(x=0, y=0, anchor="nw")


           load = Image.open(Relative_path.pathusers_image_Login)
           w, h = load.size
           f1 = 1.0 * 300 / w
           f2 = 1.0 * 150 / h
           width = int(w * f1)
           height = int(h * f2)
           load = load.resize((width, height), Image.ANTIALIAS)
           photo = ImageTk.PhotoImage(load)
           image.append(photo)
           img = tk.Label(self.frm, image=photo)
           img.place(x=100,y=0,anchor="nw")

           tk.Label(self.frm, text="User name:").place(x=90, y=150)
           tk.Label(self.frm, text="Password:").place(x=90, y=190)

           self.var_usr_name = tk.StringVar()
           self.var_usr_name.set('1-1800')
           entry_usr_name = tk.Entry(self.frm, textvariable=self.var_usr_name)
           entry_usr_name.place(x=200, y=150)

           self.var_usr_pwd = tk.StringVar()
           entry_usr_pwd = tk.Entry(self.frm, textvariable=self.var_usr_pwd, show='*')
           entry_usr_pwd.place(x=200, y=190)
           btn_login = tk.Button(self.frm, text='Log in',command=self.comfirm_login)
           btn_login.place(x=210, y=230)
           btn_sign_up = tk.Button(self.frm, text='Sign up',command=self.comfirm_signin )
           btn_sign_up.place(x=320, y=230)
    def comfirm_login(self):
        try:
            name = eval(self.var_usr_name.get())
        except:
             tk.messagebox.showerror(message="The user name must be integer")
             return
        if not isinstance(name,int):
            tk.messagebox.showerror(message="The user name must be integer")
            return
        conn,cur=Database_connect.Connect_sql()
        cur.execute("select password from Advice_Database.users where userid={}".format(self.var_usr_name.get()))
        data = cur.fetchall()

        if len(data)==0:
            tk.messagebox.showerror(message="This account is not exist")
        else:
            if data[0][0] == self.var_usr_pwd.get():
                tk.messagebox.showinfo(message="Welcome here User {}".format(self.var_usr_name.get()))
                self.userid = eval(self.var_usr_name.get())
                self.window_signup.destroy()
                self.update()
            else:
                tk.messagebox.showerror(message="sorry, This password is false")

    def comfirm_signin(self):
        try:
            name = eval(self.var_usr_name.get())
        except:
            tk.messagebox.showerror(message="The user name must be integer")
            return
        if not isinstance(name, int):
            tk.messagebox.showerror(message="The user name must be integer")
            return
        conn, cur = Database_connect.Connect_sql()
        cur.execute("select password from Advice_Database.users where userid={}".format(self.var_usr_name.get()))
        data = cur.fetchall()

        if len(data) == 0:

            cur.execute("insert into Advice_Database.users values({},{})".format(self.var_usr_name.get(), self.var_usr_pwd.get()))
            conn.commit()
            tk.messagebox.showinfo(message="Welcome here, New User {}".format(self.var_usr_name.get()))
            self.window_signup.destroy()
            self.userid = eval(self.var_usr_name.get())

            # 触发online_recommend添加上新用户的推荐列表
            online_recommendation.insertnew_user(self.userid)
            self.update()  # 刷新页面
        else:
            tk.messagebox.showerror(message="This accound had exited, Try new one.")




    def update(self):
         self.window.destroy()
         self.newFrame = tk.Frame(self.root,width=800,height=900)
         self.newFrame.place(x=0,y=0,anchor="nw")
         if self.type=="M" or self.type=="B":
              Interface.main_window.Main_window(self.root,self.newFrame,self.movie_id,self.userid)
         elif self.type=="I":
               Interface.Movie_detail_information.Movie_detail_show(self.root,self.newFrame,self.movie_id,self.userid)
         else:
             Interface.search_window.Search_window(self.root, self.newFrame, self.movie_id, self.userid)


class Search_bt():
     def __init__(self, root, window, nagvibar, movieid, uerid):
         self.movieid = movieid
         self.userid = uerid
         self.navibar = nagvibar
         self.window = window
         self.root = root
         self.Button = tk.Button(self.navibar,text="Search",command=self.search_layout)
     def search_layout(self):
         self.window.destroy()
         self.newFrame=tk.Frame(self.root,width=800,height=900)
         self.newFrame.place(x=0,y=0,anchor="nw")

         Interface.search_window.Search_window(self.root,self.newFrame,self.movieid,self.userid)

         print("well Done!")

class Main_Window_bt():
     def __init__(self,root,window,nagvibar,movieid,userid):
         self.movieid = movieid
         self.userid = userid
         self.nagvibar = nagvibar  # 当前的小幕布
         self.window = window  # 当前的主幕布
         self.root = root  # 窗口根目录
         self.Button = tk.Button(self.nagvibar, text="Main Window", command=self.turn2main)

     def turn2main(self):
        print("I am destroying the browseFootprints")
        self.window.destroy()
        print('I am creating a new Frame for Main_window')
        self.newFrame = tk.Frame(self.root, width=800, height=900)
        self.newFrame.place(x=0, y=0, anchor='nw')
        print('Prepare to create Main Window')
        Interface.main_window.Main_window(self.root, self.newFrame, self.movieid, self.userid)
        print('Well Done!')



class Browse_bt():
    def __init__(self,root,window,nagvibar,movieid,useid):
        self.movieid = movieid
        self.userid = useid
        self.nagvibar = nagvibar  # 当前的小幕布
        self.window = window  # 当前的幕布
        self.root = root  # 窗口根目录
        self.Button = tk.Button(self.nagvibar, text="BrowseFootprints", command=self.turn2Browse)

    def turn2Browse(self):
        print("I am destroying the Main_Frame")
        self.window.destroy()
        print('I am creating a new Frame for BrowseFootprint')
        self.newFrame = tk.Frame(self.root, width=800, height=900)
        self.newFrame.place(x=0, y=0, anchor='nw')
        print('Prepare to create BrowseFootprint window')
        print('Well Done!')



















class Navigation_Bar():
    def __init__(self, root, window, nagvigation_bar,movieid,userid, type):
         self.movie_id=movieid
         self.userid=userid
         self.navi_bar=nagvigation_bar
         self.root=root
         self.window=window
         self.type=type

         if userid is not None:
             Login_bt(self.root, self.window, self.navi_bar, self.movie_id, self.userid, self.type).Button.pack(
                 side="right")
             if self.type != 'S':
                 Search_bt(self.root, self.window, self.navi_bar, self.movie_id, self.userid).Button.pack(side="right")

             if self.type == "I" or self.type == "S":
                     Main_Window_bt(self.root, self.window, self.navi_bar, self.movie_id, self.userid).Button.pack(
                         side="right")

         else:
             Login_bt(self.root,self.window,self.navi_bar,self.movie_id,self.userid,self.type).Button.pack(side="right")
             if self.type=="I" or self.type=="S":
                 Main_Window_bt(self.root,self.window,self.navi_bar,self.movie_id,self.userid).Button.pack(side="right")
             if self.type !='S':
                 Search_bt(self.root,self.window,self.navi_bar,self.movie_id,self.userid).Button.pack(side="right")




