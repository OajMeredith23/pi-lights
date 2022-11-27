import board
import neopixel
import requests
from adafruit_pixel_framebuf import PixelFramebuffer
from time import sleep
import math
from perlin_noise import PerlinNoise
from datetime import datetime
from time import time
from time import sleep
from dotenv import load_dotenv
import os 
from getweather import getWeather

load_dotenv()
print(os.environ.get('weather_key'))
weather_key = os.environ.get('weather_key')
weather_url = "https://api.openweathermap.org/data/3.0/onecall?lat=51.07&lon=00.04&appid=" + weather_key


weather_data = requests.get(weather_url).json()

weatherdata = getWeather()
sunrise_time = weatherdata[0]
sunset_time = weatherdata[1]
mainweather = weatherdata[2]['main']
noise = PerlinNoise()

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
    rotation=2
    )


def dist(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5
goingUp = True
inc = 1

maxbrightness = 255
brightness_limit = 0;
pointx = 12
pointy = 4
fadeupinc = 1
chimeinc = 0
def chime(chimeinc):
    
    wait = 0
    print("chiming")
    brightness = round(abs(math.sin(chimeinc)) * 255) 
    #print(chimeinc, brightness)
    
    if(chimeinc > 3 and brightness < 10):
        return
    for x in range(pixel_width):
        for y in range(pixel_height):
            neo.pixel(x, y, (brightness, round(brightness / 4), 0))
    #sleep(0.5)
    
            
def weathereffect(effect, fadeupinc):
    y = 4
    
    for x in range(pixel_width):
        distFromLightPos1 = abs(pointx - x)
        distFromLightPos2 = abs(pointx - x + pixel_width)
        distFromLightPos3 = abs(pointx - x - pixel_width)
        distFromLightPos = min(distFromLightPos1, min(distFromLightPos2, distFromLightPos3))
        brightness = min(50 + round(min(distFromLightPos * 20, maxbrightness)), 255)
        
        
        if(effect == 'Clouds'):
            r = round(brightness)
            g = round(brightness)
            b = round(brightness)
        if(effect == 'Rain'):
            r = round(brightness / 2)
            g = round(brightness / 4)
            b = round(brightness)
        for y in range(pixel_height):
            if(x < fadeupinc):
                neo.pixel(x, y, (r, g, b))
            else:
                neo.pixel(x, y, (0, 0, 0))
                
          
def fire(inc):
    
    neo.fill(0x000000)
    for y in range(pixel_width):
        height = 1 + round(abs(noise(inc * y * 0.05)) * pixel_height) * 2
        for x in range(pixel_height):
            for n in range(height):
                neo.pixel(y, n , (255, 20, 0))
                
prev_minute = 0
chime_time = 1
chime_wait = 0
chiming = False
bedtime = 23

while True:
    now = datetime.now()
    curr_minute = now.minute
    print(now.second)
    
    isAfterSunrise = int(now.timestamp()) > sunrise_time
    isAfterSunset = int(now.timestamp()) > sunset_time
    isDaytime =  not isAfterSunset and  isAfterSunrise
    isNighttime = now.hour >= bedtime and not isAfterSunrise
    
    # If the current time is a mod of `chime_time`, and has just switched to that time (runs once on time change)
    if(not isNighttime and curr_minute % chime_time == 0):
        chiming = True
        if(now.second < 6):
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
    
    if(brightness_limit < maxbrightness):
        brightness_limit += 10
        

    
    if(not isNighttime and not chiming):
        if(isDaytime):
            weathereffect(mainweather, fadeupinc)
        
        if(isAfterSunset):
            fire(inc)
            
        if(fadeupinc <= pixel_width):
            fadeupinc += 0.2
            pointx = fadeupinc
    
    if(isNighttime):
        neo.fill(0x000000)
    
    neo.display()
    
    
    prev_minute = curr_minute
    
    
