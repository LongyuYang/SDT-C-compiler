.data
a_global:	.word	0
b_global:	.word	0
i_program:	.word	0
j_program:	.word	0
a_main:	.word	0
b_main:	.word	0
c_main:	.word	0

.text
addi $sp, $0, 0x10018000	#≥ı ºªØ’ª∂•


main:
addi $26, $0, 3
sw $26, a_main
addi $26, $0, 4
sw $26, b_main
addi $26, $0, 2
sw $26, c_main
lw $26, c_main
sw $26, 0($sp)
addi $sp, $sp, 4
jal demo
lw $10, -4($sp)
sub $sp, $sp, 4
sw $10, 0($sp)
addi $sp, $sp, 4
lw $26, b_main
sw $26, 0($sp)
addi $sp, $sp, 4
lw $26, a_main
sw $26, 0($sp)
addi $sp, $sp, 4
jal program
lw $11, -4($sp)
sub $sp, $sp, 4
add $26, $0, $11
sw $26, a_main
j end


program:
lw $8, -4($sp)
sub $sp, $sp, 4
lw $9, -4($sp)
sub $sp, $sp, 4
lw $10, -4($sp)
sub $sp, $sp, 4
addi $26, $0, 0
sw $26, i_program
add $11, $9, $10
bgt $8, $11, L0
j L1
L0:
mul $12, $9, $10
addi $13, $12, 1
add $14, $8, $13
add $26, $0, $14
sw $26, j_program
j L2
L1:
add $26, $0, $8
sw $26, j_program
L2:
lw $24, i_program
ble $24, 100, L3
j L4
L3:
lw $25, i_program
mul $15, $25, 4
lw $25, j_program
mul $16, $25, 2
addi $17, $0, 1
sub $17, $0, $17
add $18, $0, $16
sub $18, $0, $18
add $19, $18, $17
addi $20, $19, 5
add $21, $0, $20
sub $21, $0, $21
addi $22, $21, 13
add $23, $15, $22
add $26, $0, $23
sw $26, i_program
j L2
L4:
lw $26, i_program
sw $26, 0($sp)
addi $sp, $sp, 4
jr $ra


demo:
lw $24, -4($sp)
sub $sp, $sp, 4
addi $8, $24, 1
add $24, $0, $8
mul $9, $24, 2
sw $9, 0($sp)
addi $sp, $sp, 4
jr $ra
end: