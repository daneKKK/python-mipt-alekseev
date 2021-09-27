import pygame
from pygame.draw import *

screen = pygame.display.set_mode((400, 400))

rect(screen, (100, 100, 100), (0, 0, 400, 400))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
