import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

rect(screen, (255, 255, 255), (0, 0, 400, 400))
circle(screen, (255, 220, 0), (200, 200), 100, 0)
circle(screen, (255, 0, 0), (165, 170), 18, 0)
circle(screen, (255, 0, 0), (235, 170), 15, 0)
circle(screen, (0, 0, 0), (165, 170), 7, 0)
circle(screen, (0, 0, 0), (235, 170), 6, 0)
#line(screen, (0, 0, 0), (120, 120), (190, 170), 10)
polygon(screen, (0, 0, 0), [(120, 120),(130, 120),(185, 165),(180, 170)])
polygon(screen, (0, 0, 0), [(280, 120),(270, 120),(215, 165),(220, 170)])

x1 = 150; y1 = 240
x2 = 250; y2 = 260
rect(screen, (0, 0, 0), (150, 240, 100, 20))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()