import turtle
import math

def polygon(n, k):
    turtle.pendown()
    turtle.left( 90 + 180 / n)
    for i in range(n):
        turtle.forward(k)
        turtle.left(360 / n)
    turtle.right(90 + 180 / n)
    turtle.penup()
    return



turtle.shape('turtle')

k = 40
n = 12
r=math.sqrt(3) / 3 * k
for j in range(3, n):
    polygon(j, 2 * math.sin(math.pi / j) * r)
    turtle.forward(k / 2)
    r += k / 2
