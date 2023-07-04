import sys
l1=sys.stdin.read().split("\n")

i=0
 
l1=l1[:-1]

#hlt cases
if (l1.count("hlt")==0):
    print("Missing hlt Instruction")
    exit()

if(l1.count("hlt")>1):
    x=l1.index("hlt",l1.index("hlt")+1)+1
    print(f"Error on line: {x}")
    print("Multiple halts")
    exit()

binary_codes=[]
#print(l1)
#syntax error	
def syntax_error(lst,i):	
    ty=type_of_instruction(lst)	
    if ty=="A":	
        if len(lst)!=4:
            print("Error at line",i+1)	
            print("Syntax error")
            exit()	
    elif ty==("B" or "C" or "D"):	
        if len(lst)!=3:	
            print("Error at line",i+1)
            print("Syntax error")
            exit()	
    elif ty=="E":	
        if len(lst)!=2:	
            print("Error at line",i+1)
            print("Syntax error")
            exit()	
    elif ty=="F":	
        if len(lst)!=1:	
            print("Error at line",i+1)
            print("Syntax error")
            exit()
     

	#key Error check kr	
def keycheck(x,dict,i):	
    if(x in dict):	
        pass	
    else:	
        if(dict==Register_address):	
            print(f"Typo Error in resistor name in line: {i+1}")	
        elif(dict==var_codes):	
            print(f"Error in line: {i+1}\nUndefined Variable")	
        exit()	

count=0
for i in l1:
    str1=i[0:3]
    if str1=="var":
        count+=1
#print(count)
var_codes={}    
length=len(l1)
n=length-count
for j in range(count):
    st2=str(bin(n))

    st1=st2[2:]
    s3=""
    for i in range(8-len(st1)):
        s3+="0"
    s3+=st1
    
    st4=l1[j][4]
    var_codes[st4]=s3
    n+=1
#print(var_codes)
"""
for i in range(n):
    temp=l[i].split()
    if(temp[-1]=="FLAGS" and temp[0]=="mov"):
        pass
    else:
        print("Error at line:",i)
        print("Illegal use of FLAGS")
"""

j=0
label_code={}
while(j<count+1):
    temp=l1[j].split()
    if(temp[0][-1]==":"):
        
        x=temp[0][0:-1]
        
        st7=bin(j)
        s6=str(st7)
        s6=s6[2:]
        s5=""
        for i in range(8-len(s6)):
            s5+="0"
        s5+=s6
        label_code[x]=s5
    j=j+1
