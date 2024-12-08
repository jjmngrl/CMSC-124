
from syntax_functions import semantics_functions
from syntax_functions import visible_statement_checker
from syntax_functions import assignment_checker
# from syntax_functions import statement_checker
from syntax_functions import switch_checker
from syntax_functions import ifelse_checker
from syntax_functions import loop_checker
from syntax_functions import visible_statement_checker
from syntax_functions import extract_flowcontrol_block
from syntax_functions import func_call_checker
# from syntax_functions import loop_checker
from syntax_functions import gimmeh_statement_checker
from syntax_functions import function_checker
from syntax_functions import expression_checker
from syntax_functions import semantics_functions

def evaluate_body(code_block): 
    # statement_flag = False  
    valid_operations = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'BIGGR OF', 'SMALLR OF', 'MOD OF']
    print("\nCODE BLOCK: \n", code_block)
    """ Check succeeding line and determine the type of statement"""
    current_line = list(code_block.keys())[0] #This is the first line after the variable declaration
    while current_line in code_block:
        tokens = code_block[current_line]
        print(f"\nToken being checked in line {current_line}: ", tokens)



        if current_line < list(code_block.keys())[-1]:
            catch_wtf = code_block[current_line+1]
            # print(catch_wtf)
            switch_exist = False
            if catch_wtf != []:
                switch_exist = True
            # print(catch_wtf[0])
        if tokens == []:
            current_line += 1
            continue
        
        
        #check for print statement
        if tokens[0][0] == "VISIBLE":
            print("Insert print checker here")
            visible_statement_checker.visible_statement_checker(current_line, tokens)
            statement_flag = True
            current_line += 1 #Move to the next line

        # #catch for if-else
        # elif tokens[0][0] == "O RLY?" and tokens[0][1] == "KEYWORD":
        #     print(f"start of if-else block at line {current_line}")
        #     extract_block, next_line = extract_flowcontrol_block.extract_ifelse_block(code_block, current_line)
        #     print("Extracted block:\n", extract_block)
        #     #Syntax analyzer
        #     if ifelse_checker.ifelse_checker(extract_block):
        #         print(f"valid if else block at line {current_line} to line {next_line-1}")
        #         statement_flag = True
        #     else:
        #         raise Exception(f"ERROR in line {current_line}:Invalid if-else block.")
            
        #     #semantics

        #     current_line = next_line

        # #Catch switch
        # elif switch_exist == True and catch_wtf[0][0] == "WTF?":
        #     print(f"Start of switch-case block at line {current_line+1}")
        #     extracted_block, next_line = extract_flowcontrol_block.extract_switch_block(code_block, current_line+1)
        #     print("Extracted switch-case block:\n", extracted_block)
        #     if switch_checker.switch_checker(extracted_block):
        #         print(f"valid switch block at line {current_line+1} to line {next_line+1}")
        #         statement_flag = True
        #     else:
        #         raise Exception(f"ERROR in line {current_line+1}:Invalid switch block.")
        #     current_line = next_line  # Move to the next line after the block
        #     # current_line += 1

        # #Catch function call
        # elif tokens[0][0] == "I IZ":
        #     print(f"Function call at line {current_line}")
        #     result = func_call_checker.function_call_checker(tokens, current_line)
        #     if result == True:
        #         print(f"Valid function call at line {current_line}")
        #         statement_flag = True
        #     else:
        #         raise Exception(result)

        #     current_line += 1

        #catch loops
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

        # #catch input
        # elif tokens[0][0] == "GIMMEH":
        #     print(f"Input at line {current_line}")

        #     if gimmeh_statement_checker.gimmeh_statement_checker(tokens):
        #         print("Valid input/gimmeh statemet")
        #         statement_flag = True
        #     else:
        #         raise Exception(f"ERROR at line {current_line}: Input statements must follow this format: GIMMEH <varident>")

        #     current_line += 1
        
        # #catch function
        # elif tokens[0][0] == "HOW IZ I":
        #     print(f"Start of function block at line {current_line}")
        #     extracted_block, next_line = function_checker.extract_function_block(code_block, current_line)
        #     print("Extracted function block:\n",extracted_block)
        #     result = function_checker.function_checker(extracted_block)
        #     if result == True:
        #         print(f"Valid functin block at line {current_line} to line {next_line-1}")
        #         statement_flag = True
        #     else:
        #         raise Exception(result)

        #     current_line = next_line

        #catch expression
        elif expression_checker.expression_checker(tokens, semantics_functions.symbols, False) == True:
            print("Valid expression")
            current_line += 1
            statement_flag = True
            
        #catch assignment
        elif tokens[1][0] == "R" and len(tokens) == 3:
            print(f"Assignment statement at line {current_line}")
            result =  assignment_checker.assignment_semantics(current_line, tokens)
            if result:
                print("Valid assignment statent")
                statement_flag = True
            else:
                raise Exception(result)
        
            current_line += 1
            
        




        
        else:
            print("Nah")
            current_line += 1
    return statement_flag


from syntax_functions import variable_section_checker


