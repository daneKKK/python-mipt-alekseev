import turtle

turtle.shape('turtle')

k = 10

for i in range(10):
    for j in range(4):
        turtle.forward(k + i * k)
        turtle.left(90)
    turtle.penup()
    x,y=turtle.pos()
    turtle.goto(x - k / 2, y - k / 2)
    turtle.pendown()
