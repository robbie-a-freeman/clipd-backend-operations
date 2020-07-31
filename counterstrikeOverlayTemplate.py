from tkinter import *
from PIL import Image
from PIL import ImageTk

from functools import partial



window=Tk()


imageFilePath = 'data/test/0.png'
image = Image.open(imageFilePath)
#image = Image.fromarray(imageFromFile.astype('uint8'), 'RGB')
width, height = image.size
ratio = width/height
image = image.resize((600, int(600 / ratio)))
renderedImage = ImageTk.PhotoImage(image)

#add widgets


img = Label(window, image=renderedImage)
img.image = renderedImage
img.place(x=0, y=0)

isBtnActivated = False

def btnListener(btn):
    print('called')
    global isBtnActivated
    if btn['fg'] == 'red':
        btn['fg'] = 'blue'
        btn['relief'] = RAISED
        isBtnActivated = False
    else:
        if not isBtnActivated:
            btn['fg'] = 'red'
            btn['relief'] = SUNKEN
        isBtnActivated = True

team1=Button(window, text="team1", fg='blue')
team1['command'] = partial(btnListener, team1)
team1.place(x=650, y=50)

team2=Button(window, text="team2", fg='blue')
team2['command'] = partial(btnListener, team2)
team2.place(x=650, y=80)

score1=Button(window, text="score1", fg='blue')
score1['command'] = partial(btnListener, score1)
score1.place(x=650, y=110)

score2=Button(window, text="score2", fg='blue')
score2['command'] = partial(btnListener, score2)
score2.place(x=650, y=140)

currRound=Button(window, text="currRound", fg='blue')
currRound['command'] = partial(btnListener, currRound)
currRound.place(x=650, y=170)

mapScore1=Button(window, text="mapScore1", fg='blue')
mapScore1['command'] = partial(btnListener, mapScore1)
mapScore1.place(x=650, y=200)

mapScore2=Button(window, text="mapScore2", fg='blue')
mapScore2['command'] = partial(btnListener, mapScore2)
mapScore2.place(x=650, y=230)

p1=Button(window, text="p1", fg='blue')
p1['command'] = partial(btnListener, p1)
p1.place(x=650, y=260)

p2=Button(window, text="p2", fg='blue')
p2['command'] = partial(btnListener, p2)
p2.place(x=650, y=290)

p3=Button(window, text="p3", fg='blue')
p3['command'] = partial(btnListener, p3)
p3.place(x=650, y=320)

p4=Button(window, text="p4", fg='blue')
p4['command'] = partial(btnListener, p4)
p4.place(x=650, y=350)

p5=Button(window, text="p5", fg='blue')
p5['command'] = partial(btnListener, p5)
p5.place(x=650, y=380)

p6=Button(window, text="p6", fg='blue')
p6['command'] = partial(btnListener, p6)
p6.place(x=650, y=410)

p7=Button(window, text="p7", fg='blue')
p7['command'] = partial(btnListener, p7)
p7.place(x=650, y=440)

p8=Button(window, text="p8", fg='blue')
p8['command'] = partial(btnListener, p8)
p8.place(x=650, y=470)

p9=Button(window, text="p9", fg='blue')
p9['command'] = partial(btnListener, p9)
p9.place(x=650, y=500)

p10=Button(window, text="p10", fg='blue')
p10['command'] = partial(btnListener, p10)
p10.place(x=650, y=530)

window.title('CS:GO Clip\'d Template Creation Tool')
window.geometry(str(1000) + 'x' + str(600) + '+0+0')

window.mainloop()