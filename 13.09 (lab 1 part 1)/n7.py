import turtle

turtle.shape('turtle')

k = 1
n = 100

for i in range(720):
    turtle.forward( i / n)
    turtle.left(360 / n)
