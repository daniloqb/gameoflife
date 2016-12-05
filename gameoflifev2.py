#!/usr/bin/python

import os
import random
import pygame


class Organism:
    def __init__(self,x,y,state):
        self.position =(x,y)
        self.state = state
        self.qtd_neighbors = 0
        self.neighbors = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]

class Environment:
    MIN_MAGNITUDE = 4

    def __init__(self, size):

        self.width,self.height = size
        self.width /= self.MIN_MAGNITUDE
        self.height /= self.MIN_MAGNITUDE

        print self.width, self.height
        self.organisms = []
        self.deads_position = []
        self.state_map = [[0 for x in xrange(self.width)] for y in xrange(self.height)]

    def is_empty(self):
        return  not (len(self.organisms))

    def add_organism(self,position):
        x = self.width / self.MIN_MAGNITUDE
        y = self.height / self.MIN_MAGNITUDE

        if 0 <= position[0] <= x:
            if  0 <= position[1] <= y:
                print position
                org = Organism(position[0],position[1],1)
                self.organisms.append(org)

    def remove_organism(self,position):
        l = self.find_organism_by_pos(position)
        if len(l) > 0:
            self.deads_position.append(position)
            self.organisms.remove(l[0])

            return True
        else:
            return False


    def find_organism_by_pos(self,position):
        l = filter(lambda x: x.position == position,self.organisms)
        return l

    def update(self):

        l_neighbors_position = self.__checking_neighbors(self.organisms)

        list_of_deads = self.__checking_deads(l_neighbors_position, self.organisms)

        self.deads_position = self.__killing_organisms(self.organisms)

        self.__checking_new_borns(list_of_deads, self.organisms)

        self.__reinitialize_organisms(self.organisms)

    def show(self):
        for organism in self.organisms:
            print organism.position,":", organism.qtd_neighbors,
        print


    # private methods


    def __checking_neighbors(self, organisms):
        l_neighbors_position = []

        for organism in organisms:
            for neighbor_position in organism.neighbors:
                if (neighbor_position[0] > 0) and (neighbor_position[1] > 0):

                    found = False
                    list_neig = filter(lambda x:x.position == neighbor_position,organisms)
                    if len(list_neig) > 0:
                        found = True
                        organism.qtd_neighbors += 1


                    if found == False:
                        if neighbor_position not in l_neighbors_position:
                            l_neighbors_position.append(neighbor_position)


        return l_neighbors_position

    def __checking_deads(self,l,organisms):
        deads = []

        for dead in l:
            deads.append(Organism(dead[0], dead[1], 1))

        for dead_organism in deads:
            for neighbor in organisms:
                if neighbor.position in dead_organism.neighbors:
                    dead_organism.qtd_neighbors += 1

        return deads


    def __killing_organisms(self,organisms):
        organism_to_kill = []
        l_deads_position = []
        for organism in organisms:
            if organism.qtd_neighbors < 2 or organism.qtd_neighbors > 3:
                organism_to_kill.append(organism)


        for organism in organism_to_kill:
            l_deads_position.append(organism.position)
            organisms.remove(organism)

        return l_deads_position

    def __checking_new_borns(self,l,organisms):
        for organism in l:
            if organism.qtd_neighbors == 3:
                organisms.append(organism)


    def __reinitialize_organisms(self,organisms):
        for organism in organisms:
            organism.qtd_neighbors = 0




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
        for dead_position in self.environment.deads_position:
            self.board.drawCell(dead_position, 0)

        for organism in self.environment.organisms:
            self.board.drawCell(organism.position, 1)


    def update(self):

        if not self.paused:



            if self.generation > 0:
                self.environment.update()

            self.update_cells()
            self.board.update()

            print "Generation: ",self.generation, "Lives: ", len(self.environment.organisms), " Deads: ", len(self.environment.deads_position)
            self.generation += 1



            os.system(self.SLEEP)

    def __get_pos(self):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        mouseX = (mouseX - self.board.PORTION) / (self.board.MAGNITUDE + self.board.BORDER)
        mouseY = (mouseY - self.board.PORTION) / (self.board.MAGNITUDE + self.board.BORDER)
        print (mouseX,mouseY)
        return (mouseX,mouseY)

    def __toggle_pos(self,found,pos):
        if found:
            self.environment.remove_organism(pos)

        else:
            self.environment.add_organism(pos)



    def __check_organisms(self):

        pos = self.__get_pos()

        if len(self.pattern) <= 0:
            found = len(self.environment.find_organism_by_pos(pos))
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
                self.__check_organisms()

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
            l_found = environment.find_organism_by_pos(position)
            if len(l_found) <= 0:
                environment.add_organism(position)

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
            l_found = environment.find_organism_by_pos(position)
            if len(l_found) <= 0:
                environment.add_organism(position)


def fill_environment(environment):

    for x in range(0,50):
        for y in range(0,50):
            environment.add_organism((x, y))



if __name__ == "__main__":


    game = Game("Game of Life")

    #fill_environment(game.environment)


    #for g in range(20,100,5):
     #   Patterns.glider((g,20),random.randint(1,4),game.environment)

    #Patterns.glider((10,10), 1, game.environment)



    while game.running:

        game.event()
        game.update()

































