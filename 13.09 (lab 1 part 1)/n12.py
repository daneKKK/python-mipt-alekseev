import turtle

def arcR(size):
    for i in range(40):
        turtle.forward(size)
        turtle.right(180 / 40)

def arcL(size):
    for i in range(40):
        turtle.forward(size)
        turtle.left(180 / 40)



turtle.shape('turtle')
turtle.left(90)
for i in range(7):
    arcR(2)
    arcR(0.25)
