from syntax_functions import semantics_functions
from syntax_functions import expression_checker

"""
Function to check if all variable declarations are in correct order
Parameter: Lines of code between WAZZUP and BUHBYE
Return value: True - Valid Variable declarations
                False - Invalid Variable declarations
"""
def variable_declaration_checker(variable_section, classified_tokens):
    valid_operations = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'BIGGR OF', 'SMALLR OF', 'MOD OF']
    overall_flag = True
    """Iterate through all possible Variable declaration inside WAZZUP and BUHBYE"""
    for line_num, tokens in variable_section.items():
        # print("checking line: ",tokens)
        flag = True
        if not tokens:
            continue

        prompt = ""
        if tokens[0][0] != "I HAS A" or tokens[0][1] != "KEYWORD":
            prompt = f"ERROR: Line must start with 'I HAS A'."
            flag = False
            raise Exception (f"ERROR in line {line_num}: Line must start with 'I HAS A'.")
            return False
        else:
            variable_name = None
            itz_present = False
            value_part = None
            value_type = None
            

            if len(tokens) > 1 and tokens[1][1] == "IDENTIFIER":
                variable_name = tokens[1][0]

            else:
                prompt = f"ERROR in line {line_num}: Missing or invalid variable name after 'I HAS A'."
                flag = False
                raise Exception(prompt)
                return False


            """This will check if there is an ITZ in the declaration"""
            for i, (token, token_type) in enumerate(tokens):
                if token == "ITZ" and token_type == "KEYWORD":
                    itz_present = True
                    if i + 1 < len(tokens):
                        value_part = tokens[i + 1:]
                    break

            if itz_present:
                if not value_part or len(value_part) == 0:
                    prompt = f"ERROR in line {line_num}: No value provided after 'ITZ'."
                    flag = False
                    raise Exception(prompt)
                    return False
                else:
                    first_value, first_type = value_part[0]
                    value_type = first_type
                    if first_type in ["NUMBR", "YARN", "NUMBAR", "TROOF"]:
                        """Check if yarn and if it is enclosed in quotation marks"""
                        if first_type == "YARN" and not (first_value.startswith('"') and first_value.endswith('"')):
                            prompt = f"ERROR in line {line_num}: YARN '{first_value}' is not properly enclosed in quotes."
                            raise Exception(prompt)
                            flag = False
                        if value_part != None:
                            if value_part[0][1] == "NUMBAR":
                                value_part[0][0] = float(value_part[0][0])
                            elif value_part[0][1] == "NUMBR":
                                value_part[0][0] = int(value_part[0][0])

                            semantics_functions.add_symbol(variable_name, {"type": "identifier", "value": value_part[0][0], "value_type": value_type, "reference_environment": "Main"} )
                        else:
                            semantics_functions.add_symbol(variable_name, {"type": "identifier", "value": value_part, "value_type": value_type, "reference_environment": "Main"} )

                    elif first_type == "IDENTIFIER":
                        pass
                    elif first_value in valid_operations:
                        """Check if valid expression. If meron ng expression_checker, pwede iinsert dito"""
                        if expression_checker.expression_checker(value_part, semantics_functions.symbols, False) == True:
                            value_of_expr = semantics_functions.get_symbol("IT")['value']
                            value_type_of_expr = semantics_functions.get_symbol("IT")['value_type']
                            semantics_functions.add_symbol(variable_name, {"type": "identifier", "value": value_of_expr, "value_type": value_type_of_expr, "reference_environment": "Main"} )
                            
                            flag = True
 
                    else:
                        prompt = f"ERROR in line {line_num}: Invalid value '{value_part}' after 'ITZ'. Must be a valid literal, variable, or expression."
                        raise Exception(prompt)
                        flag = False
            else:
                semantics_functions.add_symbol(variable_name, {"type": "identifier", "value": None, "value_type": "NOOB", "reference_environment": "Main"} )

        if flag:
            prompt = "Valid variable declaration."
        # result.append((f"Line {line_num}: {tokens}", prompt))

        if not flag:
            raise Exception("Invalid Variable Declaration")
            overall_flag = False

    return overall_flag