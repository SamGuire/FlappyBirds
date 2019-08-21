'''

Python script if you want to play the game yourself.

'''

import pygame
from base import *
from bird import *
from pipe import *
from gameComponents import *

def draw_window(win,bird,pipes,base,score):
    win.blit(BACKGRND_IMGS,(0,0))
    for pipe in pipes :
        pipe.draw(win)

    text = STAT_FONT.render("Score: "+str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH-10-text.get_width(),10))
    base.draw(win)

    bird.draw(win)
    pygame.display.update() 



def play():

    birdIsDead = False
    base = Base(730)
    pipes = [Pipe(700)]
    bird = Bird(230,350)

    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))


    clock = pygame.time.Clock()
    score = 0

    run = True

    while run :

        clock.tick(30)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        if birdIsDead:

            bird.move()
            if bird.y + bird.img.get_height() >= 750:
                run = False
                pygame.quit()
                quit()
                break

        else :

            base.move()
        
            rem = []
            add_pipe = False

            for pipe in pipes:
                pipe.move()

                if pipe.collide(bird):
                    isDead = True
                    bird.tilt = -90
                    
                # If bird passes the pipes
                if not pipe.passed and pipe.x < bird.x :
                    pipe.passed = True
                    add_pipe = True

                # If the pipe is offscreen
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)
            


            if keys[pygame.K_SPACE]:
                bird.jump()
                
            bird.move()


            # Increase score for every pipe passed
            if add_pipe:
                score+=1
                pipes.append(Pipe(700))
            
            # Remove all pipes that are offscreen
            for removed in rem :
                pipes.remove(removed)

            # If bird hits the base
            if bird.y + bird.img.get_height() >= 750:
                run = False
                pygame.quit()
                quit()
                break
                
        
        draw_window(win,bird,pipes,base,score)