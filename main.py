import sys
import re

lista_palavras_reservadas = ["println", "readline", "if", "else", "while", "end"]   # na PI vai pedir versão 2.1
class PrePro:
    def filter(source):
        source = re.sub(r"#.*\n", "\n", source)  # remove comentários
        source = re.sub(r"#.*", "", source)  # remove linhas em branco
        return source
    
class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def evaluate(self):
        pass

class UnOp(Node):
    def evaluate(self):
        if self.value == "MINUS":
            return -self.children[0].evaluate()  # faz recursivamente. Vai fazendo os evaluate até chegar no número
        elif self.value == "NOT":
            return not self.children[0].evaluate()
        return self.children[0].evaluate()

class BinOp(Node):
    def evaluate(self):
        if self.value == "PLUS":
            return self.children[0].evaluate() + self.children[1].evaluate()
        if self.value == "MINUS":
            return self.children[0].evaluate() - self.children[1].evaluate()
        if self.value == "MULT":
            return self.children[0].evaluate() * self.children[1].evaluate()
        if self.value == "DIV":
            return self.children[0].evaluate() // self.children[1].evaluate()
        if self.value == "EQUAL_EQUAL":
            return self.children[0].evaluate() == self.children[1].evaluate()
        if self.value == "GREAT":
            return self.children[0].evaluate() > self.children[1].evaluate()
        if self.value == "LESS":
            return self.children[0].evaluate() < self.children[1].evaluate()
        if self.value == "OR":
            return self.children[0].evaluate() or self.children[1].evaluate()
        if self.value == "AND":
            return self.children[0].evaluate() and self.children[1].evaluate()
        
class IntVal(Node):
    def evaluate(self):
        return int(self.value)
    
class NoOp(Node):
    def evaluate(self):
        pass 

class Assign(Node):
    def evaluate(self):
        SymbolTable.setter(self.children[0].value, self.children[1].evaluate())

class Print(Node):
    def evaluate(self):
        print(self.children[0].evaluate())

class Identifier(Node):
    def evaluate(self):
        return SymbolTable.getter(self.value)
    
class Block(Node):
    def evaluate(self):
        for child in self.children:
            child.evaluate()

class While(Node):
    def evaluate(self):
        while self.children[0].evaluate():
            self.children[1].evaluate()

class If(Node):
    def evaluate(self):
        if self.children[0].evaluate():
            self.children[1].evaluate()
        else:
            if len(self.children) == 3:
                self.children[2].evaluate()

class Readln(Node):
    def evaluate(self):
        return int(input())  

class SymbolTable:
    table = {}

    def getter(variable):
        # return SymbolTable.table.get(variable)
        return SymbolTable.table[variable]
    def setter(variable, value):
        SymbolTable.table[variable] = value
#read sempre vai retornar int. Não tem filhos e lê input e retorna um int. cast
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source, position):
        self.source = source
        self.position = position
        self.next = Token(None, None)

    def selectNext(self):
        numero = ""
        while(len(self.source)!=self.position):
            if self.source[self.position].isnumeric():
                numero += self.source[self.position]
                self.position += 1
                while(len(self.source)!=self.position):
                    if self.source[self.position].isnumeric():
                        numero += self.source[self.position]
                        self.position += 1
                    else:
                        self.next = Token("INT", numero)
                        return
                self.next = Token("INT", numero)
                return
            elif self.source[self.position] == '+' :
                self.next = Token("PLUS", 0)
                self.position += 1
                return 
            elif self.source[self.position] == '-' :
                self.next = Token("MINUS", 0)
                self.position += 1
                return 
            elif self.source[self.position] == '*':
                self.next = Token("MULT", 0)
                self.position += 1
                return
            elif self.source[self.position] == '/':
                self.next = Token("DIV", 0)
                self.position += 1
                return
            elif self.source[self.position] == '(':
                self.next = Token("OPENPAR", 0)
                self.position += 1
                return
            elif self.source[self.position] == ')':
                self.next = Token("CLOSEPAR", 0)
                self.position += 1
                return
            elif self.source[self.position] == '\n':
                self.position += 1
                self.next = Token("NEWLINE", 0)
                return
            elif self.source[self.position] == '=':
                if self.source[self.position+1] == '=':
                    self.next = Token("EQUAL_EQUAL", 0)
                    self.position += 2
                    return
                self.next = Token("EQUAL", 0)
                self.position += 1
                return
            elif self.source[self.position] == '!':
                self.next = Token("NOT", 0)
                self.position += 1
                return
            elif self.source[self.position] == '>':
                self.next = Token("GREATER", 0)
                self.position += 1
                return
            elif self.source[self.position] == '<':
                self.next = Token("LESS", 0)
                self.position += 1
                return
            elif self.source[self.position] == '&':
                if self.source[self.position+1] == '&':
                    self.next = Token("AND", 0)
                    self.position += 2
                    return
                else:
                    sys.stderr.write("Erro lexico: & sem &")
            elif self.source[self.position] == '|':
                if self.source[self.position+1] == '|':
                    self.next = Token("OR", 0)
                    self.position += 2
                    return
                else:
                    sys.stderr.write("Erro lexico: | sem |")
            elif self.source[self.position].isalpha():
                palavra = ""
                palavra += self.source[self.position]
                self.position += 1
                while(len(self.source)!=self.position):
                    if self.source[self.position].isalpha() or self.source[self.position].isnumeric() or self.source[self.position] == "_":
                        palavra += self.source[self.position]
                        self.position += 1
                    else:
                        if palavra in lista_palavras_reservadas:
                            self.next = Token(palavra.upper(), 0)
                            return
                        else:
                            self.next = Token("IDENTIFIER", palavra)
                            return
                if palavra in lista_palavras_reservadas:
                    self.next = Token(palavra.upper(), 0)
                    return
                else:
                    self.next = Token("IDENTIFIER", palavra)
                    return   
            elif self.source[self.position] == " " :
                self.position += 1
            else:
                sys.stderr.write("Você digitou um caracter inválido")
                sys.exit(1)
        
        self.next = Token("EOF", 0)
        return


