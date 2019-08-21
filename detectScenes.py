from PIL import Image
from numpy import *
from multiprocessing import Pool
import time
# we assume a 256x224 input. Look at docs.
#Blue
blue_spot = (98, 20)
green_spot = (236, 18)
red_spot = (36, 220)
orange_spot = (27, 19)
pink_spot = (133,113)

COPYRIGHT = 0
TITLE = 1
MUSIC = 2
LEVEL = 3
IN_GAME = 4
PAUSE = 5
ROCKET = 6
HIGH_SCORE = 7
UNSURE = -1

intToState = { 0: "COPYRIGHT",
               1: "TITLE",
               2: "MUSIC",
               3: "LEVEL",
               4: "IN_GAME",
               5: "PAUSE",
               6: "ROCKET",
               7: "HIGH_SCORE",
               -1: "UNSURE"
               }

def isGrey(px):
    limit = 64
    return (128 - limit < px[0] < 128 + limit and
            128 - limit < px[1] < 128 + limit and 
            128 - limit < px[2] < 128 + limit)

def isBlack(px):    
    limit = 38
    return (px[0] < limit and
            px[1] < limit and
            px[2] < limit)

def isWhite(px):
    limit = 38
    return (px[0] > 256 - limit and
            px[1] > 256 - limit and
            px[2] > 256 - limit)

def isBlue(px):
    limitr = 100;
    limitb = 75;    
    limitg = 75;

    return (px[0] <= limitr and 
           px[1] <= 256 - limitg and
           px[2] >= 256 - limitb)

def isBlueNotRed(px):
    return px[2] > px[0]
    
def sampleBlock(pixels , spot):
    centre = array(pixels[spot[0],spot[1]])
    right = array(pixels[spot[0]+1,spot[1]])
    br = array(pixels[spot[0]+1,spot[1]+1])
    bl = array(pixels[spot[0]-1,spot[1]+1])
    
    result = (centre+right+br+bl) / 4.0
    return result
    
def decodeFile(filename):
    im = Image.open(filename)
    px = im.load()
    
    r = sampleBlock(px, red_spot)
    g = sampleBlock(px, green_spot)
    b = sampleBlock(px, blue_spot)
    o = sampleBlock(px, orange_spot)
    p = sampleBlock(px, pink_spot)
    
    if (isGrey(r) or isWhite(r))  and isBlack(g) and isBlack(b):
        return IN_GAME
    elif (isBlack(r) and isGrey(g) and isGrey(b)):
        return TITLE
    elif (isGrey(r) and isGrey(g) and isBlack(b)):
        if (isBlueNotRed(o)):
            return HIGH_SCORE
        else:
            return LEVEL
    elif (isBlack(r) and isBlack(g) and isBlack(b)):
        if (isBlack(p)):
            return COPYRIGHT
        else:
            return PAUSE
    elif (isBlue(g) and isBlue(b)):
        return ROCKET
    elif (isGrey(r)):
        return MUSIC
    
    return UNSURE
    
if __name__ == '__main__':
    t = time.time()
    pool = Pool()
    base = "C:/VideoEdit/ctao-preroll/frames/"
    results = pool.map(decodeFile, [base + "%05d" % i + ".png" for i in range (1, 100000)])
    newResult = []
    lastValue = -1
    gameCounter = 0
    for i, val in enumerate(results):
        if val == COPYRIGHT or val == UNSURE:
            continue
        if lastValue != val:
            lastValue = val
            newResult.append([i, intToState[val]])  
            if lastValue == IN_GAME:
                gameCounter += 1
    print (newResult)
    print ("took: " + str(time.time() - t))
    print ("num games:" + str(gameCounter))    
    