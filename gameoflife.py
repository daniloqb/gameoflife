class Organism:
    def __init__(self,x,y,state):
        self.position =(x,y)
        self.state = state
        self.qtd_neighbors = 0
        self.neighbors = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]

    def __str__(self):
        print self.position


if __name__ == "__main__":

    l_organism = []
    l_organism.append(Organism(5,5,1))
    l_organism.append(Organism(5, 6, 1))
    l_organism.append(Organism(4, 4, 1))
    l_organism.append(Organism(4, 6, 1))
    l_organism.append(Organism(6, 4, 1))
    gen = 0;

while gen < 3:

        gen +=1
        print gen

        l_neighrbors = []


        for organism in l_organism:
            for neighbor_position in organism.neighbors:
                for neighbor in l_organism:
                    found = False
                    if organism.position != neighbor.position:
                        if neighbor_position == neighbor.position:
                            organism.qtd_neighbors +=1
                            found = True
                            break
                if found == False:
                    if neighbor_position not in l_neighrbors:
                        l_neighrbors.append(neighbor_position)




        for organism in l_organism:
            if organism.qtd_neighbors < 2 or organism.qtd_neighbors > 3:
                print organism.position, organism.qtd_neighbors, "Vai morrer."
            else:
                print organism.position,organism.qtd_neighbors,"Se safou"

        l_dead = []

        for dead in l_neighrbors:
            l_dead.append(Organism(dead[0],dead[1],1))

        for organism in l_dead:
            for neighbor in l_organism:
                if neighbor.position in organism.neighbors and neighbor.state == 1:
                    organism.qtd_neighbors += 1


        print
        for dead in l_dead:
            if dead.qtd_neighbors == 3:
                print dead.position, "Vai nascer"

        print


        for organism in l_organism:
            print "Org: ", organism.position
            if organism.qtd_neighbors < 2 or organism.qtd_neighbors > 3:
                print "Remove", organism.position
                l_organism.remove(organism)


        for organism in l_dead:
            if organism.qtd_neighbors == 3:
                l_organism.append(organism)

        print "New"
        for organism in l_organism:
            print organism.position


        for organism in l_organism:
            organism.qtd_neighbors = 0

        for organism in l_organism:
            print "Organism: ",organism.position,"QTD Neighbors: ", organism.qtd_neighbors
            print "Neighbors: ",organism.neighbors


