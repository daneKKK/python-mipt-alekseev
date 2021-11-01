import math
from random import choice, randint

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        global ax
        global ay
        global WIDTH
        global HEIGHT
        
        self.x += self.vx
        self.y += self.vy
        self.vx += ax
        self.vy += ay

        if abs(HEIGHT - self.r - self.y) < 5:
            self.vy -= ay
            self.vx *= 0.9
        
        if self.x+self.r >= WIDTH:
            self.vx *= (-0.3)
            self.vy *= 0.3

            if abs(self.vx) < 0.1:
                self.vx = 0

            if abs(self.vy) < 1:
                self.vy = 0
            
            self.x -= 2 * (self.x + self.r - WIDTH)
        if self.y + self.r >= HEIGHT:
            self.vy *= (-0.3)
            self.vx *= 0.3

            if abs(self.vx) < 0.5:
                self.vx = 0

            if abs(self.vy) < 1:
                self.vy = 0
                
            self.y -= 2 * (self.y + self.r - HEIGHT)


    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        distance = (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2
        minimal_distance = (self.r + obj.r) ** 2
        return distance <= minimal_distance


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40
        self.y = 450

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, countBullets
        if countBullets:
            bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        coordinates = [
            (5 / 2 * math.sin(self.an) + self.x, -5 / 2 * math.cos(self.an) + self.y),
            (-5 / 2 * math.sin(self.an) + self.x, 5 / 2 * math.cos(self.an) + self.y),
            (-5 / 2 * math.sin(self.an) + self.x + math.cos(self.an) * self.f2_power,
             5 / 2 * math.cos(self.an) + self.y + math.sin(self.an) * self.f2_power),
            (5 / 2 * math.sin(self.an) + self.x + math.cos(self.an) * self.f2_power,
             -5 / 2 * math.cos(self.an) + self.y + math.sin(self.an) * self.f2_power)
            ]
        pygame.draw.polygon(
            self.screen,
            self.color,
            coordinates
            )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    points = 0
    live = 1

    def __init__(self, screen):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(2, 50)
        color = self.color = RED
        self.screen = screen
        self.vx = randint(-5, 5)
        self.vy = randint(5, 5)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
            )

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.x + self.r >= 780:
            self.x -= 2 * (self.x + self.r - 780)
            self.vx *= (-1)
        if 600 >= self.x + self.r:
            self.x += 2 * (600 - self.x - self.r)
            self.vx *= (-1)
        if self.y + self.r >= 550:
            self.y -= 2 * (self.y + self.r - 550)
            self.vy *= (-1)
        if 300 >= self.y + self.r:
            self.y += 2 * (300 - self.y - self.r)
            self.vy *= (-1)

def drawScore():
    '''
    Draws score. Takes score as global variable.
    '''
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MS', 22)
    textSurface = myFont.render(str(score), False, (0, 0, 0))
    width = textSurface.get_width()
    screen.blit(textSurface, (10, 10))

def startText():
    global bullet
    global score
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MS', 22)
    text = 'Цели уничтожены за ' + str(bullet) + ' выстрелов'
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MS', 22)
    textSurface = myFont.render(text, False, (0, 0, 0))
    width = textSurface.get_width()
    screen.blit(textSurface, ((WIDTH // 2) - (width // 2), (HEIGHT) // 3))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
numberOfTargets = 2
targets = [Target(screen) for i in range(numberOfTargets)]
score = 0
levelTimer = 4 * FPS
countBullets = True

ax = 0
ay = 1.5

clock = pygame.time.Clock()
gun = Gun(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    if len(targets) == 0:
        startText()
        if levelTimer > 0:
            levelTimer -= 1
            countBullets = False
        else:
            levelTimer = 4 * FPS
            targets = [Target(screen) for i in range(numberOfTargets)]
            bullet = 0
            countBullets = True
    
    drawScore()
    gun.draw()
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.vx ** 2 + b.vy ** 2 < 0.1:
            balls.remove(b)
        for t in targets:
            if b.hittest(t) and t.live:
                t.live = 0
                t.hit()
                score += t.points
                targets.remove(t)
    for t in targets:
        t.move()

    gun.power_up()

pygame.quit()
