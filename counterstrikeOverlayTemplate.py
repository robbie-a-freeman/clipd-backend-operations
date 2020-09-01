import os
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageGrab
from PIL import ImageTk
from PIL import ImageFilter

from functools import partial

import clipOverlayElement as coe
import clipOverlayTemplate as cot


import pytesseract

COLOR_INCOMPLETE = 'blue'
COLOR_SELECTED = 'red'
COLOR_COMPLETE = 'green'


isBtnActivated = False
queuedPoint = (-1., -1.)
secondPoint = (-1., -1.)
overlayElement = None
activeOverlay = cot.ClipOverlayTemplate()
imagePanelReference = None


def activateMouseListener(imageFrame):
    print('activated')
    imageFrame.bindToCanvas("<Button-1>", imageFrame.addFirstPointOfElement)


def btnListener(btn, element, imageFrame):
    print('called')
    global isBtnActivated
    global queuedPoint
    global overlayElement
    global imagePanelReference

    overlayElement = element
    if btn['fg'] == COLOR_SELECTED:
        queuedPoint = (-1, -1)
        btn['relief'] = RAISED
        isBtnActivated = False
        if overlayElement.p1[0] > 0 and overlayElement.p1[1] > 0 and overlayElement.p2[0] > 0 and overlayElement.p2[1] > 0:
            btn['fg'] = COLOR_COMPLETE
            imagePanelReference.changeRectColor(overlayElement.name, COLOR_COMPLETE)
        else:
            btn['fg'] = COLOR_INCOMPLETE
    else:
        if not isBtnActivated:
            queuedPoint = (-1, -1)
            activateMouseListener(imageFrame)
            btn['fg'] = COLOR_SELECTED
            btn['relief'] = SUNKEN
        isBtnActivated = True


# TODO save
def save():
    # initialize template
    print('Saving: ', activeOverlay.__dict__)
    activeOverlay.saveToFile(None)
    # call save w/o filename


# TODO load
def load():
    global activeOverlay

    # initialize template
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file")
    activeOverlay = cot.loadFromFile(filename)
    print('Loading: ', activeOverlay.__dict__)
    # TODO update the individual overlay btns and objects for each existing entry in the file


class ButtonFrame(Frame):

    imageFrame = None
    overlays = []

    def __init__(self, imageF):
        super().__init__()

        self.imageFrame = imageF
        self.initUI()

    def prefixPlayerCompNames(self, p, name):
        return 'p' + str(p) + name

    def initUI(self):

        components = ['team1', 'team2', 'score1', 'score2', 'currRound', 'mapScore1', 'mapScore2']
        btns = []

        for c in range(len(components)):
            cName = components[c]
            overlay = coe.clipOverlayElement(queuedPoint, secondPoint, cName, '[\\s\\S]*')
            btn = Button(self, text=cName, fg=COLOR_INCOMPLETE)
            btn.grid(row=(c % 20), column=0)
            btn['command'] = partial(btnListener, btn, overlay, self.imageFrame)
            self.overlays.append(overlay)
            btns.append(btn)

        components = []
        for i in range(10):
            components.extend([self.prefixPlayerCompNames(i, 'Alias'),
                               self.prefixPlayerCompNames(i, 'Gun'),
                               self.prefixPlayerCompNames(i, 'Grenades'),
                               self.prefixPlayerCompNames(i, 'Pistol'),
                               self.prefixPlayerCompNames(i, 'Defuse'),
                               self.prefixPlayerCompNames(i, 'Dead'),
                               self.prefixPlayerCompNames(i, 'Kills'),
                               self.prefixPlayerCompNames(i, 'Money'),
                               self.prefixPlayerCompNames(i, 'Health'),
                               self.prefixPlayerCompNames(i, 'Armor')])

        for c in range(len(components)):
            cName = components[c]
            overlay = coe.clipOverlayElement(queuedPoint, secondPoint, cName, '[\\s\\S]*')
            btn = Button(self, text=cName, fg=COLOR_INCOMPLETE)
            btn.grid(row=(c % 20), column=int(c * 5 / len(components))+1)
            btn['command'] = partial(btnListener, btn, overlay, self.imageFrame)
            self.overlays.append(overlay)
            btns.append(btn)

        btn = Button(self, text='save', fg='black')
        btn.grid(row=25, column=0)
        btn['command'] = partial(save)
        btns.append(btn)

        btn = Button(self, text='load', fg='black')
        btn.grid(row=25, column=1)
        btn['command'] = partial(load)
        btns.append(btn)

        # TODO button to cut down on redundancy
        def clonePlayerMappings():
            print('unimplemented')

        cpm = Button(self, text='clone player mappings', fg='black')
        cpm['command'] = partial(clonePlayerMappings)
        cpm.grid(row=21, columns=3)


