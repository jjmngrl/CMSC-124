from syntax_functions.validate_expression import validate_expression
from syntax_functions.literal_checker import literal_checker
from syntax_functions.identifier_checker import identifier_checker
from syntax_functions.expression_checker import expression_checker

def visible_statement_checker(line, tokens, result):
    # Start by adding a log entry to show we're inside the visible statement checker
    result.append("\nInside visible statement checker")

    # Define valid literal types and operations
    flag = False  # Tracks if all VISIBLE statements are valid
    
    # Add the line and tokens to the result
    result.append(f"Line: {line}")
    result.append(f"Tokens: {tokens}")

    # Check if statement starts with 'VISIBLE'
    if tokens[0][0] == 'VISIBLE':
        # Check if there's a value after 'VISIBLE'
        if len(tokens) < 2:
            result.append("ERROR: Missing value after 'VISIBLE'.")
            return False
        else:
            visible_part = tokens[1:]
            first_value, first_type = visible_part[0]

            # Check if it's a literal
            if literal_checker(visible_part[0]) == True:
                result.append("Valid literal")
                flag = True
            # Check if it's an identifier
            elif identifier_checker(visible_part[0]) == True:
                result.append("Valid identifier")
                flag = True
            # Check if it's a valid expression
            elif expression_checker(tokens[1:], False) == True:
                result.append("Valid expression")
                flag = True
            else:
                # If it's none of the above, mark it invalid
                result.append(f"ERROR: Invalid value after 'VISIBLE': {first_value}")
                flag = False
    else:
        # If the line doesn't start with 'VISIBLE', it's invalid
        result.append("ERROR: Line does not start with 'VISIBLE'.")
        return False

    # Return the result flag (True if valid, False if invalid)
    return flag
