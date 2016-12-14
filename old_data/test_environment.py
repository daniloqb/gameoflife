#!/usr/bin/python
import GameOfLife as gof

import random
import time

if __name__ == "__main__":


    env = gof.Environment((800,600))

    gof.ConwayPatterns.glider((10, 10), 1, 1, env)

    gof.ConwayPatterns.glider((30, 30), 2, 1, env)

    print "cells:",
    env.show_live_cells_location()

    p_born = 0;
    p_dead = 0;
    for cell in env.live_cells:
        env.update(cell)
        for b in range(p_born,len(env.cells_to_born)):
            print b,env.cells_to_born[b][0]
            p_born +=1




    env.kill_cells()
    env.born_cells()

    print "cells:",
    env.show_live_cells_location()


