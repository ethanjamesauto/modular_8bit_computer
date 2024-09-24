################    INSTRUCTION TABLE   ################

#    INSTRUCTION FORMAT:        [x] [xxx]  [x]  [xxx]
#                               J/M  dest  S/F  source

#"jump"         "type"
#$  0           jump_a=b
#$  1           jump_b=ff
#$  2           jump_cout
#$  3           jump_bpositive
#$  4           jump_addr
#$  5           jump_ext1
#$  6           jump_ext2
#$  7           jump_uncond
#$  0           jump_0
#$  1           jump_1
#$  2           jump_2
#$  3           jump_3
#$  4           jump_4
#$  5           jump_5
#$  6           jump_6
#$  7           jump_noflag

#"flag"         "type"
#$  8           flag_0
#$  9           flag_1
#$  a           flag_2
#$  b           flag_3
#$  c           flag_4
#$  d           flag_5
#$  e           flag_6
#$  f           flag_noflag

#"move"         "dest" 
#$  8           dest_buls
#$  9           dest_bums
#$  a           dest_ram
#$  b           dest_ra
#$  c           dest_rb
#$  d           dest_addr
#$  e           dest_card
#$  f           dest_constant

#"move"         "source"
#$  0           source_pc0
#$  1           source_pc1
#$  2           source_ram
#$  3           source_apb
#$  4           source_apbp1
#$  5           source_anandb
#$  6           source_card
#$  7           source_constant

#"load"         "value"
#$  0           load_0
#$  1           load_1
#$  2           load_2
#$  3           load_3
#$  4           load_4
#$  5           load_5
#$  6           load_6
#$  7           load_7
#$  8           load_8
#$  9           load_9
#$  a           load_a
#$  b           load_b
#$  c           load_c
#$  d           load_d
#$  e           load_e
#$  f           load_f





lut = {}
with open("assembler_2.py","r") as myself:
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
        print(line)
        if "| " in line:
            line = line.split("| ")[1]
            print(line)
        line = line.split("#")[0]
        line = line.replace("\t","")
        line = line.split(" ")
        
        #add buffer when instruction too short. TODO refine this for 2 byte instruction
        if len(line[0]) != 0:
            if len(line)==1:
                line.append("0")
            program[line_counter] = line

        line_counter = line_counter + 1

#print(program)
        
