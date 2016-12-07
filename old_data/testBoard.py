#!/usr/bin/python
import GameOfLife as gof

import random
import time

if __name__ == "__main__":

   start_time = time.time()
   resolution = (100,100)

   board = gof.Board(resolution)
   env = gof.Environment(resolution)


   #for x in range(3):
    #  for y in range(3):
     #    env.add_cell((x,y),1)

   gof.Patterns.glider((3,3),1,1,env)

   board.update_screen(env.cells_map)
   env.check()
   #print env.show_live_cells_location()
   print time.time() - start_time

   env.update()

   board.update_screen(env.cells_map)