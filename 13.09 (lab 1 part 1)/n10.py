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
for i in range(3):
    circleL(4)
    circleR(4)
    turtle.left(60)
