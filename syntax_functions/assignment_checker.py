from syntax_functions.literal_checker import literal_checker
from syntax_functions.identifier_checker import identifier_checker
from syntax_functions.expression_checker import expression_checker
from syntax_functions.semantics_functions import *
# from literal_checker import literal_checker
# from identifier_checker import identifier_checker
# from expression_checker import expression_checker

def assignment_checker(line_num, tokens):
    flag = False  # Tracks if all VISIBLE statements are valid
    # Check if statement starts with variable
    if identifier_checker(tokens[0]):
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
                if expression_checker(tokens[2:], False) == True:
                    flag = True 
            # Check if it's an identifier
            else:
                    
                if identifier_checker(visible_part[0]) == True:
                    # result.append("Valid identifier")
                    flag = True
                    
                    #Semantics - check if variable is in the symbol table
                    # symbol_exists(tokens[0][0])

                # Check if it's a valid expression
                elif literal_checker(visible_part[0]):
                        # result.append("Valid expression")
                    flag = True

            # # Check if the keyword is 'IT'
            # elif first_value == "IT":
            #     #Check if there is a token after IT
            #     if (len(visible_part)) > 1:
            #         raise Exception( f"ERRROR at line {line_num} : There should be no other token after IT")
            #     flag = True
            # else:
            #     # If it's none of the above, mark it invalid
            #     # result.append(f"ERROR: Invalid value after 'VISIBLE': {first_value}")
            #     raise Exception(f"ERROR at line {line_num}: Invalid value after 'VISIBLE': {first_value}")
            #     flag = False
    else:
        # If the line doesn't start with 'VISIBLE', it's invalid
        # result.append("ERROR: Line does not start with 'VISIBLE'.")
        # raise Exception("ERROR: Line does not start with 'VISIBLE'.")
        return False

    # Return the result flag (True if valid, False if invalid)
    return flag

test_case = {
    13: [['x', 'IDENTIFIER'], ['R', 'KEYWORD'], ['SMOOSH', 'KEYWORD'], ['x', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['y', 'IDENTIFIER']],
    14: [['y', 'IDENTIFIER'], ['R', 'KEYWORD'], ['100', 'NUMBR']],
    19: [['y', 'IDENTIFIER'], ['R', 'KEYWORD'], ['0', 'NUMBR']],
    20: [['y', 'IDENTIFIER'], ['R', 'KEYWORD'], ['MAEK', 'KEYWORD'], ['y', 'IDENTIFIER'], ['A', 'KEYWORD'], ['TROOF', 'KEYWORD']],
}



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