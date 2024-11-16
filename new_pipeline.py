def fetch_instruction(instruction_memory,pc):           #fetch data from instruction memory
    return instruction_memory[pc]


def binary_neg_decimal(decimal_value):                  #converting negative numbers, to reach back to required instruction memory address
    if decimal_value & 0x8000: 
        decimal_value = -((1 << 16) - decimal_value)
    return decimal_value


def decode_instruction(instruction,reg_memory):         #decode the fetched instruction
    op=instruction[0:6]
    opcodes = {
    "000000":"r_type" ,
    "100011":"lw" ,
    "101011":"sw",
    "001000":"addi", 
    "000101":"bne",
    "000100":"beq",
    "011100":"mul",
    "001001":"li",
    "000011":"jal",
    "000010":"j"}

    reg={
        "00001":"$at", 
        "00101":"$a1",
        "00000":"$0",
        "01000":"$t0" ,
        "01001":"$t1",
        "01010":"$t2",
        "01011":"$t3",
        "01100":"$t4",
        "01101": "$t5",
        "01110": "$t6",
        "01111": "$t7",
        "11000": "$t8",
        "11001": "$t9",
        "10000": "$s0",
        "10001": "$s1",
        "10010": "$s2",
        "10011": "$s3",
        "10100": "$s4",
        "10101": "$s5",
        "10110": "$s6",
        "10111": "$s7"
    }



    for e in opcodes:
        if(e==op):
            str=opcodes[op]
            if(str=="r_type"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                rd=instruction[16:21]
                shamt=instruction[21:26]
                funct=instruction[26:32]
                rs=reg[rs]
                rt=reg[rt]
                rd=reg[rd]
                shamt=int(shamt,2)
                funct=int(funct,2)
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                rd1=reg_memory[rd]
                l=[rs1,rt1,rd1,shamt,funct,rd,rs,rt]
                return l

            elif(str=="lw"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[opcodes[op],rs1,rt1,imm,rt,rs]
                return l

            elif(str=="addi"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[opcodes[op],rs1,rt1,imm,rt,rs]
                return l

            elif(str=="beq"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[opcodes[op],rs1,rt1,imm,rt,rs]
                return l

            elif(str=="bne"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[opcodes[op],rs1,rt1,imm,rt,rs]
                return l

            elif(str=="sw"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[opcodes[op],rs1,rt1,imm,rt,rs]
                return l

            elif(str=="li"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[opcodes[op],rs1,rt1,imm,rt,rs]
                return l

            elif(str=="mul"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                rd=instruction[16:21]
                shamt=instruction[21:26]
                funct=instruction[26:32]
                rs=reg[rs]
                rt=reg[rt]
                rd=reg[rd]
                shamt=int(shamt,2)
                funct=int(funct,2)
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                rd1=reg_memory[rd]
                l=[rs1,rt1,rd1,shamt,funct,rd,rs,rt]
                return l

            




def execute_instruction(l,pc, reg_memory):
    wb=0 #Control Lines-Write back
    wm=0 #Control Lines-Write Memory
    rm=0 #Control Lines-Read Memory
    m=[]
    
    if(len(l)==8): #r_type format
        
        funct=l[4]
        if(funct==33): #move
            wb=1
            wm=0
            rm=0
            l[2]=reg_memory[l[6]]
            m=[wb,wm,rm,l[2],l[5]]
            return m

        elif(funct==32): #add
            wb=1
            wm=0
            rm=0
            l[2]=reg_memory[l[7]]+reg_memory[l[6]]
            m=[wb,wm,rm,l[2],l[5]]
            return m

        elif(funct==0): #sll
            wb=1
            wm=0
            rm=0
            l[2]=reg_memory[l[6]]*((2*l[3])//4)
            m=[wb,wm,rm,l[2],l[5]]
            return m

        elif(funct==34): #sub
            wb=1
            wm=0
            rm=0
            l[2]=reg_memory[l[6]]-reg_memory[l[7]]
            m=[wb,wm,rm,l[2],l[5]]
            return m
            
        elif(funct==42):#slt
            wb=1
            wm=0
            rm=0
            if(reg_memory[l[6]]<reg_memory[l[7]]):
                l[2]=1
            else:
                l[2]=0
            m=[wb,wm,rm,l[2],l[5]]
            return m
        
        elif(funct==2):#mul
            wb=1
            wm=0
            rm=0
            l[2]=reg_memory[l[7]]*reg_memory[l[6]]
            m=[wb,wm,rm,l[2],l[5]]
            return m


    elif(len(l)==6): #i-type format
        op=l[0]
        imm=l[3]
        if(op=='addi'):#addi
            wb=1
            wm=0
            rm=0
            if(imm>1000):
                imm=binary_neg_decimal(imm)
                if(imm<-3):
                    imm=imm//4 
            if(imm>3):
                imm=imm//4
            l[2]=l[1]+imm
            m=[wb,wm,rm,l[2],l[4]]
            return m

        elif(op=='lw'): #lw
            wb=1
            rm=1
            wm=0
            imm=imm//4
            x=imm+l[1]
            m=[wb,wm,rm,x,l[2],l[4]]
            return m

        elif(op=='sw'): #sw
            wm=1
            wb=0
            rm=0
            imm=imm//4
            x=l[1]+imm
            m=[wb,wm,rm,x,l[2],l[4]]
            return m

        elif(op=='li'):#li
            wb=1
            wm=0
            rm=0
            if(imm>1000):
                imm=binary_neg_decimal(imm)
                if(imm<-3):
                    imm=imm//4 
            if(imm>3):
                imm=imm//4
            l[2]=l[1]+imm
            m=[wb,wm,rm,l[2],l[4]]
            return m
        
        elif(op=='bne'):#bne
            wb=0
            wm=0
            rm=0
            if(imm>1000):
                imm=binary_neg_decimal(imm)
            if(l[2]!=l[1]):
                pc=pc+imm+1
                m=[wb,wm,rm,pc]
                return m
            else:
                m=[wb,wm,rm,pc]
                return m

        elif(op=='beq'):#beq
            wb=0
            wm=0
            rm=0
            if(imm>1000):
                imm=binary_neg_decimal(imm)
            if(l[2]==l[1]):
                pc=pc + imm + 1
                m=[wb,wm,rm,pc]
                return m
            else:
                m=[wb,wm,rm,pc]
                return m

        



def memory_access(wm,rm,data_memory,x,rt1):
    if(rm==1):                          #if only need to read, written the current data_memory
        return data_memory[x],data_memory

    if(wm==1):                          #if writing to mem signal is 1, write to data_memory
        data_memory[x]=rt1
        return rt1,data_memory




def write_back(wb,reg_memory,rd1,rd):
    if(wb==1):                             #if write back signal is 1, write to reg_memory
        if(rd=='$s0'):
            rd1=abs(rd1)
        reg_memory[rd]=rd1
    return reg_memory




def find_dep(instruction_memory):           #finding dependencies
    dependency=[0]*len(instruction_memory)
    dep={}
    opcodes = {
    "000000":"r_type",
    "100011":"lw" ,
    "101011":"sw",
    "001000":"addi",
    "000101":"bne",
    "000100":"beq",
    "011100":"mul",
    "001001":"li",
    "000011":"jal",
    "000010":"j"}

    reg={
        "00001":"$at", #temporary reg for pseudo code
        "00101":"$a1",
        "00000":"$0",
        "01000":"$t0" ,
        "01001":"$t1",
        "01010":"$t2",
        "01011":"$t3",
        "01100":"$t4",
        "01101": "$t5",
        "01110": "$t6",
        "01111": "$t7",
        "11000": "$t8",
        "11001": "$t9",
        "10000": "$s0",
        "10001": "$s1",
        "10010": "$s2",
        "10011": "$s3",
        "10100": "$s4",
        "10101": "$s5",
        "10110": "$s6",
        "10111": "$s7"
    }
    c=0
    for i in range(0,len(instruction_memory)):
        instruction=instruction_memory[i]
        op=instruction[0:6]
        str=opcodes[op]

        if(str=='r_type'):
            c+=1
            rs=instruction[6:11]
            rt=instruction[11:16]
            rd=instruction[16:21]
            rs=reg[rs]
            rt=reg[rt]
            rd=reg[rd]
            dep[rd]=i
            if(rs in dep):
                dependency[i]=True

            elif(rt in dep):
                dependency[i]=True

            if(c%3==0):
                dep={}
                dep[rd]=i

        if(str=='mul'):
            c+=1
            rs=instruction[6:11]
            rt=instruction[11:16]
            rd=instruction[16:21]
            rs=reg[rs]
            rt=reg[rt]
            rd=reg[rd]
            dep[rd]=i
            if(rs in dep):
                dependency[i]=True

            if(rt in dep):
                dependency[i]=True

            if(c%3==0):
                c=0
                dep={}
                dep[rd]=i



        elif(str=='addi'):
            c+=1
            rs=instruction[6:11]
            rt=instruction[11:16]
            rs=reg[rs]
            rt=reg[rt]
            if(rs in dep):
                dependency[i]=True
                if(c%3==0):
                    c=0
                    dep={}
                    dep[rt]=i
                continue
            elif(rs==rt):
                dep[rt]=i
                if(c%3==0):
                    c=0
                    dep={}
                    dep[rt]=i
                continue
            dep[rt]=i
            if(rs in dep):
                dependency[i]=True

            if(c%3==0):
                c=0
                dep={}
                dep[rt]=i

        elif(str=='lw'):
            c+=1
            rs=instruction[6:11]
            rt=instruction[11:16]
            rs=reg[rs]
            rt=reg[rt]
            if(rs in dep):
                dependency[i]=True
                if(c%3==0):
                    c=0
                    dep={}
                    dep[rt]=i
                continue
            elif(rs==rt):
                dep[rt]=i
                if(c%3==0):
                    c=0
                    dep={}
                    dep[rt]=i
                continue
            dep[rt]=i
            if(rs in dep):
                dependency[i]=True

            if(c%3==0):
                c=0
                dep={}
                dep[rt]=i

        elif(str=='sw'):
            c+=1
            rs=instruction[6:11]
            rt=instruction[11:16]
            rs=reg[rs]
            rt=reg[rt]
            if(rs in dep):
                dependency[i]=True

            if(rt in dep):
                dependency[i]=True

            if(c%3==0):
                c=0
                dep={}

        elif(str=='beq'):
            c+=1
            rs=instruction[6:11]
            rt=instruction[11:16]
            rs=reg[rs]
            rt=reg[rt]
            if(rs in dep):
                dependency[i]=True

            if(rt in dep):
                dependency[i]=True

            if(c%3==0):
                c=0
                dep={}

        elif(str=='bne'):
            c+=1
            rs=instruction[6:11]
            rt=instruction[11:16]
            rs=reg[rs]
            rt=reg[rt]
            if(rs in dep):
                dependency[i]=True

            if(rt in dep):
                dependency[i]=True

            if(c%3==0):
                c=0
                dep={}

    return dependency

def main():
    #factorial
    instruction_memory=[
        "00100000000011100000000000000000",
        "00100001010011110000000000000000",
        "00100001011110000000000000000000",
        "10001101010011000000000000000000",
        "00100001110011100000000000000001",
        "00100000000011010000000000000001",
        "00010001100000000000000000001011",
        "00100010010100100000000000000000",
        "00100010011100110000000000000000",
        "00100010100101000000000000000000",
        "01110001101011000110100000000010",
        "00100001100011001111111111111111",
        "00100010000100000000000000000000",
        "00100010001100010000000000000000",
        "00010101100000001111111111111011",
        "10101101011011010000000000000000",
        "00100001010010100000000000000100",
        "00100001011010110000000000000100",
        "00100001100011000000000000000001",
        "00100010010100100000000000000000",
        "00100010011100110000000000000000",
        "00100010100101000000000000000000",
        "10101101011011000000000000000000",
        "00010101110010011111111111101011",
        "00100001111010100000000000000000",
        "00100011000010110000000000000000",
    ]

    #fibo
    '''instruction_memory = [
        "00100000000011110000000000000000",
        "00100001010100010000000000000000",
        "00100001011100100000000000000000",
        "10001101010010000000000000000000",
        "00100000000011000000000000000000",
        "00100000000011010000000000000000",
        "00100000000110000000000000000001",
        "00100001111011110000000000000001",
        "00100000000000010000000000000001",
        "00000001000000010100000000100010",
        "00000001100011010111000000100000",
        "00000001100110000110100000100000",
        "00000001110000000110000000100000",
        "00010101000000001111111111111010",
        "00100001010010100000000000000100",
        "10101101011011010000000000000000",
        "00100001011010110000000000000100",
        "00010101001011111111111111110001",
        "00100010001010100000000000000000",
        "00100010010010110000000000000000",
    ]'''

    n=len(instruction_memory)
    a=1
    b=int(input("Enter base address of input:"))
    c=int(input("Enter base address of output:"))
    flag=0
    dep = find_dep(instruction_memory)
    reg_memory={
            "$0":0,
            "$at":0,
            "$a1":0,
            "$s0":0,
            "$s1":0,
            "$s2":0,
            "$s3":0,
            "$s4":0,
            "$s5":0,
            "$s6":0,
            "$s7":0,
            "$t0":0,
            "$t1":a,
            "$t2":b,
            "$t3":c,
            "$t4":0,
            "$t5":0,
            "$t6":0,
            "$t7":0,
            "$t8":0,
            "$t9":0}

    pc=0
    data_memory=[0]*200
    tempf=[]
    temp_instr=[]
    stalls=[0]*5*n
    stallscpy = [0]*5*n
    stallscpy1 = [0]*5*n
    stallscpy2 = [0]*5*n
    stallscpy3 = [0]*5*n
    f = 0
    for i in range(b,b+a):
            e=int(input("Enter the number:"))
            data_memory[i]=e
    if(data_memory[b] == 0):
        f = 1

    for i in range (0,len(dep)):
        if(dep[i] == True):
            stalls[i] = 2
            stallscpy[i] = 2
            stallscpy1[i] = 2
            stallscpy2[i] = 2
            stallscpy3[i] = 2
    clock = 4
    d = 21
    pc1 = pc
    li = []
    pt = 0
    chkpt = 0
    jmp = 0
    fetch_idx = 0           #index from where data needs to be fetched
    dec_idx = 0             #index from where data needs to be decoded
    exe_idx = 0             #index from where data needs to be executed
    mem_idx = 0             #index from where data needs to be written back/read from the memory
    wb_idx = 0              #index from where data needs to be written back to registers
    while(pc<100*n and f == 0):
        if((pc-4)>-1 and wb_idx < 5*n):#Write Back
            if(wb_idx < len(tempf)):            #if all instructions are not written back once
                if(stallscpy3[wb_idx] == 0):    #if there is no dependency
                    if(len(tempf[wb_idx])==6):          #check the type of instruction
                        m=tempf[wb_idx]
                        reg_memory=write_back(m[0],reg_memory,m[4],m[5])

                    elif(len(tempf[wb_idx])==5):
                        m=tempf[wb_idx]
                        reg_memory=write_back(m[0],reg_memory,m[3],m[4])
                    wb_idx += 1                 #increase to extract next instsruction
                    flag=1
                else:
                    stallscpy3[wb_idx] -= 1         #if dependent on other instruction wait until the other goes through the memory stage
            

        if((pc-3)>-1 and mem_idx < 5*n):#Memory
            if(mem_idx < len(tempf)):
                if(stallscpy2[mem_idx] == 0):
                    if(len(tempf[mem_idx])==6):
                        m=tempf[mem_idx]
                        m[4],data_memory=memory_access(m[1],m[2],data_memory,m[3],m[4])
                        #tempf[pc-3]=m

                    elif(len(tempf[mem_idx])==4):
                        pc=tempf[mem_idx][3]
                    mem_idx += 1
                    flag=1   
                else:
                    stallscpy2[mem_idx] -= 1



        if((pc-2)>-1 and exe_idx < 5*n):#ALU
            if(exe_idx < len(tempf)):
                if(stallscpy1[exe_idx] == 0):
                    m=execute_instruction(tempf[exe_idx],exe_idx,reg_memory)
                    flag=1
                    tempf[exe_idx]=m
                    exe_idx += 1
                else:
                    stallscpy1[exe_idx] -= 1


        l=[]
        m=[]        


        if((pc-1) > -1 and dec_idx < 5*n):
            if(dec_idx < len(temp_instr)):
                if(dec_idx == 0):
                    l=decode_instruction(temp_instr[dec_idx],reg_memory)
                    tempf.append(l)
                    dec_idx += 1
                else:
                    if(stallscpy[dec_idx] == 0):
                        l=decode_instruction(temp_instr[dec_idx],reg_memory)
                        if(chkpt == 1):             #if the instruction is dependent remove the last decoded instruction, as it is not required
                            tempf.pop()
                            chkpt = 0
                        tempf.append(l)
                        dec_idx += 1
                    elif(stallscpy[dec_idx] > -1):      #if the instruction is dependent
                        l=decode_instruction(temp_instr[dec_idx],reg_memory)
                        if(stallscpy[dec_idx] < 2):     
                            tempf.pop()                 #remove the previously decoded same instruction
                            chkpt = 1
                        tempf.append(l)
                        stallscpy[dec_idx] -= 1         #reduce the stalls now needed

        if(pc > -1 and fetch_idx < n):
            if(fetch_idx == 0):
                instruction = fetch_instruction(instruction_memory, fetch_idx)
                temp_instr.append(instruction)
                fetch_idx += 1
            else:
                if(stalls[fetch_idx-1] == 0):           #check if the previous instruction is dependent or not
                    instruction = fetch_instruction(instruction_memory, fetch_idx)
                    if(pt == 1):
                        temp_instr.pop()
                        pt = 0
                    temp_instr.append(instruction)
                    fetch_idx += 1
                    l=decode_instruction(temp_instr[fetch_idx-2],reg_memory)
                    m=execute_instruction(l,fetch_idx-2,reg_memory)
                    if(l[0] == 'beq' or l[0] == 'bne'):         #if instruction has beq or bne
                        if(l[0] == 'beq' and l[1] == l[2]):
                            fetch_idx = m[3]                    #change fetch_idx to the jump address
                        elif(l[0] == 'bne' and l[1] != l[2]):
                            fetch_idx = m[3]
                elif(stalls[fetch_idx-1] > -1):
                    instruction = fetch_instruction(instruction_memory, fetch_idx)
                    if(stalls[fetch_idx-1] < 2):
                        temp_instr.pop()
                        pt = 1
                    temp_instr.append(instruction)
                    stalls[fetch_idx-1] -= 1            #reduce the stalls needed in fetch stage if previous instruction has dependency
            clock += 1
        
        pc+=1
        



    print(reg_memory)
    x=reg_memory["$t3"]
    y=reg_memory["$t1"]

    if(f == 0):
        for i in range(x,x+y):
            print(data_memory[i])
        print(f"Clock Cycles:{clock}")
    else:
        print(1)
        print(f"Clock Cycles:{d}")
    print("\n")
    
    
   
main()