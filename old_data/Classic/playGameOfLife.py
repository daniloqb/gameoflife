#!/usr/bin/python
import GameOfLifeClassic as gol

import random


if __name__ == "__main__":


    game = gol.Game("Game of Life", (1024, 768))

    gol.fill_environment(game.environment)


    #for g in range(0,1000,5):
    #  gol.Patterns.glider((random.randint(0,g),g),random.randint(1,4),random.randint(1,4),game.environment)

    #gol.Patterns.glider((10,10),1, 4, game.environment)
    #gol.Patterns.glider((10,10),2, 1, game.environment)



    while game.running:

        game.event()
        game.update()