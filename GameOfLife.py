#!/usr/bin/python

import os
import time
import pygame


class Cell:
    def __init__(self, location, type):
        self.location =location
        self.type = type
        self.qtd_neighbors = 0


class Environment:
    MIN_MAGNITUDE = 4
    STATES = {'free': 0, 'live': 1}

    cell_neighbors_location = ((0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1))

    def __init__(self, size):

        self.width, self.height = size
        self.width /= self.MIN_MAGNITUDE
        self.height /= self.MIN_MAGNITUDE

        self.live_cells = []
        self.free_cells = []

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
            self.cells_state_map[s_location[0]][s_location[1]] = self.STATES['free']
            del l[0]

            return True
        else:
            return False

    def update(self):

        list_free_neighbors_cells = []
        list_live_neighbors_cells = []
        list_new_cells = []

        for cell in self.live_cells:
            start_time = time.time()
            neighbors = self.get_neighbors_location(cell.location)

            list_live_neighbors_cells = self.__checking_live_neighbors(neighbors)
            cell.qtd_neighbors = len(list_live_neighbors_cells)
            list_free_neighbors_cells += self.__checking_free_neighbors(neighbors)

        list_free_neighbors_cells = list(set(list_free_neighbors_cells))

        list_new_cells = self.__check_new_cells(list_free_neighbors_cells)
        self.free_cells = self.__kill_cells()
        self.__born_cells(list_new_cells)




    # MODEL Functions

    def __checking_live_neighbors(self,neighbors):
        live_neighbors_list =   filter(lambda x: self.cells_state_map[x[0]][x[1]] == self.STATES['live'],neighbors)
        return live_neighbors_list

    def __checking_free_neighbors(self, neighbors):
        free_neighbors_list = filter(lambda x: self.cells_state_map[x[0]][x[1]] == self.STATES['free'],
                                            neighbors)
        return  free_neighbors_list

    def __kill_cells(self):
        list_cells_to_kill = []
        for cell in self.live_cells:
            if cell.qtd_neighbors < 2 or cell.qtd_neighbors > 3:
                list_cells_to_kill.append(cell.location)
            else:
                cell.qtd_neighbors = 0

        for cell_to_kill in list_cells_to_kill:
            self.remove_cell(cell_to_kill)

        return list_cells_to_kill

    def __born_cells(self,list_new_cells):
        for cell in list_new_cells:
            self.add_cell(cell,self.STATES['live'])

    def __check_new_cells(self,list_of_cells_location):
        list_new_cells = []
        for location in list_of_cells_location:
            neighbors = self.get_neighbors_location(location)
            list_live_neighbors_cells = self.__checking_live_neighbors(neighbors)
            if len(list_live_neighbors_cells) == 3:
                list_new_cells.append(location)
        return list_new_cells


    def get_neighbors_location(self,location):
        return map(lambda x: ((location[0] - x[0]) % self.width, (location[1] - x[1]) % self.height),self.cell_neighbors_location)


    # HELPER FUNCTION
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


class Board:

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (67, 18, 174)
    YELLOW = (255, 211, 0)
    BORDER = 2
    MAGNITUDE = 6
    PORTION = MAGNITUDE / 2

    def __init__(self,resolution):

        self.width,self.height = resolution
        pygame.init()
        self.windowSurface = pygame.display.set_mode(resolution, 0, 32)
        self.drawBoard()

    def drawBoard(self):
        self.windowSurface.fill(self.WHITE)
        for x in range(self.width / (self.MAGNITUDE + self.BORDER)):
            for y  in range(self.height / (self.MAGNITUDE + self.BORDER)):
                self.drawCell((x,y),0)

    def set_title(self,title):
        pygame.display.set_caption(title)

    def update(self):
        pygame.display.update()


    def drawCell(self,position,state):

        color = (self.BLUE,self.YELLOW)[state]
        mag = self.MAGNITUDE + self.BORDER

        xo = self.MAGNITUDE
        yo = self.MAGNITUDE

        x = (position[0] * mag) + xo
        y = (position[1] * mag) + yo

        if (0 < x < self.width) and (0 < y < self.height):
            pygame.draw.polygon(self.windowSurface, color, ((x-self.PORTION, y-self.PORTION), (x+self.PORTION, y-self.PORTION), (x+self.PORTION, y+self.PORTION), (x-self.PORTION, y+self.PORTION)))

    def zoom(self,mag):

        if 2 <= (self.MAGNITUDE + mag) <= 20:
            self.MAGNITUDE += mag
            self.PORTION = self.MAGNITUDE / 2
            self.drawBoard()



