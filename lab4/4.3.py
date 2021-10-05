# на самом деле, это 4.1, но я не сохранил смайлик в первый раз и нумерация поехала
import pygame
import numpy as np
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

rect(screen, (255, 255, 255), (0, 0, 400, 400))
circle(screen, (255, 255, 0), (200, 200), 100)  # лицо
circle(screen, (0, 0, 0), (200, 200), 100, 1)  # обводка
circle(screen, (255, 0, 0), (200 - 40, 200 - 40), 13)  # глаз левый
circle(screen, (255, 0, 0), (200 + 40, 200 - 40), 15)  # глаз правый
circle(screen, (0, 0, 0), (200 - 40, 200 - 40), 5)  # зрачок левый
circle(screen, (0, 0, 0), (200 + 40, 200 - 40), 10)  # зрачок правый
line(screen, (0, 0, 0), (125, 120), (180, 165), 10)
line(screen, (0, 0, 0), (275, 120), (220, 165), 15)
rect(screen, (0, 0, 0), (150, 235, 100, 25))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while finished is False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
