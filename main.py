import sys
import re
from tokenizer import *
from tables import *
from parser_ import *

destination_file = sys.argv[1].split(".jl")[0]
funcTable = FuncTable()

class PrePro:
    def filter(source):
        source = re.sub(r"#.*\n", "\n", source)  # remove comentários
        source = re.sub(r"#.*", "", source)  # remove linhas em branco
        return source
    

class Write:
    def write_final_output():
        with open(destination_file + ".asm", "w") as wfile:
            with open("header.asm", "r") as rfile:
                wfile.write(rfile.read())
                wfile.write("\n")
            with open("functions.asm", "r") as rfile:
                wfile.write(rfile.read())
                wfile.write("\n")
            with open("start.asm", "r") as rfile:
                wfile.write(rfile.read())
                wfile.write("\n")
            with open("main_temp.asm", "r") as rfile:
                wfile.write(rfile.read())
                wfile.write("\n")
            with open("footer.asm", "r") as rfile:
                wfile.write(rfile.read())


    def write_code(code):
        with open("main_temp.asm", "a") as file:
            file.write(code)

    def write_func(func_name):
        with open("functions.asm", "a") as file:
            with open("main_temp.asm", "r") as rfile:
                file.write(func_name + ":\n")
                file.write(rfile.read())

    def delete_main_temp_functions():
        with open("main_temp.asm", "w") as file:
            file.write("")
        with open("functions.asm", "w") as file:
            file.write("")

    def stash_data():
        with open(f"main_temp.asm", "r") as rfile:
            data = rfile.read()
        with open(f"main_temp-stash.asm", "w") as wfile:
            wfile.write(data)

    def clear_data():
        with open(f"main_temp.asm", "w") as wfile:
            wfile.write("")

    def retrive_data():
        with open(f"main_temp-stash.asm", "r") as rfile:
            data = rfile.read()
        with open(f"main_temp.asm", "w") as wfile:
            wfile.write(data)

class Node:
    i = 0
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def newId():
        Node.i += 1
        return Node.i
    def evaluate(self, funcTable, symbolTable):
        pass

