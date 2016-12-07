#!/usr/bin/python
import GameOfLife as gof

import random


if __name__ == "__main__":

    DEBUG = True

    # Step 1: Creating environment

   # env = gof.Environment((800, 600))

    #if DEBUG:
    #    env.show_live_cells_location()
    #    env.show_cell_state_map()

    # Step 2: Add new Cells

    #for x in range(2):
    #    env.add_cell((x, x), 1)

    #env.add_cell((0, 0), 1)

    #env.add_cell((1, 4), 1)
    #env.add_cell((2, 2), 1)

    #for x in range(20):
    #    for y in range(20):
    #        env.add_cell((x,y),1)
    #        print x,y
    #if DEBUG:
    #    env.show_live_cells_location()
    #    env.show_cell_state_map()

    #print

    # Find a cell out of bounds. Should be false
    #print env.find_cell_by_location((15, 15))

    # Find a cell that should exist
    #print env.find_cell_by_location((4,4))

    # remove a cell that dont exist
    # env.remove_cell((15,15))

    #if DEBUG:
    #    env.show_live_cells_location()
    #    env.show_cell_state_map



    #if DEBUG:
    #    env.show_live_cells_location()
    #    env.show_cell_state_map()

    # Testing neighbors list
    # print env.get_neighbors_location((0,0))
    # print env.get_neighbors_location((1,1))

    #if DEBUG:
    #    env.show_live_cells_location()
    #    env.show_cell_state_map()


    #for i in range(4):
    #    env.update()

    #    if DEBUG:
    #        env.show_live_cells_location()
    #        env.show_cell_state_map()



    #for cell in env.live_cells:
    #    print "{} {}".format(cell.location,cell.qtd_neighbors)
    # remove a cell that exist
    #env.remove_cell((4, 4))

    #if DEBUG:
    #    env.show_live_cells_location()
    #    env.show_cell_state_map()


if __name__ == "__main__":


    game = gof.Game("Game of Life")

    #gof.fill_environment(game.environment)


    for g in range(0,100,5):
       gof.Patterns.glider((random.randint(0,g),g),random.randint(1,2),random.randint(1,4),game.environment)

    #gof.Patterns.glider((60,60),1, 4, game.environment)
    #gof.Patterns.glider((10,10),2, 1, game.environment)



    while game.running:

        game.event()
        game.update()