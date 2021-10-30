import math
import random
import pygame

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

g = 6  # acceleration of gravity
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


class Ball:
    def __init__(self, x=40, y=450):
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
        self.color = NAVY
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
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """ Метод проверяет, сталкивалкивается ли шар с объектом obj.

        Args:
            obj: Объект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения шара и obj, иначе - False.
        """
        if math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2) <= self.r + obj.r:
            return True
        else:
            return False


class Gun:
    def __init__(self):
        """ Инициализация параметров
        M - магазин
        firepower - начальная силы выстрела
        ready - готовность к выстрелу
        angle, color - угол и цвет соотв.
        """
        self.M = 4
        self.firepower = 10
        self.ready = 0
        self.angle = 1
        self.color = GREY

    def fire(self, event):
        """ Выстрел шаром

        Происходит при отпускании кнопки мыши
        Начальные значения компонент скорости шара vx и vy зависят от положения мыши
        """
        global balls
        new_ball = Ball()
        new_ball.r += 5
        self.angle = math.atan2((450 - event.pos[1]), event.pos[0] - 40)
        new_ball.vx = self.firepower * math.cos(self.angle)
        new_ball.vy = - self.firepower * math.sin(self.angle)
        balls.append(new_ball)
        self.ready = 0
        self.firepower = 10

    def aiming(self, event):
        """ Прицеливание. Зависит от положения мыши, считываемого через event """
        if event:
            self.angle = math.atan2((450 - event.pos[1]), event.pos[0] - 40)
        if self.ready:
            self.color = NAVY
        else:
            self.color = GREY

    def draw(self):
        """ Рисование пушки в зависимости от направления и времени удержания кнопки мыши """
        pygame.draw.line(screen, self.color, [40, 450], [40 + self.firepower * math.cos(self.angle),
                                                         450 - self.firepower * math.sin(self.angle)], 4)

    def power_up(self):
        """
        Определение силы выстрела и параметров самой пушки
        в зависимости от времени удержания кнопки мыши
        """
        if self.ready:
            if self.firepower < 100:
                self.firepower += 4
            if self.M != 0:
                self.color = NAVY
            else:
                self.color = GREY
        else:
            self.color = GREY


class Target:
    def __init__(self):
        """ Задание параметров цели """
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.vx = random.randint(-20, 20)
        self.vy = random.randint(-20, 20)
        self.r = random.randint(20, 50)
        self.color = random.choice(GAME_COLORS)

    def par_target(self):
        """ Изменение параметров цели """
        self.__init__()

    def move(self):
        """ Перемещение

        Метод описывает перемещение цели за один кадр перерисовки: обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и расстановки стен.
        """

        self.x += self.vx
        self.y += self.vy

        if self.x - self.r <= WIDTH/2:
            self.x = WIDTH/2 + self.r
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
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


pygame.init()
font = pygame.font.Font(None, 40)
font_name = pygame.font.match_font('arial')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
balls = []
targets = []
timer = 0  # creates timer
score = 0

clock = pygame.time.Clock()
gun = Gun()
for _ in range(N):
    targets.append(Target())

finished = False

while not finished and timer <= FPS * 90:
    screen.fill(WHITE)
    gun.draw()
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

    pygame.display.update()

    clock.tick(FPS)
    timer += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gun.M != 0:
                gun.ready = 1
            else:
                print("Это тебе не кино, приятель! Патроны не бесконечны!")
        elif event.type == pygame.MOUSEBUTTONUP:
            if gun.ready:
                gun.fire(event)
                gun.M -= 1
        elif event.type == pygame.MOUSEMOTION:
            gun.aiming(event)

    for b in balls:
        b.move()
        for t in targets:
            if b.hittest(t):
                t.par_target()
                score += 1
                if score % 10 == 0:
                    N = N + 1
                    targets.append(Target())

    for t in targets:
        t.move()
    new_N = int((N / 10) // 1 + 1)
    for _ in range(new_N - N):
        targets.append(Target())
    N = new_N
    gun.power_up()

    if gun.M < 5 and timer % 30 == 0:
        gun.M += 1

    if timer % (FPS * 30) == 0:
        print("Прошло ", int(timer / FPS), " секунд.")
pygame.quit()

print('YOUR SCORE: ', score)