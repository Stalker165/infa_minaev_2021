import pygame as pg
from pygame.draw import *
from random import randint
pg.init()

FPS = 30
size = 800  # сделаем экран квадратным со стороной size
screen = pg.display.set_mode((size, size))
font = pg.font.Font(None, 40)  # шрифт, которым будем писать счёт
font_name = pg.font.match_font('arial')

# declare colors
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


def parameters():
    """
    choose random parameters of coordinates (x, y), speed (Vx, Vy), radius (r), color for balls
    returns these parameters as list
    """
    x = randint(0, size)
    y = randint(0, size)
    Vx = randint(-35, 35)
    Vy = randint(-35, 35)
    r = randint(30, 50)
    color = COLORS[randint(0, len(COLORS) - 1)]
    return [x, y, Vx, Vy, r, color]


def new_ball(N):
    """
    creates ball with random parameters and makes parameters of position and radius global
    x, y -- coordinates
    r -- radius
    N -- number of balls
    """
    global x, y, Vx, Vy, r, color
    x = [0]*N
    y = [0]*N
    Vx = [0]*N
    Vy = [0]*N
    r = [0]*N
    color = [0]*N
    for i in range(0, N):
        x[i], y[i], Vx[i], Vy[i], r[i], color[i] = parameters()
        circle(screen, color[i], (x[i], y[i]), r[i])


def re_ball(i):
    """
    describes behavior of ball after click -- recreate the ball like new
    i -- number of ball
    """
    x[i], y[i], Vx[i], Vy[i], r[i], color[i] = parameters()


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


def physics_of_hit(i):
    """
    describes behavior of the ball when it hit the wall and changes parameters
    i -- number of ball
    """
    if x[i] <= 0:  # physics of hits
        x[i] = 0
        Vx[i] = -Vx[i]
    elif x[i] >= size:
        x[i] = size
        Vx[i] = -Vx[i]
    elif y[i] <= 0:
        y[i] = 0
        Vy[i] = -Vy[i]
    elif y[i] >= size:
        y[i] = size
        Vy[i] = -Vy[i]


pg.mixer.init()
chpok = pg.mixer.Sound('chpok.ogg')
pg.mixer.music.load('forest theme.mp3')

pg.display.update()
clock = pg.time.Clock()
finished = False

timer = 0  # creates timer
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
                if (x[i] - event.pos[0]) ** 2 + (y[i] - event.pos[1]) ** 2 <= r[i] ** 2:  # if the click hit the ball
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
    for i in range(N):
        x[i] += Vx[i]
        y[i] += Vy[i]
        circle(screen, color[i], (x[i], y[i]), r[i])
        physics_of_hit(i)

    pg.display.update()
    screen.fill(BLACK)

pg.quit()