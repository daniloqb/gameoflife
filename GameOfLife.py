#!/usr/bin/python

import os
import time
import pygame


class Cell:
    def __init__(self,type):
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

        self.cells_map =  [[0 for y in xrange(self.height)] for x in xrange(self.width)]
        self.screen_map =  [[0 for y in xrange(self.height)] for x in xrange(self.width)]



    def is_empty(self):
        pass

    def find_cell_by_location(self, location):
        pass

    def add_cell(self, location, type):

        s_location = self.__sanitize_location(location)
        if s_location[0] < self.width and s_location[1] < self.height:
            self.cells_map[s_location[0]][s_location[1]] = (Cell(type))
            self.screen_map[s_location[0]][s_location[1]] = type

    def remove_cell(self, location):

        cell = self.cells_map[location[0]][location[1]]
        if cell:
            self.cells_map[location[0]][location[1]] = 0
            self.screen_map[location[0]][location[1]] = self.STATES['free']
            del cell

            return True
        else:
            return False

    def update(self,cell):
        pass


    def get_neighbors_location(self,location):
        return map(lambda x: ((location[0] - x[0]) % self.width, (location[1] - x[1]) % self.height),self.cell_neighbors_location)



    # HELPER FUNCTION
    def __sanitize_location(self, location):
        return location[0] % self.width, location[1] % self.height



    # DEBUG FUNCTIONS
    def show_live_cells_location(self):
        for row in self.cells_map:
            for cell in row:
                print cell.type,
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
    SCALE = MAGNITUDE + BORDER

    def __init__(self,resolution):

        self.width,self.height = resolution
        pygame.init()
        self.windowSurface = pygame.display.set_mode(resolution, 0, 32)

        self.drawBoard()

    def drawBoard(self):
        self.windowSurface.fill(self.WHITE)
        self.update()

    def draw_empty_cells(self):
        for x in xrange(self.width):
            for y  in xrange(self.height):
                self.drawCell((x,y),0)

    def set_title(self,title):
        pygame.display.set_caption(title)

    def update(self):
        self.draw_empty_cells()
        pygame.display.update()

    def update_screen(self,screen_map):
        x_range = len(screen_map)
        y_range = len(screen_map[0])

        for x in xrange(x_range):
            for y in range(y_range):
                self.drawCell((x,y),screen_map[x][y])
        pygame.display.update()

    def drawCell(self,position,state):

        color = (self.BLUE,self.YELLOW, self.GREEN)[state]

        x = (position[0] * self.SCALE) + self.MAGNITUDE
        y = (position[1] * self.SCALE) + self.MAGNITUDE

        if (0 < x < self.width) and (0 < y < self.height):
            pygame.draw.polygon(self.windowSurface, color, ((x-self.PORTION, y-self.PORTION), (x+self.PORTION, y-self.PORTION), (x+self.PORTION, y+self.PORTION), (x-self.PORTION, y+self.PORTION)))

    def zoom(self,mag):

        if 2 <= (self.MAGNITUDE + mag) <= 20:
            self.MAGNITUDE += mag
            self.PORTION = self.MAGNITUDE / 2
            self.drawBoard()
            self.SCALE = self.MAGNITUDE + self.BORDER



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
            self.board.drawCell(cell, 1)


    def update(self):

        if not self.paused:

            if self.generation > 0:

                p_born = 0;
                p_dead = 0;
                for cell in self.environment.live_cells:
                    #print 'cell:', cell.location
                    self.environment.update(cell)

                    for b in range(p_born, len(self.environment.cells_to_born)):
                        self.board.drawCell(self.environment.cells_to_born[b][0], self.environment.cells_to_born[b][1] )

                        p_born += 1

                    for d in range(p_dead, len(self.environment.cells_to_dead)):
                        self.board.drawCell(self.environment.cells_to_dead[d], 0)

                        p_dead += 1


            else:
                for cell in self.environment.live_cells:
                    self.board.drawCell(cell.location, cell.type)
                self.board.update()

            self.board.update()


            #print "Generation: ",self.generation, "Lives: ", len(self.environment.live_cells), " Deads: ", len(self.environment.cells_to_dead)
            self.generation += 1

            self.environment.kill_cells()
            self.environment.born_cells()

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
            Patterns.glider(pos,1,self.pattern_orientation,self.environment)
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
    def glider(position,type,orientation,environment):

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
                environment.add_cell(position,type)

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

    for x in range(15,60):
        for y in range(15,60):
            environment.add_cell((x, y),1)

