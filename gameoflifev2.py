import pygame


class Organism:
    def __init__(self,x,y,state):
        self.position =(x,y)
        self.state = state
        self.qtd_neighbors = 0
        self.neighbors = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]

    def __str__(self):
        print self.position


class Environment:
    def __init__(self):
        self.environment = []

    def is_empty(self):
        return  not (len(self.environment))

    def add_organism(self,position):
        org = Organism(position[0],position[1],1)
        self.environment.append(org)

    def update(self):

        l_neighbors_position = self.__checking_neighbors(self.environment)

        list_of_deads = self.__checking_deads(l_neighbors_position, self.environment)

        self.__killing_organisms(self.environment)

        self.__checking_new_borns(list_of_deads, self.environment)

        self.__reinitialize_organisms(self.environment)

    def show(self):
        for organism in self.environment:
            print organism.position,":", organism.qtd_neighbors,
        print


    # private methods


    def __checking_neighbors(self,environment):
        l_neighbors_position = []
        for organism in environment:
            for neighbor_position in organism.neighbors:
                for neighbor in environment:
                    found = False
                    if organism.position != neighbor.position:
                        if neighbor_position == neighbor.position:
                            organism.qtd_neighbors += 1
                            found = True
                            break

                if found == False:
                    if neighbor_position not in l_neighbors_position:
                        l_neighbors_position.append(neighbor_position)

        return l_neighbors_position


    def __checking_deads(self,l,environment):
        deads = []

        for dead in l:
            deads.append(Organism(dead[0], dead[1], 1))

        for dead_organism in deads:
            for neighbor in environment:
                if neighbor.position in dead_organism.neighbors:
                    dead_organism.qtd_neighbors += 1

        return deads


    def __killing_organisms(self,environment):
        organism_to_kill = []
        for organism in environment:
            if organism.qtd_neighbors < 2 or organism.qtd_neighbors > 3:
                organism_to_kill.append(organism)

        for organism in organism_to_kill:
            environment.remove(organism)

    def __checking_new_borns(self,l,environment):
        for organism in l:
            if organism.qtd_neighbors == 3:
                environment.append(organism)


    def __reinitialize_organisms(self,environment):
        for organism in environment:
            organism.qtd_neighbors = 0


if __name__ == "__main__":
    '''
    environment = []
    environment.append(Organism(5,5,1))
    environment.append(Organism(5, 6, 1))
    environment.append(Organism(4, 4, 1))
    environment.append(Organism(4, 6, 1))
    environment.append(Organism(6, 4, 1))

    environment = []
    environment.append(Organism(5, 5, 1))
    environment.append(Organism(5, 6, 1))
    environment.append(Organism(5, 7, 1))
    environment.append(Organism(5, 8, 1))
    environment.append(Organism(5, 9, 1))

    environment.append(Organism(6, 5, 1))
    environment.append(Organism(6, 6, 1))
    environment.append(Organism(6, 7, 1))
    environment.append(Organism(6, 8, 1))
    environment.append(Organism(6, 9, 1))

    environment.append(Organism(7, 5, 1))
    environment.append(Organism(7, 6, 1))
    environment.append(Organism(7, 7, 1))
    environment.append(Organism(7, 8, 1))
    environment.append(Organism(7, 9, 1))

    environment.append(Organism(8, 5, 1))
    environment.append(Organism(8, 6, 1))
    environment.append(Organism(8, 7, 1))
    environment.append(Organism(8, 8, 1))
    environment.append(Organism(8, 9, 1))

    environment.append(Organism(9, 5, 1))
    environment.append(Organism(9, 6, 1))
    environment.append(Organism(9, 7, 1))
    environment.append(Organism(9, 8, 1))
    environment.append(Organism(9, 9, 1))



    environment.append(Organism(10, 5, 1))
    environment.append(Organism(10, 6, 1))
    environment.append(Organism(10, 7, 1))
    environment.append(Organism(10, 8, 1))
    environment.append(Organism(10, 9, 1))

    environment.append(Organism(11, 5, 1))
    environment.append(Organism(11, 6, 1))
    environment.append(Organism(11, 7, 1))
    environment.append(Organism(11, 8, 1))
    environment.append(Organism(11, 9, 1))

    environment.append(Organism(12, 5, 1))
    environment.append(Organism(12, 6, 1))
    environment.append(Organism(12, 7, 1))
    environment.append(Organism(12, 8, 1))
    environment.append(Organism(12, 9, 1))

    environment.append(Organism(13, 5, 1))
    environment.append(Organism(13, 6, 1))
    environment.append(Organism(13, 7, 1))
    environment.append(Organism(13, 8, 1))
    environment.append(Organism(13, 9, 1))

    environment.append(Organism(14, 5, 1))
    environment.append(Organism(14, 6, 1))
    environment.append(Organism(14, 7, 1))
    environment.append(Organism(14, 8, 1))
    environment.append(Organism(14, 9, 1))
    '''


    environment = Environment()

    '''
    environment.add_organism((5, 5))
    environment.add_organism((5, 6))
    environment.add_organism((4, 4))
    environment.add_organism((4, 6))
    environment.add_organism((6, 4))
    '''

    '''
    environment.add_organism((5, 5))
    environment.add_organism((5, 6))
    environment.add_organism((5, 7))
    environment.add_organism((5, 8))
    environment.add_organism((5, 9))

    environment.add_organism((6, 5))
    environment.add_organism((6, 6))
    environment.add_organism((6, 7))
    environment.add_organism((6, 8))
    environment.add_organism((6, 9))

    environment.add_organism((7, 5))
    environment.add_organism((7, 6))
    environment.add_organism((7, 7))
    environment.add_organism((7, 8))
    environment.add_organism((7, 9))

    environment.add_organism((8, 5))
    environment.add_organism((8, 6))
    environment.add_organism((8, 7))
    environment.add_organism((8, 8))
    environment.add_organism((8, 9))

    environment.add_organism((9, 5))
    environment.add_organism((9, 6))
    environment.add_organism((9, 7))
    environment.add_organism((9, 8))
    environment.add_organism((9, 9))


    environment.add_organism((10, 5))
    environment.add_organism((10, 6))
    environment.add_organism((10, 7))
    environment.add_organism((10, 8))
    environment.add_organism((10, 9))

    environment.add_organism((11, 5))
    environment.add_organism((11, 6))
    environment.add_organism((11, 7))
    environment.add_organism((11, 8))
    environment.add_organism((11, 9))

    environment.add_organism((12, 5))
    environment.add_organism((12, 6))
    environment.add_organism((12, 7))
    environment.add_organism((12, 8))
    environment.add_organism((12, 9))

    environment.add_organism((13, 5))
    environment.add_organism((13, 6))
    environment.add_organism((13, 7))
    environment.add_organism((13, 8))
    environment.add_organism((13, 9))

    environment.add_organism((14, 5))
    environment.add_organism((14, 6))
    environment.add_organism((14, 7))
    environment.add_organism((14, 8))
    environment.add_organism((14, 9))
    '''

    gen = 0;


    while not environment.is_empty():
        print "Generation: ", gen," ",
        environment.show()
        environment.update()
        gen +=1





































