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
    def __init__(self):
        self.organisms = []
        self.deads_position = []

    def is_empty(self):
        return  not (len(self.organisms))

    def add_organism(self,position):
        org = Organism(position[0],position[1],1)
        self.organisms.append(org)

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

    '''
    def __checking_neighbors(self,organisms):
        l_neighbors_position = []
        i = 0
        for organism in organisms:
            for neighbor_position in organism.neighbors:
                for neighbor in organisms:
                    i += 1
                    found = False
                    if organism.position != neighbor.position:
                        if neighbor_position == neighbor.position:
                            organism.qtd_neighbors += 1
                            found = True
                            break

                if found == False:
                    if neighbor_position not in l_neighbors_position:
                        l_neighbors_position.append(neighbor_position)
        print i
        return l_neighbors_position

    '''

    def __checking_neighbors(self, organisms):
        l_neighbors_position = []
        i = 0
        for organism in organisms:
            for neighbor_position in organism.neighbors:
                i +=1
                found = False
                list_neig = filter(lambda x:x.position == neighbor_position,organisms)
                if len(list_neig) > 0:
                    found = True
                    organism.qtd_neighbors += 1


                if found == False:
                    if neighbor_position not in l_neighbors_position:
                        l_neighbors_position.append(neighbor_position)
                if organism.qtd_neighbors > 3:
                    break
        print i
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
    MAGNITUDE = 8
    X0 = 6
    Y0 = 6

    def __init__(self,resolution):

        self.width,self.height = resolution
        pygame.init()
        self.windowSurface = pygame.display.set_mode(resolution, 0, 32)
        self.windowSurface.fill(self.WHITE)
        for x in range(resolution[0] / self.MAGNITUDE):
            for y  in range(resolution[1] / self.MAGNITUDE):
                self.drawCell((x,y),0)


    def set_title(self,title):
        pygame.display.set_caption(title)

    def update(self):
        pygame.display.update()


    def drawCell(self,position,state):

        color = (self.BLUE,self.YELLOW)[state]
        mag = self.MAGNITUDE

        xo = self.X0
        yo = self.Y0

        x = (position[0] * mag) + xo
        y = (position[1] * mag) + yo

        if (0 < x < self.width) and (0 < y < self.height):
            pygame.draw.polygon(self.windowSurface, color, ((x-3, y-3), (x+3, y-3), (x+3, y+3), (x-3, y+3)))




class Game:

    WIDTH = 800
    HEIGHT = 600
    SLEEP = "sleep 0.2"


    def __init__(self,name):
        self.name = name
        self.generation = 0
        self.environment = Environment()
        self.board = Board((self.WIDTH,self.HEIGHT))

        self.running = True
        self.paused = False

        self.board.set_title(self.name + " Running!")

    def pause(self):
        self.paused = (True, False)[self.paused]
        self.board.set_title(self.name + (" Running!"," Paused...")[self.paused])


    def update(self):

        if not self.paused:

            print "Generation: ",self.generation, "Lives: ", len(self.environment.organisms), " Deads: ", len(self.environment.deads_position)
            for dead_position in self.environment.deads_position:
                self.board.drawCell(dead_position,0)

            for organism in self.environment.organisms:
                self.board.drawCell(organism.position, 1)

            self.environment.update()
            self.generation +=1


            self.board.update()

            #os.system(self.SLEEP)


    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause()

                elif event.key == pygame.K_c:
                    pass




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
            environment.add_organism(position)


def fill_environment(environment):

    for x in range(0,100):
        for y in range(0,75):
            environment.add_organism((x, y))



if __name__ == "__main__":


    game = Game("Game of Life")
    game.update()

    fill_environment(game.environment)


    #for g in range(20,100,5):
        #Patterns.glider((g,20),1,game.environment)

    #Patterns.glider((20,20), 4, game.environment)

    while game.running:

        game.event()
        game.update()

