class ImageFrame(Frame):

    gCanvas = None
    BASE_WIDTH = -1
    BASE_HEIGHT = -1
    image = None

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        imageFilePath = 'data/test/0.png'
        image = Image.open(imageFilePath)
        width, height = image.size
        ratio = width/height
        self.BASE_WIDTH = 1000
        self.BASE_HEIGHT = int(self.BASE_WIDTH / ratio)
        image = image.resize((self.BASE_WIDTH, self.BASE_HEIGHT))
        renderedImage = ImageTk.PhotoImage(image)
        self.image = renderedImage
        canvas = Canvas(self, width=self.BASE_WIDTH, height=self.BASE_HEIGHT)
        canvas.create_image(0, 0, image=renderedImage, anchor=NW)
        canvas.pack(expand=YES, fill=BOTH)
        self.gCanvas = canvas

    def syncOverlayTemplateElement(self):
        print('sync')
        global queuedPoint
        global secondPoint
        global overlayElement
        global activeOverlay

        print(overlayElement.name)
        self.gCanvas.delete(overlayElement.name)
        self.gCanvas.create_rectangle(queuedPoint[0] * self.BASE_WIDTH, queuedPoint[1] * self.BASE_HEIGHT, secondPoint[0] * self.BASE_WIDTH, secondPoint[1] * self.BASE_HEIGHT, outline=COLOR_SELECTED, tags=overlayElement.name)

        overlayElement.p1 = queuedPoint
        overlayElement.p2 = secondPoint
        setattr(activeOverlay, overlayElement.name, overlayElement)
        print("p1: " + str(overlayElement.p1[0]) + ", " + str(overlayElement.p1[1]) + ", p2: " + str(overlayElement.p2[0]) + ", " + str(overlayElement.p2[1]))
        print('element: ' + activeOverlay.__getattribute__(overlayElement.name).name)

        # PyTesseract preview
        if overlayElement.expectedInput is not 'ICON':
            print('PyTesseract preview:')
            self.previewPyTesseract(overlayElement)
        else:
            # TODO pattern match icon
            print('Icon preview not implemented yet')

    def addFirstPointOfElement(self, event):
        print('first')
        global queuedPoint
        queuedPoint = (event.x / self.BASE_WIDTH, event.y / self.BASE_HEIGHT)
        self.gCanvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, outline=COLOR_SELECTED, tags="firstPoint")
        self.gCanvas.unbind("<Button-1>")
        self.gCanvas.bind("<Button-1>", self.addSecondPointOfElement)

    def addSecondPointOfElement(self, event):
        print('second')
        global secondPoint
        secondPoint = (event.x / self.BASE_WIDTH, event.y / self.BASE_HEIGHT)
        self.gCanvas.delete("firstPoint")
        self.gCanvas.unbind("<Button-1>")
        self.syncOverlayTemplateElement()
    
    def bindToCanvas(self, button, callback):
        self.gCanvas.bind(button, callback)

    def previewPyTesseract(self, overlayElement):
        image = self.cropScreenshotWithFloats(overlayElement.p1, overlayElement.p2)
        im = image.filter(ImageFilter.SHARPEN)
        im.save("test.gif")
        text = pytesseract.image_to_string(im)
        print('PyTesseract preview: ' + overlayElement.name + ' = ' + text)
        if overlayElement.isStrCompatibleWith(text):
            print('Matching result!')
        else:
            print('Result does not match expected input.')
            print('Expected str of the form: ' + overlayElement.expectedInput)

    def cropScreenshotWithFloats(self, p1, p2):
        print(p1)
        print(p2)
        ssWidth = abs(p1[0] - p2[0]) * self.gCanvas.winfo_width()
        ssHeight = abs(p1[1] - p2[1]) * self.gCanvas.winfo_height()
        tl = (min(p1[0], p2[0]), min(p1[1], p2[1]))
        # self.image.save("out_grabtofile.png", ImageGrab.grab(bbox=self.gcanvas))
        x = self.winfo_rootx() + self.gCanvas.winfo_x() + tl[0] * self.gCanvas.winfo_width()
        y = self.winfo_rooty() + self.gCanvas.winfo_y() + tl[1] * self.gCanvas.winfo_height()
        xx = x + ssWidth
        yy = y + ssHeight
        print( x, y, xx, yy )
        # ImageGrab.grab(bbox=(x, y, xx, yy)).save("test.gif")
        return ImageGrab.grab(bbox=(x, y, xx, yy))  # .save("test.gif")

    def changeRectColor(self, tagName, color):
        self.gCanvas.itemconfigure(tagName, outline=color)

def main():
    global imagePanelReference

    root = Tk()
    f1 = ImageFrame()
    f1.pack(side=LEFT)
    f2 = ButtonFrame(f1)
    f2.pack(side=RIGHT)
    root.title('CS:GO Clip\'d Template Creation Tool')
    root.geometry(str(1700) + 'x' + str(900) + '+0+0')
    imagePanelReference = f1
    root.mainloop()

if __name__ == '__main__':
    main()