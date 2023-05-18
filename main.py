import sys
import re
from tokenizer import *
from tables import *
from parser_ import *

# lista_palavras_reservadas = ["println", "readline", "if", "else", "while", "end", "Int", "String", "function", "return" ]   # na PI vai pedir versão 2.1
class PrePro:
    def filter(source):
        source = re.sub(r"#.*\n", "\n", source)  # remove comentários
        source = re.sub(r"#.*", "", source)  # remove linhas em branco
        return source
    
class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self, funcTable, symbolTable):
        pass

class UnOp(Node):
    def evaluate(self, symbolTable):
        if self.children[0].evaluate(symbolTable)[0] == "Int":
            if self.value == "MINUS":
                return ("Int", -self.children[0].evaluate(symbolTable)[1])
            elif self.value == "NOT":
                return ("Int", not self.children[0].evaluate(symbolTable)[1]) #pega o filho da esquerda, faz o evaluate e pega o valor
            elif self.value == "PLUS":
                return ("Int", self.children[0].evaluate(symbolTable)[1])
        else:
            sys.stderr.write("Erro de tipos: operação unária entre tipos incompatíveis")
            sys.exit(1)

class BinOp(Node):

    def evaluate(self, symbolTable):
        filho_esquerda = self.children[0].evaluate(symbolTable)
        filho_direita = self.children[1].evaluate(symbolTable)
        if self.value == "CONCAT":
            return ("String", str(filho_esquerda[1]) + str(filho_direita[1]))
        if self.value == "PLUS":
            if filho_esquerda[0] == "Int" and filho_direita[0] == "Int":
                return ("Int", (filho_esquerda[1] + filho_direita[1]))
            else:
                sys.stderr.write("Erro de tipos: operação de soma entre tipos incompatíveis")
        if self.value == "MINUS":
            if filho_esquerda[0] == "Int" and filho_direita[0] == "Int":
                return ("Int", filho_esquerda[1] - filho_direita[1])
            else:
                sys.stderr.write("Erro de tipos: operação de subtração entre tipos incompatíveis")
        if self.value == "MULT":
            if filho_esquerda[0] == "Int" and filho_direita[0] == "Int":
                return ("Int", filho_esquerda[1] * filho_direita[1])
            else:
                sys.stderr.write("Erro de tipos: operação de multiplicação entre tipos incompatíveis")
        if self.value == "DIV":
            if filho_esquerda[0] == "Int" and filho_direita[0] == "Int":
                return ("Int", filho_esquerda[1] // filho_direita[1])
            else:
                sys.stderr.write("Erro de tipos: operação de divisão entre tipos incompatíveis")
        if self.value == "EQUAL_EQUAL":
            if filho_esquerda[1] == filho_direita[1]:
                return ("Int", 1)
            else:
                return ("Int", 0)
        if self.value == "GREATER":
            if filho_esquerda[1] > filho_direita[1]:
                return ("Int", 1)
            else:
                return ("Int", 0)
        if self.value == "LESS":
            if filho_esquerda[1] < filho_direita[1]:
                return ("Int", 1)
            else:
                return ("Int", 0)
        if self.value == "OR":
            if filho_esquerda[0] == "Int" and filho_direita[0] == "Int":
                valor1 = 0
                valor2 = 0
                if filho_esquerda[1] >= 1:
                    valor1 = 1
                if filho_direita[1] >= 1:
                    valor2 = 1
                return ("Int", valor1 or valor2)
            else:
                sys.stderr.write("Erro de tipos: operação de ou entre tipos incompatíveis")
        if self.value == "AND":
            if filho_esquerda[0] == "Int" and filho_direita[0] == "Int":
                valor1 = 0
                valor2 = 0
                if filho_esquerda[1] >= 1:
                    valor1 = 1
                if filho_direita[1] >= 1:
                    valor2 = 1
                return ("Int", valor1 and valor2)
            else:
                sys.stderr.write("Erro de tipos: operação de e entre tipos incompatíveis")
        
class IntVal(Node):
    def evaluate(self, symbolTable):
        return ("Int", int(self.value))
    
class StringVal(Node):
    def evaluate(self, symbolTable):
        return ("String", self.value)
    
class NoOp(Node):
    def evaluate(self, symbolTable):
        pass 

class Assign(Node):
    def evaluate(self, symbolTable):
        symbolTable.setter(self.children[0].value, self.children[1].evaluate(symbolTable))

class VarDec(Node):
    def evaluate(self, symbolTable):
        if len(self.children) == 1:
            if self.value == "Int":
                symbolTable.create(self.value, self.children[0].value, 0)
            elif self.value == "String":
                symbolTable.create(self.value, self.children[0].value, "")
        else:
            if self.value == "Int":
                symbolTable.create(self.value, self.children[0].value, self.children[1].evaluate(symbolTable)[1])
            elif self.value == "String":
                symbolTable.create(self.value, self.children[0].value, self.children[1].evaluate(symbolTable)[1])


class FuncDec(Node):
    def evaluate(self, funcTable):
        funcTable.create(self.value, self.children[0].value, self)

class FuncCall(Node):

    def evaluate(self, funcTable):
        node_funcao = funcTable.getter(self.value) #retorna a tupla com o nome e o children
        new_symbol_table = SymbolTable()
        iden, *args, block = node_funcao[1].children

        filhos_call = self.children #filhos do funcCall
        # print("filhos call: ", filhos_call)
        # print(funcTable.table)
        # print("args: ", *args)
        if len(*args) != len(filhos_call):
            sys.stderr.write(f"Erro de sintaxe: número de argumentos não corresponde ao número de parâmetros da função '{self.value}'")

        for var_dec, filho_call in zip(*args, filhos_call):
            # print("var_dec: ", var_dec)
            var_dec.evaluate(new_symbol_table)   # a gente da evaluate no vardec que são as variaveis da funcaopara saber o tipo e o nome e o filho_call é o que passei na chamada da função
            new_symbol_table.setter(var_dec.children[0].value, filho_call.evaluate(funcTable))


        (type, value) = block.evaluate(new_symbol_table)
        # print("type: ", type)
        # print(iden.value)
        # print("value: ", value)
        # print(new_symbol_table.table)


        if type != iden.evaluate(funcTable)[0]:
            sys.stderr.write(f"Erro de tipos: tipo de retorno da função '{self.value}' não corresponde ao tipo declarado")
        
        return (type, value)

class Return(Node):
    def evaluate(self, symbolTable):
        return self.children[0].evaluate(symbolTable)


class Print(Node):
    def evaluate(self, symbolTable):
        print(self.children[0].evaluate(symbolTable)[1])

class Identifier(Node):
    def evaluate(self, symbolTable):
        return symbolTable.getter(self.value)
    
    
class Block(Node):
    def evaluate(self, symbolTable):
        for child in self.children:
            block_return = child.evaluate(symbolTable)
            if block_return is not None:
                return block_return

class While(Node):
    def evaluate(self, symbolTable):
        while self.children[0].evaluate(symbolTable)[1]:
            self.children[1].evaluate(symbolTable)

class If(Node):
    def evaluate(self, symbolTable):
        if self.children[0].evaluate(symbolTable)[1]:
            self.children[1].evaluate(symbolTable)
        else:
            if len(self.children) == 3:
                self.children[2].evaluate(symbolTable)

class Readln(Node):
    def evaluate(self, symbolTable):
        return ("Int", int(input()))  



if __name__ == "__main__":
    # argv1 vai ser nome do arquivo e nao travar a extensão .
    with open(sys.argv[1], "r") as file:
        code = file.read()
    
    Parser.run(code)


