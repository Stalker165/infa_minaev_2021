import math
import random
import pygame as pg

FPS = 30

CRIMSON = (220, 20, 60)
SEAGREEN = (46, 139, 87)
BLUEVIOLET = (138, 43, 226)
NAVY = (0, 0, 128)
GOLDENROD = (218, 165, 32)
DEEPPINK = (255, 20, 147)
GAME_COLORS = [CRIMSON, SEAGREEN, BLUEVIOLET, NAVY, GOLDENROD, DEEPPINK]
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D

WIDTH = 800
HEIGHT = 600

g = 5  # acceleration of gravity
mu = 0.85  # variable of energy loss
N = 1  # number of targets


def draw_text(surf, text, size, x, y):
    """
    Генерирует текст
    surf - поверхность рисования
    size - размер
    x, y - местоположение
    """
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def RectCircleColliding(ball, rect):
    """ Проверяет, пересекается ли круг ball с прямоугольником rect """
    distX = abs(ball.x - rect.x - rect.w/2)
    distY = abs(ball.y - rect.y - rect.h/2)

    if distX > (rect.w/2 + ball.r) or distY > (rect.h/2 + ball.r):
        return False
    elif distX <= (rect.w/2) or distY <= (rect.h/2):
        return True
    else:
        dx = distX - rect.w/2
        dy = distY - rect.h/2
        return dx**2 + dy**2 <= circle.r ** 2


class Ball:
    def __init__(self, x, y, color):
        """ Конструктор класса Ball

        x, y - координаты по горизонтали и вертикали соотв.
        r - радиус
        vx, vy - скорости по горизонтали и вертикали соотв.
        color - цвет
        timer - таймер, не позволяет шарам оставаться на экране слишком долго
        hit - переменная, проверяющая, была ли уже сбита цель этим шаром
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = color
        self.timer = 0
        self.hit = 0

    def move(self):
        """ Перемещение шара по прошествии единицы времени.

        Метод описывает перемещение шара за один кадр перерисовки: обновляет значения
        self.x и self.y в соответствиии со значениями self.vx и self.vy, силы гравитации g, действующей на шар,
        и расстановки стен
        """
        if self.timer <= FPS * 3:
            self.x += self.vx
            self.y += self.vy
            self.vy += g
            if self.x + self.r >= WIDTH:
                self.x = WIDTH - self.r
                self.vx = - self.vx * mu
            elif self.y - self.r <= 0:
                self.y = self.r
                self.vy = - self.vy * mu + g
            elif self.y + self.r >= HEIGHT:
                self.y = HEIGHT - self.r
                self.vy = - self.vy * mu + g
            self.timer += 1
        else:
            self.x, self.y, self.vx, self.vy, self.r = -1, -1, 0, 0, 1
            del self

    def draw(self):
        """ Рисование шара """
        if self.timer <= FPS * 3:
            pg.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """ Метод проверяет, сталкивалкивается ли шар с объектом obj """
        if math.hypot(self.x - obj.x, self.y - obj.y) <= self.r + obj.r:
            return True
        else:
            return False


class Target:
    def __init__(self):
        """ Задание параметров цели """
        self.r = random.randint(20, 50)
        self.x = random.randint(self.r, WIDTH - self.r)
        self.y = random.randint(self.r, HEIGHT - self.r)
        self.vx = random.randint(-20, 20)
        self.vy = random.randint(-20, 20)
        self.color = random.choice(GAME_COLORS)

    def par_target(self):
        """ Изменение параметров цели """
        self.__init__()

    def move(self):
        """
        Метод описывает перемещение цели за один кадр перерисовки: обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и расстановки стен.
        """

        self.x += self.vx
        self.y += self.vy

        if self.x - self.r <= 0:
            self.x = 0 + self.r
            self.vx = - self.vx
        elif self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = - self.vx
        elif self.y - self.r <= 0:
            self.y = self.r
            self.vy = - self.vy
        elif self.y + self.r >= HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = - self.vy

    def draw(self):
        """ Рисование мишени """
        pg.draw.circle(screen, self.color, (self.x, self.y), self.r)


class Trojan:
    def __init__(self):
        """ Инициализация параметров "бомбочки", содержащей в себе другие цели - троянский конь """
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.w = 60
        self.h = 20
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)
        self.color = random.choice(GAME_COLORS)

    def move(self):
        """ Перемещение бомбы по прошествии единицы времени """
        self.x += self.vx
        self.y += self.vy
        if self.x + self.w >= WIDTH:
            self.x = WIDTH - self.w
            self.vx = - self.vx
        elif self.x - self.w <= 0:
            self.x = self.w
            self.vx = - self.vx
        elif self.y - self.h <= 0:
            self.y = self.h
            self.vy = - self.vy
        elif self.y + self.h >= HEIGHT:
            self.y = HEIGHT - self.h
            self.vy = - self.vy

    def draw(self):
        """ Рисование троянского коня """
        pg.draw.rect(screen, self.color, (self.x, self.y), (self.w, self.h))

    def hittest(self, obj):
        """ Метод проверяет, сталкивалкивается ли бомба с объектом obj """
        return RectCircleColliding(obj, self)


class Gun:
    def __init__(self, x, y, color):
        """ Инициализация параметров орудия
        x, y - положение
        V - скорость
        M - магазин
        firepower - начальная силы выстрела
        ready - готовность к выстрелу
        angle - угол
        COLOR - цвет пушки (привязан)
        color - цвет пушки в данный момент
        r - радиус круга, рисуемого вместо с пушкой
        """
        self.x = x
        self.y = y
        self.V = 5
        self.M = 4
        self.firepower = 20
        self.ready = 0
        self.angle = 1
        self.COLOR = color
        self.color = self.COLOR
        self.r = 15

    def fire(self, event):
        """ Выстрел шаром

        Происходит при отпускании кнопки мыши
        Начальные значения компонент скорости шара vx и vy зависят от положения мыши
        """
        global balls
        new_ball = Ball(self.x, self.y, self.color)
        new_ball.r += 5
        self.angle = math.atan2((self.y - event.pos[1]), event.pos[0] - self.x)
        new_ball.vx = self.firepower * math.cos(self.angle)
        new_ball.vy = - self.firepower * math.sin(self.angle)
        balls.append(new_ball)
        self.ready = 0
        self.firepower = 20

    def aiming(self, event):
        """ Прицеливание. Зависит от положения мыши, считываемого через event """
        if event:
            self.angle = math.atan2((self.y - event.pos[1]), event.pos[0] - self.x)
        if self.M != 0:
            self.color = self.COLOR
        else:
            self.color = GREY

    def draw(self):
        """ Рисование пушки в зависимости от направления и времени удержания кнопки мыши """
        pg.draw.line(screen, self.color, [self.x, self.y], [self.x + self.firepower * math.cos(self.angle),
                                                                self.y - self.firepower * math.sin(self.angle)], 8)
        pg.draw.circle(screen, self.color, [self.x, self.y], self.r)

    def power_up(self):
        """
        Определение силы выстрела и параметров самой пушки
        в зависимости от времени удержания кнопки мыши
        """
        if self.ready:
            if self.firepower < 80:
                self.firepower += 4
        if self.M != 0:
            self.color = self.COLOR
        else:
            self.color = GREY

    def move_left(self):
        """ Реализует движение влево """
        if self.x >= self.r:
            self.x -= self.V

    def move_right(self):
        """ Реализует движение вправо """
        if self.x <= WIDTH - self.r:
            self.x += self.V

pg.init()
font = pg.font.Font(None, 40)
font_name = pg.font.match_font('arial')

screen = pg.display.set_mode((WIDTH, HEIGHT))
balls = []
targets = []
trojans = []
timer = 0  # creates timer
score = 0
finished = False

clock = pg.time.Clock()
gun = Gun(40, 450, NAVY)
gun2 = Gun(WIDTH - 40, 450, CRIMSON)
for _ in range(N):
    targets.append(Target())

while not finished and timer <= FPS * 90:
    screen.fill(WHITE)
    gun.draw()
    gun2.draw()
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()
    text = font.render(str(score), True, NAVY)
    place = text.get_rect(center=(WIDTH / 3, 30))
    screen.blit(text, place)  # creates text with score

    text = font.render(str(90 - int(timer // FPS)), True, NAVY)
    place = text.get_rect(center=(3 * WIDTH / 4, 30))
    screen.blit(text, place)  # creates text with countdown

    pg.display.update()

    clock.tick(FPS)
    timer += 1

    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        gun.move_left()
    elif keys[pg.K_d]:
        gun.move_right()
    if keys[pg.K_LEFT]:
        gun2.move_left()
    elif keys[pg.K_RIGHT]:
        gun2.move_right()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # если нажата ЛКМ
                if gun.M != 0:
                    gun.ready = 1
                else:
                    print("Это тебе не кино, приятель! Патроны не бесконечны!")
            if event.button == 3:  # если нажата ПКМ
                if gun2.M != 0:
                    gun2.ready = 1
                else:
                    print("Это тебе не кино, приятель! Патроны не бесконечны!")
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if gun.ready:
                    gun.fire(event)
                    gun.M -= 1
            if event.button == 3:
                if gun2.ready:
                    gun2.fire(event)
                    gun2.M -= 1
        elif event.type == pg.MOUSEMOTION:
            gun.aiming(event)
            gun2.aiming(event)

    for b in balls:
        b.move()
        for t in targets:
            if b.hittest(t):
                t.par_target()
                score += 1

    for t in targets:
        t.move()
    new_N = int(score // 20 + 1)
    for _ in range(new_N - N):
        targets.append(Target())
    N = new_N
    gun.power_up()
    gun2.power_up()

    if gun.M < 5 and timer % 30 == 0:
        gun.M += 1
        gun2.M += 1

    if timer % (FPS * 30) == 0:
        print("Прошло ", int(timer / FPS), " секунд.")
pg.quit()

print('YOUR SCORE: ', score)
