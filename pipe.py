'''.
Implementation of the pipes


'''




import pygame
import random 

PIPE_IMG = pygame.transform.scale2x(pygame.image.load('imgs/pipe.png'))

'''
Class attributes :

    GAP : Gap between top and bottom pipe
    VEL : How fast the pipes move across the screen

'''

class Pipe :

    GAP = 200
    VEL = 5

    

    '''
    Instance attributes :

        (Param) x : How fast the base is moving
        height : The width of the base
        top : y-position of the top-pipe
        bottom : y-position of the bottom-pipe
        PIPE_TOP : Image of the top pipe (flipped version of the original image)
        PIPE_BOTTOM = Image of the bottom pipe
        passed : If the bird passed the pipes or not

    '''
    def __init__(self,x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    #Set the height of both bottom and top pipe with a gap of 200 between both surfaces
    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    #move pipe across screen
    def move(self):
        self.x -= self.VEL

    #draw the pipe in the screen
    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))
    
    #Pixel perfect collision using masks
    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x-bird.x,self.top-round(bird.y))
        bottom_offset = (self.x-bird.x,self.bottom-round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask,bottom_offset)

        top_point = bird_mask.overlap(top_mask,top_offset)

        if top_point or bottom_point :
            return True
        
        return False