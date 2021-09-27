import pygame
from pygame.draw import *

FPS = 30
screen = pygame.display.set_mode((600, 800))

#рисуем

#фон
rect(screen, (120, 120, 120), (0, 0, 600, 350))

#объекты на небе
circle(screen, (255, 255, 255), (520, 80), 40)
ellipse(screen, (70, 70, 70), (330, 110, 500, 50))
ellipse(screen, (40, 40, 40), (280, 200, 400, 50))

#дом:
def house(x, y, size, transparency):
    surface = pygame.Surface((600, 800), pygame.SRCALPHA)
    
    #first floor
    rect(surface, (40, 34, 11, transparency), (x, y, size * 300, size * 250))
    rect(surface, (43, 17, 0, transparency), (x + 30 * size, y + 100 * size,
                                             size * 60, size * 90))
    rect(surface, (43, 17, 0, transparency), (x + 120 * size, y + 100 * size,
                                             size * 60, size * 90))
    rect(surface, (212, 170, 0, transparency), (x + 210 * size, y + 100 * size,
                                             size * 60, size * 90))
    #second floor
    rect(surface, (43, 34, 0, transparency), (x, y - 200 * size,
                                             size * 300, size * 200))
    rect(surface, (72, 65, 55, transparency), (x + size * 30, y - size * 200,
                                              size * 30, size * 190))
    rect(surface, (72, 65, 55, transparency), (x + size * 100, y - size * 200,
                                              size * 30, size * 190))
    rect(surface, (72, 65, 55, transparency), (x + size * 170, y - size * 200,
                                              size * 30, size * 190))
    rect(surface, (72, 65, 55, transparency), (x + size * 240, y - size * 200,
                                              size * 30, size * 190))
    
    #balcony
    rect(surface, (26, 26, 26, transparency), (x - 30 * size, y,
                                              size * 360, size * 40))
    rect(surface, (26, 26, 26, transparency), (x - 20 * size, y - size * 40,
                                              size * 10, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + size * 20, y - size * 40,
                                              size * 20, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + size * 80, y - size * 40,
                                              size * 20, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + size * 140, y - size * 40,
                                              size * 20, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + size * 200, y - size * 40,
                                              size * 20, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + size * 260, y - size * 40,
                                              size * 20, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + 310 * size, y - size * 40,
                                              size * 10, size * 40))
    rect(surface, (26, 26, 26, transparency), (x - 10 * size, y - size * 60,
                                              size * 320, size * 20))

    #roof
    rect(surface, (26, 26, 26, transparency), (x + 160 * size, y - 260 * size,
                                              10 * size, 40 * size))
    polygon(surface, (0, 0, 0, transparency), ((x - 20 * size, y - 200 * size),
                                              (x + 320 * size, y - 200 * size),
                                              (x + 290 * size, y - 230 * size),
                                              (x + 10 * size, y - 230 * size)))
    rect(surface, (26, 26, 26, transparency), (x + 40 * size, y - 260 * size,
                                              10 * size, 40 * size))
    rect(surface, (26, 26, 26, transparency), (x + 60 * size, y - 280 * size,
                                              20 * size, 65 * size))
    rect(surface, (26, 26, 26, transparency), (x + 260 * size, y - 270 * size,
                                              10 * size, 50 * size))
    screen.blit(surface, (0, 0))

    
def ghost(x, y, size, transparency, orientation):
    surface = pygame.Surface((600, 800), pygame.SRCALPHA)
    circle(surface, (179, 179, 179, transparency),
           (x - size * orientation * 5, y + size * 10), size * 17)
    coords = ((x - orientation * size * 15, y),
              (x - orientation * size * 17, y + size * 24),
              (x - orientation * size * 20, y + size * 40),
              (x - orientation * size * 30, y + size * 50 ),
              (x - orientation * size * 35, y + size * 65 ),
              (x - orientation * size * 37, y + size * 80 ),
              (x - orientation * size * 33, y + size * 85 ),
              (x - orientation * size * 25, y + size *  82),
              (x - orientation * size * 15, y + size * 87),
              (x - orientation * size * 8, y + size *  89),
              (x - orientation * size * 0, y + size *  89),
              (x + orientation * size * 7, y + size *  85),
              (x + orientation * size * 16, y + size * 85),
              (x + orientation * size * 22, y + size *  87),
              (x + orientation * size * 28, y + size * 87),
              (x + orientation * size * 34, y + size * 80),
              (x + orientation * size * 40, y + size * 76),
              (x + orientation * size * 46, y + size * 72),
              (x + orientation * size * 48, y + size * 65),
              (x + orientation * size * 52, y + size * 60),
              (x + orientation * size * 52, y + size * 52),
              (x + orientation * size * 48, y + size * 49),
              (x + orientation * size * 40, y + size * 40),
              (x + orientation * size * 38, y + size * 34),
              (x + orientation * size * 35, y + size * 30),
              (x + orientation * size * 30, y + size *  26),
              (x + orientation * size * 25, y + size * 21),
              (x + orientation * size * 21, y + size * 15),
              (x + orientation * size * 20, y + size * 12),
              (x + orientation * size * 17, y + size * 8),
              (x + orientation * size * 12, y + size * 4),
              )
    polygon(surface, (179, 179, 179, transparency), coords)
    aalines(surface, (179, 179, 179, transparency), True, coords)
    circle(surface, (135, 205, 222, transparency),
           (x - size * orientation * 15, y + size * 10), size * 4)
    circle(surface, (0, 0, 0, transparency),
           (x - size * orientation * 16, y + size * 10), size * 1.5)
    
    circle(surface, (135, 205, 222, transparency),
           (x + size * orientation * 2, y + size * 5), size * 4)
    circle(surface, (0, 0, 0, transparency),
           (x + size * orientation * 1, y + size * 5), size * 1.5)

    #Draw diagonal ellipses on new surfaces
    ellipse_surface = pygame.Surface((size * 3, size * 2), pygame.SRCALPHA)
    ellipse(ellipse_surface, (255, 255, 255, transparency),
            (0, 0,
             size * orientation * 3, size * 2))
    ellipse_surface = pygame.transform.rotate(ellipse_surface, 30 * orientation)
    surface.blit(ellipse_surface, (x - size * orientation * 17, y + size * 7))

    ellipse_surface = pygame.Surface((size * 3, size * 2), pygame.SRCALPHA)
    ellipse(ellipse_surface, (255, 255, 255, transparency),
            (0, 0,
             size * orientation * 3, size * 2))
    ellipse_surface = pygame.transform.rotate(ellipse_surface, 30 * orientation)
    surface.blit(ellipse_surface, (x, y + size * 2))
    
    screen.blit(surface, (0, 0))
    
house(50,350, 1, 255)

#sky and repeat of some methods of house:
ellipse(screen, (50, 50, 50), (100, 65, 300, 50))
x = 50
y = 350
size = 1
rect(screen, (26, 26, 26), (x + 60 * size, y - 280 * size,
                                          20 * size, 65 * size))
ellipse(screen, (80, 80, 80), (250, 50, 300, 50))
rect(screen, (26, 26, 26), (x + 260 * size, y - 270 * size,
                                            10 * size, 50 * size))
    
ghost(450, 580, 2, 255, 1)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
