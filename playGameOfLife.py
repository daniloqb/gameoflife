#!/usr/bin/python
import GameOfLife as gof

import random


if __name__ == "__main__":


    game = gof.Game("Game of Life",(1024,768))

    gof.fill_environment(game.environment)


    #for g in range(0,10000,5):
       #gof.Patterns.glider((random.randint(0,g),g),1,random.randint(1,4),game.environment)

    #gof.Patterns.glider((60,60),1, 4, game.environment)
    #gof.Patterns.glider((10,10),2, 1, game.environment)



    while game.running:

        game.event()
        game.update()