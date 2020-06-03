import tkinter as tk
from PIL import Image, ImageTk
import Interface.main_window


Root = tk.Tk()
Root.title("RECOMMENDATIONS FOR YOUR LOVE MOVIES")
screen_width = Root.winfo_screenwidth()
screen_height = Root.winfo_screenheight()
print(screen_height)
Root.geometry('800x900+%d+0' %((screen_width-800)/2))
Frame = tk.Frame(Root,width=800, height=900)
Frame.place(x=0,y=0,anchor="nw")
Interface.main_window.Main_window(Root, Frame, 1, None)
Root.update_idletasks()

Root.mainloop()
