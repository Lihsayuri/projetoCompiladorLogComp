import sys

class PrePro:
    def filter(source):
        while "#" in source:
            start = source.find("#")
            if source[start:].find("\n") == -1:
                end = len(source)
            else:
                end = source.find("\n", start) + 2 # índice start para a função find, garante que a busca pelo fim comece a partir do início 
            comment = source[start:end]
            source = source.replace(comment, "")
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
            elif self.source[self.position] == " ":
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


    def run(code):
        code = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(code, 0)
        root = Parser.parseExpression(Parser.tokenizer)

        if Parser.tokenizer.position == len(Parser.tokenizer.source) and Parser.tokenizer.next.type == "EOF":
            resultado =  root.evaluate()
            print(resultado)
            return resultado
        else:
            sys.stderr.write("Erro de sintaxe: não consumiu tudo no diagrama sintático")
            sys.exit(1)


if __name__ == "__main__":
    # argv1 vai ser nome do arquivo e nao travar a extensão .
    with open(sys.argv[1], "r") as file:
        code = file.read()
    Parser.run(code)


