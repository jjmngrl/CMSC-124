"""
Function to check if all variable declarations are in correct order
Parameter: Lines of code between WAZZUP and BUHBYE
Return value: True - Valid Variable declarations
                False - Invalid Variable declarations
"""
def variable_declaration_checker(variable_section, classified_tokens, result):
    valid_operations = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'BIGGR OF', 'SMALLR OF', 'MOD OF']
    overall_flag = True
    print("inside var declaration checker")
    """Iterate through all possible Variable declaration inside WAZZUP and BUHBYE"""
    for line_num, tokens in variable_section.items():
        print("checking line: ",tokens)
        flag = True
        if not tokens:
            continue

        prompt = ""
        if tokens[0][0] != "I HAS A" or tokens[0][1] != "KEYWORD":
            prompt = f"ERROR: Line must start with 'I HAS A'."
            flag = False
            print("ERROR: Line must start with 'I HAS A'.")
            return False
        else:
            print("Starts with I HAS A")
            variable_name = None
            itz_present = False
            value_part = None

            if len(tokens) > 1 and tokens[1][1] == "IDENTIFIER":
                variable_name = tokens[1][0]
            else:
                prompt = f"ERROR: Missing or invalid variable name after 'I HAS A'."
                flag = False
                print("ERROR: Missing or invalid variable name after 'I HAS A'.")
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
                    prompt = f"ERROR: No value provided after 'ITZ'."
                    flag = False
                    print("ERROR: No value provided after 'ITZ'.")
                    return False
                else:
                    first_value, first_type = value_part[0]

                    if first_type in ["NUMBR", "YARN", "NUMBAR", "TROOF"]:
                        """Check if yarn and if it is enclosed in quotation marks"""
                        if first_type == "YARN" and not (first_value.startswith('"') and first_value.endswith('"')):
                            prompt = f"ERROR: YARN '{first_value}' is not properly enclosed in quotes."
                            flag = False
                    elif first_type == "IDENTIFIER":
                        pass
                    elif first_value in valid_operations:
                        """Check if valid expression. If meron ng expression_checker, pwede iinsert dito"""
                        operands = []
                        is_operand = False

                        if len(value_part) > 1:
                            operands.append(value_part[1][0])

                        for token, token_type in value_part[2:]:
                            if token == "AN" and token_type == "KEYWORD":
                                is_operand = True
                                continue

                            if is_operand:
                                operands.append(token)
                                is_operand = False

                        if len(operands) < 2:
                            prompt = f"ERROR: Operation '{first_value}' requires at least two operands."
                            flag = False
                        else:
                            for operand in operands:
                                if not any(
                                    operand == token and token_type in ["IDENTIFIER", "NUMBR", "NUMBAR", "TROOF", "YARN"]
                                    for line_tokens in classified_tokens.values()
                                    for token, token_type in line_tokens
                                ):
                                    prompt = f"ERROR: '{operand}' is not a valid operand."
                                    flag = False
                    else:
                        prompt = f"ERROR: Invalid value '{value_part}' after 'ITZ'. Must be a valid literal, variable, or expression."
                        flag = False

        if flag:
            prompt = "Valid variable declaration."
            print(prompt)
        result.append((f"Line {line_num}: {tokens}", prompt))

        if not flag:
            overall_flag = False

    return overall_flag