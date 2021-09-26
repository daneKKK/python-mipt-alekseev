import turtle

turtle.shape('circle')

dt = 0.1

vx = 25
vy = 80

ax = 0
ay = -10

x = -400
y = 0

turtle.penup()
turtle.goto(-400,0)
turtle.pendown()

for i in range(500):
    x += vx * dt + ax * dt / 2
    y += vy * dt + ay * dt / 2
    vx += ax * dt
    vy += ay * dt

    turtle.goto(x,y)
    
    if y < 0:
        y = -y
        vy = -0.8 * vy
        vx = 0.7 * vx
