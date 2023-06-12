import sys
lista_palavras_reservadas = ["println", "readline", "if", "else", "while", "end", "Int", "String", "function", "return" ]   # na PI vai pedir versão 2.1

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
            elif self.source[self.position] == ',':
                self.position += 1
                self.next = Token("COMMA", 0)
                return
            elif self.source[self.position] == '\"':
                if self.source[self.position+1] == '\"':
                    self.next = Token("STRING", "")
                    self.position += 2
                    return
                else:
                    self.position += 1
                    string = ""
                    while(self.source[self.position] != '\"'):
                        string += self.source[self.position]
                        self.position += 1
                    self.next = Token("STRING", string)
                    self.position += 1
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
            elif self.source[self.position] == ':':
                if self.source[self.position+1] == ':':
                    self.next = Token("DOUBLECOLON", 0)
                    self.position += 2
                    return
                else:
                    sys.stderr.write("Erro lexico: : sem :")
            elif self.source[self.position] == '.':
                self.next = Token("CONCAT", 0)
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
                            if palavra == "Int":
                                self.next = Token("TYPE", "Int")
                            elif palavra == "String":
                                self.next = Token("TYPE", "String")
                            else:
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
    
    def peek(self):
        saved_position = self.position
        saved_next = self.next
        
        # Obtenha o próximo token
        self.selectNext()
        next_token = self.next
        
        # Restaure a posição e o próximo token original
        self.position = saved_position
        self.next = saved_next
        
        return next_token
