pixel_width = 32
pixel_height = 8


def fire(neo, inc):
    
    neo.fill(0x000000)
    for y in range(pixel_width):
        height = 1 + round(abs(noise(inc * y * 0.05)) * pixel_height) * 2
        for x in range(pixel_height):
            for n in range(height):
                neo.pixel(y, n , (255, 20, 0))
    
                
