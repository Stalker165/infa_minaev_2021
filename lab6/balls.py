import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
size = 800  # сделаем экран квадратным со стороной size
screen = pygame.display.set_mode((size, size))
font = pygame.font.Font(None, 40)  # шрифт, которым будем писать счёт
font_name = pygame.font.match_font('arial')

# declare colors
WHITE = (255, 255, 255)
CRIMSON = (220, 20, 60)
STEELBLUE = (70, 130, 180)
SEAGREEN = (46, 139, 87)
BLUEVIOLET = (138, 43, 226)
DODGERBLUE = (30, 144, 255)
GOLDENROD = (218, 165, 32)
DEEPPINK = (255, 20, 147)
SANDYBROWN = (244, 164, 96)
BLACK = (0, 0, 0)
COLORS = [CRIMSON, STEELBLUE, SEAGREEN, BLUEVIOLET, DODGERBLUE, GOLDENROD, DEEPPINK, SANDYBROWN]
N = 5  # number of initial generating balls on the screen

def new_ball(N):
    """
    creates ball with random parameters and makes parameters of position and radius global
    x, y -- coordinates
    r -- radius
    N -- number of balls
    E -- variable of existing (after click becomes 0)
    """
    global x, y, Vx, Vy, r, color, E
    x = []
    y = []
    Vx = []
    Vy = []
    r = []
    color = []
    E = [1]*N
    for i in range(0, N):
        x.append(randint(0, size))
        y.append(randint(0, size))
        Vx.append(randint(-40, 40))
        Vy.append(randint(-40, 40))
        r.append(randint(30, 50))
        color.append(COLORS[randint(0, len(COLORS)-1)])
        circle(screen, color[i], (x[i], y[i]), r[i])


def draw_text(surf, text, size, x, y):
    """
    writes text on screen to show count
    surf -- surface of drawing
    size -- size of text
    x, y -- position
    """
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

count = 0  # creates a counter that counts points -- number of clicks by ball
new_ball(N)  # creates N balls

while not finished:
    clock.tick(FPS)
    text = font.render(str(count), True, WHITE)
    place = text.get_rect(center=(size / 2, 30))
    screen.blit(text, place)  # creates text with count
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(N):
                if (x[i] - event.pos[0]) ** 2 + (y[i] - event.pos[1]) ** 2 <= r[i] ** 2:  # if the click hit the ball
                    print('Click!')
                    count += 1
                    E[i] = 0
    for i in range(N):
        if E[i] == 1:
            x[i] += Vx[i]
            y[i] += Vy[i]
            circle(screen, color[i], (x[i], y[i]), r[i])
        else:  # doesn't draw after-click balls on visible screen
            x[i], y[i] = -1, -1
            r[i] = 0
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
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()