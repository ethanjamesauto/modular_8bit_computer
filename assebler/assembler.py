################    INSTRUCTION TABLE   ################

#D/S INSTRUCTION FORMAT:        [xxxx]  [xxxx]  [xxxx]  [xxxx]
#                               opcode   dest   source  nothing

#CONSTANT INSTUCTION FORMAT:    [xxxx]  [xxxx]  [xxxxxxxx]
#                               opcode   dest    constant


#"opcode" "abbrev"    "argument"      "description"
#$  E      lcon        dest, constant  dest <- constant
#$  F      move        dest, source
#$  D      publish     0, 0            offcard <- output data latch


#"destination" "abbrev" 
#$  F           carddata
#$  E           rd
#$  D           rc
#$  7           ra
#$  6           rb
#$  5           buls
#$  4           bums
#$  3           jump
#$  2           mals
#$  1           ram
#$  0           noop

#"source"    "abbrev"
#$  7           apb
#$  6           data

lut = {}
with open("assembler.py","r") as myself:
    for line in myself:
        if line[:2] == "#$":
            line = line.replace("\n","")
            line = line.replace("#$","")
            line = line.split(" ")
            lut_arr = []
            for token in line:
                if len(token) > 0:
                    lut_arr.append(token)
            lut[lut_arr[1]] = lut_arr[0]


print(lut)

line_counter,program,to_compile = 1,{},str(input("compile: (do not include file extension)"))
with open(to_compile+".txt","r") as fp:
    for line in fp:
        line = line.replace("\n","")
        line = line.replace("\t","")
        line = line.split("#")[0]
        line = line.split(" ")
        #add buffer when instruction too short. TODO refine this for 2 byte instruction
        if len(line[0]) != 0:
            program[line_counter] = line
        line_counter = line_counter + 1

#print(program)
        
#this will overwrite program rom with rom jump utility function
rom = {}
print(program)

#rom_util_counter = 0
#occupied_instructions = 0
#with open("rom_utils.txt","r") as rom_utils:
#    for line in rom_utils:
#        line = line.replace("\n","")
#        if len(line) > 0:
#            occupied_instructions = occupied_instructions + 1
#            rom[rom_util_counter] = line
#        rom_util_counter = rom_util_counter + 1

#print(occupied_instructions)
#print(occupied_instructions/rom_util_counter)

instruction_pointer = 0
for instruction in program:
    print(program[instruction],instruction)
    if program[instruction][0] == "load":
        rom[instruction_pointer] = lut[program[instruction][1]]+lut[program[instruction][2]]
    elif program[instruction][0] == "move":
        rom[instruction_pointer] = lut[program[instruction][1]]
    
    # if program[instruction][0] in lut:  #valid instruction
        
    #     to_write_lsb,to_write_msb = "",""
    #     print(program[instruction])

        

    #     for token in program[instruction]:
    #         if len(to_write_msb) > 1:
    #             to_write_lsb = to_write_lsb + lut[token]# + ("\n" if len(to_write) == 1 else "")
    #         else:
    #             to_write_msb = to_write_msb + lut[token]
    #     #print("trying to write "+to_write)


    #     #Offset instruction write until free spot:
    #     while instruction_pointer in rom:
    #         instruction_pointer = instruction_pointer + 1

    #     if len(to_write_msb) > 0:
    #         rom[instruction_pointer] = to_write_msb
    #     if len(to_write_lsb) > 0:

    #         rom[instruction_pointer+1] = to_write_lsb
    #     instruction_pointer = instruction_pointer + 2


#print("Successfully written instruction count: "+str(len(rom)-occupied_instructions))

#print(rom)

#ROM_HEADER = "v2.0 raw\n"
ROM_SIZE = ((2**15)-2)
NO_OP_INSTRUCTON = "FF"

with open("rom.txt","wb") as fp:
    #fp.write(ROM_HEADER)
    arr = []
    for i in range(ROM_SIZE):
        if i in rom:



            #formatted_byte = ""
            #for character in rom[i]:
                #formatted_byte = formatted_byte+str(int(character,16))
            arr.append(int(rom[i],16))
            print(rom[i])
            #fp.write(chr(int(rom[i],16)))
        #else:
            #fp.write(NO_OP_INSTRUCTON+"\n")
    thing = bytes(bytearray(arr))
    fp.write(thing)









################    ASSEMBLABLES   ################
#$  0   0
#$  1   1
#$  2   2
#$  3   3
#$  4   4
#$  5   5
#$  6   6
#$  7   7
#$  8   8
#$  9   9
#$  a   10
#$  b   11
#$  c   12
#$  d   13
#$  e   14
#$  f   15