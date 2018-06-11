# DesktopPhotoFrame

Small python Tk application that can be used as a digital photo frame on your desktop. 

Simpy said: It's a small slide show viewer with the following extras:
* No ugly borders
* Always on the foreground.
* No wasted area around photo (window size equal to scaled photo size)
* Smooth switching between different sized photos (no jumps)

## No ugly borders
The photo window is not controlled or decorated by the window manager, which results in no borders or static buttons (e.g. close window).
  
## Always on the foreground
During startup the script puts the photo window on the foreground. It stays on the foreground, even when other windows are put at the same position.

## No wasted area around photo
The photo window size is adapted to the scaled photo size. This results in no wasted area around the photos. The longest size of the photo is scaled to a predefined percentage of the screen height. 

## Smooth switching between different sized photos 
The above 'No wasted area around photo' feature may result in different photo window sizes. To prevent the photo window from 'jumping' over the screen it is kind of 'docked'
based on the nearest screen corner. Not the screen corner itself is used, but the corner of the photo image that is closest to a screen corner. The picture below shows how this works when switching between portait and landscape oriënted photos. 

![Alt text](README_images/monitor.png?raw=true "Monitor")

The red dot is the corner where the photo window is 'docked' to.   

The slideshow example of Jeremy Lowery <https://github.com/jeremylowery/slideshow> was used as a starting point. Thanks Jeremy!


