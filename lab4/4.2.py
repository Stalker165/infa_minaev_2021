import pygame
from pygame.draw import *

pygame.init()

black = (0, 0, 0)
sky_color = (0, 255, 255)
sun_color = (255, 246, 213)
bear_color = (230, 230, 230)
snow_color = (230, 230, 230)
pi = 3.14

def glare(color, x, y, r):
    '''
    имитация источника света
    '''
    layer = pygame.Surface((screen_x, screen_y))
    layer.set_colorkey((0, 0, 0))
    for i in range(int(r)):  # здесь он ругался на то, что r это float, не знаю, почему
        layer.set_alpha(25 - i*25/r)
        ellipse(layer, color, (x - 2 * i, y - 2 * i, 4 * i, 4 * i))
        screen.blit(layer, (0, 0))


def sun(color, x, y, a, b, w):
    '''
    Рисование солнца
    color - цвет
    x - координата центра солнца по горизонтали
    y - координата центра солнца по вертикали
    a - ширина солнца
    b - высота солнца
    w - относительный размер блика
    '''
    glare(color, x, y, w * 2.5)
    glare(color, x - a + w / 2, y, w * 2)
    glare(color, x + a - w / 2, y, w * 2)
    glare(color, x, y - b + w / 2, w * 2)
    glare(color, x, y + b - w / 2, w * 2)
    # размеры бликов подобраны в соответствии с размерами солнца, где w - ширина кольца на картинке

    layer = pygame.Surface((screen_x, screen_y))
    layer.set_colorkey((0, 0, 0))
    layer.set_alpha(150)
    ellipse(layer, color, (x - a, y - b, 2 * a, 2 * b), w)
    ellipse(layer, color, (x - 30, y - 30, 60, 60))
    screen.blit(layer, (0, 0))

    layer = pygame.Surface((screen_x, screen_y))
    layer.set_colorkey((0, 0, 0))
    layer.set_alpha(150)
    rect(layer, color, (x - a, y - 20, 2 * a, 40))
    screen.blit(layer, (0, 0))

    layer = pygame.Surface((screen_x, screen_y))
    layer.set_colorkey((0, 0, 0))
    layer.set_alpha(150)
    rect(layer, color, (x - 20, y - b, 40, 2 * b))
    screen.blit(layer, (0, 0))


def bear(color, x, y, m):
    '''
    Рисует медведя
    color - цвет
    x - координата медведя по горизонтали
    y - координата медведя по вертикали
    m - переменная масштабирования
    '''
    w_head = 176 * m
    h_head = 96 * m
    w_body = 256 * m
    h_body = 460 * m
    w_arm = 112 * m
    h_arm = 52 * m
    h_hole = 100 * m
    w_hole = 300 * m
    h_leg = 150 * m
    w_leg = 190 * m
    h_foot = 50 * m
    w_foot = 140 * m
    circle(screen, bear_color, (x + (96-64)*m, y - (140+40)*m), 12*m)  # ухо
    circle(screen, black, (x + (96-64)*m, y - (140+40)*m), 12*m, 1)  # обводка
    ellipse(screen, color, (x + 96*m - w_head/2, y - 140*m - h_head/2, w_head, h_head))  # голова
    ellipse(screen, black, (x + 96*m - w_head/2, y - 140*m - h_head/2, w_head, h_head), 1)
    circle(screen, black, (x + (96-12)*m, y - (140+14)*m), 7*m, 0)  # глаз
    circle(screen, black, (x + (96+85)*m, y - (140+6)*m), 7*m, 0)  # нос
    ellipse(screen, color, (x - w_body/2, y - w_body/2, w_body, h_body))  # туловище
    ellipse(screen, black, (x - w_body/2, y - w_body/2, w_body, h_body), 1)
    arc(screen, black, (x + 96*m - 398*m, y - (140-24)*m - 2*400*m, 2*400*m, 2*400*m),  # рот
                        3*pi/2, 3*pi/2 + pi/12.6, 1)
    ellipse(screen, (19, 42, 162), (x + 450*m - w_hole/2, y + 240*m - w_hole/2, w_hole, h_hole))
    ellipse(screen, (0, 9, 73), (x + 450*m - w_hole/3, y + 225*m - w_hole/3, w_hole*2/3, h_hole*2/3))  # прорубь
    line(screen, black, (x + 55*m, y + 80*m), (x + 460*m, y - 280*m), 4)  # палка
    line(screen, black, (x + 460*m, y - 280*m), (x + 460*m, y + 140*m), 1)  # леска
    ellipse(screen, color, (x + 142*m - w_arm/2, y + 16*m - h_arm/2, w_arm, h_arm))  # передняя лапа
    ellipse(screen, black, (x + 142*m - w_arm/2, y + 16*m - h_arm/2, w_arm, h_arm), 1)
    ellipse(screen, color, (x + 110*m - w_leg/2, y + 270*m - h_leg/2, w_leg, h_leg))  # задняя лапа (бедро)
    ellipse(screen, black, (x + 110*m - w_leg/2, y + 270*m - h_leg/2, w_leg, h_leg), 1)
    ellipse(screen, color, (x + 200*m - w_foot/2, y + 330*m - h_foot/2, w_foot, h_foot))  # задняя лапа (стопа)
    ellipse(screen, black, (x + 200*m - w_foot/2, y + 330*m - h_foot/2, w_foot, h_foot), 1)


