import pygame
from pygame.draw import *
from random import randint, uniform
import math
pygame.init()


#We create a list of colors out of which color for new ball will be randomly
#chosen.
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Ball():
    '''
    Ball class.
    '''
    def __init__(self):
        '''
        Creates a new ball with random position, color, speed and radius.
        '''
        self.x = randint(100, 1100)
        self.y = randint(100, 900)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.r = randint(10, 100)
        self.color = COLORS[randint(0,5)]

    def draw(self):
        '''
        Draws ball on the screen.
        '''
        circle(screen, self.color, (self.x, self.y), self.r)

    def processClick(self, event):
        '''
        Checks if position of click is in radius of a ball
        '''
        x, y = event.pos
        return (self.x - x) ** 2 + (self.y - y) ** 2 < self.r ** 2

    def move(self):
        '''
        Moves ball within screen
        '''
        self.x += self.vx
        self.y += self.vy

    def stayOnScreen(self):
        '''
        Checks if ball is in screen. If not, brings it back.
        '''
        if self.x + self.r >= X_BORDER:
            self.x -= 2 * (self.x + self.r - X_BORDER)
            self.vx *= -1
        if self.y + self.r >= Y_BORDER:
            self.y -= 2 * (self.y + self.r - Y_BORDER)
            self.vy *= -1
        if self.x - self.r <= 0:
            self.x += 2 * (self.r - self.x)
            self.vx *= -1
        if self.y - self.r <= 0:
            self.y += 2 * (self.r - self.y)
            self.vy *= -1

class Targeter():
    '''
    Objects of this class will spin around ball with speed depenging on a size
    of a ball. 
    '''
    def __init__(self, ball):
        '''
        Creates targeter with random angle, radius from ball. It's speed
        depends on size of a ball, the bigger - the faster.
        TO DO: Set more interesting color
        '''
        self.angle = uniform(-math.pi, math.pi)
        self.angleSpeed = uniform(-0.2 * ball.r ** 2 / 5000,
                                  0.2 * ball.r ** 2 / 5000)
        self.r = uniform(ball.r + 20, ball.r + 100)
        self.rSpeed = uniform(0.1 * ball.r ** 2 / 1000,
                              1 * ball.r ** 2 / 1000)
        self.color = ball.color

    def move(self):
        '''
        Updates angle and radius of targeter.
        '''
        self.angle += self.angleSpeed
        self.r -= self.rSpeed

    def draw(self, ball):
        '''
        Draws targeter.
        ball - connected ball.
        '''
        self.x, self.y = ball.x, ball.y
        
        circle(screen, self.color, (self.x + self.r * math.sin(self.angle),
                                    self.y + self.r * math.cos(self.angle)),
               10)

    def readyForDestruction(self, ball):
        '''
        Checks whether connected ball can be destroyed comparing it's radius
        with targeter radius.
        ball - connected ball.
        '''
        return self.r < ball.r

    def processClick(self, event):
        '''
        Checks if position of click is in targeter
        '''
        x, y = event.pos
        distance = (self.x + self.r * math.sin(self.angle) - x) ** 2
        distance += (self.y + self.r * math.cos(self.angle) - y) ** 2
        return distance < 100

class ClickedBall():
    '''
    Gets drawn when click on the ball has been succesful at the same place
    as the ball. It only gets drawn 10 times before destruction.
    '''
    
    
    def __init__(self, ball, FPS):
        '''
        Creates object in position of a ball with the same radius as the
        ball.
        ball - the clicked ball;
        FPS - FPS of the mainloop.
        '''
        self.x, self.y = ball.x, ball.y
        self.r = ball.r

        #Time to live is for how many frames will ClickedBall be drawn.
        self.timeToLive = FPS // 3
        
    def draw(self):
        '''
        Draws ClickedBall.
        '''
        rect(screen, (255, 255, 255), (self.x - 2, self.y - 12,
                                       4, 24))
        rect(screen, (255, 255, 255), (self.x - 12, self.y - 2,
                                       24, 4))

    def isAlive(self):
        '''
        Checks whether ball can be drawn again. If yes, reduces it's timer
        of being drawn by 1 and returns True; returns False otherwise.
        '''
        if self.timeToLive > 0:
            self.timeToLive -= 1
            return True
        else:
            return False

def drawScore():
    '''
    Draws score. Takes score as global variable.
    '''
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MS', 30)
    textSurface = myFont.render('Score: ' + str(score), False, (255, 255, 255))
    screen.blit(textSurface, (0, 10))

#Setting up a screen
FPS = 30
X_BORDER = 1200
Y_BORDER = 900
screen = pygame.display.set_mode((X_BORDER, Y_BORDER))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

N = 5 #Number of balls.

score = 0

ballObjects = [0] * N
for i in range(N):
    ballObjects[i] = Ball()
    ballObjects[i].draw()

targeterObjects = [0] * N
for i in range(N):
    targeterObjects[i] = Targeter(ballObjects[i])
    targeterObjects[i].draw(ballObjects[i])

clickedObjects = [] #Array of clicked objects

while not finished:
    clock.tick(FPS)
    succesfullyClicked = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not succesfullyClicked:
            #Checks if event is mouse click and if there was no succesful
            #click already in this frame.
            #Then checks if this click is succesful (if there was click on a
            #ball).
            #If yes, updates score, creates new ball, marks this frame
            #as the one with succesful click breaks cycle and creates
            #crosshair.
            for i in range(len(ballObjects)):
                if ballObjects[i].processClick(event):
                    clickedObjects.append(ClickedBall(ballObjects[i], FPS))
                    score += 1
                    succesfullyClicked = True
                    ballObjects[i] = Ball()
                    break

    #Moves and draws balls
    for i in ballObjects:
        i.move()
        i.stayOnScreen()
        i.draw()

    for i in range(N):
        targeterObjects[i].move()
        targeterObjects[i].draw(ballObjects[i])
        if targeterObjects[i].readyForDestruction(ballObjects[i]):
            ballObjects[i] = Ball()
            targeterObjects[i] = Targeter(ballObjects[i])
        

    #Draws crosshair
    for i in clickedObjects:
        i.draw()
        if not i.isAlive():
            clickedObjects.remove(i)

    #Draws score
    drawScore()

    
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
