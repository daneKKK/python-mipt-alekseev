import pygame
from pygame.draw import *
from random import randint
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

        
        #Checks if ball is in screen. If not, brings it back.
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

class Crosshair():
    '''
    Crosshair objects. Gets drawn when click has been succesful.
    '''
    def __init__(self, event):
        '''
        Creates crosshair objects in position of a click.
        '''
        self.x, self.y = event.pos
        
    def draw(self):
        '''
        Draws crosshair.
        '''
        rect(screen, (255, 255, 255), (self.x - 2, self.y - 12,
                                       4, 24))
        rect(screen, (255, 255, 255), (self.x - 12, self.y - 2,
                                       24, 4))

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

ballObjects = [0]*N
for i in range(N):
    ballObjects[i] = Ball()
    ballObjects[i].draw()
    

while not finished:
    clock.tick(FPS)
    succesfullyClicked = False
    crosshairObjects = [] #Array of crosshair objects
    
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
                    crosshairObjects.append(Crosshair(event))
                    score += 1
                    succesfullyClicked = True
                    ballObjects[i] = Ball()
                    break

    #Moves and draws balls
    for i in range(N):
        ballObjects[i].move()
        ballObjects[i].draw()

    #Draws crosshair
    for i in crosshairObjects:
        i.draw()

    #Draws score
    drawScore()

    
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
