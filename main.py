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
        if tokenizer.next.type == "PLUS" or tokenizer.next.type == "MINUS" or tokenizer.next.type == "EOF":
            while tokenizer.next.type == "PLUS" or tokenizer.next.type == "MINUS":
                if tokenizer.next.type == "PLUS":
                    resultado +=  Parser.parseTerm(tokenizer)
                if tokenizer.next.type == "MINUS":            
                    resultado -=  Parser.parseTerm(tokenizer)
            return resultado

        if tokenizer.next.type == "INT":
            sys.stderr.write("Erro de sintaxe")
            sys.exit(1)

    def parseTerm(tokenizer):
        resultado = 0
        tokenizer.selectNext()
        if tokenizer.next.type == "INT":
            resultado = int(tokenizer.next.value)
            tokenizer.selectNext()
            while tokenizer.next.type == "MULT" or tokenizer.next.type == "DIV":
                if tokenizer.next.type == "MULT":
                    tokenizer.selectNext()
                    if tokenizer.next.type == "INT":
                        resultado *= int(tokenizer.next.value)
                    else:
                        sys.stderr.write("Erro de sintaxe: operador depois de operador")
                        sys.exit(1)
                if tokenizer.next.type == "DIV":            
                    tokenizer.selectNext()
                    if tokenizer.next.type == "INT":
                        if int(tokenizer.next.value) == 0:
                            sys.stderr.write("Erro de sintaxe: divisão por zero")
                            sys.exit(1)
                        resultado //= int(tokenizer.next.value)
                    else:
                        sys.stderr.write("Erro de sintaxe: operador depois de operador")
                        sys.exit(1)
                tokenizer.selectNext()
                # print(resultado)
            return resultado

        else:
            sys.stderr.write("Erro de sintaxe: não pode começar com operador")
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


