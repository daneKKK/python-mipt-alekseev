import math, json
from random import choice, randint, uniform

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

X_BORDER = 800
Y_BORDER = 600


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
        global X_BORDER
        global Y_BORDER
        
        self.x += self.vx
        self.y += self.vy
        self.vx += ax
        self.vy += ay

        if abs(Y_BORDER - self.r - self.y) < 5:
            self.vy -= ay
            self.vx *= 0.9
        
        if self.x+self.r >= X_BORDER:
            self.vx *= (-0.3)
            self.vy *= 0.3

            if abs(self.vx) < 0.1:
                self.vx = 0

            if abs(self.vy) < 1:
                self.vy = 0
            
            self.x -= 2 * (self.x + self.r - X_BORDER)

        if self.x-self.r <= 0:
            self.vx *= (-0.3)
            self.vy *= 0.3

            if abs(self.vx) < 0.1:
                self.vx = 0

            if abs(self.vy) < 1:
                self.vy = 0
            
            self.x -= 2 * (self.x - self.r)
        
        if self.y + self.r >= Y_BORDER:
            self.vy *= (-0.3)
            self.vx *= 0.3

            if abs(self.vx) < 0.5:
                self.vx = 0

            if abs(self.vy) < 1:
                self.vy = 0
                
            self.y -= 2 * (self.y + self.r - Y_BORDER)


    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj, obj_side):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if obj_side == self.side:
            return False
        distance = (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2
        minimal_distance = (self.r + obj.r) ** 2
        return distance <= minimal_distance

class Rocket(Ball):
    def move(self):
        self.x += self.vx
        self.y += self.vy
        
    def draw(self):
        headingCos = self.vx / math.sqrt(self.vx ** 2 + self.vy ** 2)
        headingSin = self.vy / math.sqrt(self.vx ** 2 + self.vy ** 2)
        headingAngle = math.atan2(headingSin, headingCos)
        coordinates = [(self.x + self.r * headingCos, self.y + self.r * headingSin),
                       (self.x + self.r * math.cos(headingAngle + 2 * math.pi / 3),
                        self.y + self.r * math.sin(headingAngle + 2 * math.pi / 3)),
                       (self.x + self.r * math.cos(headingAngle - 2 * math.pi / 3),
                        self.y + self.r * math.sin(headingAngle - 2 * math.pi / 3))]
        pygame.draw.polygon(self.screen, self.color, coordinates)        

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.r = 10
        self.an = 1
        self.color = GREY
        self.x = randint(10, X_BORDER - 10)
        self.y = Y_BORDER - 10

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, countBullets, guns
        if countBullets:
            bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        new_ball.side = guns.index(self)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def rocket_fire(self, position):
        global balls, bullet, countBullets, guns
        if not countBullets:
            return
        bullet += 1
        new_rocket = Rocket(self.screen, self.x, self.y)
        new_rocket.r += 5
        self.an = math.atan2((position[1]-new_rocket.y), (position[0]-new_rocket.x))
        new_rocket.vx = 4 * math.cos(self.an)
        new_rocket.vy = 4 * math.sin(self.an)
        new_rocket.side = guns.index(self)
        balls.append(new_rocket)

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
            
        pygame.draw.rect(
            self.screen,
            GREEN,
            (self.x - 10, self.y, 20, 10))
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

    def move_left(self):
        self.x -= 5
        self.x = self.x % X_BORDER

    def move_right(self):
        self.x += 5
        self.x = self.x % X_BORDER



class Target:
    points = 0
    live = 1

    def __init__(self, screen):
        """ Инициализация новой цели. """
        x = self.x = randint(55, X_BORDER - 55)
        y = self.y = randint(55, Y_BORDER - 55)
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

        if self.x + self.r >= X_BORDER - 55:
            self.x -= 2 * (self.x + self.r - X_BORDER + 55)
            self.vx *= (-1)
        if 55 >= self.x + self.r:
            self.x += 2 * (55 - self.x - self.r)
            self.vx *= (-1)
        if self.y + self.r >= Y_BORDER - 55:
            self.y -= 2 * (self.y + self.r - Y_BORDER + 55)
            self.vy *= (-1)
        if 55 >= self.y + self.r:
            self.y += 2 * (55 - self.y - self.r)
            self.vy *= (-1)

class Invader(Target):
    
    def __init__(self, screen):
        self.x = randint(55, X_BORDER - 55)
        self.y = randint(20, 100)
        self.r = randint(2, 20)
        color = self.color = RED
        self.screen = screen
        self.vx = randint(-5, 5)
        self.vy = 0

    def draw(self):
        pygame.draw.rect(
            self.screen,
            self.color,
            (self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r)
            )

    def bomb(self):
        global balls
        new_ball = Rocket(self.screen, self.x, self.y + 2 * self.r + 10)
        new_ball.vy = 12
        new_ball.side = -1
        balls.append(new_ball)
        

def menuLoop():
    '''
    Function that will show game menu.
    '''
    def drawMenu():
        '''
        Draws text "Меню"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 40)
        textSurface = myFont.render('Меню', False, (0, 0, 0))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) - 180))

    def drawLeaderboardMenu():
        '''
        Draws text "Таблица лидеров"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Таблица лидеров', False, (0, 0, 0))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) - 60))
        
    def drawSettingsMenu():
        '''
        Draws text "Настройки"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Настройки', False, (0, 0, 0))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) - 60))

    def drawTutorialMenu():
        '''
        Draws text "Обучение"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Обучение', False, (0, 0, 0))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) - 20))

    def drawQuitMenu():
        '''
        Draws text "Выйти"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Выйти', False, (0, 0, 0))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) + 20))

    def drawQuitAndSaveMenu():
        '''
        Draws text "Выйти"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Выйти и сохранить', False, (0, 0, 0))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) + 60))
    def drawContinueMenu():
        '''
        Draws text "Продолжить"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Продолжить', False, (0, 0, 0))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) - 100))

    def processClick(event):
        '''
        Checks whether click position was in one of the menu buttons
        event - event of click
        '''
        x, y = event.pos

        nonlocal menuFinished
        global finished
        global doASave

        isOnXAxis = False
        isOnYAxis = False

        #Processing X position of click
        if  not (x >= (X_BORDER // 2) - (270 // 2) and
            x <= (X_BORDER // 2) + (270 // 2)):
            return

        #Processing Продолжить button
        if (y >= (Y_BORDER // 2) - 100 and
            y <= (Y_BORDER // 2) - 61 ):
            menuFinished = True
            return

        #Processing Таблица лидеров button
        if (y >= (Y_BORDER // 2) - 60 and
            y <= (Y_BORDER // 2) - 21):
            leaderboardLoop()
            return

        #Processing Обучение button
        if (y >= (Y_BORDER // 2) - 20 and
            y <= (Y_BORDER // 2) + 19):
            tutorialLoop()
            return

        #Processing Выход button
        if (y >= (Y_BORDER // 2) + 20 and
            y <= (Y_BORDER // 2) + 59):
            finished = True
            menuFinished = True
            return

        #Processing Выйти и сохранить
        if (y >= (Y_BORDER // 2) + 60 and
            y <= (Y_BORDER // 2) + 99):
            finished = True
            menuFinished = True
            doASave = True
            return
            
        

    global FPS
    global clock
    global finished
    global screen
    
    menuFinished = False

    #Menu Loop
    while (not menuFinished) and (not finished):
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                processClick(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finished == True
                    return

        #Drawing menu elements
        drawMenu()

        drawContinueMenu()
        drawLeaderboardMenu()
        drawTutorialMenu()
        drawQuitMenu()
        drawQuitAndSaveMenu()

        pygame.display.update()

        screen.fill((255, 255, 255))


    
def tutorialLoop():
    '''
    Starts the tutorial menu.
    '''
    def drawTutorial():
        '''
        Draws all the text of tutorial
        '''
        def drawTextTutorial():
            '''
            Draws Обучение
            '''
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 40)
            textSurface = myFont.render('Обучение', False, (0, 0, 0))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                      (Y_BORDER // 2) - 180))

        
        def drawText(text, height):
            '''
            Draws given text at the given height relative to
            y = (Y_BORDER // 2) - 120
            text - given text;
            height - given height.
            '''
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 24)
            textSurface = myFont.render(text, False, (0, 0, 0))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - 400,
                                      (Y_BORDER // 2) - 120 + height))

        drawTextTutorial()
        
        textArray = ['Цель игры:',
                     '  Уничтожайте цели и опасайтесь бомб!',
                     ' Зажимайте мышь и стреляйте.'
                     ' Будьте осторожны: бомбы (в т.ч. ',
                     'ваши) могут  разрушить танк, в который попали.',                    'Управление:',
                     '  ESC - выйти в меню;',
                     '  W - выстрел ракетой;',
                     '  A, D - движение танка;',
                     '  S - поменять танк.']

        for i in range(len(textArray)):
            drawText(textArray[i], i * 40)

        
        
        
    global FPS
    global clock
    global finished
    global screen
    
    tutorialFinished = False

    #Tutorial Loop
    while not tutorialFinished:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    tutorialFinished == True
                    return
                
        #Draw settings text
        drawTutorial()
        
        pygame.display.update()

        screen.fill((255, 255, 255))
    
def leaderboardLoop():
    '''
    Leaderboard menu
    '''
    def drawLeaderboard():
        '''
        Draw text for leaderboard
        '''

        def drawTextLeaderboard():
            '''
            Draws Таблица лидеров
            '''
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 40)
            textSurface = myFont.render('Таблица лидеров', False, (0, 0, 0))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                      (Y_BORDER // 2) - 180))

        def drawName(number, name, height):
            '''
            Draws given name and number in leaderboard at the left part
            of the screen at the given height relative to
            y = (Y_BORDER // 2) - 120.
            text - given text;
            height - given height.
            '''
            text = str(number) + '. ' + str(name)
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 24)
            textSurface = myFont.render(text, False, (0, 0, 0))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - 250,
                                      (Y_BORDER // 2) - 120 + height))
            
        def drawScore(score, height):
            '''
            Draws given score in leaderboard at the right part
            of the screen at the given height relative to
            y = (Y_BORDER // 2) - 120.
            text - given text;
            height - given height.
            '''
            text = str(score) + ' pts.'
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 24)
            textSurface = myFont.render(text, False, (255, 255, 255))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - (width // 2) + 150,
                                      (Y_BORDER // 2) - 120 + height))
        
        nonlocal data

        drawTextLeaderboard()

        number = 1
        
        for w in sorted(data, key=data.get, reverse=True):
            drawName(number, w, number * 40)
            drawScore(data[w], number * 40)
            number +=1
            if number > 10:
                break
        
    
    try:
        with open('leaderboard.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}


    leaderboardFinished = False
    
    #Leaderboard loop
    while not leaderboardFinished:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    leaderboardFinished == True
                    return
                
        #Draw leaderboard text
        drawLeaderboard()
        
        pygame.display.update()

        screen.fill((255, 255, 255))


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
    screen.blit(textSurface, ((X_BORDER // 2) - (width // 2), (Y_BORDER) // 3))


def saveData(name):
    '''
    Saves data to leaderboard.json
    name - name that will be written in file
    '''
    global score
    data = {}
    try:
        with open('leaderboard.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    if name in data:
        print('Вы уверены, что хотите сохранить очки под этим именем? \n')
        if int(data[name]) > score:
            print('Если вы впишете очки под этим именем, то понизите рекорд.\n')
        print('Если Вы уверены, то введите Y. Иначе данные не сохранятся\n')
        print('Сохранить данные?')
        answer = input()
        if answer != 'Y':
            return
        
    data[name] = score
    with open('leaderboard.json', 'w') as f:
        json.dump(data, f)

def gameOver():
    global finished
    global score
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MS', 22)
    text = 'Игра закончена. Вы заработали ' + str(score) + ' очков'
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MS', 22)
    textSurface = myFont.render(text, False, (0, 0, 0))
    width = textSurface.get_width()
    screen.blit(textSurface, ((X_BORDER // 2) - (width // 2), (Y_BORDER) // 3))

def askASave():
    answer = input('Сохранить данные? Y, если Да.\n')
    return answer == 'Y'

pygame.init()
screen = pygame.display.set_mode((X_BORDER, Y_BORDER))
bullet = 0
balls = []
numberOfTargets = 5
targets = [Target(screen) for i in range(numberOfTargets)]
for i in range(len(targets)):
    if uniform(0, 1) < 0.4:
        targets[i] = Invader(screen)

numberOfGuns = 3
activeGun = 0
guns = [Gun(screen) for i in range(numberOfGuns)]

score = 0
levelTimer = 4 * FPS
countBullets = True
doASave = False
countBullets = True
gameOverCounter = 150

ax = 0
ay = 1.5

clock = pygame.time.Clock()
gun = Gun(screen)
finished = False

while not finished:
    screen.fill(WHITE)

    if numberOfGuns <= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                doASave = askASave()
                finished = True
        if gameOverCounter <= 0:
            doASave = askASave()
            finished = True
        gameOver()
        gameOverCounter -= 1
        pygame.display.update()
        clock.tick(FPS)
        continue

    activeGun = activeGun % numberOfGuns

    
    if len(targets) == 0:
        startText()
        if levelTimer > 0:
            levelTimer -= 1
            countBullets = False
        else:
            levelTimer = 4 * FPS
            targets = [Target(screen) for i in range(numberOfTargets)]
            for i in range(len(targets)):
                if uniform(0, 1) < 0.4:
                    targets[i] = Invader(screen)
            bullet = 0
            countBullets = True
            balls = []
    
    drawScore()
    for g in guns:
        g.draw()
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
            guns[activeGun].fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            guns[activeGun].fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            
            guns[activeGun].targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menuLoop()
            elif event.key == pygame.K_w:
                guns[activeGun].rocket_fire(pygame.mouse.get_pos())
            elif event.key == pygame.K_s:
                activeGun +=1
                activeGun = activeGun % numberOfGuns

    if pygame.key.get_pressed()[pygame.K_d]:
        guns[activeGun].move_right()
    if pygame.key.get_pressed()[pygame.K_a]:
        guns[activeGun].move_left()



    for b in balls:
        b.move()
        if b.vx ** 2 + b.vy ** 2 < 0.1:
            balls.remove(b)
        for t in targets:
            if b.hittest(t, -1) and t.live:
                t.live = 0
                t.hit()
                score += t.points
                targets.remove(t)
        for g in guns:
            if b.hittest(g, guns.index(g)):
                guns.remove(g)
                numberOfGuns -= 1
    for t in targets:
        t.move()
        if uniform(0,1) < 0.03 and type(t).__name__ == 'Invader':
            t.bomb()
            
    try:
        guns[activeGun].power_up()
    except IndexError:
        pass

pygame.quit()
if doASave:
    saveData(input('Введите имя\n'))