#print(label_code)
Opcode={"add":"10000","sub":"10001","mov_type_B":"10010","mov_type_C":"10011","ld":"10100","st":"10101","mul":"10110","div":"10111","rs":"11000","ls":"11001","xor":"11010","or":"11011","and":"11100","not":"11101","cmp":"11110","jmp":"11111","jlt":"01100","jgt":"01101","je":"01111","hlt":"01010"}
Register_address={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
# Bits initiated with 0 and unused bits remain 0
R0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R1=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R2=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R3=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R4=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R5=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R6=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
FLAGS=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
def type_of_instruction(instruction):
    if(instruction[0][-1]==":"):
        instruction=instruction[1:]
    instruction_type=''
    if instruction[0]=="add" or instruction[0]=="sub" or instruction[0]=="mul" or instruction[0]=="xor" or instruction[0]=="or" or instruction[0]=="and":
        instruction_type='A'
    elif instruction[0]=="mov" or instruction[0]=="ls" or instruction[0]=="rs":
        if instruction[0]=="mov":
            if(instruction[-1][0]=='$'):
                instruction_type='B'
            else:
                instruction_type='C'
        else:
            instruction_type='B'
    elif instruction[0]=="div" or instruction[0]=="not" or instruction[0]=="cmp":
        instruction_type='C'
    elif instruction[0]=="ld" or instruction[0]=="st":
        instruction_type='D'
    elif instruction[0]=="jmp" or instruction[0]=="jlt" or instruction[0]=="jgt" or instruction[0]=="je":
        instruction_type='E'
    elif instruction[0]=="hlt":
        instruction_type='F'
    return instruction_type

def wrong_constant_error(temp,i):
    if(temp[2][0]=="$"):
        n=int(temp[2][1::])
        if(n<0 or n>255):
            print(f"Error at line {i}\nInvalid Imm!")
            exit()
  




          

i=0
while i<len(l1):
    
    # print(l[i].split()[0])
    lst=l1[i].split()
    if(lst[0][-1]==":"):
            lst=lst[1:]
    if lst[0]=="var":
        if(l1[i].rstrip().count(" ")>1):	
            print(f"Gernal Syntax Error at line: {i+1}")	
            exit()
        pass
    else :
        type=type_of_instruction(lst)
        
        s=""
        
        if type=="A":
            
            syntax_error(lst,i)
            s0=""
            s0+=Opcode[lst[0]]
            s0+="00"
            keycheck(lst[1],Register_address,i)
            s0+=Register_address[lst[1]]
            keycheck(lst[2],Register_address,i)
            s0+=Register_address[lst[2]]
            keycheck(lst[3],Register_address,i)
            s0+=Register_address[lst[3]]
            s+=s0
            binary_codes.append(s)
        elif type=="B":
            
            syntax_error(lst,i)
            s0=""
            if(lst[0]=="mov"):
                wrong_constant_error(lst,i+1)
                s0+=Opcode["mov_type_B"]
            else:
                s0+Opcode[lst[0]]
            keycheck(lst[1],Register_address,i)
            s0+=Register_address[lst[1]]
            s1=str(bin(int(lst[2][1:])))[2::]
            s2=""
            for j in range(len(s1),8):
                s2+="0"
            s1=s2+s1
            s+=s1
            # print(s1,"\n")
            s+=s1
            binary_codes.append(s)
        elif type=="C":
            
            syntax_error(lst,i)
            s0=""
            if(lst[0]=="mov"):
                s0+=Opcode["mov_type_C"]
            else:
                s0+=Opcode[lst[0]]
            s0+="00000"
            keycheck(lst[1],Register_address,i)	
            s0+=Register_address[lst[1]]	
            keycheck(lst[2],Register_address,i)
            s0+=Register_address[lst[2]]
            s=s0
            binary_codes.append(s)
        elif type=="D":
            
            syntax_error(lst,i)
            s+=Opcode[lst[0]]
            s+=Register_address[lst[1]] 
            if(lst[-1] not in var_codes):
                print("Error at line:",i)
                print("Variable not defined")
                exit()
            s+=var_codes[lst[-1]]
            binary_codes.append(s)
            ## memory addres left
        elif type=="E":
            	
           
            syntax_error(lst,i)
            s+=Opcode[lst[0]]
            s+="000"
            if(lst[-1] not in label_code):
                print("Error at line:",i)
                print("Label not defined")
                exit()
            s+=label_code[lst[-1]]
            binary_codes.append(s)
            ## memory address left 
        elif type=="F":
            
            
            syntax_error(lst,i)
            s+=Opcode[lst[0]]
            s+="0"*11
            binary_codes.append(s)
        elif type=='':
            print("Error at Line:",i+1)
            print("Typo Error")
            exit()
            
        
        
        
    i+=1
for i in binary_codes:
    print(i)
              
    # print(x)
    # s=""
    
    # if x[0]=="mov" and type=="B":
    #     s+=Opcode["mov_type_B"]
    # elif x[0]=="mov" and type=="C":
    #     s+=Opcode["mov_type_C"]
    # else:
    #     s+=Opcode[x[0]]
    
    # print(s,"\n")
    # i+=1
"""
count2=0
for i in l1:
    count2+=1
    temp=i.split(i)
    if(type_of_instruction(i)=="D" or"E"):
        if(temp[-1] not in var_codes):
            print("Error at line:",count2)
            print("Misuse of variable or label name")
"""      

