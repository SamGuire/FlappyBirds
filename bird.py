'''
Implementation of the Bird

'''



import pygame

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load('imgs/bird1.png')),pygame.transform.scale2x(pygame.image.load('imgs/bird2.png')),pygame.transform.scale2x(pygame.image.load('imgs/bird3.png'))]

'''
Class attributes :

    IMGS : How fast the base is moving
    MAX_ROTATION : The max angle the image of the bird can be tilted
    ROT_VEL : Rotation speed of the bird
    ANIMATION_TIME : How fast the bird flaps its wind (lower value -> faster flapping)

'''
class Bird :
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    '''
    Instance attributes :

        (Param) x : x-position of the bird
        (Param) y : y-position of the bird
        tilt : The angle of the image
        tick_count : Variable of the quadratic equation used for the parabolic movement of the bird *see move() method*
        vel : Vertical velocity of the bird (Horizontal velocity is zero)
        height  : Once the bird goes under this height, it goes into its falling animation *see move() method*
        img_count : Counter to determine which flapping animation to use
        img : Image of the bird


    '''
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    # Bird jump mechanic
    def jump(self):
        self.vel = -10.5 
        self.tick_count = 0
        self.height = self.y

    # Move bird across screen while taking into considerarion its tilt.
    def move(self):
        self.tick_count += 1

        #Parabolic movement of the bird
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16 :
            d = 16

        if d < 0 :
            d -= -2

        # increase of decrease the Y position of the bird
        self.y = self.y + d 

        # If the bird jumped
        if d < 0 or self.y < self.height + 50 :
            if self.tilt < self.MAX_ROTATION :
                self.tilt = self.MAX_ROTATION

        # If the bird is falling
        else :
                if self.tilt > -90:
                    self.tilt -= self.ROT_VEL
        

    
    def draw(self,win):
        self.img_count += 1

        # Flapping animation of the bird, resets onces it reaches to its initial flapping position (high,middle,low,middle,high)
        if self.img_count < self.ANIMATION_TIME:
            self.img= self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1 :
            self.img = self.IMGS[0]
            self.img_count = 0

        # When the bird jumps
        if self.tilt <= -80 :
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        # Image of the bird depending on its tilt (falling or jumping)
        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    # From 'https://www.pygame.org/docs/ref/mask.html' : "Useful for fast pixel perfect collision detection. A mask uses 1 bit per-pixel to store which parts collide."
    def get_mask(self):
        return pygame.mask.from_surface(self.img)