# projetoCompiladorLogComp

![git status](http://3.129.230.99/svg/Lihsayuri/projetoCompiladorLogComp/)

## Diagrama Sintático do roteiro 1:

![Alt text](diagramaSintatico1.drawio.png?raw=true "Title")

## Diagrama Sintático do roteiro 2:

![Alt text](diagramaSintatico2.drawio.png?raw=true "Title")

## Diagrama Sintático do roteiro 3:

![Alt text](diagramaSintatico3.drawio.png?raw=true "Title")

## Diagrama Sintático do roteiro 5:

![Alt text](diagramaSintatico4.drawio.png?raw=true "Title")


### EBNF:

- EXPRESSION = TERM, { ("+" | "-"), TERM } ;

- TERM = FACTOR, { ("*" | "/"), FACTOR } ;

- FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;

- BLOCK = {STATEMENT}

- STATEMENT = ("\n" | IDENTIFICADOR, "=" , EXPRESSION, "\n" | print, "(", EXPRESSION, ")", "\n")

- IDENTIFICADOR = (letter| "_") {letter | number | "_"}

<img src="regras_de_producao.png" width="400" height="300">
