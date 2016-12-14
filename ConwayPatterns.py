class ConwayPatterns:


    '''
    SPACESHIPS
    '''

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

    '''
        OSCILLATORS
    '''

    @staticmethod
    def blinker(position, type, orientation, environment):
        l = []
        x0, y0 = position
        l = [(x0, y0), (x0, y0+1), (x0, y0 + 2)]

        for position in l:
            environment.add_cell(position, type)

    @staticmethod
    def toad(position, type, orientation, environment):
        l = []
        x0, y0 = position
        l = [(x0 + 1, y0), (x0 + 2, y0), (x0 + 3, y0),(x0, y0 + 1),(x0 + 1, y0 + 1), (x0 + 2, y0 + 1)]

        for position in l:
            environment.add_cell(position, type)


    @staticmethod
    def beacon(position,type,orientation,environment):


        l = []
        x0,y0 = position
        if orientation == 1:
            l = [(x0,y0), (x0, y0 + 1),(x0 + 1, y0 + 0), (x0 + 2, y0 + 3), (x0 + 3, y0 + 2), (x0 + 3, y0 + 3)]
        elif orientation == 2:
            l = [(x0, y0 + 2), (x0, y0 + 3), (x0 + 1, y0 + 3), (x0 + 2, y0 + 0), (x0 + 3, y0 + 0), (x0 + 3, y0 + 1)]

        for position in l:
            environment.add_cell(position,type)




    '''
        STILL LIFE PATTERNS
    '''


    @staticmethod
    def beehive (position, type, orientation, environment):
        l = []
        x0, y0 = position
        if orientation == 1:
            l = [(x0, y0 + 1), (x0 + 1, y0), (x0 + 1, y0 + 2),(x0 + 2, y0), (x0 + 2, y0 + 2), (x0 + 3, y0 + 1)]
        elif orientation == 2:
            l = [(x0, y0 + 1), (x0, y0 + 2), (x0 + 1, y0), (x0 + 1, y0 + 3), (x0 + 2, y0 + 1),(x0 + 2, y0 + 2)]
        else:
            return
        for position in l:
            environment.add_cell(position, type)

    @staticmethod
    def boat (position, type, orientation, environment):
        l = []
        x0, y0 = position
        if orientation == 1:
            l = [(x0, y0), (x0, y0 + 1), (x0 + 1, y0),(x0 + 1, y0 + 2), (x0 + 2, y0 + 1)]
        elif orientation == 2:
            l = [(x0, y0 + 2), (x0, y0 + 1), (x0 + 1, y0), (x0 + 1, y0 + 2), (x0 + 2, y0 + 1)]
        elif orientation == 3:
            l = [(x0 + 2, y0), (x0, y0 + 1), (x0 + 1, y0), (x0 + 1, y0 + 2), (x0 + 2, y0 + 1)]
        elif orientation == 4:
            l = [(x0 + 2, y0 + 2), (x0, y0 + 1), (x0 + 1, y0), (x0 + 1, y0 + 2), (x0 + 2, y0 + 1)]
        else:
            return

        for position in l:
            environment.add_cell(position, type)

    @staticmethod
    def tube(position, type, orientation, environment):
        l = []
        x0, y0 = position
        if orientation == 1:
            l = [(x0, y0 + 1), (x0 + 1, y0), (x0 + 1, y0 + 2), (x0 + 2, y0 + 1)]
        else:
            return

        for position in l:
            environment.add_cell(position, type)



    '''
        OTHERS
    '''
    @staticmethod
    def square(position,type,size,environment):
        for x in range(position[0] - size / 2, position[0] + size / 2):
            for y in range(position[1] - size / 2, position[1] + size / 2):
                environment.add_cell((x,y),type)

    @staticmethod
    def fill_environment(environment):

        for x in range(20,100):
            for y in range(10,81):
                environment.add_cell((x, y),1)
