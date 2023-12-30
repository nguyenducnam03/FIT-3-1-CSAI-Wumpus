#READ MAP AND BUILD MAP
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

        #Logic_pos
        self.initAgentPos = (9, 0)                                                   #set default first :> ~ room(10,10)
        self.agentInit    = None

    #GRAPHIC ===========================================================================================================
    #load explored cell with entities in it.
    def loadExplored(self):
        for key in self.cell_exploreList.keys():
            self.cell_exploreList[key] = pygame.transform.scale(pygame.image.load(s_map_ele_exploredList[key]), (self.cell_size, self.cell_size))

    #show cell with its position and status
    def show_cell(self, screen, row_pos, col_pos, is_explored, entitiesList=[False, False, False, False, False]):
        # Show cell in display with its position
        x = 20 + 60 * col_pos  # (col(y) to x in graphic)
        y = 20 + 60 * row_pos  # (row(x) to y in graphic)

        # is_explored = True
        if is_explored == False:
            screen.blit(self.cell_unexplore, (x, y))
        elif is_explored == True:  # and entitiesList == [False, False, False, False, False]: #initAgent
            entitiesList = self.MapCell[row_pos][col_pos].get_cell_entities()
            # If there is Pit with another obj, only show Pit
            if entitiesList[1] == True:
                entitiesList = [False, True, False, False, False]

            screen.blit(self.cell_exploreList[str(entitiesList)], (x, y))

    #show map for the first time
    def show_map1st(self, screen):
        #Print out the map for the first time
        for row in range(self.map_size):
            for col in range(self.map_size):
                self.show_cell(screen, row, col, self.MapCell[row][col].checkExplored())
                    #for the first time, only init position of Agent is set Explored

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
                    self.agentInit = self.MapCell[row][col]                              #set agent init cell to discovered
                    self.initAgentPos = (row, col)
        file.close()


