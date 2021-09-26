import turtle

n = 12
k = 100

t=turtle.Turtle()

t.shape('turtle')

for i in range(n):
    t.forward(k)
    t.clone()

    t.left(180)
    t.forward(k)
    t.right(180 - 360 / n)
