import turtle

def circleL(size):
    for i in range(50):
        turtle.forward(size)
        turtle.left(360 / 50)

def circleR(size):
    for i in range(50):
        turtle.forward(size)
        turtle.right(360 / 50)

turtle.shape('turtle')
turtle.left(90)
for i in range(5):
    circleL(4 + i)
    circleR(4 + i)
