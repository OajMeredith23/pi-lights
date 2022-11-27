import board
import neopixel
import requests
from adafruit_pixel_framebuf import PixelFramebuffer
from time import sleep
import math
from datetime import datetime
from time import time
from time import sleep
from getweather import getWeather
from weathereffect import weatherEffect
from fire import fire
from flask import Flask, render_template, request



neo_pin = board.D18
pixel_width = 32
pixel_height = 8

pixels = neopixel.NeoPixel(
    neo_pin,
    pixel_width * pixel_height,
    brightness = 0.1,
    auto_write=False
    )

neo = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    orientation='VERTICAL',
    rotation=0
    )

mode = 0
app = Flask(__name__)

 
 
def dist(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def chime(chimeinc):
    
    wait = 0
    brightness = round(abs(math.sin(chimeinc)) * 255) 
    #print(chimeinc, brightness)
    
    if(chimeinc > 3 and brightness < 10):
        return
    for x in range(pixel_width):
        for y in range(pixel_height):
            neo.pixel(x, y, (brightness, round(brightness / 4), 0))
    #sleep(0.5)
    
          

  

def lights(mode):
    weatherdata = getWeather()
    sunrise_time = weatherdata[0]
    sunset_time = weatherdata[1]
    mainweather = weatherdata[2]['main']
    
    
    inc = 1
    fadeupinc = 1
    chimeinc = 0

    prev_minute = 0
    chime_time = 15
    chime_wait = 0
    chiming = False
    bedtime = 23
    pointx = 0

    while True:
        print("MODE", mode)
        now = datetime.now()
        curr_minute = now.minute
        
        
        isAfterSunrise = int(now.timestamp()) > sunrise_time
        isAfterSunset = int(now.timestamp()) > sunset_time
        isDaytime =  not isAfterSunset and  isAfterSunrise
        isNighttime = now.hour >= bedtime and not isAfterSunrise
        
        # If the current time is a mod of `chime_time`, and has just switched to that time (runs once on time change)
        if(not isNighttime and curr_minute % chime_time == 0):
            chiming = True
            if(now.second < 9):
                chimeinc += 0.02
                chime(chimeinc)
            else:
                chiming = False
            if(curr_minute != prev_minute):
                weatherdata = getWeather()
                print(weatherdata)
                sunrise_time = weatherdata[0]
                sunset_time = weatherdata[1]
                mainweather = weatherdata[2]['main']
                fadeupinc=0
                print("sunrise", sunrise_time, "sunset", sunset_time, "mainweather", mainweather)
        
        pointx += 0.1
        inc += 0.02
        if pointx > pixel_width:
            pointx = 0
        
        
        if(not isNighttime and not chiming):
            if(isDaytime):
                weatherEffect(neo, mainweather, fadeupinc, pointx)
            
            if(isAfterSunset):
                fire(neo, inc)
                
            if(fadeupinc <= pixel_width):
                fadeupinc += 0.2
                pointx = fadeupinc
        
        if(isNighttime):
            neo.fill(0x000000)
        
        neo.display()
        
        
        prev_minute = curr_minute
    

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    args = request.args
    templateData = {
      'mode' : args.get('mode')
    }
    args = request.args
#     lights('index')
    print("args", args.get('mode'))
    return render_template('index.html', **templateData)
# 
# @app.route('/<page_name>/')
# def render_static(page_name):
#     templateData = {
#       'mode' : page_name
#     }
# 
#     lights(page_name)
#     return render_template('index.html', **templateData)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
