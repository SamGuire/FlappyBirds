'''
Flappy Birds game. You can either play the game yourself or watch how an AI learns to play the game using the NEAT
(Neuroevolution of augmenting topologies) algorithm.

'''



import pygame
import neat
import time
import os
import random
from base import *
from bird import *
from pipe import *
from gameComponents import *
from play import *

def draw_window(win,birds,pipes,base,score):

    win.blit(BACKGRND_IMGS,(0,0))
    for pipe in pipes :
        pipe.draw(win)

    text = STAT_FONT.render("Score: "+str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH-10-text.get_width(),10))
    base.draw(win)
    for bird in birds :
        bird.draw(win)
    pygame.display.update()




def genome_evaluation(genomes,config):

    # Each position corresponds to a specific bird. Ex : nets[0] = neural network of the first bird
    #                                                    ge[0] = genome of the first bird       
    #                                                    birds[0] = first bird


    nets = []
    ge = []
    birds = []

    for genome_id,genome in genomes: 
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    base = Base(730)
    pipes = [Pipe(700)]

    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))


    clock = pygame.time.Clock()
    score = 0

    run = True

    while run and len(birds) > 0:

        clock.tick(30)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            
            # If the users quits the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(birds) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

     

        for x,bird in enumerate(birds):
            
            # Increase fitness level for every pixel the bird moves foward
            ge[x].fitness += 0.1
            bird.move()

            # Determines if the bird should jump or not
            output = nets[x].activate((bird.y,abs(bird.y - pipes[pipe_ind].height),abs(bird.y-pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        
        base.move()
        
        rem = []
        add_pipe = False

        for pipe in pipes:
            pipe.move()
            for x,bird in enumerate(birds) :

                # Remove the birds that collide with pipes
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                        
                # If bird passed the pipes
                if not pipe.passed and pipe.x < bird.x :
                    pipe.passed = True
                    add_pipe = True

            # If pipe is offscreen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        # Increase score and genome fitness of each bird that passed the pipes
        if add_pipe:
            score+=1
            for genome in ge :
                genome.fitness += 5
            pipes.append(Pipe(700))

        # Remove all pipes that are offscreen   
        for removed in rem :
            pipes.remove(removed)

        # Remove the birds that hit the base 
        for x,bird in enumerate(birds) :
            if bird.y + bird.img.get_height() >= 750:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
            
    
        draw_window(win,birds,pipes,base,score)



    
def run(config_path):

    print("Do you want to play FlappyBirds (0) or watch an AI (1) ? ",end='')
    answer = input()
    print(answer)

    while (answer.strip() != "0" and answer != "1") :

        print("Please select a 0 (play) or 1 (watch): ", end = '')
        answer = input()

    if answer.strip() == "1" :

        config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner  = p.run(genome_evaluation,50)
    
    else :

        play()


# Inititalize the NEAT configuation file and run the program
if __name__== "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"neatConf.txt")
    run(config_path)
