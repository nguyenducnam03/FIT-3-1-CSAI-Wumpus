import itertools
import copy

class KnowledgeBase:
    def __init__(self):
        self.KB = []

    # Xóa một mệnh đề khỏi cơ sở tri thức
    def rem(self, clause):
        clause = self.standard_clause(clause)
        if clause in self.KB:
            self.KB.remove(clause)

    # Lấy bản phủ của một nguyên tử âm
    # def getNegative_atom(self, atom):
    #     atom_str = str(atom)
    #     if atom_str[0] == '-':
    #         return atom_str[1:]
    #     else:
    #         return '-' + atom_str
    def getNegative_atom(self, atom):
        atom_str = str(atom)
        if atom_str and atom_str[0] == '-':
            return atom_str[1:]
        else:
            return '-' + atom_str


    # Lấy bản phủ của một truy vấn âm
    def getNegative(self, query):
        res = []
        for clause in query:
            new = []
            for atom in clause:
                new.append([self.getNegative_atom(atom)])
            res.append(new)

        if len(res) == 1:
            return list(itertools.chain.from_iterable(res))
        else:
            return self.toCNF(res)

    # Kiểm tra xem một mệnh đề có đúng hay không trong danh sách các mệnh đề
    def check_True(self, clause, list_clauses):
        for c in list_clauses:
            if set(c).issubset(set(clause)):
                return True
        return False

    # Loại bỏ các mệnh đề đánh giá đúng từ danh sách các mệnh đề
    def remove_eval(self, clauses):
        res = []
        for c in clauses:
            if not self.check_True(c, res):
                res.append(c)
        return res

    # Chuyển đổi mệnh đề sang dạng chuẩn hóa
    def toCNF(self, clauses):
        res = []
        product_all = list(itertools.product(*clauses))
        for i in product_all:
            new = self.normClause(list(itertools.chain.from_iterable(list(i))))
            if not self.checkComplementary(new) and new not in res:
                res.append(new)
        res.sort(key=len)
        res = self.remove_eval(res)
        return res

    # Kiểm tra xem một mệnh đề có chứa bổ sung không
    def checkComplementary(self, clause):
        for atom in clause:
            if self.getNegative_atom(atom) in clause:
                return True
        return False

    # Chuẩn hóa mệnh đề
    def standard_clause(self, clause):
        # Chuyển đổi nguyên tử thành chuỗi
        clause = [str(atom) for atom in clause]

        # Loại bỏ các bản sao
        clause = list(dict.fromkeys(clause))

        # Sắp xếp theo thứ tự chữ cái
        tuple_form = []
        for atom in clause:
            if atom[0] == '-':
                tuple_form.append((atom[1:], -1))
            else:
                tuple_form.append((atom, 1))
        tuple_form.sort()

        # Xây dựng lại mệnh đề
        res = []
        for tup in tuple_form:
            if tup[1] == -1:
                res.append('-' + tup[0])
            else:
                res.append(tup[0])
        return res

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
    def solve(self, query):
        tempKB = KnowledgeBase()
        tempKB.KB = self.KB.copy()

        neg_query = self.getNegative(query)
        print(neg_query)
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
                return result, False
            else:
                if ['{}'] in resolvents:
                    return result, True
                else:
                    for res in resolvents:
                        tempKB.add(res)

    # Thêm một mệnh đề vào cơ sở tri thức
    def add(self, clause):
        if clause not in self.KB and not self.checkComplementary(clause):
            self.KB.append(clause)

    # Suy luận
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