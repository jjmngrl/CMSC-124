from syntax_functions.parameter_checker import parameter_checker
from syntax_functions.visible_statement_checker import visible_statement_checker
from syntax_functions.variable_section_checker import variable_section_checker
from syntax_functions import assignment_checker
from syntax_functions import gimmeh_statement_checker
from syntax_functions import func_call_checker
from syntax_functions import extract_flowcontrol_block
from syntax_functions import ifelse_checker
from syntax_functions import switch_checker
from syntax_functions import loop_checker
from syntax_functions import expression_checker

"""
- print
- variable section
- expression
- assignment
- function call
- flow control
- input 
- input
- found yr

"""


def flow_control_body_checker(code_block):
    print("\nInside flow control body checker")
    flowcontrol_body_flag = False

    #check variable section
    wazzup_key = None
    buhbye_key = None
    variable_section_exists = False
    for line_num, tokens_var in code_block.items():
        for token_var, token_type_var in tokens_var:
            if token_var == "WAZZUP":
                variable_section_exists = True
                wazzup_key = line_num
            if token_var == "BUHBYE":
                variable_section_exists = True
                buhbye_key = line_num
    
    #raise error when there is no wazzup or buhbye
    if wazzup_key == None and variable_section_exists:
        raise Exception("ERROR: Invalid Variable Section due to missing WAZZUP")
    if buhbye_key == None and variable_section_exists:
        raise Exception("ERROR: Invalid Variable Section due to missing BUHBYE")
    
    if variable_section_exists:
        #Check if variable section is valid
        if variable_section_checker.variable_section_checker(code_block, code_block):
        #Create a new dictionary without the variable section to check what kind of statement are the remaining code
            new_code_block = {}
            for key, value in code_block.items():
                if buhbye_key is not None and key > buhbye_key:
                    new_code_block[key] = value  # Retain lines after BUHBYE
    
            code_block = new_code_block
    
    # print("function body: " ,ls_of_values[1:])


    """ Check next lines of the function"""
    current_line = list(code_block.keys())[0] #This is the first line after the variable declaration
    # current_line = line_of_func+1

    while current_line in code_block:
        tokens = code_block[current_line]
        print(f"\ntoken being checked in line {current_line}: {tokens}")

        if tokens == []:
            current_line += 1
            continue
            
        #Catch print statement
        if visible_statement_checker(current_line, tokens):
            print("Valid print statement")
            flowcontrol_body_flag = True
            current_line += 1 #Move to the next line


        
        # elif expression_checker.expression_checker
        if len(tokens) > 1:
            #elif assignment
            if tokens[1][0] == "R":
                print(f"Assignment statement at line {current_line}")
                result =  assignment_checker.assignment_checker(current_line, tokens)
                if result:
                    print("Valid assignment statent")
                    flowcontrol_body_flag = True
                else:
                    raise Exception(result)
            
                current_line += 1
            else:
                current_line += 1

        #elif func_call
        elif tokens[0][0] == "I IZ":
            print(f"Function call at line {current_line}")
            result = func_call_checker.function_call_checker(tokens, current_line)
            if result == True:
                print(f"Valid function call at line {current_line}")
                statement_flag = True
                flowcontrol_body_flag = True

            else:
                raise Exception(result)

            current_line += 1


        #if else
        elif tokens[0][0] == "O RLY?" and tokens[0][1] == "KEYWORD":
            print(f"start of if-else block at line {current_line}")
            extract_block, next_line = extract_flowcontrol_block.extract_ifelse_block(code_block, current_line)
            print("Extracted block:\n", extract_block)
            if ifelse_checker.ifelse_checker(extract_block):
                print(f"valid if else block at line {current_line} to line {next_line-1}")
                flowcontrol_body_flag = True
                statement_flag = True
            else:
                raise Exception(f"ERROR in line {current_line}:Invalid if-else block.")
            current_line = next_line
        #switch
        elif tokens[0][0] == "WTF?" and tokens[0][1] == "KEYWORD":
            print(f"Start of switch-case block at line {current_line}")
            extracted_block, next_line = extract_flowcontrol_block.extract_switch_block(code_block, current_line)
            print("Extracted switch-case block:\n", extracted_block)
            if switch_checker.switch_checker(extracted_block):
                print(f"valid switch block at line {current_line} to line {next_line-1}")
                statement_flag = True
                flowcontrol_body_flag = True
            else:
                raise Exception(f"ERROR in line {current_line}:Invalid switch block.")
            current_line = next_line  # Move to the next line after the block
        #loop
        elif tokens[0][0] == "IM IN YR":
            print(f"Start of loop black at line {current_line}")
            extract_block, next_line = extract_flowcontrol_block.extract_loop_block(code_block, current_line)
            print("Extracted loop block:\n", extract_block)
            result = loop_checker.loop_checker(extract_block)
            if result == True:
                print(f"valid loop block at line {current_line} to line {next_line-1}")
                statement_flag = True
                flowcontrol_body_flag = True
            else:
                raise Exception(result)
            current_line = next_line  # Move to the next line after the block

        #elif input
        elif tokens[0][0] == "GIMMEH":
            print(f"Input at line {current_line}")

            if gimmeh_statement_checker.gimmeh_statement_checker(tokens):
                print("Valid input/gimmeh statemet")
                flowcontrol_body_flag = True
            else:
                raise Exception(f"ERROR at line {current_line}: Input statements must follow this format: GIMMEH <varident>")

            current_line += 1

        #catch GTFO
        elif tokens[0][0] == "GTFO":
            print("Valid GTFO")
            flowcontrol_body_flag = True
            current_line += 1
        
        #elif FOUND YR (return statement)
        elif tokens[0][0] == "IF U SAY SO":
            current_line += 1
            flowcontrol_body_flag = True

        #elif expression
        elif expression_checker.expression_checker(tokens[1:], False) == True:
            print("Valid expression")
            current_line += 1
            return flowcontrol_body_flag

        else:
            current_line += 1
    
    return flowcontrol_body_flag