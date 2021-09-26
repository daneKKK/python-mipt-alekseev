import turtle
import math

def circleL(x, y, r, color):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.begin_fill()
    size=(2 * r * math.pi) / 40
    for i in range(40):
        turtle.forward(size)
        turtle.left(360 / 40)
    turtle.color(color)
    turtle.end_fill()
    turtle.color('black')

def arcL(x, y, r, color):
    turtle.color(color)
    size=(2 * r * math.pi) / 80
    turtle.pensize(size)
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    for i in range(40):
        turtle.forward(size)
        turtle.left(180 / 40)
    turtle.color('black')
    turtle.penup()
    return

def line(x1, y1, x2, y2, size, color):
    turtle.penup()
    turtle.goto(x1, y1)
    turtle.pensize(size)
    turtle.color(color)
    turtle.pendown()
    turtle.goto(x2, y2)
    turtle.penup()
    turtle.color('black')
    return



def smile():
    turtle.left(90)
    circleL(100, 0, 100, 'yellow')
    circleL(70, 40, 20, 'blue')
    circleL(-30, 40, 20, 'blue')
    line(0, 30, 0, -30, 6, 'black')
    turtle.right(180)
    arcL(-70, 0, 70, 'red')
    turtle.hideturtle()

turtle.shape('turtle')
smile()
