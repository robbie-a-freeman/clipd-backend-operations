import numpy as np
from PIL import ImageGrab
from PIL import Image
import time
import keyboard
import winsound

pils = []
path = 'C:/Users/Robbie/Documents/GitHub/clipd-backend/data'
while True:
    print("wait")
    time.sleep(1.0)
    print("snap")
    printscreen_pil =  ImageGrab.grab()
    pils.append(printscreen_pil)
    winsound.Beep(1000, 100)
    if keyboard.is_pressed('esc'):
        break
n = 0
print("saving images to disc")
for i in pils:
    i.save(path + '/mapName' + str(n) + '.png', "PNG")
    n = n + 1
