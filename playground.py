# where I test a lot of things
import logging
from threading import Timer


class PixelCountdown(object):
    """
    Class for a countdown displayed by LEDs that blink and change their color.
    Each LED will "count" down for 10 sec by displaying 10 colors (from violet
    over blue, green, yellow, orange, red to dark red).
    To display a countdown of 50 sec, you need 5 LED.
    """

    onTime = 0.8
    offTime = 1 - onTime
    offColor = (140, 0, 0)  # 0 = dark red
    defaultColors = [
        (255,   0,   0),  # 1 = red
        #(255, 140,   0),  # 1 = red-orange
        (255, 164,   0),  # 2 = yellow-orange
        (255, 255,   0),  # 3 = yellow
        (140, 255,   0),  # 4 = light green
        (  0, 255,   0),  # 5 = green
        (  0, 140,   0),  # 6 = dark green
        (  0, 140, 255),  # 7 = blue-green
        (  0,   0, 255),  # 8 = blue
        (  0,   0, 128),  # 9 = navy
        ( 76,   0, 130),  #10 = indigo
    ]
    numColors = len(defaultColors)

    defaultPixels = [
        (3, 3), (4, 3), (3, 4), (4, 4)
    ]


    def __init__(self):
        """init the countdown with default pixel positions (4 pixels)"""
#        self.__init__(defaultPixels)
        #TODO nicht möglich mehrere Konstruktoren zu haben?
        #def __init__(self, pixels):
        #"""init the countdown with pixel positions (a list of (x, y) tuples)"""
        #self.pixels = pixels
        self.pixels = self.defaultPixels
        self.initColors()
        self.t = 0

    def setColors(self, colors):
        self.colors = self.defaultColors
        self.numColors = len(self.colors)
        self.maxDuration = self.numColors * len(self.pixels)
        print("initialized {0} pixels with {1} colors each (so maxDuration={2})"
            .format(len(self.pixels), self.numColors, self.maxDuration))


    def initColors(self):
        self.setColors(self.defaultColors)

    def initPixels(self, duration):
        # TODO throw exeption if duration is longer than self.maxDuration
        self.t = duration
        # display all pixels in the correct color (first color or offColor)
        self.curPixel = self.t // self.numColors;
        self.curColor = self.t % self.numColors;
        for iPixel in range(len(self.pixels)):
            pixel = self.pixels[iPixel]
            if iPixel < self.curPixel:
                # full pixel remaining -> highest color
                self.showPixel(pixel, self.colors[self.numColors - 1])
            elif iPixel > self.curPixel:
                # pixel used -> off color
                self.showPixel(pixel, self.offColor)
            else:
                # partially used pixel -> display correct color
                self.showPixel(pixel, self.colors[self.curColor])

        print("initialized for duration ", duration)


    def update(self):
        if self.t == 0:
            print("expired!")
            return

        # TODO set timer to update after 1 sec
        t = Timer(3.0, self.update)
        t.start() # after 3 seconds, update will be called again

        oldPixel = self.t // self.numColors;
        self.t -= 1
        print('time=', self.t, '  ', end='')
        self.curPixel = self.t // self.numColors;
        self.curColor = self.t % self.numColors;
        if oldPixel != self.curPixel and oldPixel < len(self.pixels):
            # display old pixel in dark red (if there is an old pixel)
            self.showPixel(self.pixels[oldPixel], self.offColor)

        # display current pixel in current color
        self.showPixel(self.pixels[self.curPixel], self.colors[self.curColor])

        # TODO set timer after onTime: self.blink()
        t2 = Timer(3 * self.onTime, self.blink)
        t2.start()


    def blink(self):
        """ switch the current pixel off (will be switched on with the next color)"""
        p = self.pixels[self.curPixel]
        self.clearPixel(p)

    def clearPixel(self, pixel):
        """swtich pixel given pixel off - pixel is tople (x, y)"""
        #print("clear pixel ", pixel)
        print("pixel {0}/{1} is off".format(pixel[0], pixel[1]))


    def showPixel(self, pixel, color):
        """switch pixel given pixel on in the given color - pixel is tople (x, y)"""
        #print("show pixel {0} in color {1} ", pixel)
        print("pixel {0}/{1} is on in color {2}".format(pixel[0], pixel[1], color))


    def getMaxDuration(self):
        return self.maxDuration

    def state(self):
        print("time {0}, pixels: ".format(self.t, self.pixels))


    def start(self, duration):
        if duration > self.maxDuration:
            print("duration too long, will use maxDuration ", self.maxDuration)
            self.t = self.maxDuration
        else:
            self.t = duration
        print ("started countdown: ", self.t)
        self.initPixels(self.t)
        self.update()


cnt = PixelCountdown()

# Initialize
def init():
    print ("in init")
    cnt.state()


if __name__ == "__main__":
    #import sys
    #fib(int(sys.argv[1]))
    init()
