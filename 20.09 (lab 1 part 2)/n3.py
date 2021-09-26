import turtle


print('Шрифт задаётся 3 типами команд в config.txt:\n' +
      'penup - поднятие пера, pendown - опускание пера, x;y - сдвиг на x и y\n' +\
      'команды задаются в одной строке через запятую с пробелом\n')

f = open('config.txt', 'r')

draw = [0]*10

for i in range(10):
    s=f.readline()
    draw[i]=[]
    for j in s.split(', '):
        if j == 'penup' or j == 'pendown':
            draw[i].append(j)
        elif len(j)>0:
            x, y = j.split('; ')
            draw[i].append((x,y))
f.close()

input


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
            dx = int(dx)
            dy = int(dy)
            turtle.goto(x + dx, y + dy)
