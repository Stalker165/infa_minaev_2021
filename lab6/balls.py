import pygame as pg
from pygame.draw import *
from random import randint
pg.init()

FPS = 30
size = 800  # сделаем экран квадратным со стороной size
screen = pg.display.set_mode((size, size))
font = pg.font.Font(None, 40)  # шрифт, которым будем писать счёт
font_name = pg.font.match_font('arial')

# declare variables
WHITE = (255, 255, 255)
CRIMSON = (220, 20, 60)
SEAGREEN = (46, 139, 87)
BLUEVIOLET = (138, 43, 226)
DODGERBLUE = (30, 144, 255)
GOLDENROD = (218, 165, 32)
DEEPPINK = (255, 20, 147)
BLACK = (0, 0, 0)
COLORS = [CRIMSON, SEAGREEN, BLUEVIOLET, DODGERBLUE, GOLDENROD, DEEPPINK]
N = 5  # number of initial generating balls on the screen
g = 1.2  # acceleration of gravity
mu = 0.9  # variable makes extra physics for extra target
E = 0  # variable of existence of extra target


def parameters(n):
    """
    choose random parameters of coordinates (x, y), speed (Vx, Vy), radius (r), color for balls
    returns these parameters as list
    n -- variable influences V and r (n = 1 for balls and n = 2 for extra target -- faster and smaller)
    """
    x = randint(0, size)
    y = randint(0, size)
    Vx = randint(-35 * n, 35 * n)
    Vy = randint(-35 * n, 35 * n)
    r = randint(30 / n, 50 / n)
    color = COLORS[randint(0, len(COLORS) - 1)]
    return [x, y, Vx, Vy, r, color]


def new_ball(N):
    """
    creates lists of parameters for balls and extra target with index N
    creates ball with random parameters and makes parameters of position and radius global
    x, y -- coordinates
    r -- radius
    N -- number of balls
    """
    global x, y, Vx, Vy, r, color
    x = [0] * (N+1)
    y = [0] * (N+1)
    Vx = [0] * (N+1)
    Vy = [0] * (N+1)
    r = [0] * (N+1)
    color = [0] * (N+1)
    for i in range(0, N):
        x[i], y[i], Vx[i], Vy[i], r[i], color[i] = parameters(1)
        circle(screen, color[i], (x[i], y[i]), r[i])


def re_ball(i):
    """
    describes behavior of ball after click -- recreate the ball like new
    i -- number of ball
    """
    x[i], y[i], Vx[i], Vy[i], r[i], color[i] = parameters(1)


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


def physics(i, mu):
    """
    describes movement of the balland changes parameters
    i -- number of ball, or i = N means movement of extra target
    mu -- variable makes extra physics for extra target
    g -- acceleration of gravity
    x, y -- coordinates
    Vx, Vy -- velocity
    r -- radius, used when describing hit
    """
    x[i] += Vx[i]
    y[i] += Vy[i]
    if i == N:
        Vy[N] += g * (y[N] - size / 2) / abs(y[N] - size / 2)
        Vx[N] += g * (x[N] - size / 2) / abs(x[N] - size / 2)
    if x[i] - r[i] <= 0:  # physics of hits
        x[i] = r[i]
        Vx[i] = -Vx[i] * mu
    elif x[i] + r[i] >= size:
        x[i] = size - r[i]
        Vx[i] = -Vx[i] * mu
    elif y[i] - r[i] <= 0:
        y[i] = r[i]
        Vy[i] = -Vy[i] * mu
    elif y[i] + r[i] >= size:
        y[i] = size - r[i]
        Vy[i] = -Vy[i] * mu


def extra_target():
    """
    creates very fast and small target shimmers with colors from COLORS
    target subjects to gravity
    x_e, y_e -- coordinates
    Vx_e, Vy_e -- velocity
    color_e -- color
    E -- variable of existing (1 -> exists, 0 -> not exists)
    """
    global E
    E = 1
    for i in range(0, N):
        x[N], y[N], Vx[N], Vy[N], r[N], color[N] = parameters(2)
        circle(screen, color[N], (x[N], y[N]), r[N])


# print('Введите своё имя: ')
# name = str(input())
name = 'player'

pg.mixer.init()
chpok = pg.mixer.Sound('chpok.ogg')
extra = pg.mixer.Sound('extra.ogg')
pg.mixer.music.load('forest theme.mp3')

pg.display.update()
clock = pg.time.Clock()
finished = False

timer = 0  # creates timer
extra_timer = 0  # timer for extra target
score = 0  # creates a counter that counts points -- number of clicks by ball
jackpot_count = 1  # counts how many balls have some colors. Jackpot can be got <= 1 times
new_ball(N)  # creates N balls
pg.mixer.music.play(-1)

while not finished and timer <= 2999:
    clock.tick(FPS)
    timer += 1

    text = font.render(str(score), True, WHITE)
    place = text.get_rect(center=(size / 3, 30))
    screen.blit(text, place)  # creates text with count

    text = font.render(str(int((timer * 30 / 1000) // 1)), True, WHITE)
    place = text.get_rect(center=(3 * size / 4, 30))
    screen.blit(text, place)  # creates text with timer

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if jackpot_count > 0:
                jackpot_count = 1
            for i in range(N):
                if (x[i] - event.pos[0]) ** 2 + (y[i] - event.pos[1]) ** 2 <= r[i] ** 2:
                    # if the click hits the ball
                    print('Click!')
                    pg.mixer.Sound.play(chpok)
                    score += 1
                    re_ball(i)
                    for i in range(N):
                        if color[0] == color[i]:
                            jackpot_count += 1
                        if jackpot_count == N + 1:
                            print('Jackpot!')
                            score += N + len(COLORS)
                            jackpot_count = -999  # won't allow take jackpot 2 times per game
            if (x[N] - event.pos[0]) ** 2 + (y[N] - event.pos[1]) ** 2 <= r[N] ** 2:
                print('EXTRA Click!')
                pg.mixer.Sound.play(extra)
                score += 10
                E = 0
                x[N], y[N] = -1, -1
                r[N] = 0
                extra_timer = 0
    if timer % (18 * FPS) == 0:
        extra_target()
    for i in range(N):
        physics(i, 1)
        circle(screen, color[i], (x[i], y[i]), r[i])
    if E == 1:
        physics(N, mu)
        extra_timer += 1
        if timer % (FPS/2) == 0:
            color[N] = COLORS[randint(0, len(COLORS) - 1)]
        circle(screen, color[N], (x[N], y[N]), r[N])
        if extra_timer == 6 * FPS:
            E = 0
            extra_timer = 0
    pg.display.update()
    screen.fill(BLACK)

pg.quit()