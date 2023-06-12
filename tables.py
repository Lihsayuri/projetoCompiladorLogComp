import sys


class FuncTable:
    def __init__(self):
        self.table = {}

    def create(self,variable, value):
        if variable not in self.table:
            self.table[variable] = value
        else:
            sys.stderr.write("Erro: variável já declarada")

    def getter(self, variable):
        return self.table[variable]
    
    def setter(self, variable, value):
        if self.table[variable][0] == value[0]:
            self.table[variable] =  value
        else:
            sys.stderr.write("Erro de tipos: atribuição de valor incompatível com o tipo da variável")


class SymbolTable:
    def __init__(self):
        self.table = {}
        self.offset = 4

    def create(self,type, variable, value):
        if variable not in self.table:
            self.table[variable] = (type, value, ("-" + str(self.offset)))
            self.offset += 4
        else:
            sys.stderr.write("Erro: variável já declarada")

    def getter(self, variable):
        # print(self.table)
        # print(variable)
        return self.table[variable]
    
    def setter(self, variable, value):
        # print("selftable: ", self.table[variable])
        if self.table[variable][0] == value[0]:
            self.table[variable] =  (value[0], value[1], self.table[variable][2])
        else:
            sys.stderr.write("Erro de tipos: atribuição de valor incompatível com o tipo da variável")

    def funcArgsTransform(self):
        n_args = len(list(self.table.keys()))
        for i in range(n_args):
            key = list(self.table.keys())[i]
            self.table[key] = (self.table[key][0], self.table[key][1], ("+" + str(8 + (4 * (n_args - i - 1)))))
        self.offset = 4