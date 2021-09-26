import turtle


def star(n):
    for i in range(n):
        turtle.forward(200)
        turtle.right(180 - 180 / n)


turtle.shape('turtle')
turtle.left(180)
star(11)