class Parser:
    tokenizer = None

    def parseRelExp(tokenizer):
        node = Parser.parseExpression(tokenizer)
        while tokenizer.next.type == "GREATER" or tokenizer.next.type == "LESS" or tokenizer.next.type == "EQUAL_EQUAL":
            if tokenizer.next.type == "EQUAL_EQUAL":
                node = BinOp(tokenizer.next.type, [node, Parser.parseExpression(tokenizer)])
            if tokenizer.next.type == "GREATER":
                node = BinOp(tokenizer.next.type, [node, Parser.parseExpression(tokenizer)])
            if tokenizer.next.type == "LESS":    
                node = BinOp(tokenizer.next.type, [node, Parser.parseExpression(tokenizer)])
 
        if tokenizer.next.type == "INT":
            sys.stderr.write(f"Erro de sintaxe: INT não esperado.Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
            sys.exit(1)
        else:
            return node


    def parseExpression(tokenizer):
        node = Parser.parseTerm(tokenizer)
        while tokenizer.next.type == "PLUS" or tokenizer.next.type == "MINUS" or tokenizer.next.type == "OR":
            if tokenizer.next.type == "PLUS":
                node = BinOp(tokenizer.next.type, [node, Parser.parseTerm(tokenizer)])
            if tokenizer.next.type == "MINUS":    
                node = BinOp(tokenizer.next.type, [node, Parser.parseTerm(tokenizer)])
            if tokenizer.next.type == "OR":
                node = BinOp(tokenizer.next.type, [node, Parser.parseTerm(tokenizer)])
 
        if tokenizer.next.type == "INT":
            sys.stderr.write(f"Erro de sintaxe: INT não esperado.Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
            sys.exit(1)
        else:
            return node

    def parseTerm(tokenizer):
        node = Parser.parseFactor(tokenizer)
        tokenizer.selectNext()
        while tokenizer.next.type == "MULT" or tokenizer.next.type == "DIV"  or tokenizer.next.type == "AND":
            if tokenizer.next.type == "MULT":
                node = BinOp(tokenizer.next.type, [node, Parser.parseFactor(tokenizer)])
            if tokenizer.next.type == "DIV":    
                node = BinOp(tokenizer.next.type, [node, Parser.parseFactor(tokenizer)])
            if tokenizer.next.type == "AND":
                node = BinOp(tokenizer.next.type, [node, Parser.parseFactor(tokenizer)])
            # tokenizer.selectNext()
        if tokenizer.next.type == "INT":
            sys.stderr.write(f"Erro de sintaxe: INT não esperado.Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
            sys.exit(1)
        else:
            return node

 
    def parseFactor(tokenizer):
        tokenizer.selectNext()
        if tokenizer.next.type == "INT":
            node = IntVal(tokenizer.next.value, [])
            return node
        elif tokenizer.next.type == "IDENTIFIER":
            node = Identifier(tokenizer.next.value, [])   ## ele faz o getter
            return node
        elif tokenizer.next.type == "MINUS":
            node = UnOp(tokenizer.next.type, [Parser.parseFactor(tokenizer)])
            return node
        elif tokenizer.next.type == "PLUS":
            node = UnOp(tokenizer.next.type, [Parser.parseFactor(tokenizer)])
            return node
        elif tokenizer.next.type == "NOT":
            node = UnOp(tokenizer.next.type, [Parser.parseFactor(tokenizer)])
            return node
        elif tokenizer.next.type == "OPENPAR":
            node = Parser.parseRelExp(tokenizer)
            if tokenizer.next.type == "CLOSEPAR":
                return node
            else:
                sys.stderr.write(f"Erro de sintaxe: falta fechar parênteses no Factor. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                sys.exit(1)
        elif tokenizer.next.type == "READLINE":
            tokenizer.selectNext()
            if tokenizer.next.type == "OPENPAR":
                tokenizer.selectNext()
                if tokenizer.next.type == "CLOSEPAR":
                    node = Readln(None, [])
                    return node
                else:
                    sys.stderr.write(f"Erro de sintaxe: falta fechar parênteses no Factor. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                    sys.exit(1)
        else:
            sys.stderr.write(f"Erro de sintaxe: aqui só entra número, - ou +. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
            sys.exit(1)

    def parseBlock(tokenizer):
        node_Block = Block("", [])
        tokenizer.selectNext()
        while tokenizer.next.type != "EOF":
            node_Block.children.append(Parser.parseStatement(tokenizer))
            tokenizer.selectNext()
        return node_Block
    
    def parseBlockIFWhile(tokenizer):
        node_Block = Block("", [])
        tokenizer.selectNext()
        while tokenizer.next.type != "END" and tokenizer.next.type != "ELSE":
            node_Block.children.append(Parser.parseStatement(tokenizer))
            tokenizer.selectNext()
        return node_Block

    def parseStatement(tokenizer):
        if Parser.tokenizer.next.type == "IDENTIFIER":
            node_identifier = Identifier(Parser.tokenizer.next.value, [])  # vai criar um nó com o valor sendo a variável. Ex: x1 e não tem nenhum filho
            Parser.tokenizer.selectNext()
            ## aqui faz o setter do identifier
            if Parser.tokenizer.next.type != "EQUAL":
                sys.stderr.write("Erro de sintaxe: falta sinal de igual.  Caracter atual: {tokenizer.next.value}")
            node_expression = Parser.parseRelExp(Parser.tokenizer)
            if Parser.tokenizer.next.type != "NEWLINE":
                sys.stderr.write("Erro de sintaxe: não terminou a linha no identifier.  Caracter atual: {tokenizer.next.value}")
            return Assign("", [node_identifier, node_expression ])
        
        elif Parser.tokenizer.next.type == "PRINTLN":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPENPAR":
                node_print = Parser.parseRelExp(Parser.tokenizer)
                if Parser.tokenizer.next.type == "CLOSEPAR":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != "NEWLINE":
                        sys.stderr.write("Erro de sintaxe: não terminou a linha no print. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                        sys.exit(1)
                    return Print("", [node_print])

                else:
                    sys.stderr.write("Erro de sintaxe: falta fechar parênteses no println. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                    sys.exit(1)
            else:
                sys.stderr.write("Erro de sintaxe: falta abrir parênteses pro print. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                sys.exit(1)

        elif Parser.tokenizer.next.type == "WHILE":
            node_rel_exp = Parser.parseRelExp(Parser.tokenizer)
            if Parser.tokenizer.next.type != "NEWLINE":
                sys.stderr.write("Erro de sintaxe: não terminou a linha no while. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                sys.exit(1)
            node_block = Parser.parseBlockIFWhile(Parser.tokenizer)
            if Parser.tokenizer.next.type != "END":
                sys.stderr.write("Erro de sintaxe: falta end. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                sys.exit(1)
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "NEWLINE":
                sys.stderr.write("Erro de sintaxe: não terminou a linha no end. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                sys.exit(1)
            return While("", [node_rel_exp, node_block])
        
        elif Parser.tokenizer.next.type == "IF":
            node_rel_exp = Parser.parseRelExp(Parser.tokenizer)
            if Parser.tokenizer.next.type != "NEWLINE":
                sys.stderr.write("Erro de sintaxe: não terminou a linha no if. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                sys.exit(1)
            node_block = Parser.parseBlockIFWhile(Parser.tokenizer)

            if Parser.tokenizer.next.type == "END":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != "NEWLINE":
                    sys.stderr.write("Erro de sintaxe: não terminou a linha no end. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                    sys.exit(1)
                return If("", [node_rel_exp, node_block])
            elif Parser.tokenizer.next.type == "ELSE":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != "NEWLINE":
                    sys.stderr.write("Erro de sintaxe: não terminou a linha no else. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                    sys.exit(1)
                node_block_else = Parser.parseBlockIFWhile(Parser.tokenizer)
                if Parser.tokenizer.next.type != "END":
                    sys.stderr.write("Erro de sintaxe: falta end. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                    sys.exit(1)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != "NEWLINE":
                    sys.stderr.write("Erro de sintaxe: não terminou a linha no end. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                    sys.exit(1)
                return If("", [node_rel_exp, node_block, node_block_else])
            else:
                sys.stderr.write("Erro de sintaxe: falta end ou else. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                sys.exit(1)


        elif Parser.tokenizer.next.type == "NEWLINE":
            return NoOp("", [])
        


    def run(code):
        code = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(code, 0)
        root = Parser.parseBlock(Parser.tokenizer)

        if Parser.tokenizer.position == len(Parser.tokenizer.source) and Parser.tokenizer.next.type == "EOF":
            resultado =  root.evaluate()
            return resultado
        else:
            sys.stderr.write("Erro de sintaxe: não consumiu tudo no diagrama sintático")
            sys.exit(1)


if __name__ == "__main__":
    # argv1 vai ser nome do arquivo e nao travar a extensão .
    with open(sys.argv[1], "r") as file:
        code = file.read()
    
    Parser.run(code)


