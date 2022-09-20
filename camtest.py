from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image, ImageDraw, ImageFont
import time
import datetime
import math
import numpy as np
import string
import random
import os
import keyboard
import xml.etree.ElementTree as ET

tstart = datetime.datetime.now()

menuposition = np.array([1, 1, 1], np.int32)
pos = "root[0]"

modes = 2
# range
rangetype = 0
rangefaction = 0
rangedomain = 0
rangeclass = 0
rangemodel = 0
rangevalue = 0
model = ""
rangestep = 3
rangestepval = 100
sizeat100m = 200
label = ""
value = 0
# setup
setupoption = 0
# system
recording = False

tree = ET.parse('database/vehicles-short.xml')
root = tree.getroot()

# display size		TODO: fetch output resolution
w, h = 1920, 1080
dw, dh = w / 16, h / 16
line = int(dh / 2)
# size
wp, hp = int(dw * 10), int(dh * 8)  # picture
wr, hr = int(dw * 10), int(dh * 7)  # resized picture
wt, ht = int(dw * 5), int(dh * 3)  # target
ws, hs = int(dw * 6), int(dh * 7)  # status
wl, hl = int(dw * 16), int(dh * 9)  # livefeed
# position
xp, yp = int(dw * 6), int(dh * 8)  # picture
xr, yr = int(dw * 6), int(dh * 9)  # resized picture
xt, yt = int(dw * 11), int(dh * 3)  # target
xs, ys = int(dw * 0), int(dh * 9)  # status
xl, yl = int(dw * 0), int(dh * 0)  # livefeed

camera = PiCamera()
camera.resolution = (int(dw * 16), int(dh * 9))
camera.window = (xl, yl, wl, hl)
camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(640,480))
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", int(dh / 3))

# create overlay masters
overlaycanvaspicturemaster = Image.new('RGB', (wp, hp))
overlaycanvastargetmaster = Image.new('RGB', (wt, ht))
overlaycanvasstatusmaster = Image.new('RGB', (ws, hs))
overlaycanvaslivefeedmaster = Image.new('RGB', (wl, hl))

# create work files from masters
overlaycanvaspicture = overlaycanvaspicturemaster.copy()
overlaycanvastarget = overlaycanvastargetmaster.copy()
overlaycanvasstatus = overlaycanvasstatusmaster.copy()
overlaycanvaslivefeed = overlaycanvaslivefeedmaster.copy()

# create overlays from work files
picture = camera.add_overlay(overlaycanvaspicture.tobytes(), size=(wp, hp), format='rgb', layer=5, alpha=32,
                             fullscreen=False, window=(xp, yp, wp, hp))
target = camera.add_overlay(overlaycanvastarget.tobytes(), size=(wt, ht), format='rgb', layer=6, alpha=32,
                            fullscreen=False, window=(xt, yt, wt, ht))
status = camera.add_overlay(overlaycanvasstatus.tobytes(), size=(ws, hs), format='rgb', layer=3, alpha=0,
                            fullscreen=False, window=(xs, ys, ws, hs))
livefeed = camera.add_overlay(overlaycanvaslivefeed.tobytes(), size=(wl, hl), format='rgb', layer=4, alpha=0,
                              fullscreen=False, window=(xl, yl, wl, hl))


def switchmode():
    menuposition[0] += 1
    if menuposition[0] > modes:
        menuposition[0] = 1


def switchstep():
    global rangestep, rangestepval
    rangestep += 1
    if rangestep > 4: rangestep = 1
    if rangestep == 1:
        rangestepval = 25
    elif rangestep == 2:
        rangestepval = 50
    elif rangestep == 3:
        rangestepval = 100
    elif rangestep == 4:
        rangestepval = 200


def calinc():
    global sizeat100m
    sizeat100m += 1


def caldec():
    global sizeat100m
    sizeat100m -= 1


def camcapture():
    camera.capture('/capture/{timestamp}.png', format='png')


def camrecord():
    global recording
    if not recording:
        camera.start_recording('/capture/{timestamp}.h264', format='h264')
    if recording:
        camera.stop_recording()
    recording ^= recording


def rangenext():
    global rangetype, rangefaction, rangedomain, rangeclass, rangemodel, rangevalue, rangestep
    if menuposition[1] == 1:
        rangetype += 1
        if rangetype == len(root):
            rangetype = 0
    elif menuposition[1] == 2:
        rangefaction += 1
        if rangefaction == len(root[rangetype]):
            rangefaction = 0
    elif menuposition[1] == 3:
        rangedomain += 1
        if rangedomain == len(root[rangetype][rangefaction]):
            rangedomain = 0
    elif menuposition[1] == 4:
        rangeclass += 1
        if rangeclass == len(root[rangetype][rangefaction][rangedomain]):
            rangeclass = 0
    elif menuposition[1] == 5:
        rangemodel += 1
        if rangemodel == len(root[rangetype][rangefaction][rangedomain][rangeclass]):
            rangemodel = 0
    elif menuposition[1] == 6:
        rangevalue += rangestepval
        if rangevalue > 4000:
            rangevalue = 4000


