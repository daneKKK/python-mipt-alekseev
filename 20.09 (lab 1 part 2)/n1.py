import random
import turtle

turtle.shape('turtle')

for i in range(40):
    turtle.forward(random.randint(1,30))
    turtle.left(random.randint(-179,180))
