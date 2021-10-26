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
M = 4  # magazine of weapon


def draw_text(surf, text, size, x, y):
    """
    writes text on screen to show count
    surf -- surface of drawing
    size -- size of text
    x, y -- position
    """
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Ball:
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x, y -- координаты по горизонтали и вертикали соотв.
        r - радиус
        vx, vy -- скорости по горизонтали и вертикали соотв.
        color -- цвет
        timer -- таймер, не позволяет шарам оставаться на экране слишком долго
        hit -- переменная, проверяющая, была ли уже сбита цель этим мячом
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
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.timer <= 90:
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
        if self.timer <= FPS * 3:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2) <= self.r + obj.r:
            return True
        else:
            return False


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball()
        new_ball.r += 5
        self.an = math.atan2((450 - event.pos[1]), event.pos[0] - 40)
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((450 - event.pos[1]), event.pos[0] - 40)
        if self.f2_on:
            self.color = NAVY
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(screen, self.color, [40, 450], [40 + self.f2_power * math.cos(self.an),
                                                         450 - self.f2_power * math.sin(self.an)], 4)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 4
            self.color = NAVY
        else:
            self.color = GREY


class Target:
    def __init__(self):
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.vx = random.randint(-20, 20)
        self.vy = random.randint(-20, 20)
        self.r = random.randint(20, 50)
        self.color = random.choice(GAME_COLORS)

    def par_target(self):
        """ Инициализация новой цели. """
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.vx = random.randint(-20, 20)
        self.vy = random.randint(-20, 20)
        self.r = random.randint(20, 50)
        self.color = random.choice(GAME_COLORS)

    def move(self):
        """Переместить цель по прошествии единицы времени.

        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и стен по краям окна (размер окна 800х600).
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
for _ in range (N):
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

    text = font.render(str(90 - int((timer * FPS / 900) // 1)), True, NAVY)
    place = text.get_rect(center=(3 * WIDTH / 4, 30))
    screen.blit(text, place)  # creates text with countdown"""

    pygame.display.update()

    clock.tick(FPS)
    timer += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if M > 0:
                gun.fire2_end(event)
                M -= 1
            else:
                print("Это тебе не кино, приятель! Патроны не бесконечны!")
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
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
    new_N = int((N/10) // 1 + 1)
    for _ in range(new_N - N):
        targets.append(Target())
    N = new_N
    gun.power_up()

    if M < 5 and timer % 30 == 0:
        M += 1

    if timer % (FPS * 30) == 0:
        print("Прошло ", int(timer/FPS), " секунд.")
pygame.quit()

print('YOUR SCORE: ', score)