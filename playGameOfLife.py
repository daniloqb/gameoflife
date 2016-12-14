#!/usr/bin/python
import GameOfLife as gol
from ConwayPatterns import *
import random


if __name__ == "__main__":


    game = gol.Game("Game of Life", (1024, 768))

    ConwayPatterns.fill_environment(game.environment)


    #for g in range(0,1000,5):
      #Patterns.glider((random.randint(0,g),g),random.randint(1,4),random.randint(1,4),game.environment)

    #Patterns.glider((10,10),1, 4, game.environment)
    #Patterns.glider((10,10),2, 1, game.environment)

    #ConwayPatterns.beacon((20, 20), 1, 2, game.environment)

    while game.running:

        game.event()
        game.update()