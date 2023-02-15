import sys


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
            elif self.source[self.position] == " ":
                self.position += 1
            else:
                sys.stderr.write("Você digitou um caracter inválido")
                sys.exit(1)
        else:
            self.next = Token("EOF", 0)
            return

class Parser:
    tokenizer = None

    def parseExpression(tokenizer):
        resultado = 0
        if tokenizer.next.type == "INT":
            resultado = int(tokenizer.next.value)
            tokenizer.selectNext()
            while tokenizer.next.type == "PLUS" or tokenizer.next.type == "MINUS":
                if tokenizer.next.type == "PLUS":
                    tokenizer.selectNext()
                    if tokenizer.next.type == "INT":
                        resultado += int(tokenizer.next.value)
                    else:
                        sys.stderr.write("Erro de sintaxe: operador depois de operador")
                        sys.exit(1)
                if tokenizer.next.type == "MINUS":            
                    tokenizer.selectNext()
                    if tokenizer.next.type == "INT":
                        resultado -= int(tokenizer.next.value)
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
        Parser.tokenizer = Tokenizer(code, 0)
        Parser.tokenizer.selectNext()
        resultado = Parser.parseExpression(Parser.tokenizer)

        if Parser.tokenizer.position == len(Parser.tokenizer.source) and Parser.tokenizer.next.type == "EOF":
            print(resultado)
            return resultado
        else:
            sys.stderr.write("Erro de sintaxe: não consumiu tudo no diagrama sintático")
            sys.exit(1)


if __name__ == "__main__":
    Parser.run(sys.argv[1])


