from syntax_functions.validate_expression import validate_expression
from syntax_functions.literal_checker import literal_checker
from syntax_functions.identifier_checker import identifier_checker
from syntax_functions.expression_checker import expression_checker
from syntax_functions import semantics_functions

def visible_statement_checker(line_num, tokens):
    # Start by adding a log entry to show we're inside the visible statement checker
    # result.append("\nInside visible statement checker")

    # Define valid literal types and operations
    flag = False  # Tracks if all VISIBLE statements are valid
    
    # Add the line and tokens to the result
    # result.append(f"Line: {line}")
    # result.append(f"Tokens: {tokens}")

    # Check if statement starts with 'VISIBLE'
    if tokens[0][0] == 'VISIBLE':
        # Check if there's a value after 'VISIBLE'
        if len(tokens) < 2:
            # result.append("ERROR: Missing value after 'VISIBLE'.")
            raise Exception ("ERROR at line {line_num}: Missing value after 'VISIBLE'.")
            return False
        else:
            visible_part = tokens[1:]
            first_value, first_type = visible_part[0]
            # Check if it's a literal
            if literal_checker(visible_part[0]) == True:
                # result.append("Valid literal")
                semantics_functions.update_symbol("IT", value=first_value, value_type=first_type )
                output = semantics_functions.get_symbol("IT")['value']
                print(output)
                flag = True
            # Check if it's an identifier
            elif identifier_checker(visible_part[0]) == True:
                # result.append("Valid identifier")
                flag = True
                #check if the variable is in the symbol table
                result = semantics_functions.symbol_exists(visible_part[0][0])
                var_name = tokens[0][0]
                if not result:
                    raise Exception(f"Error in line {line_num}: Variable {visible_part[0][0]} is not declared")
                output = semantics_functions.get_symbol(visible_part[0][0])['value']
                print(output)


            
            # Check if it's a valid expression
            elif  len(visible_part) >= 2:
                if expression_checker(tokens[1:], semantics_functions.symbols, False) == True:
                    # result.append("Valid expression")
                    flag = True
                    output = semantics_functions.get_symbol("IT")['value']
                    print(output)
            # Check if the keyword is 'IT'
            elif first_value == "IT":
                #Check if there is a token after IT
                if (len(visible_part)) > 1:
                    raise Exception( f"ERRROR at line {line_num} : There should be no other token after IT")
                flag = True
                output = semantics_functions.get_symbol("IT")['value']
                print(output)
            else:
                # If it's none of the above, mark it invalid
                # result.append(f"ERROR: Invalid value after 'VISIBLE': {first_value}")
                raise Exception(f"ERROR at line {line_num}: Invalid value after 'VISIBLE': {first_value}")
                flag = False
    else:
        # If the line doesn't start with 'VISIBLE', it's invalid
        # result.append("ERROR: Line does not start with 'VISIBLE'.")
        # raise Exception("ERROR: Line does not start with 'VISIBLE'.")
        return False

    return flag
