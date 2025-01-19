import pygame as pg
import random, math
from datetime import datetime

pg.init()

# Constants
W, H = 1500, 900

screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

offsetX = 30
offsetY = 30

amountSegmentsW = 10
amountSegmentsH = 5

wSegmentLength = (W - 2 * offsetX) / (amountSegmentsW - 1)
hSegmentLength = (H - 2 * offsetY) / (amountSegmentsH - 1)

segmentDepth = 3

timeRange = (1, 7)
pauseRange = (1, 7)
probabilityRange = (1, 100) # 100 ->  1/100 chance of showing a segment 60 times a frame

# segments

class Segment:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y

        self.s = pg.Surface((w, h), pg.SRCALPHA)

        self.s.fill((255, 255, 255))

        self.s.set_alpha(0)

        self.showProcess = False
        self.hideProcess = False
        self.pause = 0
        self.m = 0
        self.shown = False

        self.important = False
        self.importantOn = False
        self.importantOff = False

    def show(self, time):
        self.showProcess = True
        self.shown = False

        self.m = 255 / time

    def hide(self, time, pause):
        self.hideProcess = True
        self.shown = False
        self.pause = pause

        self.m = 255 / time

    def draw(self, dt):
        global segmentDepth, wSegmentLength, hSegmentLength

        if self.important:
            self.s.fill((255, 0, 0))
        elif self.shown == False and self.hideProcess == False:
            self.s.fill((255, 255, 255))

        if self.showProcess:
            newAlpha = math.ceil(self.s.get_alpha() + self.m * dt)
            if newAlpha >= 255:
                newAlpha = 255
                self.showProcess = False
                self.shown = True
            self.s.set_alpha(newAlpha)

        elif self.hideProcess:
            newAlpha = math.floor(self.s.get_alpha() - self.m * dt)
            if newAlpha <= 0:
                newAlpha = 0
                self.hideProcess = False
                self.shown = False
            self.s.set_alpha(newAlpha)

        elif self.pause > 0:
            self.pause -= dt
            if self.pause <= 0:
                self.pause = 0

        screen.blit(self.s, (self.x, self.y))

numbersX = [
    [1, 0, 1],
    [0, 0, 0],
    [1, 1, 1],
    [1, 1, 1],
    [0, 1, 0],
    [1, 1, 1],
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1],
    [1, 1, 1]
]

numbersY = [
    [1, 1, 1, 1],
    [0, 0, 1, 1],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 1, 1, 1],
    [1, 0, 1, 1]
]


def numbersXToSegmentIndex(offsetX, offsetY, number):
    indizes = []
    for i in range(len(number)):
        indizes.append(offsetY + i + offsetX * amountSegmentsH)
        if number[i] == 1:
            allSegments[indizes[-1]].important = True
            allSegments[indizes[-1]].importantOn = True
        else:
            allSegments[indizes[-1]].importantOff = True

    return indizes

def numbersYToSegmentIndex(offsetX, offsetY, number):
    indizes = []
    for i in range(len(number)):
        if i < 2:
            indizes.append(len(segmentsX) + offsetY + i + offsetX * (amountSegmentsH - 1))
        else:
            indizes.append(len(segmentsX) + offsetY + amountSegmentsH + i - 3 + offsetX * (amountSegmentsH - 1))

        if number[i] == 1:
            allSegments[indizes[-1]].important = True
            allSegments[indizes[-1]].importantOn = True
        else:
            allSegments[indizes[-1]].importantOff = True

    return indizes

# generate segments
segmentsX = []
segmentsY = []

for i in range(amountSegmentsW):
    for j in range(amountSegmentsH):
        if i != amountSegmentsW - 1:
            segmentsX.append(Segment(i * wSegmentLength + offsetX, j * hSegmentLength + offsetY, wSegmentLength, segmentDepth))
        if j != amountSegmentsH - 1:
            segmentsY.append(Segment(i * wSegmentLength + offsetX, j * hSegmentLength + offsetY, segmentDepth, hSegmentLength))

allSegments = segmentsX + segmentsY

indizes = []
showTime = False
currentNum = 9

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                showTime = not showTime

                # lol += 1

    dt = clock.tick(60) / 1000

    screen.fill((0, 0, 0))

    s: Segment
    for s in allSegments:
        
        if s.important:
            continue

        if s.shown == True and s.hideProcess == False:
            s.hide(random.randint(timeRange[0], timeRange[1]), random.randint(pauseRange[0], pauseRange[1]))
    
        if s.shown == False and s.pause == 0 and random.randint(probabilityRange[0], probabilityRange[1]) == 1:
            s.show(random.randint(timeRange[0], timeRange[1]))

    # for i in range(lol):
    #     allSegments[i].show(1)

    if showTime:
        if len(indizes) == 0:
            now = datetime.now()

            l = now.strftime("%H:%M").split(":")

            indizes = numbersXToSegmentIndex(1, 1, numbersX[int(l[0][0])]) + numbersYToSegmentIndex(1, 1, numbersY[int(l[0][0])])
            indizes += numbersXToSegmentIndex(3, 1, numbersX[int(l[0][1])]) + numbersYToSegmentIndex(3, 1, numbersY[int(l[0][1])])
            indizes += numbersXToSegmentIndex(5, 1, numbersX[int(l[1][0])]) + numbersYToSegmentIndex(5, 1, numbersY[int(l[1][0])])
            indizes += numbersXToSegmentIndex(7, 1, numbersX[int(l[1][1])]) + numbersYToSegmentIndex(7, 1, numbersY[int(l[1][1])])

        for i in indizes:
            if allSegments[i].importantOn:
                if random.randint(0, 40) == 1:
                    allSegments[i].show(random.randint(timeRange[0], timeRange[1]))
            else:
                allSegments[i].hide(random.randint(timeRange[0], timeRange[1]), random.randint(pauseRange[0], pauseRange[1]))
    else:
        for i in indizes:
            allSegments[i].important = False
            allSegments[i].importantOn = False
            allSegments[i].importantOff = False
        indizes = []

    for s in allSegments:
        s.draw(dt)

    pg.display.flip()