class Game:

    WIDTH = 800
    HEIGHT = 600
    SLEEP = "sleep 0.1"


    def __init__(self,name):
        self.name = name
        self.generation = 0
        self.environment = Environment((self.WIDTH,self.HEIGHT))
        self.board = Board((self.WIDTH,self.HEIGHT))

        self.running = True
        self.paused = False

        self.board.set_title(self.name + " Running!")

        self.pattern = ""
        self.pattern_orientation = 1


    def pause(self):
        self.paused = (True, False)[self.paused]
        self.board.set_title(self.name + (" Running!"," Paused...")[self.paused])


    def update_cells(self):
        for free_location in self.environment.free_cells:
            self.board.drawCell(free_location, 0)

        for cell in self.environment.live_cells:
            self.board.drawCell(cell.location, 1)


    def update(self):

        if not self.paused:



            if self.generation > 0:
                self.environment.update()

            self.update_cells()
            self.board.update()

            print "Generation: ",self.generation, "Lives: ", len(self.environment.live_cells), " Deads: ", len(self.environment.free_cells)
            self.generation += 1



            #os.system(self.SLEEP)

    def __get_pos(self):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        mouseX = (mouseX - self.board.PORTION) / (self.board.MAGNITUDE + self.board.BORDER)
        mouseY = (mouseY - self.board.PORTION) / (self.board.MAGNITUDE + self.board.BORDER)

        return (mouseX,mouseY)

    def __toggle_pos(self,found,pos):
        if found:
            self.environment.remove_cell(pos)

        else:
            self.environment.add_cell(pos,1)



    def __check_cells(self):

        pos = self.__get_pos()

        if len(self.pattern) <= 0:
            found = len(self.environment.find_cell_by_location(pos))
            self.__toggle_pos(found, pos)
        else:
            self.__add_pattern(pos)

        self.update_cells()
        self.board.update()

    def __add_pattern(self,pos):

        if self.pattern == "glider":
            Patterns.glider(pos,self.pattern_orientation,self.environment)
        elif self.pattern == "lwss":
            Patterns.lwss(pos,self.pattern_orientation,self.environment)


    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.paused = True
                self.__check_cells()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause()

                elif event.key == pygame.K_LEFT:
                    if len(self.pattern) > 0:
                        self.pattern_orientation = 1
                elif event.key == pygame.K_RIGHT:
                    if len(self.pattern) > 0:
                        self.pattern_orientation = 2

                elif event.key == pygame.K_UP:
                    if len(self.pattern) > 0:
                        self.pattern_orientation = 3

                elif event.key == pygame.K_DOWN:
                    if len(self.pattern) > 0:
                        self.pattern_orientation = 4

                elif event.key == pygame.K_EQUALS:
                    self.board.zoom(2)
                elif event.key == pygame.K_MINUS:
                    self.board.zoom(-2)

                # patterns
                elif event.key == pygame.K_1:
                    self.pattern = "glider"
                elif event.key == pygame.K_2:
                    self.pattern = "lwss"
                elif event.key == pygame.K_DELETE:
                    self.pattern = ""
                    self.pattern_position = 1





class Patterns:

    @staticmethod
    def glider(position,orientation,environment):

        l = []
        x0,y0 = position
        if orientation == 1:
            l = [(x0,y0), (x0, y0 + 2),(x0 + 1, y0 + 1), (x0 + 2, y0 + 1), (x0 + 1, y0 + 2)]
        elif orientation == 2:
            l = [(x0, y0),(x0, y0 + 2),(x0 - 1, y0 + 1), (x0 - 2, y0 + 1),  (x0 - 1, y0 + 2)]
        elif orientation == 3:
            l = [(x0, y0), (x0, y0 - 2), (x0 + 1, y0 - 1), (x0 + 2, y0 - 1), (x0 + 1, y0 - 2)]
        elif orientation == 4:
            l = [(x0, y0), (x0, y0 - 2), (x0 - 1, y0 - 1), (x0 - 2, y0 - 1), (x0 - 1, y0 - 2)]

        for position in l:
            l_found = environment.find_cell_by_location(position)
            if len(l_found) <= 0:
                environment.add_cell(position,1)

    @staticmethod
    def lwss(position,orientation,environment):

        l = []
        x0,y0 = position
        if orientation == 1:
            l = [(x0,y0 + 1), (x0 + 1, y0 + 2),(x0 + 1, y0 + 1), (x0 + 1, y0), (x0 + 2, y0), (x0 + 3, y0 + 1), (x0 + 4, y0 + 1)
                , (x0 + 2, y0 + 2), (x0 + 3, y0 + 2), (x0 + 4, y0 + 2), (x0 + 3, y0 + 3), (x0 + 2, y0 + 3)]
        elif orientation == 2:
            l = [(x0,y0 + 1), (x0 + 1, y0 + 2),(x0 + 1, y0 + 1), (x0 + 1, y0), (x0 + 2, y0), (x0 + 3, y0 + 1), (x0 + 4, y0 + 1)
                , (x0 + 2, y0 + 2), (x0 + 3, y0 + 2), (x0 + 4, y0 + 2), (x0 + 3, y0 + 3), (x0 + 2, y0 + 3)]
        elif orientation == 3:
            l = [(x0,y0 + 1), (x0 + 1, y0 + 2),(x0 + 1, y0 + 1), (x0 + 1, y0), (x0 + 2, y0), (x0 + 3, y0 + 1), (x0 + 4, y0 + 1)
                , (x0 + 2, y0 + 2), (x0 + 3, y0 + 2), (x0 + 4, y0 + 2), (x0 + 3, y0 + 3), (x0 + 2, y0 + 3)]
        elif orientation == 4:
            l = [(x0,y0 + 1), (x0 + 1, y0 + 2),(x0 + 1, y0 + 1), (x0 + 1, y0), (x0 + 2, y0), (x0 + 3, y0 + 1), (x0 + 4, y0 + 1)
                , (x0 + 2, y0 + 2), (x0 + 3, y0 + 2), (x0 + 4, y0 + 2), (x0 + 3, y0 + 3), (x0 + 2, y0 + 3)]

        for position in l:
            l_found = environment.find_cell_by_location(position)
            if len(l_found) <= 0:
                environment.add_cell(position,1)


def fill_environment(environment):

    for x in range(0,100):
        for y in range(0,100):
            environment.add_cell((x, y),1)

