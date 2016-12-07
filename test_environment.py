#!/usr/bin/python
import GameOfLife as gof

import random
import time

if __name__ == "__main__":


    env = gof.Environment((800,600))

    gof.Patterns.glider((10,10),1,env)


    env.show_live_cells_location()

    for cell in env.live_cells:
        env.update(cell)