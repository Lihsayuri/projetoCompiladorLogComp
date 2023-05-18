
import sys
from main import PrePro, Node, UnOp, BinOp, IntVal, StringVal, Identifier, FuncCall, VarDec, Block, Assign, Readln, Print, Return, While, If, FuncDec, NoOp
from tokenizer import *
from tables import *


## vê onde tu parou, mas basicamente: o funcCall acho que tá ok no identifier. O problema tá sendo definir a variável a = x+ y. Algum select next
# Alguma logica mal feita

class Parser:
    tokenizer = None

    def parseRelExp(tokenizer):
        node = Parser.parseExpression(tokenizer)
        while tokenizer.next.type == "GREATER" or tokenizer.next.type == "LESS" or tokenizer.next.type == "EQUAL_EQUAL" or tokenizer.next.type == "CONCAT":
            if tokenizer.next.type == "EQUAL_EQUAL":
                node = BinOp(tokenizer.next.type, [node, Parser.parseExpression(tokenizer)])
            if tokenizer.next.type == "GREATER":
                node = BinOp(tokenizer.next.type, [node, Parser.parseExpression(tokenizer)])
            if tokenizer.next.type == "LESS":    
                node = BinOp(tokenizer.next.type, [node, Parser.parseExpression(tokenizer)])
            if tokenizer.next.type == "CONCAT":
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
            tokenizer.selectNext()
        if tokenizer.next.type == "INT":
            sys.stderr.write(f"Erro de sintaxe: INT não esperado.Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
            sys.exit(1)
        else:
            return node

 
    def parseFactor(tokenizer):
        tokenizer.selectNext()
        # print(tokenizer.next.type, tokenizer.next.value)
        if tokenizer.next.type == "INT":
            # print("entrei no int")
            # print("Olha o que recebi do INT: ", tokenizer.next.type, tokenizer.next.value)
            node = IntVal(tokenizer.next.value, [])
            return node
        elif tokenizer.next.type == "IDENTIFIER":  ## CORRIGIR ESSA PARTEEEEE
            node = Identifier(tokenizer.next.value, [])   ## ele faz o getter
            # tokenizer.selectNext()
            # print(tokenizer.peek().type)
            # print(tokenizer.peek().value)
            if tokenizer.peek().type == "OPENPAR":
                node_call = FuncCall(node.value, [])
                tokenizer.selectNext()
                if tokenizer.next.type != "CLOSEPAR":
                    while tokenizer.next.type != "CLOSEPAR":
                        node_rel_exp = Parser.parseRelExp(tokenizer)
                        node_call.children.append(node_rel_exp)
                        if tokenizer.next.type != "COMMA" and tokenizer.next.type != "CLOSEPAR":
                            sys.stderr.write("Erro de sintaxe: falta vírgula no funcCall. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                    return node_call

            else:
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
        
        elif tokenizer.next.type == "STRING":
            node = StringVal(tokenizer.next.value, [])
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
        while tokenizer.next.type != "END" and tokenizer.next.type != "ELSE"  and tokenizer.next.type != "EOF":
            node_Block.children.append(Parser.parseStatement(tokenizer))
            tokenizer.selectNext()
        return node_Block

    def parseStatement(tokenizer):
        if Parser.tokenizer.next.type == "IDENTIFIER":
            node_identifier = Identifier(Parser.tokenizer.next.value, [])  # vai criar um nó com o valor sendo a variável. Ex: x1 e não tem nenhum filho
            Parser.tokenizer.selectNext()
            ## aqui faz o setter do identifier
            if Parser.tokenizer.next.type == "EQUAL":
                # tokenizer.selectNext()
                node_expression = Parser.parseRelExp(Parser.tokenizer)   ### PAREIIII AQUI
                # print("Settei a variável: ", node_identifier.value, " com o valor: ", node_expression.children)
                if Parser.tokenizer.next.type != "NEWLINE":
                    sys.stderr.write("AQUIIErro de sintaxe: não terminou a linha no identifier.  Caracter atual: {tokenizer.next.value}")
                return Assign(None, [node_identifier, node_expression])
            elif Parser.tokenizer.next.type == "DOUBLECOLON":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "TYPE":
                    tipo_da_var = Parser.tokenizer.next.value
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "EQUAL":
                        node_expression = Parser.parseRelExp(Parser.tokenizer)
                        if Parser.tokenizer.next.type != "NEWLINE":
                            sys.stderr.write("Erro de sintaxe: não terminou a linha no identifier.  Caracter atual: {tokenizer.next.value}")
                        return VarDec(tipo_da_var, [node_identifier, node_expression])
                    elif Parser.tokenizer.next.type == "NEWLINE":
                        # print("Criei a variável: ", node_identifier.value, " do tipo: ", tipo_da_var)
                        return VarDec(tipo_da_var, [node_identifier])
                    sys.stderr.write("Erro de sintaxe: não terminou a linha no identifier.  Caracter atual: {tokenizer.next.value}")
                else:
                    sys.stderr.write("Erro de sintaxe: falta o tipo no VARDEC. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                    sys.exit(1)
            elif Parser.tokenizer.next.type == "OPENPAR":   ## CONFERIR ISSO AQUI
                node_call = FuncCall(node_identifier.value, [])
                if Parser.tokenizer.next.type != "CLOSEPAR":
                    while Parser.tokenizer.next.type != "CLOSEPAR":
                        node_rel_exp = Parser.parseRelExp(Parser.tokenizer)
                        node_call.children.append(node_rel_exp)
                        # print("Aquii no while, o tokenizer: ", Parser.tokenizer.next.type, Parser.tokenizer.next.value)
                        if Parser.tokenizer.next.type != "COMMA" and Parser.tokenizer.next.type != "CLOSEPAR":
                            sys.stderr.write("Erro de sintaxe: falta vírgula no funcCall. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != "NEWLINE":
                        sys.stderr.write("Erro de sintaxe: não terminou a linha no identifier.  Caracter atual: {tokenizer.next.value}")
                    return node_call
        elif Parser.tokenizer.next.type == "RETURN":
            node_rel_expl = Parser.parseRelExp(Parser.tokenizer)
            if Parser.tokenizer.next.type != "NEWLINE":
                sys.stderr.write("Erro de sintaxe: não terminou a linha no return.  Caracter atual: {tokenizer.next.value}")
            return Return("return", [node_rel_expl])
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
        elif Parser.tokenizer.next.type == "FUNCTION":
            Tokenizer.selectNext(Parser.tokenizer)
            if Parser.tokenizer.next.type == "IDENTIFIER":
                node_identifier_func = Identifier(Parser.tokenizer.next.value, [])
                Tokenizer.selectNext(Parser.tokenizer)
                if Parser.tokenizer.next.type == "OPENPAR":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "IDENTIFIER":
                        node_identifier_var = Identifier(Parser.tokenizer.next.value, [])
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == "DOUBLECOLON":
                            Parser.tokenizer.selectNext()
                            if Parser.tokenizer.next.type == "TYPE":
                                tipo_da_var = Parser.tokenizer.next.value
                                node_var_dec = VarDec(tipo_da_var, [node_identifier_var])
                                lista_var_decs = [node_var_dec]
                                Parser.tokenizer.selectNext()
                                while Parser.tokenizer.next.type == "COMMA":
                                    Parser.tokenizer.selectNext()
                                    if Parser.tokenizer.next.type == "IDENTIFIER":
                                        node_identifier_var = Identifier(Parser.tokenizer.next.value, [])
                                        Parser.tokenizer.selectNext()
                                        if Parser.tokenizer.next.type == "DOUBLECOLON":
                                            Parser.tokenizer.selectNext()
                                            if Parser.tokenizer.next.type == "TYPE":
                                                tipo_da_var = Parser.tokenizer.next.value
                                                node_var_dec = VarDec(tipo_da_var, [node_identifier_var])
                                                lista_var_decs.append(node_var_dec)
                                                Parser.tokenizer.selectNext()
                                            else:
                                                sys.stderr.write("Erro de sintaxe: falta o tipo no function. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                                sys.exit(1)
                                        else:
                                            sys.stderr.write("Erro de sintaxe: falta o :: no function. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                            sys.exit(1)
                                    else:
                                        sys.stderr.write("Erro de sintaxe: falta o identificador no function. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                        sys.exit(1)
                                if Parser.tokenizer.next.type == "CLOSEPAR":
                                    Parser.tokenizer.selectNext()
                                    if Parser.tokenizer.next.type == "DOUBLECOLON":
                                        Parser.tokenizer.selectNext()
                                        if Parser.tokenizer.next.type == "TYPE":
                                            tipo_da_funcao = Parser.tokenizer.next.value
                                            Parser.tokenizer.selectNext()
                                            if Parser.tokenizer.next.type == "NEWLINE":
                                                node_Block = Block("", [])
                                                tokenizer.selectNext()
                                                while tokenizer.next.type != "END" and tokenizer.next.type != "EOF":
                                                    node_Block.children.append(Parser.parseStatement(tokenizer))
                                                    tokenizer.selectNext()
                                                if Parser.tokenizer.next.type != "END":
                                                    sys.stderr.write("Erro de sintaxe: falta end. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                                    sys.exit(1)
                                                Parser.tokenizer.selectNext()
                                                if Parser.tokenizer.next.type != "NEWLINE":
                                                    sys.stderr.write("Erro de sintaxe: não terminou a linha no end. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                                    sys.exit(1)
                                                return FuncDec(tipo_da_funcao, [node_identifier_func, lista_var_decs, node_Block])
                                            else:
                                                sys.stderr.write("Erro de sintaxe: não terminou a linha no function. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                                sys.exit(1)
                                        else:
                                            sys.stderr.write("Erro de sintaxe: falta o tipo no function. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                            sys.exit(1)
                                    else:
                                        sys.stderr.write(" Erro de sintaxe: falta o :: no function. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                        sys.exit(1)
                elif Parser.tokenizer.next.type == "CLOSEPAR":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "DOUBLECOLON":
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == "TYPE":
                            tipo_da_funcao = Parser.tokenizer.next.value
                            Parser.tokenizer.selectNext()
                            if Parser.tokenizer.next.type == "NEWLINE":
                                node_block_else = Parser.parseBlockIFWhile(Parser.tokenizer)
                                if Parser.tokenizer.next.type != "END":
                                    sys.stderr.write("Erro de sintaxe: falta end. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                    sys.exit(1)
                                Parser.tokenizer.selectNext()
                                if Parser.tokenizer.next.type != "NEWLINE":
                                    sys.stderr.write("Erro de sintaxe: não terminou a linha no end. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                    sys.exit(1)
                                return FuncDec(tipo_da_funcao, [node_identifier, node_block])
                            else:
                                sys.stderr.write("Erro de sintaxe: não terminou a linha no function. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                                sys.exit(1)
                        else:
                            sys.stderr.write("Erro de sintaxe: falta o tipo no function. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                            sys.exit(1)
                    else:
                        sys.stderr.write("Erro de sintaxe: falta o :: no function. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                        sys.exit(1)
                        
            else:
                sys.stderr.write("Erro de sintaxe: falta o identificador no function. Tipo atual: {tokenizer.next.type}. Caracter atual: {tokenizer.next.value}")
                sys.exit(1)


        elif Parser.tokenizer.next.type == "NEWLINE":
            return NoOp("", [])
        


    def run(code):
        code = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(code, 0)
        root = Parser.parseBlock(Parser.tokenizer)

        if Parser.tokenizer.position == len(Parser.tokenizer.source) and Parser.tokenizer.next.type == "EOF":
            resultado =  root.evaluate(symbolTable=SymbolTable())
            return resultado
        else:
            sys.stderr.write("Erro de sintaxe: não consumiu tudo no diagrama sintático")
            sys.exit(1)
