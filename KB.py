import copy
import itertools

class KnowledgeBase:
    def __init__(self):
        self.KB = []


    def add(self, clause):
        if clause not in self.KB and not self.checkComplementary(clause):
            self.KB.append(clause)

    def getNegative_atom(self, atom):
        print('atom = ', atom)
        if atom[0] == '-':
            return atom[1:]
        else:
            return '-' + atom

    def check_True(self, clause, list_clauses):
        for c in list_clauses:
            if set(c).issubset(set(clause)):
                return True
        return False

    def rem(self, clauses):
        res = []
        for c in clauses:
            if not self.check_True(c, res):
                res.append(c)
        return res

    def toCNF(self, clauses):
        res = []
        product_all = list(itertools.product(*clauses))
        for i in product_all:
            new = self.normClause(list(itertools.chain.from_iterable(list(i))))
            if not self.checkComplementary(new) and new not in res:
                res.append(new)
        res.sort(key=len)
        res = self.rem(res)
        return res

    def checkComplementary(self, clause):
        for atom in clause:
            if self.getNegative_atom(atom) in clause:
                return True
        return False

    def standard_clause(self, clause):
        # clause = [str(atom) for atom in clause]

        clause = list(dict.fromkeys(clause))

        tuple_form = []
        for atom in clause:
            if atom[0] == '-':
                tuple_form.append((atom[1:], -1))
            else:
                tuple_form.append((atom, 1))
        tuple_form.sort()

        res = []
        for tup in tuple_form:
            if tup[1] == -1:
                res.append('-' + tup[0])
            else:
                res.append(tup[0])
        return res

    # Thêm một mệnh đề vào cơ sở tri thức
    def add(self, clause):
        if clause not in self.KB and not self.checkComplementary(clause):
            self.KB.append(clause)

    # Giải quyết một cặp mệnh đề
    def resolve(self, clause_i, clause_j):
        new_clause = []
        for atom in clause_i:
            neg_atom = self.getNegative_atom(atom)
            if neg_atom in clause_j:
                temp_c_i = clause_i.copy()
                temp_c_j = clause_j.copy()
                temp_c_i.remove(atom)
                temp_c_j.remove(neg_atom)
                if not temp_c_i and not temp_c_j:
                    new_clause.append(['{}'])
                else:
                    clause = temp_c_i + temp_c_j
                    clause = self.standard_clause(clause)
                    if not self.checkComplementary(clause) and clause not in self.KB:
                        new_clause.append(clause)
        return new_clause

    # Giải quyết truy vấn
    def solve(self, neg_query):
        tempKB = KnowledgeBase()
        tempKB.KB = self.KB.copy()

        # neg_query = self.getNegative_query(query)
        # print(neg_query)

        for neg_atom in neg_query:
            tempKB.add(neg_atom)

        result = []
        while True:
            clause_pairs = list(itertools.combinations(range(len(tempKB.KB)), 2))

            resolvents = []
            for pair in clause_pairs:
                resolvent = tempKB.resolve(tempKB.KB[pair[0]], tempKB.KB[pair[1]])
                if resolvent and resolvent not in resolvents:
                    resolvents.append(resolvent)

            resolvents = list(itertools.chain.from_iterable(resolvents))
            result.append(resolvents)

            if not resolvents:
                return result, True
            else:
                if ['{}'] in resolvents:
                    return result, False
                else:
                    for res in resolvents:
                        tempKB.add(res)

    def inference(self, not_alpha):
        tempKB = KnowledgeBase()
        KB_list = tempKB.KB.copy()
        negative_alpha = not_alpha
        for i in KB_list:
            tempKB.add(i)
        for i in negative_alpha:
            tempKB.add(i)
        result, is_entailed = tempKB.solve(not_alpha)

        return not is_entailed