def syntax_body(code_block, classified_tokens):           
    print("syntax chec if else body")
    statement_flag = False
    print("CODE BLOCK: \n", code_block)
    """ Check succeeding line and determine the type of statement"""
    current_line = list(code_block.keys())[0] #This is the first line after the variable declaration
    print("current line")
    while current_line in code_block:
        tokens = code_block[current_line]
        print(f"\nToken being checked in line {current_line}: ", tokens)

        # print(code_block[current_line+1])
        if current_line < list(code_block.keys())[-1]:
            catch_wtf = code_block[current_line+1]
            # print(catch_wtf)
            switch_exist = False
            if catch_wtf != []:
                switch_exist = True
            # print(catch_wtf[0])
        if tokens == []:
            current_line += 1
            continue
        #check for print statement
        if visible_statement_checker.visible_statement_checker(current_line, tokens):
            print("Valid print statement")
            statement_flag = True
            current_line += 1 #Move to the next line

        #catch for if-else
        elif tokens[0][0] == "O RLY?" and tokens[0][1] == "KEYWORD":
            print(f"start of if-else block at line {current_line}")
            extract_block, next_line = extract_flowcontrol_block.extract_ifelse_block(code_block, current_line)
            print("Extracted block:\n", extract_block)
            #Syntax analyzer
            if ifelse_checker.ifelse_checker(extract_block):
                print(f"valid if else block at line {current_line} to line {next_line-1}")
                statement_flag = True
            else:
                raise Exception(f"ERROR in line {current_line}:Invalid if-else block.")
            
            #semantics

            current_line = next_line

        #Catch switch
        elif switch_exist == True and catch_wtf[0][0] == "WTF?":
            print(f"Start of switch-case block at line {current_line+1}")
            extracted_block, next_line = extract_flowcontrol_block.extract_switch_block(code_block, current_line+1)
            print("Extracted switch-case block:\n", extracted_block)
            if switch_checker.switch_checker(extracted_block):
                print(f"valid switch block at line {current_line+1} to line {next_line+1}")
                statement_flag = True
            else:
                raise Exception(f"ERROR in line {current_line+1}:Invalid switch block.")
            current_line = next_line  # Move to the next line after the block
            # current_line += 1

        #Catch function call
        elif tokens[0][0] == "I IZ":
            print(f"Function call at line {current_line}")
            result = func_call_checker.function_call_checker(tokens, current_line)
            if result == True:
                print(f"Valid function call at line {current_line}")
                statement_flag = True
            else:
                raise Exception(result)

            current_line += 1

        #catch loops
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

        #catch input
        elif tokens[0][0] == "GIMMEH":
            print(f"Input at line {current_line}")

            if gimmeh_statement_checker.gimmeh_statement_checker(tokens):
                print("Valid input/gimmeh statemet")
                statement_flag = True
            else:
                raise Exception(f"ERROR at line {current_line}: Input statements must follow this format: GIMMEH <varident>")

            current_line += 1
        
        #catch function
        elif tokens[0][0] == "HOW IZ I":
            print(f"Start of function block at line {current_line}")
            extracted_block, next_line = function_checker.extract_function_block(code_block, current_line)
            print("Extracted function block:\n",extracted_block)
            result = function_checker.function_checker(extracted_block)
            if result == True:
                print(f"Valid functin block at line {current_line} to line {next_line-1}")
                statement_flag = True
            else:
                raise Exception(result)

            current_line = next_line

        #catch expression
        elif expression_checker.expression_checker(tokens, False) == True:
            print("Valid expression")
            current_line += 1
            statement_flag = True
            
        #catch assignment
        elif tokens[1][0] == "R":
            print(f"Assignment statement at line {current_line}")
            result =  assignment_checker.assignment_checker(current_line, tokens)
            if result:
                print("Valid assignment statent")
                statement_flag = True
            else:
                raise Exception(result)
        
            current_line += 1
            
        




        
        else:
            print("Nah")
            current_line += 1
    # for line_num, tokens in code_block.items():
    #     print(f"\nToken being checked in line {line_num}: ", tokens)
    #     if tokens == []:
    #         continue
    #     # for token, token_type in tokens:
    #     #     if token == []: #skip the spac es
    #     #         continue
    #     #     print(token)

    #         #Check for print statement
    #     if visible_statement_checker.visible_statement_checker(line_num, tokens) == True:
    #         print("Valid print statement")
    #         statement_flag = True

    #     #Catch for if-else
    #     elif tokens[0][0] == "O RLY?" and tokens[0][1] == "KEYWORD":
    #         print("start of if else")
    #         extracted_block = extract_ifelse_block.extract_ifelse_block(code_block, line_num)
    #         print("IF ELSE BLOCK: \n",extracted_block)
    #         #Process the if-else blocks
            

    #         #

    #         # print("if else block: ",ifelse_blocks)


    #         # if line_num in ifelse_blocks:
    #         #     print("Dictionary created for if else checker: \n", {line_num: ifelse_blocks[line_num]})
    #         #     result = ifelse_checker.ifelse_checker({line_num: ifelse_blocks[line_num]})
    #         #     print("RESULT!!: ", result)
    #         #     if result:
    #         #         print(f"valid if-else statement at block {line_num}")
    #         #         statement_flag = True
    #         #     else:
    #         #         raise Exception(f"Invalid if-else statement at block {line_num}")
                
    #     # Check for switch block
    #     elif switch_section_exists and token == "WTF?" and token_type == "KEYWORD":
    #         if line_num in switch_blocks:
    #             result = switch_checker.switch_checker({line_num: switch_blocks[line_num]})
    #             if result:
    #                 print(f"Valid switch statement at block {line_num}")
    #                 statement_flag = True
    #             else:
    #                 raise Exception(f"Invalid switch statement at block {line_num}")
    return statement_flag
