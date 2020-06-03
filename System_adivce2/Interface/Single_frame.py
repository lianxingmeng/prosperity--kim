import tkinter as tk
import Get_url
import Interface.Movie_detail_information

class single_frame:

    def __init__(self, movieId, userId, Frame, second_window, root, type="base", **kw):
         self.movied_Id = movieId
         self.user_Id = userId
         self.window = Frame
         self.Second_window = second_window
         self.root = root
         self.url_imdbid = Get_url.get_movie_url(self.movied_Id)
         self.src, self.title, self.date, self.genres, self.briefinfo = Get_url.get_detail_movie(self.url_imdbid,self.movied_Id)

         self.frm = tk.Frame(self.window,width=90,height=120)

         if type=="similarDegree":
             tk.Label(self.frm,text='Similarity:{:.2f}'.format(kw['SimilarDegree']),font=('',9)).pack()

         self.tk_image = Get_url.get_image(self.src)
         self.button = tk.Button(self.frm, image=self.tk_image, width=80,height=120,bg="brown" ,command=self.createmovie_detail)
         self.button.pack()

         tk.Label(self.frm, text='{}'.format(self.title), width=20, height=1,font=('',10)).pack()
         tk.Label(self.frm, text='{}'.format(self.date), width=20, height=1, font=('',10)).pack()

    def createmovie_detail(self):
        print("I am destroying the Frame")
        self.Second_window.destroy()
        print("I am a creating a new Frame")
        self.Frame = tk.Frame(self.root, width=800,height=900)
        self.Frame.place(x=0,y=0,anchor="nw")
        print('prepare to create a new movie info window')
        print('userid:',self.user_Id)
        Interface.Movie_detail_information.Movie_detail_show(self.root,self.Frame,self.movied_Id,self.user_Id)
        print("You got it!")