def rangeprev():
    global rangetype, rangefaction, rangedomain, rangeclass, rangemodel, rangevalue, rangestep
    if menuposition[1] == 1:
        rangetype -= 1
        if rangetype < 0:
            rangetype = len(root[rangetype]) - 1
    elif menuposition[1] == 2:
        rangefaction -= 1
        if rangefaction < 0:
            rangefaction = len(root[rangetype][rangefaction]) - 1
    elif menuposition[1] == 3:
        rangedomain -= 1
        if rangedomain < 0:
            rangedomain = len(root[rangetype][rangefaction][rangedomain]) - 1
    elif menuposition[1] == 4:
        rangeclass -= 1
        if rangeclass < 0:
            rangeclass = len(root[rangetype][rangefaction][rangedomain][rangeclass]) - 1
    elif menuposition[1] == 5:
        rangemodel -= 1
        if rangemodel < 0:
            rangemodel = len(root[rangetype][rangefaction][rangedomain][rangeclass][rangemodel]) - 1
    elif menuposition[1] == 6:
        rangevalue -= rangestepval
        if rangevalue < 0:
            rangevalue = 0


def rangefwd():
    menuposition[1] += 1
    if menuposition[1] == 7: menuposition[1] = 0


def rangeback():
    menuposition[1] -= 1


def select(direction):
    if menuposition[0] == 1:  # rangefinder
        if menuposition[1] == 0:  # rangefinder main
            if direction == "u": switchmode()
            if direction == "d": menuposition[1] = 1
            if direction == "l": camcapture()
            if direction == "r": camrecord()
        else:  # rangefinder sub
            if direction == "u": rangeback()
            if direction == "d": rangefwd()
            if direction == "l": rangeprev()
            if direction == "r": rangenext()
        rangeupdate()
    elif menuposition[0] == 2:  # calibrate
        if direction == "u": switchmode()
        if direction == "d": switchstep()
        if direction == "l": caldec()
        if direction == "r": calinc()


def rangeupdate():
    global label, value, rangevalue, model
    if menuposition[1] == 0:
        label = "RANGEFINDER"
        value = ""
    if menuposition[1] == 1:
        label = "TYPE"
        value = root[rangetype].tag
    if menuposition[1] == 2:
        label = "FACTION"
        value = root[rangetype][rangefaction].tag
    if menuposition[1] == 3:
        label = "DOMAIN"
        value = root[rangetype][rangefaction][rangedomain].tag
    if menuposition[1] == 4:
        label = "CLASS"
        value = root[rangetype][rangefaction][rangedomain][rangeclass].tag
    if menuposition[1] == 5:
        label = "MODEL"
        value = root[rangetype][rangefaction][rangedomain][rangeclass][rangemodel].tag
        model = value
    if menuposition[1] == 6:
        label = "RANGE"
        value = rangevalue
    # print(label + " " + str(value))
    rfdraw()


def rfdraw():
    global label, value, model

    overlaycanvaspicture = overlaycanvaspicturemaster.copy()
    drawpicture = ImageDraw.Draw(overlaycanvaspicture)
    drawpicture.text((20, 0), label + ": " + str(value), font=font, fill=(255, 255, 255))  # current selection

    if menuposition[1] >= 5:
        image = Image.open(model + ".jpg")
        image.thumbnail((wr, hr))
        overlaycanvaspicture.paste(image, (dh, 0))  # picture of selected model
    picture.update(overlaycanvaspicture.tobytes())


def statusdraw():
    global tstart
    tloc = datetime.datetime.now().strftime("%H:%M:%S")
    tutc = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    tup = tstart - datetime.datetime.now()
    overlaycanvasstatus = overlaycanvasstatusmaster.copy()
    drawstatus = ImageDraw.Draw(overlaycanvasstatus)
    drawstatus.text((0, int(0 * line)), "STATUS", font=font, fill=(255, 255, 255))
    drawstatus.text((0, int(1 * line)), "LOC: " + tloc, font=font, fill=(255, 255, 255))
    drawstatus.text((0, int(2 * line)), "UTC: " + tutc, font=font, fill=(255, 255, 255))
    drawstatus.text((0, int(3 * line)), "UP:  " + tup, font=font, fill=(255, 255, 255))
    drawstatus.text((0, int(4 * line)), "BAT: ", font=font, fill=(255, 255, 255))
    drawstatus.text((0, int(5 * line)), "LON: ", font=font, fill=(255, 255, 255))
    drawstatus.text((0, int(6 * line)), "LAT: ", font=font, fill=(255, 255, 255))
    drawstatus.text((0, int(7 * line)), "CMP: ", font=font, fill=(255, 255, 255))
    drawstatus.text((0, int(8 * line)), "ELV: ", font=font, fill=(255, 255, 255))
    drawstatus.text((0, int(9 * line)), "INC: ", font=font, fill=(255, 255, 255))
    status.update(overlaycanvasstatus.tobytes())


keyboard.add_hotkey('w', lambda: select('u'))
keyboard.add_hotkey('s', lambda: select('d'))
keyboard.add_hotkey('a', lambda: select('l'))
keyboard.add_hotkey('d', lambda: select('r'))

# try:
while True:
    # overlay=overlaycanvas.copy()
    # drawoverlay=ImageDraw.Draw(overlay)
    # drawoverlay.text((20,20),"hello",font=font,fill=(255,255,255))
    # menu.update(overlay.tobytes())
    statusdraw()
    # status.update(overlaycanvasstatus.tobytes())
    # environment.update(overlaycanvasenvironment.tobytes())
    time.sleep(0.2)
'''
except KeyboardInterrupt:
    exit()

finally:
    exit()
'''
