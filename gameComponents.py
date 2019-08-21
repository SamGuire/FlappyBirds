'''
Components of the game window

'''

import pygame



pygame.font.init()
pygame.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
BACKGRND_IMGS = pygame.transform.scale2x(pygame.image.load('imgs/bg.png'))

STAT_FONT = pygame.font.SysFont("comicsans",50)
