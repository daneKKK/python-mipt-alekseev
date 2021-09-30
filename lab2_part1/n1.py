import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

#Background
rect(screen, (150, 150, 150), (0, 0, 400, 400))

#Face
circle(screen, (0, 0, 0), (200, 200), 100)
circle(screen, (255, 255, 0), (200, 200), 99)

#Left eye
circle(screen, (0, 0, 0), (150, 175), 20)
circle(screen, (255, 0, 0), (150, 175), 19)
circle(screen, (0, 0, 0), (150, 175), 5)

#Right eye
circle(screen, (0, 0, 0), (250, 175), 22)
circle(screen, (255, 0, 0), (250, 175), 21)
circle(screen, (0, 0, 0), (250, 175), 7)

#Mouth
rect(screen, (0, 0, 0), (150, 250, 100, 20))

#Brows
polygon(screen, (0, 0, 0), ((175, 165), (180, 160), (100, 115), (95, 120)))
polygon(screen, (0, 0, 0), ((225, 170), (220, 165), (300, 95), (305, 100)))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
