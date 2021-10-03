import pygame
from pygame.draw import *

pygame.init()

def glare(color, x, y, r):
    # имитация источника света
    layer = pygame.Surface((screen_x, screen_y))
    layer.set_colorkey((0, 0, 0))
    for i in range(int(r)):  # здесь он ругался на то, что r это float, не знаю, почему
        layer.set_alpha(25 - i*25/r)
        ellipse(layer, color, (x - 2*i, y - 2*i, 4*i, 4*i))
        screen.blit(layer, (0, 0))

def sun(color, x, y, a, b, w):
    # солнышко
    glare(color, x, y, w * 2.5)
    glare(color, x - a + w/2, y, w * 2)
    glare(color, x + a - w/2, y, w * 2)
    glare(color, x, y - b + w/2, w * 2)
    glare(color, x, y + b - w/2, w * 2)
    # размеры бликов подобраны в соответствии с размерами солнца, где w - ширина кольца на картинке

    layer = pygame.Surface((screen_x, screen_y))
    layer.set_colorkey((0, 0, 0))
    layer.set_alpha(150)
    ellipse(layer, color, (x-a, y-b, 2*a, 2*b), w)
    ellipse(layer, color, (x - 30, y - 30, 60, 60))
    screen.blit(layer, (0, 0))

    layer = pygame.Surface((screen_x, screen_y))
    layer.set_colorkey((0, 0, 0))
    layer.set_alpha(150)
    rect(layer, color, (x-a, y-20, 2*a, 40))
    screen.blit(layer, (0, 0))

    layer = pygame.Surface((screen_x, screen_y))
    layer.set_colorkey((0, 0, 0))
    layer.set_alpha(150)
    rect(layer, color, (x-20, y-b, 40, 2*b))
    screen.blit(layer, (0, 0))

#def bear(x, y, m):


#def fish (x,y):



FPS = 30
screen_x = 794
screen_y = 1123
screen = pygame.display.set_mode((screen_x, screen_y))

horizont = screen_y // 2  # линия горизонта

rect(screen, (0, 255, 255), (0, 0, screen_x, horizont))  # вторая точка указывается относительно первой!
rect(screen, (230, 230, 230), (0, horizont, screen_x, screen_y))
line(screen, (0, 0, 0), (0, horizont), (screen_x, horizont))
circle(screen, (255, 220, 0), (200, 200), 100, 0)
polygon(screen, (0, 0, 0), [(120, 120), (130, 120),
                            (185, 165), (180, 170)])

sun((255, 246, 213), 472, 193, 230, 230, 40)

pygame.image.save(screen, "bear.png")

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True


pygame.quit()