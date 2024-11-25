from syntax_functions.validate_expression import validate_expression
<<<<<<< Updated upstream
=======
from syntax_functions.literal_checker import literal_checker
from syntax_functions.identifier_checker import identifier_checker
from syntax_functions.bool_checker import bool_checker
>>>>>>> Stashed changes

def visible_statement_checker(code_block, classified_tokens, result):
    valid_literals = ["YARN", "NUMBR", "NUMBAR", "TROOF"]
    valid_operations = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'BIGGR OF', 'SMALLR OF', 'MOD OF', 'BOTH SAEM', 'DIFFRINT', 'BOTH OF', 'EITHER OF', 'WON OF']
    flag = True  # Tracks if all VISIBLE statements are valid

    for line_num, tokens in code_block.items():
        if not tokens:
            continue

        prompt = ""
        if tokens[0][0] != "VISIBLE" or tokens[0][1] != "KEYWORD":
            continue

        if len(tokens) < 2:
            prompt = "ERROR: Missing value after 'VISIBLE'."
            flag = False
        else:
            visible_part = tokens[1:]
            first_value, first_type = visible_part[0]

<<<<<<< Updated upstream
            # Check for literals
            if first_type in valid_literals:
                prompt = "Valid VISIBLE statement."
            # Check for identifiers
            elif first_type == "IDENTIFIER":
                if not any(
                    first_value == token
                    for line_tokens in classified_tokens.values()
                    for token, token_type in line_tokens
                    if token_type == "IDENTIFIER"
                ):
                    prompt = f"ERROR: Undefined identifier '{first_value}' used in 'VISIBLE'."
                    flag = False
                else:
                    prompt = "Valid VISIBLE statement."
            # Check for expressions or comparisons
            elif first_value in valid_operations:
                expression_result, is_valid = validate_expression(visible_part, classified_tokens)
                prompt = expression_result
                if not is_valid:
                    flag = False
            else:
                prompt = f"ERROR: Invalid VISIBLE statement starting with '{first_value}'."
                flag = False
=======
            #Check if Literal
            if literal_checker(visible_part[0]) == True:
                print("valid literal")
                flag = True
            #check if identifier
            elif identifier_checker(visible_part[0]) == True:
                flag = True
                print("Valid identifier")
            #check if valid expression - insert valid expression checker
            # check if bool
            elif bool_checker(visible_part[0]) == True:
                flag = True
                print("Valid bool")
>>>>>>> Stashed changes

        result.append((f"Line {line_num}: {tokens}", prompt))

    # Append a global summary if all statements were valid
    if flag:
        result.append(("", "All VISIBLE statements are valid."))

    return flag
