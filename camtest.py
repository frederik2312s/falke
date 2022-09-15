from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image, ImageDraw, ImageFont
import time
import numpy as np
import string
import random
import os

w,h=1920,1080
wo,ho=int(w*10/16),int(h*7/16)
ws,hs=int(w*6/16),int(h*3/16)
we,he=int(w*6/16),int(h*4/16)
wl,hl=int(w*16/16),int(h*9/16)
xo,yo=int(w*0/16),int(h*9/16)
xs,ys=int(w*10/16),int(h*13/16)
xe,ye=int(w*10/16),int(h*9/16)
xl,yl=int(w*0/16),int(h*0/16)

camera = PiCamera()
camera.resolution = (w,h)
camera.framerate = 32
#rawCapture = PiRGBArray(camera, size=(640,480))
font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 40)

#create overlay
overlaycanvasoptionsmaster=Image.new('RGB',(wo,ho))
overlaycanvasstatusmaster=Image.new('RGB',(ws,hs))
#overlaycanvasenvironmentmaster=Image.new('RGB',(we,he))
overlaycanvaslivefeedmaster=Image.new('RGB',(wl,hl))


camera.start_preview()
overlaycanvasoptions=overlaycanvasoptionsmaster.copy()
overlaycanvasstatus=overlaycanvasstatusmaster.copy()
#overlaycanvasenvironment=overlaycanvasenvironmentmaster.copy()
overlaycanvaslivefeed=overlaycanvaslivefeedmaster.copy()

options=camera.add_overlay(overlaycanvasoptions.tobytes(),size=(wo,ho),format='rgb',layer=3,alpha=64,fullscreen=False,window=(xo,yo,xo+wo-1,yo+ho-1))
time.sleep(1)
status=camera.add_overlay(overlaycanvasstatus.tobytes(),size=(ws,hs),format='rgb',layer=4,alpha=128,fullscreen=False,window=(xs,ys,xs+ws-1,ys+hs-1))
time.sleep(1)
#environment=camera.add_overlay(overlaycanvasenvironment.tobytes(),size=(we,he),format='rgb',layer=5,alpha=192,fullscreen=False,window=(xe,ye,xe+we-1,ye+he-1))
livefeed=camera.add_overlay(overlaycanvaslivefeed.tobytes(),size=(wl,hl),format='rgb',layer=6,alpha=255,fullscreen=False,window=(xl,yl,xl+wl-1,yl+hl-1))

i=0

try:
	while True:
		#overlay=overlaycanvas.copy()
		#drawoverlay=ImageDraw.Draw(overlay)
		#drawoverlay.text((20,20),"hello",font=font,fill=(255,255,255))
		#menu.update(overlay.tobytes())
		options.update(overlaycanvasoptions.tobytes())
		time.sleep(1)
		status.update(overlaycanvasstatus.tobytes())
		time.sleep(1)
		#environment.update(overlaycanvasenvironment.tobytes())
		livefeed.update(overlaycanvaslivefeed.tobytes())
		time.sleep(1)
except KeyboardInterrupt:
	camera.remove_overlay(menu)
	camera.stop_preview()
finally:
	camera.remove_overlay(menu)


#camera.start_preview()


#shape=[20,20,80,80]
#img=Image.new("RGB",(100,100))
#ImageDraw.Draw(img).rectangle(shape,outline='red')
#img.show()
#time.sleep(15)
camera.stop_preview()