#this will overwrite program rom with rom jump utility function
rom = {}

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
line_number = 1
for instruction in program:
    #get pair of bytes
    print(program[instruction])
    note = ""
    if program[instruction][0] in ["move","jump","load","flag"]:    
        note = "NO_NOTE"
    else:
        program[instruction] = program[instruction][1:]
        note = "NO_NOTE"
    if program[instruction][0] == "move":
        rom[instruction_pointer] = [lut["dest_"+program[instruction][1]]+lut["source_"+program[instruction][2]],note]
        if rom[instruction_pointer][1] == "NO_NOTE":
            program[line_number].append("line_"+str(line_number)+",instr_"+str(instruction_pointer)+","+rom[instruction_pointer][0])
        instruction_pointer = instruction_pointer + 1
        line_number = line_number + 1
    elif program[instruction][0] == "jump":
        rom[instruction_pointer] = [lut["jump_"+program[instruction][1]]+lut["jump_"+program[instruction][2]],note]
        if rom[instruction_pointer][1] == "NO_NOTE":
            print("line_"+str(line_number)+",instr_"+str(instruction_pointer)+","+rom[instruction_pointer][0])
            program[line_number].append("line_"+str(line_number)+",instr_"+str(instruction_pointer)+","+rom[instruction_pointer][0])
        instruction_pointer = instruction_pointer + 1
        line_number = line_number + 1
    elif program[instruction][0] == "flag":
        rom[instruction_pointer] = [lut["jump_"+program[instruction][1]]+lut["flag_"+program[instruction][2]],note]
        instruction_pointer = instruction_pointer + 1
        if rom[instruction_pointer][1] == "NO_NOTE":
            program[line_number].append("line_"+str(line_number)+",instr_"+str(instruction_pointer)+","+rom[instruction_pointer][0])
        line_number = line_number + 1
    elif program[instruction][0] == "load":
        #
        rtl_defined_constant_eight_bits = lut["load_"+program[instruction][1]]+lut["load_"+program[instruction][2]]
        map_byte = [1, 2, 5, 6, 0, 3, 4, 7]
        #map_byte = [0, 1, 2, 3, 4, 5, 6, 7]
        #convert byte to a number
        b = int(rtl_defined_constant_eight_bits, 16)
        print(b)
        out = 0
        for i in range(8):
            bit = (b >> i) & 1
            out |= bit << map_byte[i]
        print(len(hex(out)[2:]))
        constant_after_look_up = hex(out)[2:] if len(hex(out)[2:]) == 2 else "0"+hex(out)[2:]
        #if len(constant_after_look_up) == 1:
            #constant_after_look_up = '0' + constant_after_look_up
        print(constant_after_look_up)

        rom[instruction_pointer] = [lut["dest_constant"]+constant_after_look_up[0],note]
        rom[instruction_pointer+1] = [lut["dest_constant"]+constant_after_look_up[1],note]
        if rom[instruction_pointer][1] == "NO_NOTE":
            program[line_number].append("line_"+str(line_number)+",instr_"+str(instruction_pointer)+","+rom[instruction_pointer][0]+","+rom[instruction_pointer+1][0])
        instruction_pointer = instruction_pointer + 2
        line_number = line_number + 1

    
print(rom)
# instruction_pointer = 0
# for instruction in program:
#     if program[instruction][0] in lut:  #valid instruction
        
#         to_write_lsb,to_write_msb = "",""
#         print(program[instruction])

        

#         for token in program[instruction]:
#             if len(to_write_msb) > 1:
#                 to_write_lsb = to_write_lsb + lut[token]# + ("\n" if len(to_write) == 1 else "")
#             else:
#                 to_write_msb = to_write_msb + lut[token]
#         #print("trying to write "+to_write)


#         #Offset instruction write until free spot:
#         while instruction_pointer in rom:
#             instruction_pointer = instruction_pointer + 1

#         if len(to_write_msb) > 0:
#             rom[instruction_pointer] = to_write_msb
#         if len(to_write_lsb) > 0:

#             rom[instruction_pointer+1] = to_write_lsb
#         instruction_pointer = instruction_pointer + 2


#print("Successfully written instruction count: "+str(len(rom)-occupied_instructions))

#print(rom)

ROM_HEADER = "v2.0 raw\n"
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
            arr.append(int(rom[i][0],16))
            print(rom[i][0])
            #fp.write(chr(int(rom[i],16)))
        #else:
            #fp.write(NO_OP_INSTRUCTON+"\n")
    thing = bytes(bytearray(arr))
    fp.write(thing)


with open("rom_logisim.txt","w") as fp:
    fp.write(ROM_HEADER)
    for i in range(ROM_SIZE):
        if i in rom:
            fp.write(rom[i][0]+"\n")


with open("test_output.txt","w") as fp:
    #ooohhhhhh need to remove all nonchars
    
    for line_counter in program:
        content = []
        for token in program[line_counter]:
            if len(token) > 0:
                content.append(token)
        print(content[3])
        to_write = content[3]+(" "*(40-len(content[3])))+"| "+content[0]+" "+content[1]+" "+content[2]
        fp.write(to_write+"\n")
            



################    ASSEMBLABLES   ################
#  0   0
#  1   1
#  2   2
#  3   3
#  4   4
#  5   5
#  6   6
#  7   7
#  8   8
#  9   9
#  a   10
#  b   11
#  c   12
#  d   13
#  e   14
#  f   15