import sys

class FuncTable:
    table = {}

    def create(type, variable, value):
        if variable not in FuncTable.table:
            FuncTable.table[variable] = (type, value)
        else:
            sys.stderr.write("Erro: variável já declarada")

    def getter(variable):
        return FuncTable.table[variable]
    
    def setter(variable, value):
        if FuncTable.table[variable][0] == value[0]:
            FuncTable.table[variable] =  value
        else:
            sys.stderr.write("Erro de tipos: atribuição de valor incompatível com o tipo da variável")

class SymbolTable:
    def __init__(self):
        self.table = {}

    def create(self,type, variable, value):
        if variable not in self.table:
            self.table[variable] = (type, value)
        else:
            sys.stderr.write("Erro: variável já declarada")

    def getter(self, variable):
        # print(self.table)
        # print(variable)
        return self.table[variable]
    
    def setter(self, variable, value):
        # print("selftable: ", self.table[variable])
        if self.table[variable][0] == value[0]:
            self.table[variable] =  value
        else:
            sys.stderr.write("Erro de tipos: atribuição de valor incompatível com o tipo da variável")
