
import sys
import matplotlib.pyplot as plt
import math
import numpy as np
cycle_number=[]
memory_instruction=[]
memory_instruction_number=0
l=sys.stdin.read().split("\n")
l=l[:-1]
i=0
for x in l:
    lst=[]
    for j in range(len(x)):
        lst.append(int(x[j]))
    x=lst
def string_to_value(str1):
    res=0
    i=0
    for j in range(len(str1)-1,-1,-1):
        res+=int(str1[j])*pow(2,i)
        i+=1
    return res
for i in range(256-len(l)):
    l.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
pc=[0,0,0,0,0,0,0,0]
def Memory(address):
    return l[address]
def register_file(register_name):
    return value_from_list(register_values[register_name])
def decimal_to_binary(n):
    n=int(n)
    return bin(n).replace("0b","")
def pc_and_register_values():
    
    str1=""
    for i in pc:
        str1+=str(i)
    x=string_to_value(str1)
    x=x-1
    str1=decimal_to_binary(x)
    n=""
    for i in range(8-len(str1)):
        n+="0"
    for x in str1:
        n+=x
    str1=n
    str1+=" "
    for i in register_values.values():
        for j in i:
            str1+=str(j)
        str1+=" "
    

    sys.stdout.write(str1+"\n")
def memory_value():
    for x in l:
        str2=""
        for j in x:
            str2+=str(j)
        sys.stdout.write(str2+"\n")
