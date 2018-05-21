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
        self.root.config(bg="black", width=500, height=500)
        self._fullscreen = True
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
        self.check_image_size()

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
        self.fit_to_box()
        self.last_view_time = time.time()

    def check_image_size(self):
        if not self.image:
            return
        self.fit_to_box()

    def scaled_size(self, width, height, box_width, box_height):
        source_ratio = width / float(height)
        box_ratio = box_width / float(box_height)
        if source_ratio < box_ratio:
            return int(box_height/float(height) * width), box_height
        else:
            return box_width, int(box_width/float(width) * height)

    def fit_to_box(self):
        if self.image:
            if self.image.size[0] == self.box_width: return
            if self.image.size[1] == self.box_height: return
        width, height = self.original_image.size
        new_size = self.scaled_size(width, height, self.box_width, self.box_height)
        self.image = self.original_image.resize(new_size, Image.ANTIALIAS)
        self.label.place(x=self.box_width/2, y=self.box_height/2, anchor=tk.CENTER)
        tkimage = ImageTk.PhotoImage(self.image)
        self.label.configure(image=tkimage)
        self.label.image = tkimage

    @property
    def box_width(self):
        return self.root.winfo_width()

    @property
    def box_height(self):
        return self.root.winfo_height()

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