class Cell:
    def __init__(self, location, state):
        self.location =location
        self.state = state
        self.qtd_neighbors = 0


class Environment:
    MIN_MAGNITUDE = 4
    STATES = {'dead': 0, 'live': 1}

    cell_neighbors_location = ((0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1))

    def __init__(self, size):

        self.width, self.height = size
        self.width /= self.MIN_MAGNITUDE
        self.height /= self.MIN_MAGNITUDE

        self.live_cells = []
        self.dead_cells = []

        self.cells_state_map = [[0 for y in xrange(self.height)] for x in xrange(self.width)]


    def is_empty(self):
        return not (len(self.live_cells))

    def find_cell_by_location(self, location):
        l = filter(lambda x: x.location == location, self.live_cells)
        return l

    def add_cell(self, location, state):

        s_location = self.__sanitize_location(location)
        if s_location[0] < self.width and s_location[1] < self.height:
            if not (self.find_cell_by_location(s_location)):
                self.live_cells.append(Cell(s_location,state))
                self.cells_state_map[s_location[0]][s_location[1]] = self.STATES['live']

    def remove_cell(self,location):

        s_location = self.__sanitize_location(location)
        l = self.find_cell_by_location(s_location)
        if l:
            self.live_cells.remove(l[0])
            self.cells_state_map[s_location[0]][s_location[1]] = self.STATES['dead']
            del l[0]

            return True
        else:
            return False



    def update(self):

        self.__checking_neighbors()

    # HELPER FUNCTION

    def __checking_neighbors(self):

        for cell in self.live_cells:
            neighbors = self.get_neighbors_location(cell.location)
            cell.qtd_neighbors = reduce(lambda x,y: x + y,map(lambda x: self.cells_state_map[x[0]][x[1]] == self.STATES['live'],neighbors))


    def get_neighbors_location(self,location):
        return map(lambda x: ((location[0] - x[0]) % self.width, (location[1] - x[1]) % self.height),self.cell_neighbors_location)

    def __sanitize_location(self, location):
        return location[0] % self.width, location[1] % self.height



    # DEBUG FUNCTIONS
    def show_live_cells_location(self):
        for cell in self.live_cells:
            print '({} {})'.format(cell.location,cell.qtd_neighbors),
        print

    def show_cell_state_map(self):
        for l in range(len(self.cells_state_map)):
            print self.cells_state_map[l]
