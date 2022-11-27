import board
from random import random
pixel_width = 32
pixel_height = 8

maxbrightness = 255

def weatherEffect(neo, effect, fadeupinc, pointx):
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
        
        randx = round(random() * pixel_width)
        
        for y in range(pixel_height):
            if(x < fadeupinc):
                neo.pixel(x, y, (r, g, b))
            else:
                neo.pixel(x, y, (0, 0, 0))
    
                