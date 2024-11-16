inp = '''move $s7,$0
move $t7,$t2
addi $t4,$t2,288
move $s5,$t3
lw $t9,0($t2)
sw $t9,0($t4)
addi $t4,$t4,4
addi $t2,$t2,4
addi $s7,$s7,1
bne $s7,$t1,loop_original
move $s7,$0
move $t4,$0
move $t2,$t7
addi $t4,$t2,288	
beq $s7,$t1,Done	
move $s6,$0
move $t8,$0
mul $s0,$s6,4
add $s0,$t4,$s0
lw $t5,0($s0)
lw $t6,4($s0)
bge $t6,$t5,no_swap
sw $t6,0($s0)
sw $t5,4($s0)
li $t8,1
addi $s6,$s6,1
blt $s6,$t1,inner_loop2
addi $s7,$s7,1
bnez $t8,outer_loop1
move $s4,$0
subi $s4,$s4,1
lw $s3,4($t4)
sw $s3,0($s5)
addi $t4,$t4,4
addi $s5,$s5,4
addi $s4,$s4,1
bne $s4,$t1,loop_final'''

l = inp.split('\n')

opcodes = {
    "move": "000000",
    "lw": "100011",
    "sw": "101011",
    "addi": "001000",
    "bne": "000101",
    "beq": "000100",
    "slt": "000000",
    "li": "001001",
    "sub": "000000",
    "jal": "000011",
    "j": "000010",
    "syscall": "00000000000000000000000000001100",
    "jr": "00000011111000000000000000001000",
}

reg = {
    "$at": "00001",
    "$0": "00000",
    "$t0": "01000",
    "$t1": "01001",
    "$t2": "01010",
    "$t3": "01011",
    "$t4": "01100",
    "$t5": "01101",
    "$t6": "01110",
    "$t7": "01111",
    "$t8": "11000",
    "$t9": "11001",
    "$s0": "10000",
    "$s1": "10001",
    "$s2": "10010",
    "$s3": "10011",
    "$s4": "10100",
    "$s5": "10101",
    "$s6": "10110",
    "$s7": "10111",
    "$zero": "00000",
}

address = {
    "loop_original": "1111111111111010",
    "Done": "0000000000010001",
    "no_swap": "0000000000001101",
    "inner_loop2": "0000000000001001",
    "outer_loop1": "1111111111101110",
    "loop_final": "1111111111111010",
    "print_inp_statement": "00010000000000000101001100",
    "input_int": "00010000000000000100011000",
    "print_inp_int_statement": "00010000000000000101100000",
    "print_out_int_statement": "00010000000000000101110100",
    "loop1end": "0000000000000110",
    "print_enter_int": "00010000000000000110001000",
    "loop1": "00010000000000000000101100",
    "end": "0000000000000110",
    "print_int": "00010000000000000100101000",
    "print_line": "00010000000000000100111000",
    "loop": "00010000000000000011110100",
    "next_line": "0000000000000000",
    "inp_statement": "0000000000000010",
    "inp_int_statement": "0000000000101111",
    "out_int_statement": "0000000001100101",
    "enter_int": "0000000010011101",
    "288": "0000000100100000",
    "4": "0000000000000100",
    "1": "0000000000000001",
    "0": "0000000000000000",
    "10": "0000000000001010",
    "5": "0000000000000101",
    "12": "0000000000001100",
}

out = []
for i in l:
    if(i.find('move') != -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        a3 = a1[1]
        ns = opcodes["move"] + reg["$0"] + reg[a3] + reg[a2] + "00000100001"
        out.append(ns)
    if(i.find('addi') != -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        a3 = a1[1]
        a4 = a1[2].rstrip()
        ns = opcodes["addi"] + reg[a3] + reg[a2] + address[a4]
        out.append(ns)
    if(i.find('subi') != -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        a3 = a1[1]
        a4 = a1[2].rstrip()
        ns = opcodes["addi"] + reg["$0"] + reg["$at"] + address[a4]
        out.append(ns)
        ns = opcodes["sub"] + reg[a3] + reg["$at"] + reg[a2] + "00000100010"
        out.append(ns)
    if(i.find('lw') != -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        l2 = a1[1].split("(")
        a3 = l2[0]
        a4 = l2[1].rstrip(")")
        ns = opcodes["lw"] + reg[a4] + reg[a2] + address[a3] 
        out.append(ns)
    if(i.find('sw') != -1 and i.find('swap') == -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        l2 = a1[1].split("(")
        a3 = l2[0]
        a4 = l2[1].rstrip(")")
        ns = opcodes["sw"] + reg[a4] + reg[a2] + address[a3]
        out.append(ns)
    if(i.find('bne') != -1 and i.find('bnez') == -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        a3 = a1[1]
        a4 = a1[2]
        ns = opcodes["bne"] + reg[a2] + reg[a3] + address[a4]
        out.append(ns)
    if(i.find('bnez') != -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        a4 = a1[1]
        a3 = '$0'
        ns = opcodes["bne"] + reg[a2] + reg[a3] + address[a4]
        out.append(ns)
    if(i.find('beq') != -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        a3 = a1[1]
        a4 = a1[2].rstrip()
        ns = opcodes["beq"] + reg[a2] + reg[a3] + address[a4]
        out.append(ns)
    if(i.find('bge') != -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        a3 = a1[1]
        a4 = a1[2]
        ns = opcodes["slt"] + reg[a2] + reg[a3] + reg['$at'] + "00000101010"
        out.append(ns)
        ns = opcodes["beq"] + reg['$at'] + reg['$0'] + address[a4]
        out.append(ns)
    if(i.find('blt') != -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        a3 = a1[1]
        a4 = a1[2]
        ns = opcodes["slt"] + reg[a2] + reg[a3] + reg['$at'] + "00000101010"
        out.append(ns)
        ns = opcodes["bne"] + reg['$at'] + reg['$0'] + address[a4]
        out.append(ns)
    if(i.find('li') != -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        a3 = a1[1]
        ns = opcodes["li"] + reg["$0"] + reg[a2] + address[a3]
        out.append(ns)
    if(i.find('mul') != -1):
        nl = i.split(" ")
        a1 = nl[1].split(",")
        a2 = a1[0]
        a3 = a1[1]
        a4 = a1[2]
        out.append(opcodes["addi"] + reg["$0"] + reg["$at"] + address[a4])
        out.append("01110010110000011000000000000010")
    if(i.find('jal') != -1):
        n1 = i.split(" ")
        a1 = n1[0]
        a2 = n1[1]
        ns = opcodes[a1] + address[a2]
        out.append(ns)
    if(i.find('jr') != -1):
        out.append(opcodes["jr"])
    if(i.find('j') != -1):
        n1 = i.split(" ")
        a1 = n1[0]
        a2 = n1[1]
        ns = opcodes[a1] + address[a2]
        out.append(ns)
    if(i.find('syscall') != -1):
        out.append(opcodes["syscall"])
    if(i.find('la') != -1):
        out.append("00111100000000010001000000000001")
        n1 = i.split(",")
        a1 = n1[0]
        a2 = n1[1]
        s1 = "0011010000100100"
        s2 = s1 + address[a2]
        out.append(s2)


for i in out:
    print(i)

