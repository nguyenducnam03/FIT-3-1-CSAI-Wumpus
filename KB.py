import itertools
import copy
import re
import cell as Cell
from constant import *

def extract_number(s):
    number = re.search(r'\d+', s)
    if number:
        return int(number.group())
    else:
        return None

class KnowledgeBase:
    # Constructor.
    def __init__(self):
        self.KB = []
        self.alpha = []
        self.new_clauses_list = []
        self.solution = False

    #Return a standardized clause:
    @staticmethod
    def standard_clause(clause: list):
        return sorted(list(set(copy.deepcopy(clause))), key=lambda x: x[-3])

    def add(self, clause):
        clause = self.standard_clause(clause)
        if clause not in self.KB:  # and not self.checkComplementary(clause):
            self.KB.append(clause)

    def rem(self, clause):
        clause = self.standard_clause(clause)
        if clause in self.KB:
            self.KB.remove(clause)

    #Get Negative of literal
    @staticmethod
    def getNegative(literal: str):
        if literal[0] == '-':
            return literal[1:]
        return '-' + literal

    #Check if 2 literals are complementary (etc: P11 vs -P11)
    @staticmethod
    def is_complentary_literals(literal_1: str, literal_2: str):
        return len(literal_1) != len(literal_2) and literal_1[-3:] == literal_2[-3:]

    # # Check if a clause is empty.
    # @staticmethod
    # def is_empty_clause(clause: list):
    #     return len(clause) == 0

    # Check if a clause is valid (always True).
    def is_valid_clause(self, clause):
        for i in range(len(clause) - 1):
            if self.is_complentary_literals(clause[i], clause[i + 1]):
                return True
        return False

    # Resolve 2 clauses then return a list of resolvents (list of clauses).
    def resolve(self, clause_1: list, clause_2: list):
        resolvents = []
        for i in range(len(clause_1)):
            for j in range(len(clause_2)):
                if self.is_complentary_literals(clause_1[i], clause_2[j]):
                    resolvent = clause_1[:i] + clause_1[i + 1:] + clause_2[:j] + clause_2[j + 1:]
                    resolvents.append(self.standard_clause(resolvent))
        return resolvents

    #PL Resolution
    def inference(self, cell_pos ,self_logic, type):
        clause_list = copy.deepcopy(self.KB)
        #Inference
        if type==1: #isPIT
            neg_alpha = [cell_pos.get_Literal(s_entities_pit, '-')]
        elif type==2:#isNotPit
            neg_alpha = [cell_pos.get_Literal(s_entities_pit, '+')]
        elif type==3:#isWumpus
            neg_alpha = [cell_pos.get_Literal(s_entities_wum, '-')]
        elif type==4:#isNotWumpus
            neg_alpha = [cell_pos.get_Literal(s_entities_wum, '+')]

        
        if neg_alpha in clause_list:
            return False

        #Inference
        adj_cell = cell_pos.get_adjCells(self_logic.map)
        if type==1: #isPIT
            T = True
            for adj in adj_cell:
                temp = [adj.get_Literal(s_entities_bre, '+')]
                if temp not in clause_list:
                    T = False
                else:
                    T2 = True
                    sub_adj_cell = adj.get_adjCells(self_logic.map)
                    sub_adj_cell.remove(cell_pos)
                    for sub_adj in sub_adj_cell:
                        temp = [sub_adj.get_Literal(s_entities_pit, '-')]
                        if temp not in clause_list:
                            T2 = False
                    if T2==True:
                        T = True
                        break            
            return T
        elif type==2:#isNotPit
            T = True
            for adj in adj_cell:
                temp = [adj.get_Literal(s_entities_bre, '-')]
                if temp not in clause_list:
                    T = False
                    return T
            return T
        elif type==3:#isWumpus
            T = True
            for adj in adj_cell:
                temp = [adj.get_Literal(s_entities_ste, '+')]
                if temp not in clause_list:
                    T = False
                else:
                    T2 = True
                    sub_adj_cell = adj.get_adjCells(self_logic.map)
                    sub_adj_cell.remove(cell_pos)
                    for sub_adj in sub_adj_cell:
                        temp = [sub_adj.get_Literal(s_entities_wum, '-')]
                        if temp not in clause_list:
                            T2 = False
                    if T2==True:
                        T = True
                        break            
            return T
        elif type==4:#isNotWumpus
            T = True
            for adj in adj_cell:
                temp = [adj.get_Literal(s_entities_ste, '-')]
                if temp not in clause_list:
                    T = False
                    return T
            return T