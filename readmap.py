#READ MAP AND BUILD MAP
import copy

import cell as cell
import agent as agent
from constant import *

class Map:
    def __init__(self):
        #Init value
        self.map_size  = 10
        self.cell_size = 60

        #Graphic
        self.cell_unexplore = pygame.image.load(s_map_ele_unexplored)
        self.cell_explore   = pygame.image.load(s_map_ele_explored)
        self.cell_pit       = pygame.image.load(s_map_ele_pit)
        self.cell_exploreList = {key:None for key in list(s_map_ele_exploredList.keys())}
        self.loadExplored()

        #Map_Cellmatrix_Pos
        self.MapCell     = [[None]*self.map_size for _ in range(self.map_size)]
        self.InitMapCell = None

        #Logic_pos
        self.exploredCell = [[False]*self.map_size for _ in range(self.map_size)]
        self.initAgentPos = (9, 0)                                                   #set default first :> ~ room(10,10)
        self.agentInit    = None

    #GRAPHIC ===========================================================================================================
    #load explored cell with entities in it.
    def loadExplored(self):
        for key in self.cell_exploreList.keys():
            self.cell_exploreList[key] = pygame.transform.scale(pygame.image.load(s_map_ele_exploredList[key]), (60,60))

    #show cell with its position and status
    def show_cell(self, screen, row_pos, col_pos, is_explored, entitiesList=[False, False, False, False, False]):
        #Show cell in display with its position
        x = 20 + 60 * col_pos #(col(y) to x in graphic)
        y = 20 + 60 * row_pos #(row(x) to y in graphic)

        #is_explored = True
        if is_explored == False:
            screen.blit(self.cell_unexplore, (x, y))
        elif is_explored == True: #and entitiesList == [False, False, False, False, False]: #initAgent
            entitiesList = self.MapCell[row_pos][col_pos].get_cell_entities()
            screen.blit(self.cell_exploreList[str(entitiesList)], (x, y))

    #show map for the first time
    def show_map1st(self, screen):
        #Print out the map for the first time
        for row in range(self.map_size):
            for col in range(self.map_size):
                self.show_cell(screen, row, col, self.MapCell[row][col].checkExplored())
                    #for the first time, only init position of Agent is set Explored

    #POS <-> COOR ======================================================================================================
    def pos_to_coor(self, pos):
        return (pos[1] + 1, self.size - pos[0])

    def coor_to_pos(self, coor):
        return (self.size - coor[1], coor[0] - 1)

    #AGENT =============================================================================================================
    #get agent's init cell
    def getInit_agent(self):
        return self.initAgentPos

    #READ MAP ==========================================================================================================
    def read_map(self, filename):
        file = open(filename, 'r')
        self.map_size = int(file.readline())
        raw  = [line.split('.') for line in file.read().splitlines()]

        for row in range(self.map_size):
            for col in range(self.map_size):
                self.MapCell[row][col] = cell.Cell((row, col), self.map_size, raw[row][col])
                #Init Agent Position
                if 'A' in raw[row][col]:
                    self.agentInit = self.MapCell[row][col]
                    self.exploredCell[row][col] = True                                #set agent init cell to discovered
                    self.initAgentPos = (row, col)
                    # self.agent_cell.update_parent(self.cave_cell)
                    # self.init_agent_cell = copy.deepcopy(self.agent_cell)
        file.close()
        self.InitMapCell = copy.deepcopy(self.agentInit)
        # result, pos = self.is_valid_map()
        # if not result:
        #     if pos is None:
        #         raise TypeError('Input Error: The map is invalid! There is no Agent!')
        #     raise TypeError(
        #         'Input Error: The map is invalid! Please check at row ' + str(pos[0]) + ' and column ' + str(pos[1]) + '.')

    #ACTION ============================================================================================================
    #set cell discovered
    def discoverCell(self, pos):
        self.exploredCell[pos[0]][pos[1]] = True

    #check cell is_discovered?
    def checkDiscovered(self, pos):
        return self.exploredCell[pos[0]][pos[1]]

