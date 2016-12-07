#!/usr/bin/python
import GameOfLife as gof

import random
import time

if __name__ == "__main__":


   board = gof.Board((800,600))

   start_time =time.time()
   board.drawBoard()

   print time.time() - start_time