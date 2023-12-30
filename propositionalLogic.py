import pygame.time

import agent as Agent
import readmap as Map
import cell as Cell
import KB
from constant import *
import copy

import copy
speed_time = 100


previousCell_list = []
class Propositional_Logic:
    def __init__(self, wumpusgame, screen, map, agent, agent_init, outfile):
        #logic/graphic
        self.game   = wumpusgame
        self.screen = screen
        self.objmap = map
        self.agent  = agent
        #
        self.map = map.MapCell
        self.map_size = 10
        #
        self.KB = KB.KnowledgeBase()
        self.agent_cell = map.agentInit
        self.agent_init = map.agentInit
        self.cave_cell  = self.agent_init
        #out
        self.stopgame = False
        self.outfile = outfile
        self.score = 0
        self.font = pygame.font.Font(s_display_font, 24)

    def cell_check_explored(self, cell):
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

    def showScore(self):
        #Back
        pygame.draw.rect(self.screen, s_color_white, (645, 55, 150, 50))
        #Score
        score_text = self.font.render(str(self.score), True, s_color_black)
        score_rect = score_text.get_rect(center=(645+150//2, 55+50//2))
        self.screen.blit(score_text, score_rect)

    #ACTION -----------------------------------------------------------------------------------------------------------|
    def Action(self, action, position=None):
        # PRINT ACTION
        if action in [s_action_right, s_action_left, s_action_up, s_action_down]:
            self.print_output('================================')
            self.write_output('================================')
        if position is not None:
            self.print_output(str(action) + ': ' + str(position))
            self.write_output(str(action) + ': ' + str(position))
        else:
            self.print_output(str(action))
            self.write_output(str(action))
        # HOME
        self.stopgame = self.game.stageGame_action()

        #Show Score
        self.showScore()

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
        self.Action(s_action_move, cell.get_Room())

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

    #BACTRACK-SEARCH BW -----------------------------------------------------------------------------------------------|
    #Add to Knowledge Base
    def add_to_KB_BW(self, cell):
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
    
    def add_clause_KB(self,clause):
        self.KB.add(clause)

    # Backtrack Search
    def backtrackSearch_BW(self):
        # Check condition ---------------------------------------------------|
        if self.agent_cell.checkWumpus():
            self.Action(s_action_eaten)
            self.stopgame = True
            return False  # eaten by Wumpus

        if self.agent_cell.checkPit():
            self.Action(s_action_fall)
            self.stopgame = True
            return False  # fall into Pit

        if self.agent_cell.checkGold():
            self.agent_cell.take_Gold()
            self.Action(s_action_grab)

        if self.agent_cell.checkBreeze():
            self.Action(s_action_breeze, self.agent_cell.get_Room())

        if self.agent_cell.checkStench():
            self.Action(s_action_stench, self.agent_cell.get_Room())

        if (not self.cell_check_explored(self.agent_cell)) or (self.agent_cell == self.agent_init):
            self.agent_cell.setexploredCell()
            self.add_to_KB_BW(self.agent_cell)

        # Create adj cell list to find safe next_cell_list
        adjCell = self.agent_cell.get_adjCells(self.map)
        adjCell_list = copy.deepcopy(adjCell)

        # Remove previous cell in adjCell
        if self.agent_cell.previous in adjCell:
            adjCell.remove(self.agent_cell.previous)

        # Remove explored cell in adjCell
        exploredCell = []
        for cell in adjCell:
            # if cell.checkExplored():
            if self.cell_check_explored(cell):
                exploredCell.append(cell)
        for cell in exploredCell:
            if cell in adjCell:
                adjCell.remove(cell)

        previousCell = self.agent_cell

        dangerCell = []  # To store dangerous cell can infer from this cell?
        # current cell contain Stench, Breeze -> inference from KB to make decision
        type = -1
        if not self.agent_cell.isSafe():
            # Inference PIT if current cell contain Breeze
            # dangerCell = []
            # Inference WUMPUS if current cell contain Stench
            if self.agent_cell.checkStench():
                for adj in adjCell:
                    type = 3
                    self.Action(s_action_infer_wumpus, adj.get_Room())
                    iswum = self.KB.inference(adj, self, type)

                    # Wumpus inferencable: there is wumpus -> kill -> safe
                    if iswum:
                        self.Action(s_action_de_wumpus, adj.get_Room())

                        self.Action(s_action_shoot)
                        self.Action(s_action_kill, adj.get_Room())
                        adj.kill_Wumpus(self.map, self.KB)

                        clause = [adj.get_Literal(s_entities_wum, '-')]
                        self.add_clause_KB(clause)

                        clause = [adj.get_Literal(s_entities_pit, '-')]
                        print("add KB no PIT here", clause)
                        self.add_clause_KB(clause)

                    # Wumpus uninferencable: cant infer wumpus
                    else:
                        type = 4
                        self.Action(s_action_infer_nwumpus, adj.get_Room())
                        isnotwum = self.KB.inference(adj, self, type)

                        # no Wumpus inferencable: there is no wumpus
                        if isnotwum:
                            self.Action(s_action_de_nwumpus, adj.get_Room())

                            clause = [adj.get_Literal(s_entities_ste, '-')]
                            self.add_clause_KB(clause)

                        # No Wumpus uninferencable / Wumpus uninferencable
                        else:
                            dangerCell.append(adj)

            # Still cant not inference Wumpus/Not Wumpus -> bắn đại
            if self.agent_cell.checkStench():
                direction = self.agent_cell.get_adjCells(self.map)

                # delete previous cell (wumpus cant be there)
                if self.agent_cell.previous in direction:
                    direction.remove(self.agent_cell.previous)

                # delete previous explored cell (if wumpus there, agent would have known :v)
                explored = []
                for cell in direction:
                    # if cell.checkExplored():
                    if self.cell_check_explored(cell):
                        explored.append(cell)
                for cell in explored:
                    direction.remove(cell)

                # Try shooting
                for dir in direction:
                    self.turn_to(dir)

                    self.Action(s_action_shoot, dir.get_Room())

                    # Shoot graphic
                    self.agent.shoot(self.screen, dir.pos_matrix)
                    pygame.time.delay(speed_time)
                    self.objmap.show_cell(self.screen, dir.pos_matrix[0], dir.pos_matrix[1], False)

                    if dir.checkWumpus():
                        self.Action(s_action_kill, dir.get_Room())
                        dir.kill_Wumpus(self.map, self.KB)

                        clause = [dir.get_Literal(s_entities_pit, '-')]
                        print("add KB no PIT here", clause)
                        self.add_clause_KB(clause)

                        # self.write_output(str(self.KB.KB))

                    # Killed
                    if self.agent_cell.checkStench() == False:  # there are no Wumpus arround because Stench is gone
                        self.agent_cell.set_nextCell([dir])
                        if dir in dangerCell:
                            dangerCell.remove(dir)
                        break

            if self.agent_cell.checkBreeze():
                for adj in adjCell:
                    # Infer
                    self.Action(s_action_infer_pit, adj.get_Room())
                    type = 1
                    ispit = self.KB.inference(adj, self, type)
                    # neg_alpha = [adj.get_Literal(s_entities_pit, '-')]
                    # ispit = self.KB.inference(neg_alpha)

                    # Pit inferencable: there is pit in adj
                    if ispit:
                        self.Action(s_action_de_pit, adj.get_Room())

                        adj.setexploredCell()
                        clause = [adj.get_Literal(s_entities_pit, '+')]
                        self.add_clause_KB(clause)
                        self.objmap.show_cell(self.screen, adj.pos_matrix[0], adj.pos_matrix[1], True)
                        adj.set_previousCell(adj)
                        dangerCell.append(adj)

                    # Pit uninferencable: cant infer pit
                    else:
                        # check if agent can inference no Pit
                        self.Action(s_action_infer_npit)
                        type = 2
                        isnotpit = self.KB.inference(adj, self, type)

                        # Not Pit inferencable: there is no pit
                        if isnotpit:
                            self.Action(s_action_de_npit, adj.get_Room())

                            clause = [adj.get_Literal(s_entities_pit, '-')]
                            self.add_clause_KB(clause)

                        # No Pit uninferencable / Pit uninferencable: add :>
                        else:
                            dangerCell.append(adj)

        # Remove all danger cell in next_cell_list -> safe next_cell_list
        dangerCell = list(set(dangerCell))
        for danger in dangerCell:
            if danger in adjCell:
                adjCell.remove(danger)
        self.agent_cell.set_nextCell(adjCell)

        saved_agent_pos = self.agent_cell.pos_matrix

        if len(self.agent_cell.next_list) == 0:
            temp_T = True
            for cell in self.agent_cell.next_list:
                if not (self.cell_check_explored(cell)):
                    temp_T = False

            if temp_T:
                temp = []
                for cell_nam in adjCell_list:
                    if cell_nam.pos_matrix == previousCell_list[-1]:
                        continue
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
                    if count_nam == 0:
                        break
                    pos = previousCell_list[index_nam]
                    temp_cell = self.map[pos[0]][pos[1]]
                    temp_cell_adjs = temp_cell.get_adjCells(self.map)
                    #
                    exploredCell = []
                    for temp_cell_check in temp_cell_adjs:
                        # if temp_cell_check.checkExplored():
                        if self.cell_check_explored(temp_cell_check):
                            exploredCell.append(temp_cell_check)
                    for temp_cell_check in exploredCell:
                        if temp_cell_check in temp_cell_adjs:
                            temp_cell_adjs.remove(temp_cell_check)
                    if len(temp_cell_adjs) > 0:
                        break
                    index_nam -= 1
                pygame.time.delay(speed_time)

                if len(previousCell_list) == 0:
                    return

                self.move_to(adjCell_list[index_previous])
                while (previousCell_list[-1] != adjCell_list[index_previous].pos_matrix):
                    previousCell_list.remove(previousCell_list[-1])
                previousCell_list.remove(previousCell_list[-1])
                # self.write_output('Backtrack: ' + str(previousCell.pos_matrix))

        else:
            for cell in self.agent_cell.next_list:
                # if cell.checkExplored():
                if self.cell_check_explored(cell):
                    continue

                self.game.stageGame_action()
                previousCell_list.append(previousCell.pos_matrix)
                pygame.time.delay(speed_time)
                self.move_to(cell)
                # self.write_output('Move to: ' + str(self.agent_cell.pos_matrix))

                if not self.backtrackSearch_BW():
                    return False

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
                        if count_nam == 0:
                            break

                        pos = previousCell_list[index_nam]
                        temp_cell = self.map[pos[0]][pos[1]]
                        temp_cell_adjs = temp_cell.get_adjCells(self.map)
                        ####
                        exploredCell = []
                        for temp_cell_check in temp_cell_adjs:
                            if self.cell_check_explored(temp_cell_check):
                                exploredCell.append(temp_cell_check)
                        for temp_cell_check in exploredCell:
                            if temp_cell_check in temp_cell_adjs:
                                temp_cell_adjs.remove(temp_cell_check)
                        if len(temp_cell_adjs) > 0:
                            break
                        index_nam -= 1

                    pygame.time.delay(100)

                    if len(previousCell_list) == 0:
                        return

                    self.move_to(adjCell_list[index_previous])

                    while (previousCell_list[-1] != adjCell_list[index_previous].pos_matrix):
                        previousCell_list.remove(previousCell_list[-1])
                    previousCell_list.remove(previousCell_list[-1])
        return True

    #BACTRACK-SEARCH RE -----------------------------------------------------------------------------------------------|
    #Add to Knowledge Base
    def add_to_KB_RE(self, cell):
        adjCell = cell.get_adjCells(self.map)
        #Pit
        if cell.checkPit():
            self.KB.addP([cell.get_Literal(s_entities_pit, '+')])
            self.KB.addW([cell.get_Literal(s_entities_wum, '-')])
        #Wumpus (if Pit in this cell, there is no Wum)
        elif cell.checkWumpus():
            self.KB.addW([cell.get_Literal(s_entities_wum, '+')])
            self.KB.addP([cell.get_Literal(s_entities_pit, '-')])
        #No Wumpus and No Pit
        elif not cell.checkPit() and not cell.checkWumpus():
            self.KB.addW([cell.get_Literal(s_entities_wum, '-')])
            self.KB.addP([cell.get_Literal(s_entities_pit, '-')])
        #Breeze ------------------------------------------------------------|
        if cell.checkBreeze():
            self.KB.addP([cell.get_Literal(s_entities_bre, '+')])
            #B => Pa v Pb v Pc v Pd
            clause  = []
            for adj in adjCell:
                clause.append(adj.get_Literal(s_entities_pit, '+'))
            self.KB.addP(clause)
        #no Breeze
        elif not cell.checkBreeze():
            self.KB.addP([cell.get_Literal(s_entities_bre, '-')])
            #-B => -Pa ^ -Pb ^ -Pc ^ -Pd
            for adj in adjCell:
                clause = [adj.get_Literal(s_entities_pit, '-')]
                self.KB.addP(clause)
        #Stench -------------------------------------------------------------|
        if cell.checkStench():
            self.KB.addW([cell.get_Literal(s_entities_ste, '+')])
            # S => Wa v Wb v Wc v Wd
            clause  = []
            for adj in adjCell:
                clause.append(adj.get_Literal(s_entities_wum, '+'))
            self.KB.addW(clause)
        #no Stench
        elif not cell.checkStench():
            self.KB.addW([cell.get_Literal(s_entities_ste, '-')])
            #-S => -Wa ^ -Wb ^ -Wc ^ -Wd
            for adj in adjCell:
                clause = [adj.get_Literal(s_entities_wum, '-')]
                self.KB.addW(clause)

        #Print out
        self.print_output('Knowledge base with matrix coordinate:')
        self.print_output(self.KB.KB_P)
        self.print_output(self.KB.KB_W)
        self.write_output('Knowledge base with matrix coordinate:')
        self.write_output(self.KB.KB_P)
        self.write_output(self.KB.KB_W)

    #Backtrack Search
    def backtrackSearch_RE(self):
        # Check condition ---------------------------------------------------|
        if self.agent_cell.checkWumpus():
            self.Action(s_action_eaten)
            self.stopgame = True
            return False  # eaten by Wumpus

        if self.agent_cell.checkPit():
            self.Action(s_action_fall)
            self.stopgame = True
            return False  # fall into Pit

        if self.agent_cell.checkGold():
            self.agent_cell.take_Gold()
            self.Action(s_action_grab)

        if self.agent_cell.checkBreeze():
            self.Action(s_action_breeze, self.agent_cell.get_Room())

        if self.agent_cell.checkStench():
            self.Action(s_action_stench, self.agent_cell.get_Room())

        if (not self.cell_check_explored(self.agent_cell)) or (self.agent_cell == self.agent_init):
            self.agent_cell.setexploredCell()
            self.add_to_KB_RE(self.agent_cell)

        # Create adj cell list to find safe next_cell_list
        adjCell = self.agent_cell.get_adjCells(self.map)
        adjCell_list = copy.deepcopy(adjCell)

        # Remove previous cell in adjCell
        if self.agent_cell.previous in adjCell:
            adjCell.remove(self.agent_cell.previous)

        # Remove explored cell in adjCell
        exploredCell = []
        for cell in adjCell:
            if self.cell_check_explored(cell):
                exploredCell.append(cell)
        for cell in exploredCell:
            if cell in adjCell:
                adjCell.remove(cell)

        previousCell = self.agent_cell

        dangerCell = []  # To store dangerous cell can infer from this cell?
        # current cell contain Stench, Breeze -> inference from KB to make decision
        if not self.agent_cell.isSafe():
            # Inference PIT if current cell contain Breeze
            if self.agent_cell.checkBreeze():
                for adj in adjCell:
                    #Infer
                    self.Action(s_action_infer_pit, adj.get_Room())
                    neg_alpha = [adj.get_Literal(s_entities_pit, '-')]
                    ispit = self.KB.inferenceP(neg_alpha)

                    #Pit: there is pit in adj
                    if ispit:
                        self.Action(s_action_de_pit, adj.get_Room())

                        adj.setexploredCell()
                        self.KB.addP([adj.get_Literal(s_entities_pit, '+')])
                        self.KB.addW([adj.get_Literal(s_entities_wum, '-')])

                        self.objmap.show_cell(self.screen, adj.pos_matrix[0], adj.pos_matrix[1], True)
                        adj.set_previousCell(adj)
                        dangerCell.append(adj)

                    #Pit: cant infer pit
                    else:
                        # check if agent can inference no Pit
                        self.Action(s_action_infer_npit, adj.get_Room())

                        neg_alpha = [adj.get_Literal(s_entities_pit, '+')]
                        isnotpit  = self.KB.inferenceP(neg_alpha)

                        #Not Pit inferencable: there is no pit
                        if isnotpit:
                            self.Action(s_action_de_npit, adj.get_Room())
                            self.KB.addP([adj.get_Literal(s_entities_pit, '-')])

                        #Can't know: No Pit / Pit
                        else:
                            dangerCell.append(adj)

            #Inference WUMPUS if current cell contain Stench
            if self.agent_cell.checkStench():
                for adj in adjCell:
                    #Infer
                    self.Action(s_action_infer_wumpus, adj.get_Room())
                    neg_alpha = [adj.get_Literal(s_entities_wum, '-')]
                    iswum = self.KB.inferenceW(neg_alpha)

                    #Wumpus: there is wumpus -> kill -> safe
                    if iswum:
                        self.Action(s_action_de_wumpus, adj.get_Room())

                        #self.KB.addP([adj.get_Literal(s_entities_pit, '-')])

                        # Kill Wumpus
                        self.turn_to(adj)
                        self.Action(s_action_shoot, adj.get_Room())
                        # Shoot graphic
                        self.agent.shoot(self.screen, adj.pos_matrix)
                        pygame.time.delay(500)
                        self.objmap.show_cell(self.screen, adj.pos_matrix[0], adj.pos_matrix[1], False)
                        self.Action(s_action_kill, adj.get_Room())
                        adj.kill_Wumpus_Re(self.map, self.KB)

                    #Wumpus: can't infer wumpus
                    else:
                        #check if agent can inference no Wumpus
                        self.Action(s_action_infer_nwumpus, adj.get_Room())
                        neg_alpha = [adj.get_Literal(s_entities_wum, '+')]
                        isnotwum = self.KB.inferenceW(neg_alpha)

                        # no Wumpus: there is no wumpus
                        if isnotwum:
                            self.Action(s_action_de_nwumpus, adj.get_Room())
                            self.KB.addP([adj.get_Literal(s_entities_wum, '-')])

                        # Can't know: no Wumpus/Wumpus
                        else:
                            dangerCell.append(adj)

            # Still cant not inference Wumpus/Not Wumpus -> bắn đại
            if self.agent_cell.checkStench():
                direction = self.agent_cell.get_adjCells(self.map)

                # delete previous cell (wumpus cant be there)
                if self.agent_cell.previous in direction:
                    direction.remove(self.agent_cell.previous)

                # delete previous explored cell (if wumpus there, agent would have known :v)
                explored = []
                for cell in direction:
                    if self.cell_check_explored(cell):
                        explored.append(cell)
                for cell in explored:
                    direction.remove(cell)

                # Try shooting
                for dir in direction:
                    self.turn_to(dir)

                    self.Action(s_action_shoot, dir.get_Room())

                    # Shoot graphic
                    self.agent.shoot(self.screen, dir.pos_matrix)
                    pygame.time.delay(speed_time)
                    self.objmap.show_cell(self.screen, dir.pos_matrix[0], dir.pos_matrix[1], False)

                    if dir.checkWumpus():
                        self.Action(s_action_kill, dir.get_Room())
                        dir.kill_Wumpus_Re(self.map, self.KB)

                    # Killed
                    if self.agent_cell.checkStench() == False:  # there are no Wumpus arround because Stench is gone
                        self.agent_cell.set_nextCell([dir])
                        if dir in dangerCell:
                            dangerCell.remove(dir)
                        break

        # Remove all danger cell in next_cell_list -> safe next_cell_list
        dangerCell = list(set(dangerCell))
        for danger in dangerCell:
            if danger in adjCell:
                adjCell.remove(danger)
        self.agent_cell.set_nextCell(adjCell)

        saved_agent_pos = self.agent_cell.pos_matrix

        if len(self.agent_cell.next_list) == 0:
            temp_T = True
            for cell in self.agent_cell.next_list:
                if not (self.cell_check_explored(cell)):
                    temp_T = False

            if temp_T:
                temp = []
                for cell_nam in adjCell_list:
                    if cell_nam.pos_matrix == previousCell_list[-1]:
                        continue
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
                    if count_nam == 0:
                        break
                    pos = previousCell_list[index_nam]
                    temp_cell = self.map[pos[0]][pos[1]]
                    temp_cell_adjs = temp_cell.get_adjCells(self.map)
                    #
                    exploredCell = []
                    for temp_cell_check in temp_cell_adjs:
                        if self.cell_check_explored(temp_cell_check):
                            exploredCell.append(temp_cell_check)
                    for temp_cell_check in exploredCell:
                        if temp_cell_check in temp_cell_adjs:
                            temp_cell_adjs.remove(temp_cell_check)
                    if len(temp_cell_adjs) > 0:
                        break
                    index_nam -= 1
                pygame.time.delay(speed_time)

                if len(previousCell_list) == 0:
                    return

                self.move_to(adjCell_list[index_previous])
                if self.stopgame == True: return
                while (previousCell_list[-1] != adjCell_list[index_previous].pos_matrix):
                    previousCell_list.remove(previousCell_list[-1])
                previousCell_list.remove(previousCell_list[-1])
                # self.write_output('Backtrack: ' + str(previousCell.pos_matrix))
        else:
            for cell in self.agent_cell.next_list:
                if self.cell_check_explored(cell):
                    continue

                if self.stopgame == True: return
                previousCell_list.append(previousCell.pos_matrix)
                pygame.time.delay(speed_time)
                self.move_to(cell)

                if not self.backtrackSearch_RE():
                    return False
                if self.stopgame == True: return

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
                        if count_nam == 0:
                            break

                        pos = previousCell_list[index_nam]
                        temp_cell = self.map[pos[0]][pos[1]]
                        temp_cell_adjs = temp_cell.get_adjCells(self.map)
                        ####
                        exploredCell = []
                        for temp_cell_check in temp_cell_adjs:
                            if self.cell_check_explored(temp_cell_check):
                                exploredCell.append(temp_cell_check)
                        for temp_cell_check in exploredCell:
                            if temp_cell_check in temp_cell_adjs:
                                temp_cell_adjs.remove(temp_cell_check)
                        if len(temp_cell_adjs) > 0:
                            break
                        index_nam -= 1

                    pygame.time.delay(100)

                    if len(previousCell_list) == 0:
                        return

                    self.move_to(adjCell_list[index_previous])
                    if self.stopgame == True: return
                    while (previousCell_list[-1] != adjCell_list[index_previous].pos_matrix):
                        previousCell_list.remove(previousCell_list[-1])
                    previousCell_list.remove(previousCell_list[-1])
        return True

    #Solving map ------------------------------------------------------------------------------------------------------|
    def solving_BW(self):

        self.backtrackSearch_BW()
        self.Action(s_action_climb)
        print('END')

        return self.score

    def solving_RE(self):

        self.backtrackSearch_RE()
        self.Action(s_action_climb)
        print('END')

        return self.score

