import pygame.time

import agent as Agent
import readmap as Map
import cell as Cell
import KB
from constant import *
import copy

import copy



previousCell_list = []
class Propositional_Logic:
    def __init__(self, wumpusgame, screen, map, agent, output, agent_init, outfile):
        #logic/graphic
        self.game   = wumpusgame
        self.screen = screen
        self.objmap = map
        self.agent  = agent
        #
        self.output = output
        self.map = map.MapCell
        self.map_size = 10
        #
        self.KB = KB.KnowledgeBase()
        self.agent_cell = map.agentInit
        self.agent_init = map.agentInit
        self.cave_cell  = self.agent_init
        #out
        self.outfile = outfile
        self.action = []
        self.score = 0
    def cell_check_explored(self,cell):
        return self.map[cell.pos_matrix[0]][cell.pos_matrix[1]].checkExplored()

    #OUTPUT -----------------------------------------------------------------------------------------------------------|
    # write output file
    def write_output(self, content):
        content = str(content)
        self.outfile.write(content + '\n')

    # print output
    @staticmethod
    def print_output(content):
        if True:
            print(content)

    #ACTION -----------------------------------------------------------------------------------------------------------|
    def Action(self, action, position=None):
        self.action.append(action)

        # PRINT ACTION
        if position is not None:
            self.print_output(str(action) + ': ' + str(position))
        else:
            self.print_output(str(action))

        #CHECK ACTION
        if action in [s_action_up, s_action_down, s_action_left, s_action_right, s_action_breeze, s_action_stench, s_action_victory,
                      s_action_kill, s_action_nkill, s_action_de_pit, s_action_de_npit, s_action_de_wumpus, s_action_de_nwumpus,
                      s_action_infer_pit, s_action_infer_npit, s_action_infer_safe, s_action_infer_nsafe, s_action_infer_wumpus, s_action_infer_nwumpus]:
            pass
        elif action == s_action_move: #MOVE
            self.score -= 10
            self.write_output('Score: ' + str(self.score))
        elif action == s_action_grab: #GRAB GOLD
            self.score += 100
            self.write_output('Score: ' + str(self.score))
        elif action == s_action_shoot: #SHOOTING ARROW
            self.score -= 100
            self.write_output('Score: ' + str(self.score))
        elif action == s_action_fall: #FALL INTO PIT
            self.score -= 10000
            self.write_output('Score: ' + str(self.score))
        elif action == s_action_eaten: #BE EATEN BY WUMPUS
            self.score -= 10000
            self.write_output('Score: ' + str(self.score))
        elif action == s_action_climb: #CLIMB OUT
            self.score += 10
            self.write_output('Score: ' + str(self.score))

    def move_to(self, cell):
        dir = self.turn_to(cell)
        self.Action(s_action_move, cell.pos_matrix)

        self.objmap.show_cell(self.screen, self.agent_cell.pos_matrix[0], self.agent_cell.pos_matrix[1], True)
        self.agent_cell = cell
        self.objmap.show_cell(self.screen, self.agent_cell.pos_matrix[0], self.agent_cell.pos_matrix[1], True)
        self.agent.move(self.screen, dir)

    def turn_to(self, cell):
        if self.agent_cell.pos_matrix[0] == cell.pos_matrix[0]: #Turn LEFT/RIGHT
            if self.agent_cell.pos_matrix[1] + 1 == cell.pos_matrix[1]:
                self.Action(s_action_right)
                self.objmap.show_cell(self.screen, self.agent_cell.pos_matrix[0], self.agent_cell.pos_matrix[1], True)
                self.agent.turn(self.screen, s_agent_direction_right)
                return s_agent_direction_right
            else:
                self.Action(s_action_left)
                self.objmap.show_cell(self.screen, self.agent_cell.pos_matrix[0], self.agent_cell.pos_matrix[1], True)
                self.agent.turn(self.screen, s_agent_direction_left)
                return s_agent_direction_left
        elif self.agent_cell.pos_matrix[1] == cell.pos_matrix[1]: #Turn UP/DOWN
            if self.agent_cell.pos_matrix[0] + 1 == cell.pos_matrix[0]:
                self.Action(s_action_down)
                self.objmap.show_cell(self.screen, self.agent_cell.pos_matrix[0], self.agent_cell.pos_matrix[1], True)
                self.agent.turn(self.screen, s_agent_direction_down)
                return s_agent_direction_down
            else:
                self.Action(s_action_up)
                self.objmap.show_cell(self.screen, self.agent_cell.pos_matrix[0], self.agent_cell.pos_matrix[1], True)
                self.agent.turn(self.screen, s_agent_direction_up)
                return s_agent_direction_up

    #ADD to KNOWLEDGE-BASE --------------------------------------------------------------------------------------------|
    def add_to_KB(self, cell):
        adjCell = cell.get_adjCells(self.map)

        #Pit
        if cell.checkPit():
            self.KB.add([cell.get_Literal(s_entities_pit)])
            self.KB.add([cell.get_Literal(s_entities_wum, '-')])
        #Wumpus (if Pit in this cell, there is no Wum)
        elif cell.checkWumpus():
            self.KB.add([cell.get_Literal(s_entities_wum)])
            self.KB.add([cell.get_Literal(s_entities_pit, '-')])

        #Breeze ------------------------------------------------------------|
        if cell.checkBreeze():
            self.KB.add([cell.get_Literal(s_entities_bre, '+')])

            # B => Pa v Pb v Pc v Pd
            clause = [cell.get_Literal(s_entities_bre, '-')]
            for adj in adjCell:
                clause.append(adj.get_Literal(s_entities_pit, '+'))
            self.KB.add(clause)

            # Pa v Pb v Pc v Pd => B
            for adj in adjCell:
                clause = [cell.get_Literal(s_entities_bre, '+'), adj.get_Literal(s_entities_pit, '-')]
                self.KB.add(clause)
        #no Breeze
        else:
            self.KB.add([cell.get_Literal(s_entities_bre, '-')])

            #-B => -Pa ^ -Pb ^ -Pc ^ -Pd
            for adj in adjCell:
                clause = [adj.get_Literal(s_entities_pit, '-')]
                self.KB.add(clause)

        #Stench -------------------------------------------------------------|
        if cell.checkStench():
            self.KB.add([cell.get_Literal(s_entities_ste, '+')])

            # S => Wa v Wb v Wc v Wd
            clause = [cell.get_Literal(s_entities_ste, '-')]
            for adj in adjCell:
                clause.append(adj.get_Literal(s_entities_wum, '+'))
            self.KB.add(clause)

            # Pa v Pb v Pc v Pd => B
            for adj in adjCell:
                clause = [cell.get_Literal(s_entities_ste, '+'), adj.get_Literal(s_entities_wum, '-')]
                self.KB.add(clause)
        #no Stench
        else:
            self.KB.add([cell.get_Literal(s_entities_ste, '-')])

            #-B => -Pa ^ -Pb ^ -Pc ^ -Pd
            for adj in adjCell:
                clause = [adj.get_Literal(s_entities_wum, '-')]
                self.KB.add(clause)

        #Print out
        # self.print_output(self.KB.KB)
        # self.write_output(self.KB.KB)

    #BACTRACK-SEARCH --------------------------------------------------------------------------------------------------|
    def backtrackSearch(self):
        #Check condition ---------------------------------------------------|
        if self.agent_cell.checkWumpus():
            self.Action(s_action_eaten)
            return False #eaten by Wumpus

        if self.agent_cell.checkPit():
            self.Action(s_action_fall)
            return False #fall into Pit

        if self.agent_cell.checkGold():
            self.agent_cell.take_Gold()
            self.Action(s_action_grab)

        if self.agent_cell.checkBreeze():
            self.Action(s_action_breeze)

        if self.agent_cell.checkStench():
            # print("Detect stench")
            self.Action(s_action_stench)

        if (not self.cell_check_explored(self.agent_cell)) or (self.agent_cell == self.agent_init):
            self.agent_cell.setexploredCell()
            self.add_to_KB(self.agent_cell)

        #Create adj cell list to find safe next_cell_list
        adjCell = self.agent_cell.get_adjCells(self.map)

        adjCell_list = copy.deepcopy(adjCell)
        # for cell in adjCell:
            # adjCell_list.append(cell.pos_matrix)

        #Remove previous cell in adjCell
        if self.agent_cell.previous in adjCell:
            adjCell.remove(self.agent_cell.previous)

        #Remove explored cell in adjCell
        exploredCell = []
        for cell in adjCell:
            # if cell.checkExplored():
            if self.cell_check_explored(cell):
                exploredCell.append(cell)
        for cell in exploredCell:
            if cell in adjCell:
                adjCell.remove(cell)

        #Store again previous cell --> this cell
        previousCell = self.agent_cell

        dangerCell = [] #To store dangerous cell can infer from this cell?
        # current cell contain Stench, Breeze -> inference from KB to make decision
        if not self.agent_cell.isSafe():
            #remove Pit cell that already known
            knownPit_cell = []
            for adj in adjCell:
                # if adj.checkExplored() and adj.checkPit(): #Có dư không khi đã check explored phía trên rồi
                if self.cell_check_explored(adj) and adj.checkPit(): #Có dư không khi đã check explored phía trên rồi
                    knownPit_cell.append(adj)
            for cell in knownPit_cell:
                adjCell.remove(cell)

            #Inference PIT if current cell contain Breeze
            dangerCell = []
            if self.agent_cell.checkBreeze():
                for adj in adjCell:
                    #Print
                    self.print_output('Inference Pit: ' + str(adj.pos_matrix))
                    #self.write_output('Inference Pit: ' + str(adj.pos_matrix))

                    #Infer
                    self.Action(s_action_infer_pit)
                    neg_alpha = [adj.get_Literal(s_entities_pit, '-')]
                    ispit = self.KB.inference(neg_alpha)

                    #Pit inferencable: there is pit in adj
                    if ispit:
                        self.Action(s_action_de_pit)
                        self.print_output("Detect Pit in " + str(adj.pos_matrix))

                        adj.setexploredCell()
                        self.objmap.show_cell(self.screen, adj.pos_matrix[0], adj.pos_matrix[1], True)
                        adj.set_previousCell(adj)
                        dangerCell.append(adj)

                    #Pit uninferencable: cant infer pit
                    else:
                        #check if agent can inference no Pit
                        self.Action(s_action_infer_npit)
                        neg_alpha = [adj.get_Literal(s_entities_pit, '+')]
                        isnotpit  = self.KB.inference(neg_alpha)

                        #Not Pit inferencable: there is no pit
                        if isnotpit:
                            self.Action(s_action_de_npit)
                            self.print_output("Detect no Pit in " + str(adj.pos_matrix))

                            adj.setexploredCell()

                        #No Pit uninferencable / Pit uninferencable: add :>
                        else:
                            dangerCell.append(adj)

            #Inference WUMPUS if current cell contain Stench
            if self.agent_cell.checkStench():
                for adj in adjCell:
                    #Print
                    self.print_output('Inference Wumpus: ' + str(adj.pos_matrix))
                    #self.write_output('Inference Wumpus: ' + str(adj.pos_matrix))

                    #Infer
                    self.Action(s_action_infer_wumpus)
                    neg_alpha = [adj.get_Literal(s_entities_wum, '-')]
                    iswum = self.KB.inference(neg_alpha)

                    #Wumpus inferencable: there is wumpus -> kill -> safe
                    if iswum:
                        self.Action(s_action_de_wumpus)
                        self.print_output("Detect Wumpus in " + str(adj.pos_matrix))

                        # adj.setexploredCell()

                        self.Action(s_action_shoot)
                        self.Action(s_action_kill)
                        adj.kill_Wumpus(self.map, self.KB)

                        #self.write_output(str(self.KB.KB))

                    #Wumpus uninferencable: cant infer wumpus
                    else:
                        #check if agent can inference no Wumpus
                        self.Action(s_action_infer_nwumpus)
                        neg_alpha = [adj.get_Literal(s_entities_wum, '+')]
                        isnotwum = self.KB.inference(neg_alpha)

                        #no Wumpus inferencable: there is no wumpus
                        if isnotwum:
                            self.Action(s_action_de_nwumpus)
                            #self.print_output("Detect no Wumpus in " + str(adj.pos_matrix))

                            # adj.setexploredCell()

                        #No Wumpus uninferencable / Wumpus uninferencable
                        else:
                            dangerCell.append(adj)

            #Still cant not inference Wumpus/Not Wumpus -> bắn đại
            if self.agent_cell.checkStench():
                direction = self.agent_cell.get_adjCells(self.map)

                #delete previous cell (wumpus cant be there)
                if self.agent_cell.previous in direction:
                    direction.remove(self.agent_cell.previous)

                #delete previous explored cell (if wumpus there, agent would have known :v)
                explored = []
                for cell in direction:
                    # if cell.checkExplored():
                    if self.cell_check_explored(cell):
                        explored.append(cell)
                for cell in explored:
                    direction.remove(cell)

                #Try shooting
                for dir in direction:
                    self.print_output('Try shoot: ' + str(dir.pos_matrix))
                    #self.write_output('Try shoot: ' + str(dir.pos_matrix))
                    self.turn_to(dir)

                    self.Action(s_action_shoot)

                    #Shoot graphic
                    self.agent.shoot(self.screen, dir.pos_matrix)
                    pygame.time.delay(100)
                    self.objmap.show_cell(self.screen, dir.pos_matrix[0], dir.pos_matrix[1], False)

                    if dir.checkWumpus():
                        self.Action(s_action_kill)
                        dir.kill_Wumpus(self.map, self.KB)

                        #self.write_output(str(self.KB.KB))

                    #Killed
                    if self.agent_cell.checkStench() == False: #there are no Wumpus arround because Stench is gone
                        self.agent_cell.set_nextCell([dir])
                        if dir in dangerCell:
                            dangerCell.remove(dir)
                        break

        #Remove all danger cell in next_cell_list -> safe next_cell_list
        dangerCell = list(set(dangerCell))
        for danger in dangerCell:
            if danger in adjCell:
                adjCell.remove(danger)
        self.agent_cell.set_nextCell(adjCell)
        #Print debuging
        # for cell in adjCell:
        #     print(cell.pos_matrix)
        # for cell in self.agent_cell.next_list:
        #     print(cell.pos_matrix)

        saved_agent_pos = self.agent_cell.pos_matrix

        if len(self.agent_cell.next_list)==0:
            temp_T = True
            for cell in self.agent_cell.next_list:
                # if not self.map[cell.pos_matrix[0]][cell.pos_matrix[1]].checkExplored():
                if not (self.cell_check_explored(cell)):
                    temp_T = False
            
            if temp_T:
                temp = []
                for cell_nam in adjCell_list:
                    if not cell_nam.isSafe():
                        temp.append(cell_nam)
                    if not cell_nam.pos_matrix in previousCell_list:
                        temp.append(cell_nam)
                for cell_nam in temp:
                    try:
                        adjCell_list.remove(cell_nam)
                    except:
                        pass

                count_nam = len(adjCell_list)
                index_nam = -1
                index_previous = 0
                while True:
                    for i, cell_check in enumerate(adjCell_list):
                        if previousCell_list[index_nam] == cell_check.pos_matrix:
                            count_nam -= 1
                            index_previous = i
                    if count_nam==0:
                        break
                    # pos = cell_check.pos_matrix
                    pos = previousCell_list[index_nam]
                    temp_cell = self.map[pos[0]][pos[1]]
                    temp_cell_adjs = temp_cell.get_adjCells(self.map)
                    ####
                    exploredCell = []
                    for temp_cell_check in temp_cell_adjs:
                        # if temp_cell_check.checkExplored():
                        if self.cell_check_explored(temp_cell_check):
                            exploredCell.append(temp_cell_check)
                    for temp_cell_check in exploredCell:
                        if temp_cell_check in temp_cell_adjs:
                            temp_cell_adjs.remove(temp_cell_check)
                    if len(temp_cell_adjs)>0:              
                        break
                    index_nam-=1
                print()

                self.move_to(adjCell_list[index_previous])
                while (previousCell_list[-1] != adjCell_list[index_previous].pos_matrix):
                    previousCell_list.remove(previousCell_list[-1])
                previousCell_list.remove(previousCell_list[-1])
                #self.write_output('Backtrack: ' + str(previousCell.pos_matrix))
        else:
            for cell in self.agent_cell.next_list:
                # if cell.checkExplored():
                if self.cell_check_explored(cell):
                    continue
                pygame.time.delay(50)
                self.game.stageGame_action()
                previousCell_list.append(previousCell.pos_matrix)
                self.move_to(cell)
                if cell.pos_matrix == (3,2):
                    print("ducnam ne")
                #self.write_output('Move to: ' + str(self.agent_cell.pos_matrix))

                if not self.backtrackSearch():
                    return False
                pygame.time.delay(50)

                if saved_agent_pos == (2,0):
                    print("ducnam ne")    

                if self.agent_cell.pos_matrix != saved_agent_pos:
                    break
                
                temp_T = True
                for cell in self.agent_cell.next_list:
                    # if not self.map[cell.pos_matrix[0]][cell.pos_matrix[1]].checkExplored():
                    if not self.cell_check_explored(cell):
                        temp_T = False
                
                if temp_T:
                    temp = []
                    for cell_nam in adjCell_list:
                        if not cell_nam.isSafe():
                            temp.append(cell_nam)
                        if not cell_nam.pos_matrix in previousCell_list:
                            temp.append(cell_nam)
                    for cell_nam in temp:
                        try:
                            adjCell_list.remove(cell_nam)
                        except:
                            pass

                    count_nam = len(adjCell_list)
                    index_nam = -1
                    index_previous = 0
                    while True:
                        for i, cell_check in enumerate(adjCell_list):
                            if previousCell_list[index_nam] == cell_check.pos_matrix:
                                count_nam -= 1
                                index_previous = i
                        if count_nam==0:
                            break
                        # pos = cell_check.pos_matrix
                        pos = previousCell_list[index_nam]
                        temp_cell = self.map[pos[0]][pos[1]]
                        temp_cell_adjs = temp_cell.get_adjCells(self.map)
                        ####
                        exploredCell = []
                        for temp_cell_check in temp_cell_adjs:
                            # if temp_cell_check.checkExplored():
                            if self.cell_check_explored(temp_cell_check):
                                exploredCell.append(temp_cell_check)
                        for temp_cell_check in exploredCell:
                            if temp_cell_check in temp_cell_adjs:
                                temp_cell_adjs.remove(temp_cell_check)
                        if len(temp_cell_adjs)>0:              
                            break
                        index_nam-=1
                    print()

                    self.move_to(adjCell_list[index_previous])
                    while (previousCell_list[-1] != adjCell_list[index_previous].pos_matrix):
                        previousCell_list.remove(previousCell_list[-1])
                    previousCell_list.remove(previousCell_list[-1])
                    #self.write_output('Backtrack: ' + str(previousCell.pos_matrix))
        return True

    #Solving map
    def solving(self):

        self.backtrackSearch()
        print('END')

        return self.score



