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
# Slide show time in milliseconds.
SLIDE_SHOW_TIME_MS = 300 * 1000

# Window height in portrait orientation. The same value is used
# for the window width in landscape orientation.
WINDOW_HEIGHT_IN_PERCENTAGE_OF_SCREEN_HEIGHT = 30

# Button size in pixels
BUTTON_SIZE_PX = 20

# Window opacity when mouse button is down within window area
# (value between 0.0 and 1.0)
MOUSE_BUTTON_DOWN_OPACITY = 0.3
###################

class Win(tk.Tk):
    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.config(bg="black", width=1, height=1)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", 1)
        self.pack_propagate(False)
        
        self.offsetx = 0
        self.offsety = 0
        
        self.canvas = tk.Canvas(self,borderwidth=0,highlightthickness=0)
        self.canvas_image = self.canvas.create_image(0,0,anchor=tk.NW,image=None)
        self.quit_button = tk.Button(self, text = "x", command = self.close, borderwidth=0)
        self.quit_button_window = self.canvas.create_window(0, 0, anchor='nw', width=BUTTON_SIZE_PX,height=BUTTON_SIZE_PX, window=self.quit_button, state='hidden')
        self.minimize_button = tk.Button(self, text = "-", command = self.minimize, borderwidth=0)
        self.minimize_button_window = self.canvas.create_window(BUTTON_SIZE_PX, 0, anchor='nw', width=BUTTON_SIZE_PX,height=BUTTON_SIZE_PX,window=self.minimize_button, state='hidden')
        self.canvas.pack(expand = True, fill = "both")
        
        self.bind('<ButtonPress-1>',self.mouse_button_press)
        self.bind('<ButtonRelease-1>',self.mouse_button_release)
        self.bind('<B1-Motion>',self.dragwin)
        self.bind("<Configure>", self.restore)
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        
    def enter(self,event):
        self.canvas.itemconfigure(self.quit_button_window,state = 'normal')
        self.canvas.itemconfigure(self.minimize_button_window,state = 'normal')
                
    def leave(self,event):
        if str(event.widget) == '.':
            self.canvas.itemconfigure(self.quit_button_window,state = 'hidden')
            self.canvas.itemconfigure(self.minimize_button_window,state = 'hidden')
        
    def dragwin(self,event):
        x = self.winfo_pointerx() - self.offsetx
        y = self.winfo_pointery() - self.offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def mouse_button_press(self,event):
        self.offsetx = event.x
        self.offsety = event.y
        self.wm_attributes('-alpha', MOUSE_BUTTON_DOWN_OPACITY)
        
    def mouse_button_release(self,event):
        self.wm_attributes('-alpha', 1.0)
        
    def close(self,event=None):
        self.destroy()
        
    def minimize(self,event=None):
        self.overrideredirect(False)
        self.wm_state('iconic')
    
    def restore(self,event):
        if self.winfo_viewable():
            self.overrideredirect(True)    
    
    @property
    def is_viewable(self):
        return self.winfo_viewable()
    
class App():
    def __init__(self):
        self.root = Win()
        self.root.bind("<Right>", self.show_next_image)
        
        self.images = cycle([img for img in os.listdir('.') if img.lower()[-4:] in ('.jpg', '.png', '.gif')])
        self.image = None
    
        self.root.after(100, self.timer_cb) 
        self.root.mainloop()
    
    def timer_cb(self,e=None):
        if self.root.is_viewable:
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
        new_img_width, new_img_height = self.new_image.size
        new_img_aspect_ratio = float(new_img_width) / float(new_img_height)
        
        # calculate new window size
        new_win_height_port = int(screen_height * (WINDOW_HEIGHT_IN_PERCENTAGE_OF_SCREEN_HEIGHT / 100.0))
        
        if new_img_width > new_img_height:
            # landscape
            new_win_width = new_win_height_port
            new_win_height = int(new_win_width / new_img_aspect_ratio)
        else:
            # portrait
            new_win_height = new_win_height_port
            new_win_width = int(new_win_height * new_img_aspect_ratio)
            
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
        self.image = ImageTk.PhotoImage(self.new_image.resize(new_win_size, Image.ANTIALIAS))
        self.root.canvas.itemconfig(self.root.canvas_image, image=self.image)
        
if __name__ == '__main__': app=App()
