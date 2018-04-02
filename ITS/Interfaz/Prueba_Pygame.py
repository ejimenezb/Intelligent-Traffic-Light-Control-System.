import pygame
from pygame.locals import *

pygame.init()

pantalla = pygame.display.set_mode((1200, 600))

imagen = pygame.image.load("Luz_roja_b.jpg")

imagen = pygame.transform.scale(imagen, (50, 50))
while True:
    for eventos in pygame.event.get():
        if eventos.type == pygame.QUIT:
            exit()
    pantalla.blit(imagen, (100, 20))

    #if

    pygame.display.update()


#pygame.transform.scale(Surface, (width, height), DestSurface = None)