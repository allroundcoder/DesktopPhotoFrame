import glob
import os
import sys
import time
from itertools import cycle
from PIL import Image
from PIL import ImageTk

if sys.version_info < (3, 0):
    import Tkinter as tk
else:
    import tkinter as tk

###################
# General setings #  
###################
SLIDE_SHOW_TIME_MS = 3 * 1000

# Window height in portrait orientation. The same value is used
# for the window width in landscape orientation.
WINDOW_HEIGHT_IN_PERCENTAGE_OF_SCREEN_HEIGHT = 30
###################

class Win(tk.Tk):
    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.config(bg="black", width=1, height=1)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", 1)
        self.pack_propagate(False)
        
        self.bind('<ButtonPress-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)
        self.bind("<Escape>", self.esc_handler)
        self.bind("q", self.esc_handler)
        self.bind('<Triple-Button-1>',self.esc_handler)
        
        self.offsetx = 0
        self.offsety = 0
        
    def dragwin(self,event):
        x = self.winfo_pointerx() - self.offsetx
        y = self.winfo_pointery() - self.offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self.offsetx = event.x
        self.offsety = event.y
    
    def esc_handler(self,event):
        self.destroy()
    
class App():
    def __init__(self):
        self.root = Win()
        self.root.bind("<Right>", self.show_next_image)
        
        self.images = cycle([img for img in os.listdir('.') if img.lower()[-4:] in ('.jpg', '.png', '.gif')])
        self.image = None
    
        self.label = tk.Label(self.root, image=None)
        self.label.configure(borderwidth=0)
        self.label.pack()
    
        self.root.after(100, self.timer_cb) 
        self.root.mainloop()
    
    def timer_cb(self,e=None):
        self.show_next_image()
        self.root.after(SLIDE_SHOW_TIME_MS, self.timer_cb)

    def show_next_image(self, e=None):
        self.new_image = Image.open(next(self.images))
        self.image = None

        # screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        screen_nr = int(self.root.winfo_x() / screen_width)
        screen_center_x = (screen_width / 2) + (screen_nr * screen_width)
        screen_center_y = (screen_height / 2)

        # window
        win_x = self.root.winfo_x()
        win_y = self.root.winfo_y()
        win_width = self.root.winfo_width()
        win_height = self.root.winfo_height()
        win_center_x = win_x + (win_width / 2)
        win_center_y = win_y + (win_height / 2)

        # new image
        img_width, img_height = self.new_image.size
        img_aspect_ratio = float(img_width) / float(img_height)
        
        # calculate new window size
        new_win_height_port = int(screen_height * (WINDOW_HEIGHT_IN_PERCENTAGE_OF_SCREEN_HEIGHT / 100.0))
        
        if img_width > img_height:
            # landscape
            new_win_width = new_win_height_port
            new_win_height = int(new_win_width / img_aspect_ratio)
        else:
            # portrait
            new_win_height = new_win_height_port
            new_win_width = int(new_win_height * img_aspect_ratio)
            
        new_win_size = (new_win_width,new_win_height)
         
        # calculate new window position
        if win_center_x < screen_center_x:
            # left
            new_win_x = win_x
        else:
            # right
            new_win_x = win_x + win_width - new_win_width
            
        if win_center_y < screen_center_y:
            # top
            new_win_y = win_y
        else:
            # bottom
            new_win_y = win_y + win_height - new_win_height
            
        # apply changes
        self.root.geometry('{0}x{1}+{2}+{3}'.format(new_win_width, new_win_height, new_win_x, new_win_y))
        self.image = self.new_image.resize(new_win_size, Image.ANTIALIAS)
        self.label.place(x=0, y=0, width=new_win_width,height=new_win_height)
        tkimage = ImageTk.PhotoImage(self.image)
        self.label.configure(image=tkimage)
        self.label.image = tkimage
        
if __name__ == '__main__': app=App()
