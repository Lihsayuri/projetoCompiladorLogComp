countdown:
PUSH EBP
MOV EBP, ESP
IF_20:
MOV EBX, [EBP+8]
PUSH EBX
MOV EBX, 0
POP EAX
CMP EAX, EBX
call binop_je
CMP EBX, False
JE ELSE_20
MOV EBX, 42
PUSH EBX
CALL print
POP EBX
JMP END_IF_20
ELSE_20:
MOV EBX, [EBP+8]
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP+8]
PUSH EBX
MOV EBX, 1
POP EAX
SUB EAX, EBX
MOV EBX, EAX
PUSH EBX
CALL countdown
POP EDX
END_IF_20:
MOV EBX, 0
MOV ESP, EBP
POP EBP
RET
