import turtle, math
from random import *

class Particle:

    def __init__(self, x, y, vx, vy):

        self.drawParticle = turtle.Turtle()
        self.drawParticle.shape('circle')
        self.drawParticle.penup()
        self.drawParticle.speed(50)
        self.drawParticle.goto(x, y)
        self.drawParticle.turtlesize(0.5,0.5,1)
        
        self.x = x
        self.y = y
        self.vx = vx
        self. vy = vy

    def accelerate(self,ax, ay, dt):
        self.vx += ax * dt
        self.vy += ay * dt

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.drawParticle.goto(self.x, self.y)



def distance(P1,P2):
    k0 = 2 * k
    if abs(P1.x - P2.x) < abs(P1.x - P2.x - k0):
        dx = P1.x - P2.x
    else:
        dx = P1.x - P2.x - k0

    if abs(P1.y - P2.y) < abs(P1.y - P2.y - k0):
        dy = P1.y - P2.y
    else:
        dy = P1.y - P2.y - k0
    return dx, dy

def force(P1, P2):
    r0 = 30
    dx, dy = distance(P1, P2)

    dr = math.sqrt(dx ** 2 + dy ** 2)

    if dr >= 100:
        return 0, 0
    
    f = 12 * (r0 ** 12) / (dr ** 13) - 6 * (r0 ** 6) / (dr ** 7)

    fx = f * dx / dr
    fy = f * dy / dr
    return fx, fy

def main():

    
    N = int(input('Введите количество частиц:\n'))
    global k
    k = 1 / 2 * int(input('Введите размер коробки:\n'))
    dt = 0.001

    window = turtle.Screen()
    window.tracer(N)

    border=turtle.Turtle()
    for i in range(N):
        border.penup()
        border.goto(k,k)
        border.pendown()
        border.goto(k,-k)
        border.goto(-k,-k)
        border.goto(-k,k)
        border.goto(k,k)
        border.hideturtle()
    
    particles=[0]*N
    for i in range(N):
            x = randint(-k, k)
            y = randint(-k, k)
            minr=1600
            if i!=0:
                for j in range(i-1):
                    dr = (x - particles[j].x) ** 2 + (y - particles[j].y) ** 2
                    minr = min(dr, minr)
            while minr < 225:
                minr = 1600
                x = randint(-k+20, k-20)
                y = randint(-k+20, k-20)
                for j in range(i-1):
                    dr = (x - particles[j].x) ** 2 + (y - particles[j].y) ** 2
                    minr = min(dr, minr)
                    
                
            particles[i]=Particle(x,y,randint(-k,k),randint(-k,k))

    while True:
        for i in range(N):
            ax = 0
            ay = 0

            for j in range(N):
                if j != i:
                    dax, day = force(particles[i], particles[j])
                
                    ax += dax
                    ay += day

            particles[i].accelerate(ax, ay, dt)

        for i in particles:
            i.move(dt)

            i.x = -k + (i.x + k) % (2 * k)
            i.y = -k + (i.y + k) % (2 * k)

        
        
main()        
            
