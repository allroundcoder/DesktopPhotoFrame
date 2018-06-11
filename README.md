# DesktopPhotoFrame

Small python Tk application that can be used as a digital photo frame on your desktop. 

Simpy said: It's a small slide show viewer with the following extras:
* No ugly borders
* Always on the foreground.
* No wasted area around photo (window size equal to scaled photo size)
* Smooth switching between different sized photos (no jumps)

## No ugly borders
A flag (overrideredirect) is set to prevent the window manager from controlling the photo window. Because it is not controlled by the window manager, it is also not decorated by the window manager, which means no borders or static buttons (e.g. close window).
  
## Always on the foreground
Another result of the photo window not being controlled by the window manager, is that is stays where it is left. During startup the script puts the window on the foreground. It stays on the foreground, even when other windows are put at the same position.

## No wasted area around photo
In most applications the content size is adapted to the window size. This script uses a different approach. Here the window size is adapted to the scaled photo size. The results in no wasted area around the photos. The longest size of the photo is scaled to a predefined percentage of the screen height. 

## Smooth switching between different sized photos 
The above 'No wasted area around photo' feature may result in different photo window sizes. To prevent the photo window from 'jumping' over the screen it is kind of 'docked'
based on the nearest screen corner. Not the screen corner itself is used, but the corner of the photo image that is closest to a screen corner. The picture below shows how this works when switching between portait and landscape oriënted photos. 

![Alt text](README_images/monitor.png?raw=true "Monitor")

The red dot is the corner that is kept at the same position. It depends on current the position of the photo window on the screen. For each screen quadrant another corner is kept stable. This approach reduces the amount of wasted area around the photo.   

The slideshow example of Jeremy Lowery <https://github.com/jeremylowery/slideshow> was used as a starting point. Thanks Jeremy!


