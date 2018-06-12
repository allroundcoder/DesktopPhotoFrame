# DesktopPhotoFrame

Small python Tk application that can be used as a digital photo frame on your desktop. 

Simpy said: It's a small slide show viewer with the following extras:
* Borderless window
* Always on the foreground.
* No wasted window area around photo
* Automatic docking to outmost window corner

## Borderless window
The photo window is free of window decoration (e.g. borders and static buttons) to let it look like a real photo as much as possible.
  
## Always on the foreground (does not work on a Mac)
The photo window stays on the foreground, on top of all other windows.

## No wasted window area around photo
The photo window size is fit to the scaled photo size, to prevent waste of window area around the photo. The longest side of the photo is scaled to a predefined percentage of the screen height. 

## Automatic docking to outmost window corner 
When switching between different photos, the outmost window corner (closest to a screen corner) is kept stable to prevent the photo window from 'jumping' over the screen.

The picture below shows how the docking works when switching between portait and landscape oriënted photos. 

![Alt text](README_images/monitor.png?raw=true "Monitor")

The red dot represents the outmost window corner in each of the four screen quadrants.   

## Acknowledgement

The slideshow example of Jeremy Lowery <https://github.com/jeremylowery/slideshow> was used as a starting point. Thanks Jeremy!