def fish(x, y, m):
    '''
    Рисует рыбу
    x - координата рыбы по горизонтали
    y - координата рыбы по вертикали
    m - масштаб
    '''
    color_1 = (191, 203, 200)
    color_2 = (221, 166, 166)
    a = 50 * m
    b = 25 * m
    r = 5 * m
    polygon(screen, color_2, ((x + 0.6*a, y), (x + 0.6*a - 2*b, y - 2*b),
                              (x - a, y - b), (x - 8*a/10, y)))  # плавник
    polygon(screen, black, ((x + 0.6*a, y), (x + 0.6*a - 2*b, y - 2*b),
                            (x - a, y - b), (x - 8*a/10, y)), 1)
    polygon(screen, color_1, ((x - 8*a/10, y), (x - 2*a, y + b), (x - 2*a, y - b)))  # хвост
    polygon(screen, black, ((x - 8*a/10, y), (x - 2*a, y + b), (x - 2*a, y - b)), 1)
    ellipse(screen, color_1, (x - a, y - b, 2 * a, 2 * b))  # тело
    ellipse(screen, black, (x - a, y - b, 2 * a, 2 * b), 1)
    circle(screen, (121, 121, 242), (x + 0.6*a, y), r)  # глаз
    circle(screen, black, (x + 0.6*a, y), r - 2*m)  # зрачок
    circle(screen, (255, 255, 255), (x + 0.6*a - 1*m, y - 1*m), r - 3*m)  # блик


def bearandfish(x, y, m):
    '''
    Создание шаблона из медведя и 5 рыбок
    x - координата по горизонтали
    y - координата по вертикали
    m - масштаб
    '''
    fish(x + 490*m, y + 320*m, m)
    fish(x + 400*m, y + 300*m, m)
    fish(x + 490*m, y + 320*m, m)
    fish(x + 600*m, y + 260*m, m)
    fish(x + 490*m, y + 20*m, 0.6*m)
    fish(x + 350*m, y + 60*m, 0.6*m)
    bear(bear_color, x, y, m)


FPS = 30
screen_x = 794
screen_y = 1123
screen = pygame.display.set_mode((screen_x, screen_y))

horizont = 621  # линия горизонта

rect(screen, sky_color, (0, 0, screen_x, horizont))  # вторая точка указывается относительно первой!
rect(screen, snow_color, (0, horizont, screen_x, screen_y))
line(screen, black, (0, horizont), (screen_x, horizont))

sun(sun_color, 472, 193, 230, 230, 40)
bearandfish(140, horizont, 0.2)
bearandfish(85, 800, 0.8)
bearandfish(500, 650, 0.3)
bearandfish(85, 800, 0.8)

pygame.image.save(screen, "bear.png")

print('я считаю это абсолютной победой!')

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
