from sense_hat import SenseHat
import time
import colorsys

# Mögliche Farben sind im RGB-565-Raum (rot 5 Bits, grün 6 Bits, blau 5 Bits).
@ Also: Rot- und Blau-Anteil durch 8 teilbar, Grün-Anteil durch 4 teilbar

s = SenseHat()
s.low_light = True
#s.low_light = False

def listColors(f):
    for i in range(1,256,4):
        color = f(i)
        pos = i // 4
        x = pos // 8
        y = pos % 8
        s.set_pixel(x, y, color)

def getColorRed(i):
    return (i, 0, 0)

def getColorYellow(i):
    return (i, i, 0)

def getColorGreen(i):
    return (0, i, 0)

def getColorBlue(i):
    return (0, 0, i)

def getColorViolet(i):
    return (i, 0, i)

def getColorRed2Green(i):
    return (i, 256-i, 0)

def getColorGreen2Blue(i):
    return (0, i, 256-i)

def getColorBlue2Red(i):
    return (256-i, 0, i)

def getColorRainbow(i):
    c = i/256
    color = colorsys.hls_to_rgb(c, 0.5, 1)
    return


s.clear()
time.sleep(2)
#listColors(getColorRed)
listColors(getColorRed2Green)
time.sleep(2)
#listColors(getColorGreen2Blue)
listColors(getColorRainbow)
time.sleep(2)
#listColors(getColorBlue2Red)

#listColors(getColorYellow)
#listColors(getColorGreen)
#listColors(getColorBlue)
#listColors(getColorViolet)

