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
        resultado = Parser.parseTerm(tokenizer)
        while tokenizer.next.type == "PLUS" or tokenizer.next.type == "MINUS":
            if tokenizer.next.type == "PLUS":
                resultado +=  Parser.parseTerm(tokenizer)
            if tokenizer.next.type == "MINUS":            
                resultado -=  Parser.parseTerm(tokenizer)
 
        if tokenizer.next.type == "INT":
            sys.stderr.write("Erro de sintaxe")
            sys.exit(1)
        else:
            return resultado

    def parseTerm(tokenizer):
        resultado = Parser.parseFactor(tokenizer)
        tokenizer.selectNext()
        while tokenizer.next.type == "MULT" or tokenizer.next.type == "DIV" :
            if tokenizer.next.type == "MULT":
                resultado *= Parser.parseFactor(tokenizer)
            if tokenizer.next.type == "DIV":            
                resultado //= Parser.parseFactor(tokenizer)
            tokenizer.selectNext()
        if tokenizer.next.type == "INT":
            sys.stderr.write("Erro de sintaxe: aqui só entra * ou /")
            sys.exit(1)
        else:
            return resultado

 
    def parseFactor(tokenizer):
        tokenizer.selectNext()
        if tokenizer.next.type == "INT":
            return int(tokenizer.next.value)
        elif tokenizer.next.type == "MINUS":
            return -Parser.parseFactor(tokenizer)
        elif tokenizer.next.type == "PLUS":
            return Parser.parseFactor(tokenizer)
        elif tokenizer.next.type == "OPENPAR":
            resultado = Parser.parseExpression(tokenizer)
            if tokenizer.next.type == "CLOSEPAR":
                return resultado
            else:
                sys.stderr.write("Erro de sintaxe: falta fechar parênteses")
                sys.exit(1)
        else:
            sys.stderr.write("Erro de sintaxe: aqui só entra número, - ou +")
            sys.exit(1)


    def run(code):
        code = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(code, 0)
        resultado = Parser.parseExpression(Parser.tokenizer)

        if Parser.tokenizer.position == len(Parser.tokenizer.source) and Parser.tokenizer.next.type == "EOF":
            print(resultado)
            return resultado
        else:
            sys.stderr.write("Erro de sintaxe: não consumiu tudo no diagrama sintático")
            sys.exit(1)


if __name__ == "__main__":
    Parser.run(sys.argv[1])


