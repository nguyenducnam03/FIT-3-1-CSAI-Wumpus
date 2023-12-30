import copy
import itertools
import cell as Cell
from constant import *

class KnowledgeBase:
    def __init__(self):
        self.KB = []
        self.KB_W = []
        self.KB_P = []

    #Return a standardized clause:
    @staticmethod
    def standard_clause(clause: list):
        return sorted(list(set(copy.deepcopy(clause))), key=lambda x: x[-3:])

    # Pl_Forward =======================================================================================================

    # ADD to KB
    def addP(self, clause):
        clause = self.standard_clause(clause)
        if clause not in self.KB_P and not self.is_valid_clause(clause):
            self.KB_P.append(clause)

    # ADD to KB
    def addW(self, clause):
        clause = self.standard_clause(clause)
        if clause not in self.KB_W:  # and not self.checkComplementary(clause):
            self.KB_W.append(clause)

    # REMOVE from KB
    def remW(self, clause):
        clause = self.standard_clause(clause)
        if clause in self.KB_W:
            self.KB_W.remove(clause)

    #Get Negative of literal
    @staticmethod
    def getNegative(literal: str):
        if literal[0] == '-':
            return literal[1:]
        return '-' + literal

    # Check if 2 literals are complementary (etc: P11 vs -P11)
    def is_complementary_literals(self, literal_1, literal_2):
        return len(literal_1) != len(literal_2) and literal_1[-3:] == literal_2[-3:]

    # Check if a clause is valid (always True).
    def is_valid_clause(self, clause):
        for i in range(len(clause) - 1):
            if self.is_complementary_literals(clause[i], clause[i + 1]):
                return True
        return False

    def resolve(self, clause_1: list, clause_2: list):
        resolvents = []
        for literal_1 in clause_1:
            neg_literal_1 = self.getNegative(literal_1)
            if neg_literal_1 in clause_2:
                resolvent = clause_1 + clause_2
                resolvent.remove(literal_1)
                resolvent.remove(neg_literal_1)
                if not resolvent:
                    resolvents.append([])
                elif not any([self.getNegative(literal) in resolvent for literal in resolvent]):
                    resolvents.append(self.standard_clause(resolvent))
        return resolvents

    #PL Resolution
    def inferenceP(self, neg_alpha):
        clause_list = copy.deepcopy(self.KB_P)

        if neg_alpha not in clause_list:
            clause_list.append(neg_alpha)

        while True:
            new_clauses = []

            for (clause_i, clause_j) in itertools.combinations(clause_list, 2):
                resolvents = self.resolve(clause_i, clause_j)
                if [] in resolvents:
                    new_clauses.append([])
                    return True

                for resolvent in resolvents:
                    if self.is_valid_clause(resolvent):
                        break
                    if resolvent not in clause_list and resolvent not in new_clauses:
                        new_clauses.append(resolvent)

            if not new_clauses:
                return False
            clause_list += new_clauses

    def inferenceW(self, neg_alpha):
        clause_list = copy.deepcopy(self.KB_W)

        if neg_alpha not in clause_list:
            clause_list.append(neg_alpha)

        while True:
            new_clauses = []

            for (clause_i, clause_j) in itertools.combinations(clause_list, 2):
                resolvents = self.resolve(clause_i, clause_j)
                if [] in resolvents:
                    new_clauses.append([])
                    print('====TRUE====')
                    return True

                for resolvent in resolvents:
                    if self.is_valid_clause(resolvent):
                        break
                    if resolvent not in clause_list and resolvent not in new_clauses:
                        new_clauses.append(resolvent)

            if not new_clauses:
                print('====FAlSE====')
                return False
            clause_list += new_clauses

    #PL_Backward =======================================================================================================
    def add(self, clause):
        clause = self.standard_clause(clause)
        if clause not in self.KB:
            self.KB.append(clause)

    def rem(self, clause):
        clause = self.standard_clause(clause)
        if clause in self.KB:
            self.KB.remove(clause)

    def inference(self, cell_pos, self_logic, type):
        clause_list = copy.deepcopy(self.KB)
        # Inference
        if type == 1:  # isPIT
            neg_alpha = [cell_pos.get_Literal(s_entities_pit, '-')]
            pos_alpha = [cell_pos.get_Literal(s_entities_pit, '+')]
        elif type == 2:  # isNotPit
            neg_alpha = [cell_pos.get_Literal(s_entities_pit, '+')]
            pos_alpha = [cell_pos.get_Literal(s_entities_pit, '-')]
        elif type == 3:  # isWumpus
            neg_alpha = [cell_pos.get_Literal(s_entities_wum, '-')]
            pos_alpha = [cell_pos.get_Literal(s_entities_wum, '+')]
        elif type == 4:  # isNotWumpus
            neg_alpha = [cell_pos.get_Literal(s_entities_wum, '+')]
            pos_alpha = [cell_pos.get_Literal(s_entities_wum, '-')]

        if neg_alpha in clause_list:
            return False
        if pos_alpha in clause_list:
            return True
        # Inference
        adj_cell = cell_pos.get_adjCells(self_logic.map)
        if type == 1:  # isPIT
            T = True  # P10 <---- B9 B11 B20 B0
            for adj in adj_cell:
                temp = [adj.get_Literal(s_entities_bre, '+')]
                if temp not in clause_list:
                    T = False
                else:  # adj is breeze
                    # B9 ^ 3 thang xung quanh B9 ko la pit --> P10
                    T2 = True
                    sub_adj_cell = adj.get_adjCells(self_logic.map)
                    sub_adj_cell.remove(cell_pos)
                    for sub_adj in sub_adj_cell:
                        temp = [sub_adj.get_Literal(s_entities_pit, '-')]
                        if temp not in clause_list:
                            T2 = False
                    if T2 == True:
                        T = True
                        break
            return T
        elif type == 2:  # isNotPit
            T = True
            for adj in adj_cell:
                temp = [adj.get_Literal(s_entities_bre, '-')]
                if temp not in clause_list:
                    T = False
                    return T
            return T
        elif type == 3:  # isWumpus
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
                    if T2 == True:
                        T = True
                        break
            return T
        elif type == 4:  # isNotWumpus
            T = True
            for adj in adj_cell:
                temp = [adj.get_Literal(s_entities_ste, '-')]
                if temp not in clause_list:
                    T = False
                    return T
            return T