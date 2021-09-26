import turtle

draw0 = (
    'pendown', (0, -40), (20, 0), (0, 40), (-20, 0), 'penup', (20, 0)
    )

draw1 = (
    (0, -20), 'pendown', (20, 20), (0, -40), 'penup', (0, 40)
    )

draw2 = (
    'pendown', (20, 0), (0, -20), (-20, -20), (20, 0), 'penup', (0, 40)
    )

draw3 = (
    'pendown', (20, 0), (-20, -20), (20, 0), (-20, -20), 'penup', (20, 40)
    )

draw4 = (
    'pendown', (0, -20), (20, 0), (0, -20), (0, 40), 'penup'
    )

draw5 = (
    (0, -40), 'pendown', (20, 0), (0, 20), (-20, 0), (0, 20),
    (20, 0), 'penup'
    )

draw6 = (
    (0, -20), 'pendown', (0, -20), (20, 0), (0, 20), (-20, 0),
    (20, 20), 'penup'
    )

draw7 = (
    'pendown', (20, 0), (-20, -20), (0, -20), 'penup', (20, 40)
    )

draw8 = (
    'pendown', (0, -40), (20, 0), (0, 20), (-20, 0), (0, 20),
    (20, 0), (0, -20), (0, 20), 'penup'
    )

draw9 = (
    (0, -40), 'pendown', (20, 20), (0, 20), (-20, 0), (0, -20),
    (20, 0), (0, 20), 'penup'
    )

draw = [draw0, draw1, draw2, draw3, draw4, draw5, draw6, draw7, draw8, draw9]

numbers = input('Введите числа:\n')
turtle.shape('turtle')
turtle.penup()
turtle.goto(-200,0)

for i in numbers:
    for j in draw[int(i)]:
        if j == 'pendown':
            turtle.pendown()
        elif j == 'penup':
            turtle.penup()
        else:
            x, y = turtle.pos()
            dx, dy = j
            turtle.goto(x + dx, y + dy)
    turtle.forward(20)
    
