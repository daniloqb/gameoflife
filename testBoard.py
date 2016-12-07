#!/usr/bin/python
import GameOfLife as gof

import random
import time

if __name__ == "__main__":

   start_time = time.time()
   resolution = (800,600)

   board = gof.Board(resolution)
   env = gof.Environment(resolution)


   for x in range(200):
      for y in range(150):
         env.add_cell((x,y),1)
   board.update_screen(env.screen_map)

   for x in range(40):
      for y in range(40):
         env.remove_cell((x, y))
   board.update_screen(env.screen_map)

   for x in range(40):
      for y in range(40):
         env.add_cell((x,y),2)
   board.update_screen(env.screen_map)


   print time.time() - start_time
