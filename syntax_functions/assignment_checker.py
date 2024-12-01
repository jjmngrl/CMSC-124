from syntax_functions.literal_checker import literal_checker
from syntax_functions.identifier_checker import identifier_checker
from syntax_functions.expression_checker import expression_checker

def assignment_checker(line_num, tokens):
    flag = False  # Tracks if all VISIBLE statements are valid
    # Check if statement starts with variable
    if identifier_checker(tokens[0]):
        # Check if there's a value after 'R'
        if len(tokens) < 3:
            # result.append("ERROR: Missing value after 'VISIBLE'.")
            raise Exception ("ERROR at line {line_num}: Missing value after 'R'.")
            return False
        else:
            visible_part = tokens[2:]
            first_value, first_type = visible_part[0]
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