class UnOp(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children

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
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children

    def evaluate(self, symbolTable):
        filho_esquerda = self.children[0].evaluate(symbolTable)
        Write.write_code("PUSH EBX\n")
        filho_direita = self.children[1].evaluate(symbolTable)
        if self.value == "CONCAT":
            return ("String", str(filho_esquerda[1]) + str(filho_direita[1]))
        if self.value == "PLUS":
            if filho_esquerda[0] == "Int" and filho_direita[0] == "Int":
                Write.write_code("POP EAX\n")
                Write.write_code("ADD EAX, EBX\n")
                Write.write_code("MOV EBX, EAX\n")
                return ("Int", (filho_esquerda[1] + filho_direita[1]))
            else:
                sys.stderr.write("Erro de tipos: operação de soma entre tipos incompatíveis")
        if self.value == "MINUS":
            if filho_esquerda[0] == "Int" and filho_direita[0] == "Int":
                Write.write_code("POP EAX\n")
                Write.write_code("SUB EAX, EBX\n")
                Write.write_code("MOV EBX, EAX\n")
                return ("Int", filho_esquerda[1] - filho_direita[1])
            else:
                sys.stderr.write("Erro de tipos: operação de subtração entre tipos incompatíveis")
        if self.value == "MULT":
            if filho_esquerda[0] == "Int" and filho_direita[0] == "Int":
                Write.write_code("POP EAX\n")
                Write.write_code("IMUL EAX, EBX\n")
                Write.write_code("MOV EBX, EAX\n")
                return ("Int", filho_esquerda[1] * filho_direita[1])
            else:
                sys.stderr.write("Erro de tipos: operação de multiplicação entre tipos incompatíveis")
        if self.value == "DIV":
            if filho_esquerda[0] == "Int" and filho_direita[0] == "Int":
                Write.write_code("POP EAX\n")
                Write.write_code("IDIV EAX, EBX\n")
                Write.write_code("MOV EBX, EAX\n")
                return ("Int", filho_esquerda[1] // filho_direita[1])
            else:
                sys.stderr.write("Erro de tipos: operação de divisão entre tipos incompatíveis")
        if self.value == "EQUAL_EQUAL":
            Write.write_code("POP EAX\n")
            Write.write_code("CMP EAX, EBX\n")
            Write.write_code("call binop_je\n")
            if filho_esquerda[1] == filho_direita[1]:
                return ("Int", 1)
            else:
                return ("Int", 0)
        if self.value == "GREATER":
            Write.write_code("POP EAX\n")
            Write.write_code("CMP EAX, EBX\n")
            Write.write_code("call binop_jg\n")
            if filho_esquerda[1] > filho_direita[1]:
                return ("Int", 1)
            else:
                return ("Int", 0)
        if self.value == "LESS":
            Write.write_code("POP EAX\n")
            Write.write_code("CMP EAX, EBX\n")
            Write.write_code("call binop_jl\n")
            if filho_esquerda[1] < filho_direita[1]:
                return ("Int", 1)
            else:
                return ("Int", 0)
        if self.value == "OR":
            Write.write_code("POP EAX\n")
            Write.write_code("OR EAX, EBX\n")
            Write.write_code("MOV EBX, EAX\n")
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
            Write.write_code("POP EAX\n")
            Write.write_code("AND EAX, EBX\n")
            Write.write_code("MOV EBX, EAX\n")
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
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        Write.write_code("MOV EBX, " + str(self.value)+"\n")
        return ("Int", int(self.value))
    
class StringVal(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        return ("String", self.value)
    
class NoOp(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        pass 

class Assign(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        filho_da_direita = self.children[1].evaluate(symbolTable)
        symbolTable.setter(self.children[0].value, filho_da_direita)
        index = symbolTable.getter(self.children[0].value)[2]
        Write.write_code("MOV [EBP " + str(index) + "], EBX\n")

class VarDec(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        if len(self.children) == 1:
            if self.value == "Int":
                Write.write_code("PUSH DWORD 0\n")
                symbolTable.create(self.value, self.children[0].value, 0)
            elif self.value == "String":
                symbolTable.create(self.value, self.children[0].value, "")
        else:
            if self.value == "Int":
                Write.write_code("PUSH DWORD 0\n")
                symbolTable.create(self.value, self.children[0].value, self.children[1].evaluate(symbolTable)[1])
            elif self.value == "String":
                symbolTable.create(self.value, self.children[0].value, self.children[1].evaluate(symbolTable)[1])


class Print(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        filho_esquerda = self.children[0].evaluate(symbolTable)
        Write.write_code("PUSH EBX\n")
        Write.write_code("CALL print\n")
        Write.write_code("POP EBX\n")
        print(filho_esquerda[1])

class Identifier(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        valor_i = symbolTable.getter(self.value)
        print("valor_i: ", valor_i)
        Write.write_code("MOV EBX, [EBP" + valor_i[2] + "]" + "\n")
        return valor_i
    
class Block(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        for child in self.children:
            block_return = child.evaluate(symbolTable)
            if block_return is not None:
                return block_return

class While(Node):
    def __init__(self, value, children):
        self.id = Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        Write.write_code("LOOP_" + str(self.id) + ":\n")
        filho_esquerdo = self.children[0].evaluate(symbolTable)[1]
        Write.write_code("CMP EBX, False" + "\n")
        Write.write_code("JE EXIT_LOOP_" + str(self.id) + "\n")
        # while self.children[0].evaluate(symbolTable)[1]:
        #     self.children[1].evaluate(symbolTable)
        filho_direito = self.children[1].evaluate(symbolTable)
        Write.write_code("JMP LOOP_" + str(self.id) + "\n")
        Write.write_code("EXIT_LOOP_" + str(self.id) + ":\n")

class If(Node):
    def __init__(self, value, children):
        self.id = Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        Write.write_code("IF_" + str(self.id) + ":\n")
        filho_esquerdo = self.children[0].evaluate(symbolTable)
        Write.write_code("CMP EBX, False" + "\n")
        Write.write_code("JE ELSE_" + str(self.id) + "\n")
        self.children[1].evaluate(symbolTable)
        # if filho_esquerdo[1]:
        Write.write_code("JMP END_IF_" + str(self.id) + "\n")
            # self.children[1].evaluate(symbolTable)
        # else:
        Write.write_code("ELSE_" + str(self.id) + ":\n")

        if len(self.children) == 3:
            self.children[2].evaluate(symbolTable)
        Write.write_code("END_IF_" + str(self.id) + ":\n")

class Readln(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        return ("Int", int(input()))  


class FuncDec(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children

    def evaluate(self, symbolTable):
        funcTable.create(self.children[0].value, self)
        print("funcTable: ", funcTable.table)
        symbolTableTemp = SymbolTable()
        Write.stash_data()
        for filho in self.children[1]:
            print("filho: ", filho.children[0].value)
            filho.evaluate(symbolTableTemp)
        Write.clear_data()
        symbolTableTemp.funcArgsTransform()

        print("Olha o st create: ", symbolTableTemp.table)

        Write.write_code("PUSH EBP\n")
        Write.write_code("MOV EBP, ESP\n")
        self.children[2].evaluate(symbolTableTemp)
        Write.write_func(self.children[0].value)
        Write.retrive_data()
        # self.children[-1].evaluate(symbolTableTemp)

class FuncCall(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children

    def evaluate(self, symbolTable):
        nome_da_funcao = self.value
        print("nome_da_funcao: ", nome_da_funcao)
        print("funcTable: ", funcTable.table)
        node_funcao = funcTable.getter(nome_da_funcao)
        # new_symbol_table = SymbolTable()
        iden, *args, block = node_funcao.children

        filhos_call = self.children
        if len(*args) != len(filhos_call):
            sys.stderr.write(f"Erro de sintaxe: número de argumentos não corresponde ao número de parâmetros da função '{self.value}'")


        for filho in filhos_call:
            filho.evaluate(symbolTable)
            Write.write_code("PUSH EBX\n")

        Write.write_code("CALL " + self.value + "\n")
        
        for i in range(len(filhos_call)):
            Write.write_code("POP EDX\n")

        # for var_dec, filho_call in zip(*args, filhos_call):
        #     var_dec.evaluate(new_symbol_table)
        #     new_symbol_table.setter(var_dec.children[0].value, filho_call.evaluate(funcTable))

        # if type != iden.evaluate(funcTable)[0]:
        #     sys.stderr.write(f"Erro de tipos: tipo de retorno da função '{self.value}' não corresponde ao tipo declarado")

        # (type, value) = block.evaluate(new_symbol_table)
        
        # return (type, value)
        return ("Int", 1)

class Return(Node):
    def __init__(self, value, children):
        Node.newId()
        self.value = value
        self.children = children
    def evaluate(self, symbolTable):
        resultado = self.children[0].evaluate(symbolTable)
        Write.write_code("MOV ESP, EBP\n")
        Write.write_code("POP EBP\n")
        Write.write_code("RET\n")
        return ("return", resultado)


if __name__ == "__main__":
    # argv1 vai ser nome do arquivo e nao travar a extensão .
    with open(sys.argv[1], "r") as file: 
        code = file.read()
    
    Parser.run(code)

