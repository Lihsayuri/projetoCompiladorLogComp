import sys

#print(sys.argv[1])


def confere_sinal_apos_sinal(string):
    for i in range(len(string)):
        if (string[i] == '+' or string[i] == '-') and (string[i+1] == '+' or string[i+1] == '-'):
            sys.stderr.write("Operador após operador, isso não é permitido")
            sys.exit(1)

def confere_numero_apos_numero(string):
    partes = string.split(" ")
    #print(partes)
    partes_sem_espacos = []
    for parte in partes:
        if parte != "":
            partes_sem_espacos.append(parte)

    #print(partes_sem_espacos)

    eh_numero = False
    for i in range(len(partes_sem_espacos)):
        if partes_sem_espacos[i].isnumeric() and eh_numero:
            sys.stderr.write("Número após número, isso não é permitido")
            sys.exit(1)
        if partes_sem_espacos[i].isnumeric():
            eh_numero = True
        else:
            eh_numero = False

    return partes_sem_espacos
    
 

def soma_sub(string):
    resultado = 0
    lista = []

    if string[0] == '+' or string[0] == '-':
        sys.stderr.write("Operação inválida")
        sys.exit(1)

    partes_sem_espacos = confere_numero_apos_numero(string)

    
    junta_string = ""
    for i in range(len(partes_sem_espacos)):
        junta_string += partes_sem_espacos[i]
        #print(junta_string)

    confere_sinal_apos_sinal(junta_string)


    print(eval(junta_string))


soma_sub(sys.argv[1])