from constant import *

class Cell:
    def __init__(self, pos_matrix, size, entities):
        self.pos_matrix = pos_matrix
        self.pos_coor   = self.matrix_to_coordinate(pos_matrix, size)
        self.map_size   = size
        #
        self.explored = False
        self.entities = self.set_cell_entites(entities)
        #
        self.previous  = None
        self.next_list = []

    #WORLD COORDINATE ==================================================================================================
    #matrix -> coordinate (room)
    def matrix_to_coordinate(self, pos_matrix, map_size): # |x --y to --x |y
        #(0,0) -> (1,10) | (9,0) -> (1,1) | (0,9) -> (10,10) | (9,9) -> (10,1)
        return (pos_matrix[1] + 1, map_size - pos_matrix[0])

    # get cell's coordinate (Room)
    def get_Room(self):
        return self.pos_coor

    #CELL'S ENTITIES ===================================================================================================
    # set cell's entities list
    def set_cell_entites(self, entities):
        dict = {entity:False for entity in s_entities_list} #[False]*5 #[Gold, Pit, Wumpus, Breeze, Stench]
        for entity in entities:
            if dict.get(entity) != None:
                dict[entity] = True
        return dict

    # get entities list [Gold, Pit, Wumpus, Breeze, Stench]
    def get_cell_entities(self):
        return [bool(element) for element in self.entities.values()]

    # check cell's entity
    def checkGold(self):
        return self.entities['G']
    def checkPit(self):
        return self.entities['P']
    def checkWumpus(self):
        return self.entities['W']
    def checkBreeze(self):
        return self.entities['B']
    def checkStench(self):
        return self.entities['S']

    #Explorer ==========================================================================================================
    # explored cell
    def setexploredCell(self):
        self.explored = True

    # check if cell explored
    def checkExplored(self):
        return self.explored

    #CELL'S LOGIC ======================================================================================================
    # check next cell of current cell if safe = mean current cell not contain entities: breeze or stench
    def isSafe(self):
        return not(self.entities['B'] or self.entities['S'])

    # set previous cell lead to current cell
    def set_previousCell(self, previousCell):
        self.previous = previousCell

    # set next cell available to go
    def set_nextCell(self, adjCell):
        for cell in adjCell:
            if cell.previous == None:
                self.next_list.append(cell)
                # cell.set_previousCell(self) #Error
                self.set_previousCell(cell)

    def get_adjCells(self, map_cell):
        adj = []
        #Left
        x = self.pos_matrix[0]
        y = self.pos_matrix[1] - 1
        if 0 <= x < self.map_size and 0 <= y < self.map_size:
            adj.append(map_cell[x][y])
        #Right
        x = self.pos_matrix[0]
        y = self.pos_matrix[1] + 1
        if 0 <= x < self.map_size and 0 <= y < self.map_size:
            adj.append(map_cell[x][y])
        #Up
        x = self.pos_matrix[0] - 1
        y = self.pos_matrix[1]
        if 0 <= x < self.map_size and 0 <= y < self.map_size:
            adj.append(map_cell[x][y])
        #Down
        x = self.pos_matrix[0] + 1
        y = self.pos_matrix[1]
        if 0 <= x < self.map_size and 0 <= y < self.map_size:
            adj.append(map_cell[x][y])

        return adj

    def get_Literal(self, entity: str, sign='+'):
        literal = ''
        if sign == '-':
            literal += sign
        literal += entity[0] + str(self.pos_matrix[0]) + str(self.pos_matrix[1])
        return literal

    #AGENT INTERACTING =================================================================================================
    # agent take gold
    def take_Gold(self):
        self.entities['G'] = False

    # agent kill Wumpus
    def kill_Wumpus(self, map_cell, KB):
        # Remove Wumpus flag
        self.entities['W'] = False
        # Delete adjacent cells's  ~ Stench
        adj = self.get_adjCells(map_cell)

        for cell in adj:
            # check if any Wumpus nearby (another Wumpus) if yes, stench still there
            remove = True
            cellAdj = cell.get_adjCells(map_cell)
            for adjCell in cellAdj:
                if adjCell.checkWumpus():
                    remove = False  # Another Wumpus -> not remove Stench
                    break

            # remove Stench
            if remove:
                cell.entities['S'] = False

                # KNOWLEDGE BASE CONFIGURATION--------------------------------|
                # remove KB Cell stench and add KB Cell -stench
                KB.rem([cell.get_Literal(s_entities_ste, '+')])
                KB.add([cell.get_Literal(s_entities_ste, '-')])

                # remove: S => Wa v Wb v Wb v Wb (line 118/propositionalLogic)
                clause = [cell.get_Literal(s_entities_ste, '-')]
                cell_Adj = cell.get_adjCells(map_cell)
                for adjCell in cell_Adj:
                    clause.append(adjCell.get_Literal(s_entities_wum, '+'))
                KB.rem(clause)

                # remove: Wa v Wb v Wc v Wd => S (line 124/propositionalLogic)
                for adjCell in cell_Adj:
                    clause = [cell.get_Literal(s_entities_ste, '+'), adjCell.get_Literal(s_entities_wum, '-')]
                    KB.rem(clause)

    def kill_Wumpus_Re(self, map_cell, KB):
        #Remove Wumpus flag
        self.entities['W'] = False
        KB.addP([self.get_Literal(s_entities_pit, '-')])
        #Delete adjacent cells's  ~ Stench
        adj = self.get_adjCells(map_cell)

        for cell in adj:
            #check if any Wumpus nearby (another Wumpus) if yes, stench still there
            remove = True
            cellAdj = cell.get_adjCells(map_cell)
            for adjCell in cellAdj:
                if adjCell.checkWumpus():
                    remove = False #Another Wumpus -> not remove Stench
                    break

            #remove Stench
            if remove:
                cell.entities['S'] = False

                #KNOWLEDGE BASE CONFIGURATION--------------------------------|
                KB.remW([cell.get_Literal(s_entities_ste, '+')])
                KB.addW([cell.get_Literal(s_entities_ste, '-')])

                #remove: S => Wa v Wb v Wb v Wb
                clause = []
                cell_Adj = cell.get_adjCells(map_cell)
                for adjCell in cell_Adj:
                    clause.append(adjCell.get_Literal(s_entities_wum, '+'))
                KB.remW(clause)