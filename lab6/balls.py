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

x = [0] * (N + 1)
y = [0] * (N + 1)
Vx = [0] * (N + 1)
Vy = [0] * (N + 1)
r = [0] * (N + 1)
color = [0] * (N + 1)


def parameters(n):
    """
    choose random parameters of coordinates (x, y), velocity (Vx, Vy), radius (r), color for balls
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
    Vx, Vy -- velocity
    r -- radius
    N -- number of balls
    """
    for i in range(0, N):
        x[i], y[i], Vx[i], Vy[i], r[i], color[i] = parameters(1)
        circle(screen, color[i], (x[i], y[i]), r[i])


def re_ball(i):
    """
    describes behavior of ball after click -- recreate the ball like new
    x, y -- coordinates
    Vx, Vy -- velocity
    r -- radius
    color -- color
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
        # 0.5 to avoid division by zero
        Vy[N] += g * (y[N] - size / 2 + 0.5) / abs(y[N] - size / 2 + 0.5)
        Vx[N] += g * (x[N] - size / 2 + 0.5) / abs(x[N] - size / 2 + 0.5)
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
    x, y -- coordinates
    Vx, Vy -- velocity
    r -- radius
    color -- color
    E -- variable of existing (1 -> exists, 0 -> not exists)
    """
    global E
    E = 1
    x[N], y[N], Vx[N], Vy[N], r[N], color[N] = parameters(2)
    circle(screen, color[N], (x[N], y[N]), r[N])


pg.mixer.init()
chpok = pg.mixer.Sound('chpok.ogg')
extra = pg.mixer.Sound('extra.ogg')
jackpot = pg.mixer.Sound('jackpot.ogg')
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
    screen.blit(text, place)  # creates text with score

    text = font.render(str(90 - int((timer * FPS / 1000) // 1)), True, WHITE)
    place = text.get_rect(center=(3 * size / 4, 30))
    screen.blit(text, place)  # creates text with countdown

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for i in range(N):
                if (x[i] - event.pos[0]) ** 2 + (y[i] - event.pos[1]) ** 2 <= r[i] ** 2:
                    # if the click hits the ball
                    pg.mixer.Sound.play(chpok)
                    print('Click!')
                    score += 1
                    re_ball(i)
                    if jackpot_count > 0:
                        jackpot_count = 1
                    for i in range(N):
                        if color[0] == color[i]:
                            jackpot_count += 1
                        if jackpot_count == N + 1:
                            pg.mixer.Sound.play(jackpot)
                            print('Jackpot!')
                            score += N + len(COLORS)
                            jackpot_count = -999  # won't allow take jackpot 2 times per game
            if (x[N] - event.pos[0]) ** 2 + (y[N] - event.pos[1]) ** 2 <= r[N] ** 2:
                pg.mixer.Sound.play(extra)
                print('EXTRA Click!')
                score += 10
                E, extra_timer, r[N] = 0, 0, 0
                x[N], y[N] = -1, -1
    if timer % (18 * FPS) == 0:
        extra_target()
    for i in range(N):
        physics(i, 1)
        circle(screen, color[i], (x[i], y[i]), r[i])
    if E == 1:
        physics(N, mu)
        extra_timer += 1
        if E == 1 and timer % (FPS/2) == 0:
            color[N] = COLORS[randint(0, len(COLORS) - 1)]
        circle(screen, color[N], (x[N], y[N]), r[N])
        if extra_timer == 6 * FPS:
            E = 0
            extra_timer = 0
    pg.display.update()
    screen.fill(BLACK)
pg.quit()

print('YOUR SCORE: ', score)
print('Enter your name: ')
name_now = str(input())
if len(name_now) < 9:
    name_now = ' ' * (9 - len(name_now)) + name_now

line_count = 0
place = []
name = []
result = []
with open('Balls game leaders.txt', 'r') as f:
    tab = f.read
    for line in f:
        name.append(line.split(' | ')[1])
        result.append(line.split(' | ')[2])
        result[line_count] = int(result[line_count].replace("\n", ""))
        line_count += 1

place_now = line_count
for i in range(0, line_count):
    if score > int(result[i]):
        place_now = i
        break

name.insert(place_now, name_now)
result.insert(place_now, score)

with open('Balls game leaders.txt', 'w') as file:
    for i in range(0, line_count + 1):
        stroka = str(i+1) + ' | ' + str(name[i]) + ' | ' + str(result[i]) + '\n'
        file.write(stroka)

print('Your place:', place_now + 1)