import random
from tkinter import *

root = Tk()
root.title('Snake')

GRID_X = 20
GRID_Y = 20
OFFSET_X = 10
OFFSET_Y = 10
BOX_SIZE = 20

INIT_RANDOM_X = random.randint(0, GRID_X - 1)
INIT_RANDOM_Y = random.randint(0, GRID_Y - 1)

TICK_DELAY = 300

movement = 'Right'
score = 0
enableKeys = True

class SnakeBox:
    def __init__(self, dx, dy, tag, color):
        self.x = dx * BOX_SIZE + OFFSET_X
        self.y = dy * BOX_SIZE + OFFSET_Y
        self.tag = tag
        self.color = color

class Snake:
    initX = 5 * BOX_SIZE + OFFSET_X
    initY = 5 * BOX_SIZE + OFFSET_Y
    bodies = [
        SnakeBox(2, 5, 'body', '#f20'),
        SnakeBox(3, 5, 'body', '#f40'),
        SnakeBox(4, 5, 'body', '#f60'),
        # SnakeBox(1, 5, 'body')
    ]
    head = SnakeBox(5, 5, 'head', '#00f')
    food = SnakeBox(INIT_RANDOM_X, INIT_RANDOM_Y, 'food', '#93f')


canvas = Canvas(root)

# draw grids
for y in range(GRID_Y):
    for x in range(GRID_X):
        dx = x * BOX_SIZE + OFFSET_X
        dx2 = dx + BOX_SIZE
        dy = y * BOX_SIZE + OFFSET_Y
        dy2 = dy + BOX_SIZE
        canvas.create_rectangle(dx, dy, dx2, dy2, outline="#000", fill="#eee")

# draw initial body
for body in Snake.bodies:
    dx = body.x
    dx2 = dx + BOX_SIZE
    dy = body.y
    dy2 = dy + BOX_SIZE
    color = body.color
    canvas.create_rectangle(dx, dy, dx2, dy2, fill=color, tag="body")

# head
dx = Snake.head.x
dx2 = dx + BOX_SIZE
dy = Snake.head.y
dy2 = dy + BOX_SIZE
color = Snake.head.color
canvas.create_rectangle(dx, dy, dx2, dy2, fill=color, tag="head")

# food
dx = Snake.food.x
dx2 = dx + BOX_SIZE
dy = Snake.food.y
dy2 = dy + BOX_SIZE
color = Snake.food.color
canvas.create_rectangle(dx, dy, dx2, dy2, fill=color, tag="food")


# score
canvas.create_text(GRID_X * BOX_SIZE + (OFFSET_X * 2), OFFSET_Y, text="Score: ", fill="#333", anchor=NW)

# score
canvas.create_text(GRID_X * BOX_SIZE + (OFFSET_X * 2) + 50, OFFSET_Y, text="0", tag="score", fill="#333", anchor=NW)

canvas.pack(fill=BOTH, expand=1)

def onKeyDownd(e):
    global movement
    global enableKeys

    if enableKeys == True:

        if movement == 'Left' and e.keysym == 'Right':
            return
        elif movement == 'Right' and e.keysym == 'Left':
            return
        elif movement == 'Down' and e.keysym == 'Up':
            return
        elif movement == 'Up' and e.keysym == 'Down':
            return
        
        movement = e.keysym
        enableKeys = False
    

def onTimeFrame():
    global enableKeys
    
    head = canvas.find_withtag('head')
    food = canvas.find_withtag('food')
    bodies = canvas.find_withtag('body')
    bodyfoods = canvas.find_withtag('bodyfood')
    headCoords = canvas.coords(head)
    # print(headCoords[0])

    items = bodies + bodyfoods + head
    i = 0

    # print('\nitems', items)

    for i in range( len(items) - 1 ):
        c1 = canvas.coords( items[i] )
        c2 = canvas.coords( items[i + 1] )
        
        canvas.move( items[i], c2[0]-c1[0], c2[1]-c1[1])
        i += 1

    
    if isHeadHitBound() == False :
        if movement == 'Left':
            canvas.move(head, - BOX_SIZE, 0)
        
        if movement == 'Right':
            canvas.move(head, BOX_SIZE, 0)
        
        if movement == 'Up':
            canvas.move(head, 0, -BOX_SIZE)
        
        if movement == 'Down':
            canvas.move(head, 0, BOX_SIZE)
    
    headCoords = canvas.coords(head)
    foodCoords = canvas.coords(food)
    
    if headCoords[0] == foodCoords[0] and headCoords[1] == foodCoords[1]:
        eatFoodAt(c2[0], c2[1])

    enableKeys = True
    root.after(TICK_DELAY, onTimeFrame)


def eatFoodAt(dx, dy):
    global score

    dx2 = dx + BOX_SIZE
    dy2 = dy + BOX_SIZE
    color = '#f80'
    canvas.create_rectangle(dx, dy, dx2, dy2, fill=color, tag='bodyfood')
    newRandomFood()

    score += 1
    
    scoreText = canvas.find_withtag("score")
    canvas.itemconfigure(scoreText, text=score)


def newRandomFood():
    food = canvas.find_withtag('food')
    dx = random.randint(0, GRID_X - 1) * BOX_SIZE + OFFSET_X
    dy = random.randint(0, GRID_Y - 1) * BOX_SIZE + OFFSET_Y

    pointFrom = canvas.coords( food )
    pointTo = [dx, dy]

    canvas.move( food, pointTo[0] - pointFrom[0], pointTo[1] - pointFrom[1])

def isHeadHitBound():
    head = canvas.find_withtag('head')
    headCoords = canvas.coords(head)

    if headCoords[0] < OFFSET_X or headCoords[0] >= GRID_X * BOX_SIZE + OFFSET_X or headCoords[1] < OFFSET_Y or headCoords[1] >= GRID_Y * BOX_SIZE + OFFSET_Y:
        resetGame()
        return True
    
    return False

def resetGame():
    global movement
    global score

    print('reset')
    head = canvas.find_withtag('head')
    bodies = canvas.find_withtag('body')
    bodyfoods = canvas.find_withtag('bodyfood')
    
    headCoords = canvas.coords(head)

    movement = 'Right'
    score = 0

    scoreText = canvas.find_withtag("score")
    canvas.itemconfigure(scoreText, text=score)

    canvas.move(head, 
        (Snake.initX - headCoords[0]), 
        (Snake.initY - headCoords[1])
    )

    i = 0
    for i in range( len(bodies) ):
        pointFrom = canvas.coords( bodies[i] )
        pointTo = [ Snake.bodies[i].x, Snake.bodies[i].y ]
        
        canvas.move( bodies[i], pointTo[0] - pointFrom[0], pointTo[1] - pointFrom[1])
        i += 1

    # canvas.delete(bodyfoods)
    for bodyfood in bodyfoods:
        canvas.delete(bodyfood)

    newRandomFood()


root.bind_all('<Key>', onKeyDownd)
root.after(TICK_DELAY, onTimeFrame)

resetGame()

root.geometry('600x600')
root.mainloop()

