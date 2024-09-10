recognized_types = ["byte","addr"]
conditional_reserved_strings = ["if","else"]
recognized_operators = ["=="]
nested_conditional_operators_pending_closure = {}
defined_variables = {}



PROGRAM = {}
PROGRAM_LINE_INDEX = 1
RAM_VAR_DEFINE_INDEX = 1

def str_byte_to_str_two_halves(str_byte_to_become_two_halves):
    return int(str_byte_to_become_two_halves,2)
    

def int_to_16bconstant(number_to_become_constant):
    return str(number_to_become_constant//256),str(number_to_become_constant%256)


to_compile_line_index = 0
to_compile = input(":")+".txt"
compiled_name = to_compile+"_compiled.txt"
with open(to_compile,"r") as fp:
    required_indentation_to_continue_conditional,if_incomplete,num_nested_conditionals = 0, False,0
    for line in fp:
        to_compile_line_index = to_compile_line_index + 1
        line = line.split("\n")[0]
        line = line.split(" ")


        #count tabs, remove indentation
        len_indentation,line_index = 0,0
        if len(line) > 0:
            while len(line[line_index]) == 0:
                len_indentation = len_indentation+1
                line_index = line_index + 1
        num_tabs = len_indentation // 4
        line_without_tab = []
        for token in line:
            if len(token) >0:
                line_without_tab.append(token)
        line = line_without_tab
        #print(line, num_tabs, defined_variables)



        #check indentation to see if an if needs completion
        if if_incomplete:
            if line[0].replace(":","") != "else":
                if num_tabs < required_indentation_to_continue_conditional:
                    print("LINE "+str(to_compile_line_index)+" ERROR: above conditional statement must be terminated with a negative clause")
                    quit()
            


        #parse command type: SYNTAX "byte/addr" "name" "values"
        if line[0] in recognized_types: #command type is define new variable
            variable_name = line[1]
            if variable_name not in defined_variables: #not an already defined variable
                defined_variables[line[1]] = line[3],RAM_VAR_DEFINE_INDEX
                #the new variable will be defined at the next available definition index in ram.
                #create a constant referring to the next available ram index:
                msb,lsb = int_to_16bconstant(RAM_VAR_DEFINE_INDEX)
                PROGRAM[PROGRAM_LINE_INDEX] = "load "+
                PROGRAM_LINE_INDEX = PROGRAM_LINE_INDEX + 1
                print(PROGRAM)
            else:   #user attempting to define variable already defined. must destroy first.
                print("LINE "+str(to_compile_line_index)+" ERROR: variable '"+line[1]+"' already defined.")
                quit()


        #dereference: SYNTAX "destroy" "name"
        elif line[0] == "destroy":
            variable_name = line[1]
            if variable_name in defined_variables: #ensure the variable trying to destroy was defined
                del defined_variables[line[1]]
            else:
                print("LINE "+str(to_compile_line_index)+" ERROR: variable '"+line[1]+"' cannot be destroyed as it was never defined.")
                quit()
        

        #conditional if/then: SYNTAX "if" "conditional" 
        elif line[0].replace(":","") in conditional_reserved_strings:
            if conditional_reserved_strings.index(line[0].replace(":","")) == 0:    #if
                conditional_operator = line[2]
                if conditional_operator in recognized_operators:    #operator exists
                    operands = line[1].replace(":",""),line[3].replace(":","")
                    if len(operands) == 2:  #ensure two operands only
                        if operands[0] in defined_variables:    #ensure operand 0 exists
                            if operands[1] in defined_variables:    #ensure operand 1 exists
                                
                                #VALID CONDITIONAL. track indentation
                                required_indentation_to_continue_conditional,if_incomplete = num_nested_conditionals + 1,True
                                nested_conditional_operators_pending_closure[num_nested_conditionals] = [conditional_operator,operands[0],operands[1]]
                                num_nested_conditionals = num_nested_conditionals + 1
                                


                                #TODO think of a way to track tags. autogenerate? line number?
                                #behavior depends on the specific conditional.
                                #if conditional_operator == "==":    #equals
                                    #processor jumps when two operands are equal. otherwise steps to next instruction


                            else:
                                print("LINE "+str(to_compile_line_index)+" ERROR: operand '"+operands[1]+"' has not been defined.")
                                quit()
                        else:
                            print("LINE "+str(to_compile_line_index)+" ERROR: operand '"+operands[0]+"' has not been defined.")
                            quit()
                    else:
                        print("LINE "+str(to_compile_line_index)+" ERROR: too many operands")
                        quit()
                else:
                    print("LINE "+str(to_compile_line_index)+" ERROR: operator '"+line[2]+"' does not exist.")
                    quit()
            elif conditional_reserved_strings.index(line[0].replace(":","")) == 1:  #else
                print("CLOSING: "+str(nested_conditional_operators_pending_closure[num_nested_conditionals-1]))
                
                #TODO terminate the if-else
                
                del nested_conditional_operators_pending_closure[num_nested_conditionals-1]
                num_nested_conditionals = num_nested_conditionals - 1
                required_indentation_to_continue_conditional = num_nested_conditionals
                if num_nested_conditionals == 0:
                    if_incomplete = False




#print(defined_variables)
        
        