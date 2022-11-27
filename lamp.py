import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
from time import sleep
import math
from perlin_noise import PerlinNoise
from datetime import datetime
from time import time
from time import sleep


weather_url = "https://api.openweathermap.org/data/3.0/onecall?lat=51.07&lon=00.04&appid=80c7fa82e62481d23bffb600ecda8f11"
import requests

weather_data = requests.get(weather_url).json()


sunrise_time = weather_data['current']['sunrise']
sunset_time = weather_data['current']['sunset']
weather_next_hour = weather_data['hourly'][1]['weather']


noise = PerlinNoise()

neo_pin = board.D18
pixel_width = 8
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
    weather_next_hour = weather_data['hourly'][1]['weather']
    return [sunrise_time, sunset_time, weather_next_hour]

def effect(effect, brightness_limit):
    
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
    
    neo.fill(0x993333)
    for y in range(pixel_width):
        height = 1 + round(abs(noise(inc * (y * 0.1))) * pixel_height) * 2
        for x in range(pixel_height):
            for n in range(height):
                neo.pixel(y, n , (255, 0, 0))
                
prev_minute = 0
chime_time = 2
while True:
    now = datetime.now()
    curr_minute = now.minute
    
    print(curr_minute)
    # If the current time is a mod of `chime_time`, and has just switched to that time (runs once on time change)
    if(curr_minute % chime_time == 0 and curr_minute != prev_minute):
        weatherdata = getWeather()
        sunrise = weatherdata[0]
        sunset = weatherdata[1]
        mainweather = weatherdata[2]
        print("sunrise", sunrise, "sunset", sunset, "mainweather", mainweather)
    
    pointx += 0.03
    inc += 0.02
    if pointx > pixel_width:
        pointx = 0
    
    if(brightness_limit < maxbrightness):
        brightness_limit += 10
    effect('Clouds', brightness_limit)
    neo.display()
    
    sleep(1)
    
    prev_minute = curr_minute
    
    
