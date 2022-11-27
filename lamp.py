import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
from time import sleep
import math
from perlin_noise import PerlinNoise
from datetime import datetime
from time import time
from time import sleep
from dotenv import load_dotenv
import os 

load_dotenv()
print(os.environ.get('weather_key'))
weather_key = os.environ.get('weather_key')
weather_url = "https://api.openweathermap.org/data/3.0/onecall?lat=51.07&lon=00.04&appid=" + weather_key
import requests

weather_data = requests.get(weather_url).json()


sunrise_time = weather_data['current']['sunrise']
sunset_time = weather_data['current']['sunset']
weather_next_hour = weather_data['hourly'][1]['weather']
mainweather = weather_data['hourly'][1]['weather'][0]['main']

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

def getWeather():
    weather_data = requests.get(weather_url).json()
    sunrise_time = weather_data['current']['sunrise']
    sunset_time = weather_data['current']['sunset']
    weather_next_hour = weather_data['hourly'][1]['weather'][0]
    return [sunrise_time, sunset_time, weather_next_hour]

fadeupinc = 1
chimeinc = 0
def chime(chimeinc):
    
    #print(chimeinc)
    #print(math.sin(chimeinc))
    #chimeinc += 1
    wait = 0
    brightness = round(abs(math.sin(chimeinc)) * 255) 
    #print(chimeinc, brightness)
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
                #neo.pixel(x, y, (brightness, brightness, brightness))
                neo.pixel(x, y, (r, g, b))
            else:
                neo.pixel(x, y, (0, 0, 0))
                
            #sleep(0.02)
                
        # Actual effect, runs after inital pass 
        #if(fadeupinc >= pixel_width):
           # neo.pixel(x, y, (brightness, round(brightness * 0.8), brightness))
    
def bffect(effect, brightness_limit):
    
    maxbrightness = 60 + abs(round(math.sin(inc * 0.1) * 185))
    #print(maxbrightness)
    r = maxbrightness
    g = maxbrightness
    b = maxbrightness
    
    
    
    for x in range(pixel_width):
        distFromLightPos1 = abs(pointx - x)
        distFromLightPos2 = abs(pointx - x + pixel_width)
        distFromLightPos3 = abs(pointx - x - pixel_width)
        distFromLightPos = min(distFromLightPos1, min(distFromLightPos2, distFromLightPos3))
        brightness = round(min(distFromLightPos * 55, maxbrightness))
        
        if(effect == 'Clouds'):
            
            r = max(50, maxbrightness)
            g = max(50, brightness)
            b = max(50, brightness)
            
        if(effect == 'Rain'):
            g = brightness
            
        for y in range(pixel_height):
            neo.pixel(x, y, (round(r), round(g), round(b)))

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
while True:
    now = datetime.now()
    curr_minute = now.minute
    
    # If the current time is a mod of `chime_time`, and has just switched to that time (runs once on time change)
    if(curr_minute % chime_time == 0 and curr_minute != prev_minute):
        weatherdata = getWeather()
        print(weatherdata)
        sunrise_time = weatherdata[0]
        sunset_time = weatherdata[1]
        mainweather = weatherdata[2]['main']
        fadeupinc=0
        chime(chimeinc)
        print("sunrise", sunrise_time, "sunset", sunset_time, "mainweather", mainweather)
    
    pointx += 0.1
    inc += 0.02
    if pointx > pixel_width:
        pointx = 0
    
    if(brightness_limit < maxbrightness):
        brightness_limit += 10
        
    
   
    #sleep(1)
    #weathereffect(mainweather, fadeupinc)
    #fire(inc)
    #fadeupinc += 1
    if(fadeupinc <= pixel_width):
        fadeupinc += 0.2
        pointx = fadeupinc
        #sleep(0.05)
        
    neo.display()
    
    
    prev_minute = curr_minute
    
    
