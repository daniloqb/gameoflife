import GameOfLife as gof

if __name__ == "__main__":

    DEBUG = True

    # Step 1: Creating environment

    env = gof.Environment((20, 20))

    if DEBUG:
        env.show_live_cells_location()
        env.show_cell_state_map()

    # Step 2: Add new Cells

    for x in range(2):
        env.add_cell((x, x), 1)

    env.add_cell((0, 0), 1)

    env.add_cell((-1, -1), 1)
    env.add_cell((1, 12), 1)
    env.add_cell((2, 2), 1)

    if DEBUG:
        env.show_live_cells_location()
        env.show_cell_state_map()

    # Find a cell out of bounds. Should be false
    print env.find_cell_by_location((15, 15))

    # Find a cell that should exist
    print env.find_cell_by_location((4,4))

    # remove a cell that dont exist
    # env.remove_cell((15,15))

    # if DEBUG:
    #    env.show_live_cells_location()
    #    print env.cells_state_map



    if DEBUG:
        env.show_live_cells_location()
        env.show_cell_state_map()

    # Testing neighbors list
    # print env.get_neighbors_location((0,0))
    # print env.get_neighbors_location((1,1))

    env.update()

    if DEBUG:
        env.show_live_cells_location()
        env.show_cell_state_map()


    # remove a cell that exist
    env.remove_cell((4, 4))

    if DEBUG:
        env.show_live_cells_location()
        env.show_cell_state_map()
