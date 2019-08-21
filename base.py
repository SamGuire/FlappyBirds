'''
Implementation of the Base (Floor of the window).

'''


import pygame


BASE_IMGS = pygame.transform.scale2x(pygame.image.load('imgs/base.png'))

'''
Class attributes :

    VEL : How fast the base is moving
    WIDTH : The width of the base
    IMG : The image of the Base

'''
class Base :
    VEL = 5
    WIDTH = BASE_IMGS.get_width()
    IMG = BASE_IMGS

    '''
    Instance attributes :

    (Param) y : y-position of the base
    x1 : left side of the base
    x2 : right side of the base

    '''
    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # Resets the position of the Base image once its off screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
    
        if self.x2 + self.WIDTH < 0 :
            self.x2 = self.x1 + self.WIDTH

    # Draw the base in the screen
    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))

