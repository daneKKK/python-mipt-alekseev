import turtle

turtle.shape('circle')

dt = 0.1

vx = 25
vy = 80

ax = 0
ay = -10

k = 0.05

x = -200
y = 0

turtle.penup()
turtle.goto(x,y)
turtle.pendown()

for i in range(500):
    x += vx * dt + ax * dt / 2
    y += vy * dt + ay * dt / 2
    ax = -k * vx
    ay = -k * vy - 10
    vx += ax * dt
    vy += ay * dt

    turtle.goto(x,y)
    
    if y < 0:
        y = -y
        vy = -vy
        vx = vx
