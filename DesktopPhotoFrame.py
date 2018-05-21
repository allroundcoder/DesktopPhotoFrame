import glob
import os
import sys
import time

from PIL import Image
from PIL import ImageTk

if sys.version_info < (3, 0):
    import Tkinter as tk
else:
    import tkinter as tk

class Win(tk.Tk):
    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", 1)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<ButtonPress-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)
        
    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y

class App():
    def __init__(self):
        self.root = Win()
        self.root.pack_propagate(False)
        self._images = [img for img in os.listdir('.') if img.lower()[-4:] in ('.jpg', '.png', '.gif')]
        self._image_pos = -1

        self.root.bind("<space>", self.space_handler)
        self.root.bind("<Escape>", self.esc_handler)
        self.root.bind("<Left>", self.show_previous_image)
        self.root.bind("<Right>", self.show_next_image)
        self.root.bind("q", self.esc_handler)
        self.root.after(100, self.show_next_image)

        self.label = tk.Label(self.root, image=None)
        self.label.configure(borderwidth=0)
        self.label.pack()

        self.set_timer()
        self.root.mainloop()
   
    slide_show_time = 4
    last_view_time = 0
    paused = False
    image = None
    percentage_of_screen_width = 20
    percentage_of_screen_height = 40

    def esc_handler(self, e):
        self.root.destroy()

    def space_handler(self, _):
        self.paused = not self.paused

    def set_timer(self):
        self.root.after(300, self.update_clock)

    def update_clock(self):
        if time.time() - self.last_view_time > self.slide_show_time \
           and not self.paused:
            self.show_next_image()
        self.set_timer()

    def show_next_image(self, e=None):
        fname = self.next_image()
        if not fname:
            return
        self.show_image(fname)

    def show_previous_image(self, e=None):
        fname = self.previous_image()
        if not fname:
            return
        self.show_image(fname)

    def show_image(self, fname):
        self.original_image = Image.open(fname)
        self.image = None
        
        width, height = self.original_image.size
        aspect_ratio = float(width) / float(height)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        if width > height:
            # landscape
            new_width = int(screen_width * (self.percentage_of_screen_width / 100.0))
            new_height = int(new_width / aspect_ratio)  
        else:
            # portrait
            new_height = int(screen_height * (self.percentage_of_screen_height / 100.0))
            new_width = int(new_height * aspect_ratio)
            
        new_size = (new_width,new_height)
        self.root.geometry('%dx%d' % new_size)
        self.image = self.original_image.resize(new_size, Image.ANTIALIAS)
        self.label.place(x=0, y=0, width=new_width,height=new_height)
        tkimage = ImageTk.PhotoImage(self.image)
        self.label.configure(image=tkimage)
        self.label.image = tkimage
        
        self.last_view_time = time.time()
        
    def next_image(self):
        if not self._images: 
            return None
        self._image_pos += 1
        self._image_pos %= len(self._images)
        return self._images[self._image_pos]

    def previous_image(self):
        if not self._images: 
            return None
        self._image_pos -= 1
        return self._images[self._image_pos]

if __name__ == '__main__': app=App()
