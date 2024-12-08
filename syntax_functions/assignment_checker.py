from syntax_functions.literal_checker import literal_checker
from syntax_functions.identifier_checker import identifier_checker
from syntax_functions.semantics_functions import *
from syntax_functions import semantics_functions
# from literal_checker import literal_checker
# from identifier_checker import identifier_checker
# from expression_checker import expression_checker
# from semantics_functions import *

def assignment_checker(line_num, tokens):
    from syntax_functions.expression_checker import expression_checker
    flag = False  # Tracks if all VISIBLE statements are valid
    # Check if statement starts with variable
    if identifier_checker(tokens[0]):
        result = semantics_functions.symbol_exists(tokens[0][0])
        if not result:
            raise Exception(f"Error in line {line_num}: Variable {tokens[0][0]} not declared")
        # Check if there's a value after 'R'
        if len(tokens) < 3:
            # result.append("ERROR: Missing value after 'VISIBLE'.")
            raise Exception ("SYNTAX ERROR at line {line_num}: Missing value after 'R'.")
            return False
        else:
            visible_part = tokens[2:]
            # first_value, first_type = visible_part[0]

            # Check if it's a literal
            if len(visible_part) > 1   == True:
                # result.append("Valid literal")
                if expression_checker(tokens[2:], semantics_functions.symbols, False) == True:
                    val_of_it = semantics_functions.get_symbol("IT")['value']
                    type_of_val = semantics_functions.get_symbol("IT")['value_type']
                    semantics_functions.update_symbol(tokens[0][0], value=val_of_it, value_type=type_of_val)
                    flag = True 
            # Check if it's an identifier
            else:
                    
                if identifier_checker(visible_part[0]) == True:
                    # result.append("Valid identifier")

                    result = semantics_functions.symbol_exists(visible_part[0][0])
                    var_name = visible_part[0][0]
                    # print("result" ,result) 
                    if not result:
                        raise Exception(f"Error in line {line_num}: Variable {visible_part[0][0]} is not declared")
                    flag = True

                    val_of_var = semantics_functions.get_symbol(var_name)['value']
                    type_of_var = semantics_functions.get_symbol(var_name)['value_type']
                    semantics_functions.update_symbol(tokens[0][0], value=val_of_var, value_type=type_of_var)
                    #Semantics - check if variable is in the symbol table
                    # symbol_exists(tokens[0][0])

                # Check if it's a valid expression
                elif literal_checker(visible_part[0]):
                        # result.append("Valid expression")
                    
                    if visible_part[0][1] == "NUMBAR":
                        visible_part[0][0] = float(visible_part[0][0])
                    elif visible_part[0][1] == "NUMBR":
                        visible_part[0][0] = int(visible_part[0][0])
                    semantics_functions.update_symbol(tokens[0][0], value=visible_part[0][0], value_type=visible_part[0][1])
                    flag = True
    else:
        return False
    return flag



def assignment_semantics(line_num, tokens):
    print("assignment semantics")
    token_index = 0
    # print(len(tokens))
    value_of_ass = 0  
    type_of_ass = ""
    var_name = ""
    for idx in range(len(tokens)):
        print(tokens[idx][0])

        #check if the variable is declared
        if tokens[idx][1] == "IDENTIFIER":
            result = symbol_exists(tokens[0][0])
            var_name = tokens[0][0]
            # print("result" ,result) 
            if not result:
                raise Exception(f"Error in line {line_num}: Variable {tokens[0][0]} is not declared")
            idx += 1
        
        elif tokens[idx][0] != "R" and tokens[idx][1] == "KEYWORD":
            print("expression")
            print(tokens[idx:])
            #Store the value of expression to the value of the symbol
            idx += 1
            break

        elif literal_checker(tokens[idx]):
            #assign the value
            print("value: ", tokens[idx][0])
            if tokens[idx][1] == "NUMBAR":
                tokens[idx][0] = float(tokens[idx][0])
            elif tokens[idx][1] == "NUMBR":
                tokens[idx][0] = int(tokens[idx][0])
            update_symbol(var_name, value=tokens[idx][0], value_type=tokens[idx][1])
            print(symbols)
            idx += 1
        else:
            idx += 1
    
    return True






# # Run test cases
# for i, (line_num, tokens) in enumerate(test_case.items()):
#     # print(i)
#     result = assignment_semantics(line_num,tokens)
#     print(f"Test Case {i}: {'Valid' if result == True else result}")
#     # print(symbols)

# print(symbol_table)