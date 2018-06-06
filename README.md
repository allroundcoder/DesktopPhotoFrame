# DesktopPhotoFrame

Small python Tk application that can be used as a digital photo frame on your desktop. 

## My use case

I started writing this small script for the reason that I like to have some family photos around at my work place, but without big photo frames on my desk. Having it in digital form on the desktop would solve this issue. Of course there are already a lot of other tools/scripts that can show photos on the desktop.

However, I was not able to find an application that would exactly fit my needs/wishes:
* display portrait and landscape photo, without wasted area around it.
* always on the foreground.
* keep one corner at the same position when switching between portrait and landscape (but no docking)
* slideshow possibility
* ...
  
The figure below shows what is meant by 'keep one corner at the same position when switching between portrait and landscape'. 

![Alt text](README_images/monitor.png?raw=true "Monitor")

The red dot is the corner that is kept at the same position. It depends on current the position of the photo frame window on the screen. For each screen quadrant another corner is kept stable. This approach reduces the amount of wasted area around the photo.   


The slideshow example of Jeremy Lowery <https://github.com/jeremylowery/slideshow> was used as a starting point. Thanks Jeremy!


