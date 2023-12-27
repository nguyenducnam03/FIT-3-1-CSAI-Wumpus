import itertools
import copy

import re
def extract_number(s):
    number = re.search(r'\d+', s)
    if number:
        return int(number.group())
    else:
        return None

# class KnowledgeBase2:
    def __init__(self):
        self.KB = []

    @staticmethod  # phương thức tĩnh, thuộc về lớp chứ không phải thể hiện của lớp
    def standardize_clause(clause):
        return sorted(list(set(clause)))

    #Add / Remove clause to KB -----------------------------------------------------------------------------------------
    def add(self, clause):
        clause = self.standardize_clause(clause)
        if clause not in self.KB: #and not self.checkComplementary(clause):
            self.KB.append(clause)

    # def remove(self, clause):
    #     clause = self.standardize_clause(clause)
    #     if clause in self.KB:
    #         self.KB.remove(clause)

    #Get Negative Form of literal --------------------------------------------------------------------------------------
    @staticmethod
    def getNegative(literal):
        if literal[0] == '-':
            return literal[1:]
        else:
            return '-' + literal

    def check_True(self, clause, list_clauses):
        for c in list_clauses:
            if set(c).issubset(set(clause)):
                return True
        return False

    #Remove always True clause -----------------------------------------------------------------------------------------
    def remove_eval(self, clauses):
        res = []
        for c in clauses:
            if not self.check_True(c, res):
                res.append(c)
        return res

    #Check (a v -a) in  clause ----------------------------------------------------------------------------------------|
    def checkComplementary(self, clause):
        for literal in clause:
            if self.getNegative(literal) in clause:
                return True
        return False

    #Remove duplicate literals (in 1 clause) and sort them lexicographically ------------------------------------------|
    def normClause(self, clause):
        # Remove duplicates
        clause = list(dict.fromkeys(clause))

        # Sort by alphabet
        tuple_form = []
        for literal in clause:
            if literal[0] == '-':
                tuple_form.append((literal[1:], -1))
            else:
                tuple_form.append((literal[0:], 1))
        tuple_form.sort()

        # Rebuild clause
        res = []
        for tup in tuple_form:
            if tup[1] == -1:
                res.append('-' + tup[0])
            else:
                res.append(tup[0])
        return res

    #Implementation of Resolution Inference Rule -----------------------------------------------------------------------
    """
    Caluclating resolvents step in programs delete two opposite facts:
    a (in sentence 1) & -a (in sentence 2) -> empty
    """
    def resolve(self, clause_i, clause_j):
        new_clause = []
        for literal in clause_i:
            neg_literal = self.getNegative(literal)
            if neg_literal in clause_j:
                temp_c_i = clause_i.copy()
                temp_c_j = clause_j.copy()
                print('temp_c_i', temp_c_i, 'temp_c_j', temp_c_j)
                temp_c_i.remove(literal)
                temp_c_j.remove(neg_literal)
                print('temp_c_i', temp_c_i, 'temp_c_j', temp_c_j)
                print('----------------------------------------')
                #if (not temp_c_i) and (not temp_c_j):
                if len(temp_c_i) == 0 and len(temp_c_j) == 0:
                    new_clause.append(['{}'])
                else:
                    clause = temp_c_i + temp_c_j
                    if clause not in self.KB:
                        new_clause.append(clause)
        return new_clause

    #PL resolution
    def inference(self, neg_alpha):
        tempKB = KnowledgeBase()
        tempKB.KB = self.KB.copy()

        # neg_alpha = [item for sublist in neg_alpha for item in sublist]
        print('Negative alpha: ', neg_alpha)
        tempKB.add(neg_alpha)

        result = []
        while True:
            clause_pairs = list(itertools.combinations(range(len(tempKB.KB)), 2))
            resolvents = []
            for pair in clause_pairs:
                resolvent = tempKB.resolve(tempKB.KB[pair[0]], tempKB.KB[pair[1]])
                if resolvent and resolvent not in resolvents:
                    resolvents.append(resolvent)

            #resolvents = list(itertools.chain.from_iterable(resolvents))
            print('resolvents:', resolvents, 'len:', len(resolvents))
            result.append(resolvents)

            if not resolvents:
                return False
            else:
                if ['{}'] in resolvents:
                    return True
                else:
                    for res in resolvents:
                        tempKB.add(res)

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
    def inference(self, neg_alpha):
        clause_list = copy.deepcopy(self.KB)
        temp_num = extract_number(neg_alpha[0])
        # clause_list = KnowledgeBase()
        for KB in self.KB:
            for kb in KB:
                number_part = extract_number(kb)
                if abs(number_part-temp_num) not in [1,10,9,11,2,20,18,22,21,19,8,12]:
                # if abs(number_part-temp_num) not in [1,10,9,11]:
                    clause_list.remove(KB)
                    break

        if neg_alpha not in clause_list:
            clause_list.append(neg_alpha)

        while True:
            self.new_clauses_list.append([])

            for i in range(len(clause_list)):
                for j in range(i + 1, len(clause_list)):
                    resolvents = self.resolve(clause_list[i], clause_list[j])
                    if [] in resolvents:
                        self.new_clauses_list[-1].append([])
                        return True

                    for resolvent in resolvents:
                        if self.is_valid_clause(resolvent):
                            break
                        if resolvent not in clause_list and resolvent not in self.new_clauses_list[-1]:
                            self.new_clauses_list[-1].append(resolvent)

            if len(self.new_clauses_list[-1]) == 0:
                return False

            clause_list += self.new_clauses_list[-1]