Opcode={"10000":"add","10001":"sub","10010":"mov_type_B","10011":"mov_type_C","10100":"ld","10101":"st","10110":"mul","10111":"div","11000":"rs","11001":"ls","11010":"xor","11011":"or","11100":"and","11101":"not","11110":"cmp","11111":"jmp","01100":"jlt","01101":"jgt","01111":"je","01010":"hlt"}
Register_address={"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS"}
# Bits initiated with 0 and unused bits remain 0
register_values={

"R0":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"R1":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"R2":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"R3":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"R4":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"R5":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"R6":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"FLAGS":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
def binary_to_decimal(n):
    s=register_values[Register_address[n]]
    s1=""
    for x in s:
        s1+=str(x)
    return int(s1,2)
def value_from_list(instruction):
    res=0
    i=0
    for j in range(len(instruction)-1,-1,-1):
        
        res+=int(instruction[j])*math.pow(2,i)
        
        i+=1
    return res
def list_from_value(number):
    lst=[]
    
    s=str(bin(int(number)))
    s=s[2:]
    if(len(s)>16):
        s=s[0:16]
        for x in s:
            lst.append(int(x))
        
    else:
        for j in range(16-len(s)):
            lst.append(0)
        for j in s:
            lst.append(int(j))
    return lst

def pc_value(i):
    x=str(bin(i))
    x=x[2:]
    if(len(x)<8):
        x=x+(8-len(x))*"0"
    return x
def overflow(number,key_type):
    if(key_type=="add"):
        if(number>pow(2,16)-1):
            return 1
        return 0
    if(key_type=="mul"):
        if(number>pow(2,16)-1):
            return 1
        return 0
    if(key_type=="sub"):
        if(number<0):
            return 1
        return 0
def reset_flag():
    for i in range(16):
        register_values["FLAGS"][i]=0
def cycle_and_memoryindex():
    global memory_instruction_number
    global pc

    cycle_number.append(memory_instruction_number)
    memory_instruction_number+=1
    memory_instruction.append(value_from_list(pc))
    pc=list_from_value(value_from_list(pc)+1)
    pc=pc[8:]
def operation(key_type, instruction1):

    global memory_instruction_number
    global pc
    instruction=""
    for x in instruction1:
        instruction+=x
    if(key_type=="add"):
        x1=instruction[7:10]
        
        x2=instruction[10:13]
        x3=instruction[13:16]
        
        x2_val=binary_to_decimal(x2)
        x3_val=binary_to_decimal(x3)
        
        add_result=x2_val+x3_val
        
        reset_flag()
        if(overflow(add_result,key_type)):
            register_values["FLAGS"][12]=1
        register_values[Register_address[x1]]=list_from_value(add_result)
        cycle_and_memoryindex()
    elif(key_type=="sub"):
        x1=instruction[7:10]
        x2=instruction[10:13]
        x3=instruction[13:16]
        x2_val=binary_to_decimal(x2)
        x3_val=binary_to_decimal(x3)
        sub_result=x2_val-x3_val
        reset_flag()
        if(overflow(sub_result,key_type)):
            register_values["FLAGS"][12]=1
            register_values[Register_address[x1]]=list_from_value(0)
        else:
            register_values[Register_address[x1]]=list_from_value(sub_result)
        cycle_and_memoryindex()
    elif(key_type=="mul"):
        
        x1=instruction[7:10]
        
        x2=instruction[10:13]
        x3=instruction[13:]
        x2_val=binary_to_decimal(x2)
        
        x3_val=binary_to_decimal(x3)
        mul_result=x2_val*x3_val
        
        reset_flag()
        if(overflow(mul_result,key_type)):
            register_values["FLAGS"][12]=1
        register_values[Register_address[x1]]=list_from_value(mul_result)
        cycle_and_memoryindex()
    elif(key_type=="xor"):
        x1=instruction[7:10]
        x2=instruction[10:13]
        x3=instruction[13:16]
        x2_val=binary_to_decimal(x2)
        x3_val=binary_to_decimal(x3)
        xor_result=x2_val^x3_val
        reset_flag()
        register_values[Register_address[x1]]=list_from_value(xor_result)
        cycle_and_memoryindex()
    elif(key_type=="or"):
        x1=instruction[7:10]
        x2=instruction[10:13]
        x3=instruction[13:16]
        x2_val=binary_to_decimal(x2)
        x3_val=binary_to_decimal(x3)
        or_result=x2_val|x3_val
        reset_flag()
        register_values[Register_address[x1]]=list_from_value(or_result)
        cycle_and_memoryindex()
    elif(key_type=="and"):
        x1=instruction[7:10]
        x2=instruction[10:13]
        x3=instruction[13:16]
        x2_val=binary_to_decimal(x2)
        x3_val=binary_to_decimal(x3)
        and_result=x2_val&x3_val
        reset_flag()
        register_values[Register_address[x1]]=list_from_value(and_result)
        cycle_and_memoryindex()
    elif(key_type=="mov_type_B"):
        x1=instruction[5:8]
        immediate=[]
        immediate.append(instruction[8:])
        imm=[]
        for i in range(8):
            imm.append(0)
        for x in immediate:
            imm.append(x)
        reset_flag()
        register_values[Register_address[x1]]=imm
        cycle_and_memoryindex()
    elif(key_type=="ls"):
        x1=instruction[5:8]
        imm=instruction[8:]
        
        
        reset_flag()
        
        s1=binary_to_decimal(x1)
        s2=binary_to_decimal(imm)
        s3=s1<<s2

        register_values[Register_address[x1]]=list_from_value(s3)
        cycle_and_memoryindex()
    elif(key_type=="rs"):
        x1=instruction[5:8]
        immediate=instruction[8:]
        
        s1=binary_to_decimal(register_values[Register_address[x1]])
        s2=binary_to_decimal(immediate)
        s3=s1>>s2
        reset_flag()
        register_values[Register_address[x1]]=list_from_value(s3)
        cycle_and_memoryindex()
    elif(key_type=="mov_type_C"):
        x1=instruction[10:13]
        x2=instruction[13:]
        reset_flag()
        register_values[Register_address[x1]]=register_values[Register_address[x2]].copy()
        cycle_and_memoryindex()
    elif(key_type=="div"):
        x1=instruction[10:13]
        x2=instruction[13:]
        reset_flag()
        register_values["R0"]=list_from_value(value_from_list(register_values[Register_address[x1]])/value_from_list(register_values[Register_address[x2]]))
        register_values["R1"]=list_from_value(value_from_list(register_values[Register_address[x1]])%value_from_list(register_values[Register_address[x2]]))
        cycle_and_memoryindex()
    elif(key_type=="not"):
        x1=instruction[10:13]
        x2=instruction[13:]
        reset_flag()
        x1_val=[]
        x1_val=register_values[Register_address[x1]]
        for x in x1_val:
            if(x==0):
                x=1
            else:
                x=0
        register_values[Register_address[x2]]=x1_val.copy()
        cycle_and_memoryindex()
    elif(key_type=="cmp"):
        x1=instruction[10:13]
        x2=instruction[13:]
        reset_flag()
        x1_val=value_from_list(register_values[Register_address[x1]])
        x2_val=value_from_list(register_values[Register_address[x2]])
        if(x1_val<x2_val):
            register_values["FLAGS"][13]=1
        elif(x1_val==x2_val):
            register_values["FLAGS"][15]=1
        elif(x1_val>x2_val):
            register_values["FLAGS"][14]=1
        cycle_and_memoryindex()
    elif(key_type=="ld"):
        x1=instruction[5:8]
        address=instruction[8:]
        ls=len(address)
        sum=0
        ls-=1
        for i in address:
            sum+=int(i)*pow(2,ls)
            ls-=1
        value=Memory(sum)
        reset_flag()
        register_values[Register_address[x1]]=value
        cycle_and_memoryindex()
    elif(key_type=="st"):
        x1=instruction[5:8]
        address=instruction[8:]
        ls=len(address)
        sum=0
        ls-=1
        for i in address:
            sum+=int(i)*pow(2,ls)
            ls-=1
        reset_flag()
        l[sum]=register_values[Register_address[x1]]
        cycle_and_memoryindex()
    elif(key_type=="jmp"):
        address_mem=instruction[8:]
        reset_flag()
        cycle_number.append(memory_instruction_number)
        memory_instruction_number+=1
        memory_instruction.append(value_from_list(pc))
        pc=list_from_value(string_to_value(address_mem))
        pc=pc[8:]
    elif(key_type=="jlt"):
        address_mem=instruction[8:]
        if(register_values["FLAGS"][3]==1):
            pc_new=list_from_value(string_to_value(address_mem))
            pc_new=pc_new[8:]
            reset_flag()
            cycle_number.append(memory_instruction_number)
            memory_instruction_number+=1
            memory_instruction.append(value_from_list(pc))
            pc=pc_new
        else:
            reset_flag()
            cycle_number.append(memory_instruction_number)
            memory_instruction_number+=1
            memory_instruction.append(value_from_list(pc))
            pc=list_from_value(value_from_list(pc)+1)
            pc=pc[8:]
    elif(key_type=="jgt"):
        address_mem=instruction[8:]
        if(register_values["FLAGS"][2]==1):
            pc_new=list_from_value(string_to_value(address_mem))
            pc_new=pc_new[8:]
            reset_flag()
            cycle_number.append(memory_instruction_number)
            memory_instruction_number+=1
            memory_instruction.append(value_from_list(pc))
            pc=pc_new
        else:
            reset_flag()
            cycle_number.append(memory_instruction_number)
            memory_instruction_number+=1
            memory_instruction.append(value_from_list(pc))
            pc=list_from_value(value_from_list(pc)+1)
            pc=pc[8:]
    elif(key_type=="je"):
        address_mem=instruction[8:]
        if(register_values["FLAGS"][4]==1):
            pc_new=list_from_value(string_to_value(address_mem))
            pc_new=pc_new[8:]
            reset_flag()
            cycle_number.append(memory_instruction_number)
            memory_instruction_number+=1
            memory_instruction.append(value_from_list(pc))
            pc=pc_new
        else:
            reset_flag()
            
            pc=list_from_value(value_from_list(pc)+1)
            pc=pc[8:]
    
    pc_and_register_values()
def plot_memory_accesses():
    arr1=np.array(cycle_number)
    arr2=np.array(memory_instruction)
    plt.scatter(arr1,arr2)
    plt.title("Memory access in each cycle")
    plt.xlabel("Cycle")
    plt.ylabel("Address")
    plt.show()
def run():
    key_type=""
    global pc
    while key_type!="hlt":
        ind=value_from_list(pc)
        
        instruction=Memory(int(ind))
        opcode_1=""
        for i in range(5):
            opcode_1+=instruction[i]
        key_type=Opcode[opcode_1]
        if(key_type!="hlt"):
            operation(key_type,instruction)
        else:
            x=value_from_list(pc)
            x+=1
            pc=list_from_value(x)
            pc_and_register_values()
run()
memory_value()
plot_memory_accesses()