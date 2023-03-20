import sys
import re

lista_palavras_reservadas = ["println"]   # na PI vai pedir versão 2.1
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

class SymbolTable:
    table = {}

    def getter(variable):
        return SymbolTable.table.get(variable)
    def setter(variable, value):
        SymbolTable.table[variable] = value

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
                self.next = Token("EQUAL", 0)
                self.position += 1
                return
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

    def parseExpression(tokenizer):
        node = Parser.parseTerm(tokenizer)
        while tokenizer.next.type == "PLUS" or tokenizer.next.type == "MINUS":
            if tokenizer.next.type == "PLUS":
                node = BinOp(tokenizer.next.type, [node, Parser.parseTerm(tokenizer)])
            if tokenizer.next.type == "MINUS":    
                node = BinOp(tokenizer.next.type, [node, Parser.parseTerm(tokenizer)])
 
        if tokenizer.next.type == "INT":
            sys.stderr.write(f"Erro de sintaxe: INT não esperado. Caracter atual: {tokenizer.next.value}")
            sys.exit(1)
        else:
            return node

    def parseTerm(tokenizer):
        node = Parser.parseFactor(tokenizer)
        tokenizer.selectNext()
        while tokenizer.next.type == "MULT" or tokenizer.next.type == "DIV" :
            if tokenizer.next.type == "MULT":
                node = BinOp(tokenizer.next.type, [node, Parser.parseFactor(tokenizer)])
            if tokenizer.next.type == "DIV":    
                node = BinOp(tokenizer.next.type, [node, Parser.parseFactor(tokenizer)])
            tokenizer.selectNext()
        if tokenizer.next.type == "INT":
            sys.stderr.write(f"Erro de sintaxe: INT não esperado. Caracter atual: {tokenizer.next.value}")
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
        elif tokenizer.next.type == "OPENPAR":
            node = Parser.parseExpression(tokenizer)
            if tokenizer.next.type == "CLOSEPAR":
                return node
            else:
                sys.stderr.write(f"Erro de sintaxe: falta fechar parênteses.  Caracter atual: {tokenizer.next.value}")
                sys.exit(1)
        else:
            sys.stderr.write(f"Erro de sintaxe: aqui só entra número, - ou +.  Caracter atual: {tokenizer.next.value}")
            sys.exit(1)

    def parseBlock(tokenizer):
        node_Block = Block("", [])
        tokenizer.selectNext()
        while tokenizer.next.type != "EOF":
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
            node_expression = Parser.parseExpression(Parser.tokenizer)
            if Parser.tokenizer.next.type != "NEWLINE":
                sys.stderr.write("Erro de sintaxe: não terminou a linha no identifier.  Caracter atual: {tokenizer.next.value}")
            return Assign("", [node_identifier, node_expression ])
        elif Parser.tokenizer.next.type == "PRINTLN":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPENPAR":
                node_print = Parser.parseExpression(Parser.tokenizer)
                if Parser.tokenizer.next.type == "CLOSEPAR":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != "NEWLINE":
                        sys.stderr.write("Erro de sintaxe: não terminou a linha no print.  Caracter atual: {tokenizer.next.value}")
                        sys.exit(1)
                    return Print("", [node_print])

                else:
                    sys.stderr.write("Erro de sintaxe: falta fechar parênteses.  Caracter atual: {tokenizer.next.value}")
                    sys.exit(1)
            else:
                sys.stderr.write("Erro de sintaxe: falta abrir parênteses pro print.  Caracter atual: {tokenizer.next.value}")
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


