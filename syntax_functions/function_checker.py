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
Function to check if smoosh (concatenation) is valid
Parameter: tokens for the smoosh
Return value: True - valid smoosh
                False - invalid smoosh
"""




"""
In integrating in statement_checker.py, check this condition:
if token[1][0][0] == 'HOW' and token[1][1][0] == 'IZ' and token[1][2][0] == 'I' and token[3][1] == 'IDENTIFIER':
if true, find the tokens IF U SAY SO 
"""
def function_checker(code_block):
    print("\nInside function checker")

    ls_of_values = list(code_block.values()) #3d list 
    line_of_func = list(code_block.keys())[0]

    print(ls_of_values)
    # print(len(ls_of_values[0]))
    parameter_flag = True
    flag = False

    if ls_of_values[0][0][0] == 'HOW IZ I' and ls_of_values[0][1][1] == "IDENTIFIER":
        #If function has parameter/s, check if the parameters are valid parameters
        if len(ls_of_values[0]) > 2:
            print("Function has multiparameter")
            #check if function header has 'YR'
            if ls_of_values[0][2][0] == "YR":
                parameters = ls_of_values[0][3:]
                if parameter_checker(parameters,line_of_func) == True:
                    print("parameter/s is/are valid")
                    parameter_flag == True
                else:
                    parameter_flag == False
            else:
                print("Invalid function header")
                return f"Invalid function header"
        
        #Check if there is IF U SAY SO
        if code_block[list(code_block.keys())[len(code_block.values())-1]][0][0] == "IF U SAY SO":
            if parameter_flag == True: 
                #check the function body (Same logic with statement checker)
                
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
                        function_body_flag = True
                        current_line += 1 #Move to the next line


                    
                    # elif expression_checker.expression_checker
                    
                    #elif assignment
                    elif tokens[1][0] == "R":
                        print(f"Assignment statement at line {current_line}")
                        result =  assignment_checker.assignment_checker(current_line, tokens)
                        if result:
                            print("Valid assignment statent")
                        else:
                            raise Exception(result)
                    
                        current_line += 1

                    #elif func_call
                    elif tokens[0][0] == "I IZ":
                        print(f"Function call at line {current_line}")
                        result = func_call_checker.function_call_checker(tokens, current_line)
                        if result == True:
                            print(f"Valid function call at line {current_line}")
                            statement_flag = True
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
                        else:
                            raise Exception(result)
                        current_line = next_line  # Move to the next line after the block

                    #elif input
                    elif tokens[0][0] == "GIMMEH":
                        print(f"Input at line {current_line}")

                        if gimmeh_statement_checker.gimmeh_statement_checker(tokens):
                            print("Valid input/gimmeh statemet")
                        else:
                            raise Exception(f"ERROR at line {current_line}: Input statements must follow this format: GIMMEH <varident>")

                        current_line += 1

                    #catch GTFO
                    elif tokens[0][0] == "GTFO":
                        print("Valid GTFO")
                        function_body_flag = True
                        current_line += 1
                    
                    #elif FOUND YR (return statement)
                    elif tokens[0][0] == "IF U SAY SO":
                        current_line += 1
                        function_body_flag = True

                    #elif expression
                    elif expression_checker.expression_checker(tokens[1:], False) == True:
                        print("Valid expression")
                        current_line += 1

                    else:
                        current_line += 1


        else:
            return f"ERROR at line {list(code_block.keys())[len(code_block.values())-1]}: Functions must be closed with IF U SAY SO"
    else:
        if ls_of_values[0][1][1] != "IDENTIFIER":
            return f"ERROR at line {line_of_func}: HOW IZ I should be followed by a valid identifier "
    return function_body_flag


            # if visible




    
    
    #Check if if start of line is HOW IZ I followed by an identifier
    # if token[2][0][0] == 'HOW' and token[2][1][0] == 'IZ' and token[2][2][0] == 'I' and token[3][1] == 'IDENTIFIER':
    #     print("valid")
    #     #Find the 
    # else:
    #     print("not valid")


    #check if the first 3 tokens is HOW IZ I and 4th token is an identifier
    



def extract_function_block(code_block, start_line):
    extracted_block = {}
    in_function_block = False

    for line_num, tokens in code_block.items():
        if line_num < start_line:
            continue #skitps lines before the start

        for token, token_type in tokens:
            if token == "HOW IZ I" and line_num == start_line:
                in_function_block = True #Mark the start of the block
                extracted_block[line_num] = tokens
            elif token == "IF U SAY SO" and in_function_block:
                extracted_block[line_num] =  tokens #Add the closing line to the dictionary
                in_function_block = False
                return extracted_block,line_num + 1 #Return the function block and the next line
            elif in_function_block:
                extracted_block[line_num] = tokens #Add the function code
    raise Exception("IF U SAY SO not found on the function")

# for key, value in code_tokens.items():
#     if len(value) >= 3:
#         # Check if the first 3 tokens are 'HOW IZ I'
#         if value[0][0] == 'HOW' and value[1][0] == 'IZ' and value[2][0] == 'I':
#             # Find the line/key of 'IF U SAY SO' - end of the function
#             end_of_function = None
#             for subsequent_key in range(key + 1, len(code_tokens) + 1):
#                 # Check if line contains 'IF U SAY SO'
#                 if all(token[0] == word for token, word in zip(code_tokens[subsequent_key], ['IF', 'U', 'SAY', 'SO'])):
#                     end_of_function = subsequent_key
#                     break
#             #Function starts with 'HOW IZ I' and ends with 'IF U SAYO SO'    
#             if end_of_function is not None:
#                 # Create a new dictionary of the contents inside the function starting from 'HOW IZ I'
#                 function_contents = {k: v for k, v in code_tokens.items() if k >= key and k < end_of_function}
#                 function_checker(function_contents)
#                 # for line, tokens in function_contents.items():
#                 # print(function_contents)
#                 #     print(f"Line {line}: {tokens}")
            
#             else: #function does not end with IF U SAY SO
#                 print(f"no end for function starting at line {key}")
