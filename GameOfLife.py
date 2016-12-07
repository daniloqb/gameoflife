#!/usr/bin/python

'''

This is the default version of Jhon Conways' Game of Life.
I try to use python objects because the next level of this game will introduce other rules and object types.
The code could be more simple.

'''

import pygame
import random


class Cell:

    cell_neighbors_location = ((0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1))
    #cell_neighbors_location = ((0, -1), (0, 1), (1, 0), (-1, 0))
    #cell_neighbors_location = ((1, -1), (1, 1), (-1, -1), (-1, 1))
    def __init__(self,type,):
        self.type = type

    def get_neighbors_location(self,location, limits):
            return map(lambda x: ((location[0] - x[0]) % limits[0], (location[1] - x[1]) % limits[1]),
                       self.cell_neighbors_location)


class Environment:
    MIN_MAGNITUDE = 8
    STATES = {'free': 0, 'live': 1}



    def __init__(self, size):

        self.width, self.height = size
        self.width /= self.MIN_MAGNITUDE
        self.height /= self.MIN_MAGNITUDE

        self.cells_map =  [[Cell(0) for y in xrange(self.height)] for x in xrange(self.width)]
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
            self.cells_map[location[0]][location[1]] = Cell(0)
            self.screen_map[location[0]][location[1]] = 0

            del cell

            return True
        else:
            return False

    def check(self):
        for x,row in enumerate(self.cells_map):
            for y,cell in enumerate(row):
                neighbors = cell.get_neighbors_location((x,y),(self.width,self.height))
                qtd_neighbors = len(self.__checking_live_neighbors(neighbors,1))
                if cell.type == 0 and qtd_neighbors ==3:
                    self.screen_map[x][y] = 1
                elif cell.type == 1:
                    if qtd_neighbors < 2 or qtd_neighbors > 3:
                        self.screen_map[x][y] = 0
                    else:
                        self.screen_map[x][y] = 1

    '''
    def update(self):
        for x, row in enumerate(self.screen_map):
            for y, item in enumerate(row):
                cell = self.cells_map[x][y]
                if  cell.type != item:
                    del cell
                    self.cells_map[x][y] = Cell(item)
    '''
    def update(self):
        for x in xrange(len(self.screen_map)):
            for y in xrange(len(self.screen_map[0])):
                if self.cells_map[x][y].type != self.screen_map[x][y]:
                    self.cells_map[x][y] = Cell(self.screen_map[x][y])

    def __checking_live_neighbors(self, neighbors, type):
        return  filter(lambda x: self.cells_map[x[0]][x[1]].type == type,neighbors)

           # HELPER FUNCTION
    def __sanitize_location(self, location):
        return location[0] % self.width, location[1] % self.height



    # DEBUG FUNCTIONS
    def show_live_cells_location(self):
        for row in self.cells_map:
            for cell in row:
                print cell.type,
            print



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
        self.draw_empty_cells()
        pygame.display.update()

    def draw_empty_cells(self):
        for x in xrange(self.width):
            for y  in xrange(self.height):
                self.drawCell((x,y),0)

    def set_title(self,title):
        pygame.display.set_caption(title)


    def update_screen(self,screen_map):
        x_range = len(screen_map)
        y_range = len(screen_map[0])


        for x in xrange(x_range):
            for y in range(y_range):
                self.drawCell((x,y),screen_map[x][y].type)


        pygame.display.update()

    def drawCell(self,position,state):

        color = (self.BLUE,self.YELLOW, self.GREEN, self.BLACK, self.RED)[state]

        x = (position[0] * self.SCALE) + self.MAGNITUDE
        y = (position[1] * self.SCALE) + self.MAGNITUDE

        if (0 < x < self.width) and (0 < y < self.height):
            pygame.draw.polygon(self.windowSurface, color, ((x-self.PORTION, y-self.PORTION), (x+self.PORTION, y-self.PORTION), (x+self.PORTION, y+self.PORTION), (x-self.PORTION, y+self.PORTION)))

    def zoom(self,mag):

        if 2 <= (self.MAGNITUDE + mag) <= 20:
            self.MAGNITUDE += mag
            self.PORTION = self.MAGNITUDE / 2
            self.SCALE = self.MAGNITUDE + self.BORDER
            self.drawBoard()


class Game:

    def __init__(self,name,resolution):
        self.WIDTH, self.HEIGHT = resolution

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


    def update(self):

        if not self.paused:


            self.environment.check()

            self.board.update_screen(self.environment.cells_map)
            self.environment.update()

            print "Generation: ",self.generation
            self.generation +=1


            #os.system(self.SLEEP)

    def __get_pos(self):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        mouseX = (mouseX - self.board.PORTION) / (self.board.MAGNITUDE + self.board.BORDER)
        mouseY = (mouseY - self.board.PORTION) / (self.board.MAGNITUDE + self.board.BORDER)

        return (mouseX,mouseY)

    def __toggle_pos(self,cell,pos):
        if cell.type != 0:
            self.environment.remove_cell(pos)

        else:
            self.environment.add_cell(pos,1)



    def __check_cells(self):

        pos = self.__get_pos()

        if len(self.pattern) <= 0:
            cell = self.environment.cells_map[pos[0]][pos[1]]
            self.__toggle_pos(cell,pos)
        else:
            self.__add_pattern(pos)

        self.board.update_screen(self.environment.cells_map)

    def __add_pattern(self,pos):

        if self.pattern == "glider":
            Patterns.glider(pos,1,self.pattern_orientation,self.environment)
        elif self.pattern == "lwss":
            Patterns.lwss(pos,1,self.pattern_orientation,self.environment)


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
            environment.add_cell(position,type)

    @staticmethod
    def lwss(position,type,orientation,environment):

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
            environment.add_cell(position,type)


def fill_environment(environment):

    for x in range(170):
        for y in range(110):
            environment.add_cell((x, y),1)

