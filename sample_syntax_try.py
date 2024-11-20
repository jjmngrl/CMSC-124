from lexical_analyzer import *

"""
Function to check if the lol code starts with HAI and ends with KTHXBYE
Parameter: List containing each line of the lol code
Return value: If true, will call the function to check the code block
                else, return false
"""
def program_checker(code, result):
    line_numbers = sorted(code.keys())

    index_of_HAI = None
    for line_num in line_numbers:
        for token, token_type in code[line_num]:
            if token_type == 'KEYWORD' and token == 'HAI':
                index_of_HAI = line_num
                result.append((f"Line {line_num}: {code[line_num]}", "HAI found, program starts here."))
                break
        if index_of_HAI is not None:
            break

    index_of_KTHXBYE = None
    for line_num in reversed(line_numbers):
        for token, token_type in code[line_num]:
            if token_type == 'KEYWORD' and token == 'KTHXBYE':
                index_of_KTHXBYE = line_num
                result.append((f"Line {line_num}: {code[line_num]}", "KTHXBYE found, program ends here."))
                break
        if index_of_KTHXBYE is not None:
            break

    if index_of_HAI is not None and index_of_KTHXBYE is not None and index_of_HAI < index_of_KTHXBYE:
        return index_of_HAI, index_of_KTHXBYE
    else:
        result.append(("Program structure validation.", "ERROR: The program must start with HAI and end with KTHXBYE."))
        return False


"""
Function to check if all variable declarations are in correct order
Parameter: Lines of code between WAZZUP and BUHBYE
Return value: True - Valid Variable declarations
                False - Invalid Variable declarations
"""
def variable_declaration_checker(variable_section, classified_tokens, result):
    valid_operations = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'BIGGR OF', 'SMALLR OF', 'MOD OF']
    overall_flag = True

    for line_num, tokens in variable_section.items():
        flag = True
        if not tokens:
            continue

        prompt = ""

        if not tokens[0][0] == "I HAS A" or tokens[0][1] != "KEYWORD":
            prompt = f"ERROR: Line must start with 'I HAS A'."
            flag = False
        else:
            variable_name = None
            itz_present = False
            value_part = None

            if len(tokens) > 1 and tokens[1][1] == "IDENTIFIER":
                variable_name = tokens[1][0]
            else:
                prompt = f"ERROR: Missing or invalid variable name after 'I HAS A'."
                flag = False

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
                else:
                    first_value, first_type = value_part[0]

                    if first_type in ["NUMBR", "YARN", "NUMBAR", "TROOF"]:
                        if first_type == "YARN" and not (first_value.startswith('"') and first_value.endswith('"')):
                            prompt = f"ERROR: YARN '{first_value}' is not properly enclosed in quotes."
                            flag = False
                    elif first_type == "IDENTIFIER":
                        pass
                    elif first_value in valid_operations:
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
        result.append((f"Line {line_num}: {tokens}", prompt))

        if not flag:
            overall_flag = False

    return overall_flag

""" 
Function to check if the all variable declarations are enclosed in WAZZUP and BUHBYE
Parameter: List containing each line of the lol code and the list of tokens
Return value: True - valid variable section
                False - invalid variable section
"""
def variable_section_checker(code_block, classified_tokens, result):
    index_of_WAZZUP = None
    index_of_BUHBYE = None

    # Find the indices of WAZZUP and BUHBYE
    for line_num, tokens in code_block.items():
        for token, token_type in tokens:
            if token_type == "KEYWORD" and token == "WAZZUP":
                index_of_WAZZUP = line_num
                result.append((f"Line {line_num}: {tokens}", "WAZZUP found, start of variable section."))
            if token_type == "KEYWORD" and token == "BUHBYE":
                index_of_BUHBYE = line_num
                result.append((f"Line {line_num}: {tokens}", "BUHBYE found, end of variable section."))

    # Validate the existence and order of WAZZUP and BUHBYE
    if index_of_WAZZUP is None or index_of_BUHBYE is None or index_of_WAZZUP >= index_of_BUHBYE:
        result.append(("Variable section check.", "ERROR: Missing or improperly ordered WAZZUP and BUHBYE."))
        return False

    # Extract the variable section (lines between WAZZUP and BUHBYE)
    variable_section = {
        k: classified_tokens[k]
        for k in sorted(classified_tokens.keys())
        if index_of_WAZZUP < k < index_of_BUHBYE
    }

    # Validate the variable declarations in the extracted section
    if variable_declaration_checker(variable_section, classified_tokens, result):
        result.append(("", "Variable section is valid."))
        return True
    else:
        result.append(("", "ERROR: Invalid variable declarations in the variable section."))
        return False


""" 
Function to check if the all variable declarations are enclosed in WAZZUP and BUHBYE
Parameter: List containing each line of the lol code and the list of tokens
Return value: True - valid variable section
                False - invalid variable section
"""
def statement_checker(code_block, classified_tokens, result):
    variable_section_exists = False

    for line_num, tokens in code_block.items():
        for token, token_type in tokens:
            if token_type == "KEYWORD" and token == "WAZZUP":
                variable_section_exists = True
            if token_type == "KEYWORD" and token == "BUHBYE":
                variable_section_exists = True

    if variable_section_exists:
        return variable_section_checker(code_block, classified_tokens, result)
    else:
        result.append(("Variable section check.", "No variable section found."))
        return False

def validate_expression(expression_tokens, classified_tokens):
    """
    Validates expressions, including unary, binary, and nested operations.
    """
    valid_operations = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF']
    index = 0

    def is_valid_operand(token, token_type):
        """Validates if a token is a valid operand."""
        if token_type in ["NUMBR", "NUMBAR", "TROOF", "YARN"]:
            return True
        if token_type == "IDENTIFIER":
            return any(
                token == t and tt == "IDENTIFIER"
                for line_tokens in classified_tokens.values()
                for t, tt in line_tokens
            )
        return False

    def parse_unary():
        """Parses unary operations like NOT <operand>."""
        nonlocal index
        if index < len(expression_tokens) and expression_tokens[index][0] == "NOT":
            index += 1
            if index < len(expression_tokens):
                token, token_type = expression_tokens[index]
                if is_valid_operand(token, token_type):
                    index += 1
                    return True, "Valid unary operation."
                return False, f"ERROR: Invalid operand '{token}' for NOT operation."
        return False, "ERROR: Invalid unary operation."

    def parse_binary():
        """Parses binary operations like BOTH OF <operand> AN <operand>."""
        nonlocal index
        if index < len(expression_tokens) and expression_tokens[index][0] in ['BOTH OF', 'EITHER OF', 'WON OF']:
            operation = expression_tokens[index][0]
            index += 1
            if index < len(expression_tokens):
                token1, token_type1 = expression_tokens[index]
                if is_valid_operand(token1, token_type1):
                    index += 1
                    if index < len(expression_tokens) and expression_tokens[index][0] == "AN":
                        index += 1
                        if index < len(expression_tokens):
                            token2, token_type2 = expression_tokens[index]
                            if is_valid_operand(token2, token_type2):
                                index += 1
                                return True, f"Valid binary operation: {operation}."
                            return False, f"ERROR: Invalid second operand '{token2}'."
                    return False, f"ERROR: Missing 'AN' in binary operation '{operation}'."
                return False, f"ERROR: Invalid first operand '{token1}'."
        return False, "ERROR: Invalid binary operation."

    def parse_nested():
        """Parses nested operations like ALL OF <operand> AN <operand> ... MKAY."""
        nonlocal index
        if index < len(expression_tokens) and expression_tokens[index][0] in ["ALL OF", "ANY OF"]:
            operation = expression_tokens[index][0]
            index += 1
            has_operands = False
            while index < len(expression_tokens):
                token, token_type = expression_tokens[index]
                if token == "MKAY":
                    if has_operands:
                        index += 1
                        return True, f"Valid nested operation: {operation}."
                    return False, f"ERROR: Missing operands for nested operation '{operation}'."
                elif is_valid_operand(token, token_type):
                    index += 1
                    has_operands = True
                    # Allow optional 'AN' between operands
                    if index < len(expression_tokens) and expression_tokens[index][0] == "AN":
                        index += 1
                else:
                    return False, f"ERROR: Invalid operand '{token}' in nested operation '{operation}'."
            return False, f"ERROR: Missing 'MKAY' in nested operation '{operation}'."
        return False, "ERROR: Invalid nested operation."

    # Parsing starts here
    valid = False
    message = "ERROR: Invalid expression."
    if index < len(expression_tokens):
        token = expression_tokens[index][0]
        if token == "NOT":
            valid, message = parse_unary()
        elif token in ["BOTH OF", "EITHER OF", "WON OF"]:
            valid, message = parse_binary()
        elif token in ["ALL OF", "ANY OF"]:
            valid, message = parse_nested()
        elif is_valid_operand(expression_tokens[index][0], expression_tokens[index][1]):
            valid = True
            message = "Valid literal or identifier."

    # Ensure all tokens are consumed
    if valid and index < len(expression_tokens):
        return "ERROR: Unexpected tokens after valid expression.", False

    return message, valid




def visible_statement_checker(code_block, classified_tokens, result):
    """
    Validates VISIBLE statements.
    """
    valid_literals = ["YARN", "NUMBR", "NUMBAR", "TROOF"]
    valid_operations = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF']
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

        result.append((f"Line {line_num}: {tokens}", prompt))

    # Append a global summary if all statements were valid
    if flag:
        result.append(("", "All VISIBLE statements are valid."))

    return flag



def bool_checker(tokens, classified_tokens, result):
    """
    Validate boolean expressions.
    Parameters:
        tokens: List of tokens to validate the boolean expressions.
        classified_tokens: All classified tokens for cross-reference.
        result: List to append error or validation messages.
    Returns:
        bool: True if the boolean expressions are valid, False otherwise.
    """
    def validate_bool_expression(tokens):
        """
        Recursive helper to validate a single boolean expression.
        Parameters:
            tokens: The list of tokens for the boolean expression.
        Returns:
            bool: True if valid, False otherwise.
        """
        if not tokens:
            return False

        if tokens[0][0] in ["BOTH OF", "EITHER OF", "WON OF"]:
            # Validate "BOTH OF <x> AN <y>", "EITHER OF <x> AN <y>", "WON OF <x> AN <y>"
            if len(tokens) < 5:
                result.append((tokens, "ERROR: Insufficient tokens for binary boolean operation."))
                return False
            if tokens[2][0] != "AN":
                result.append((tokens, "ERROR: Missing 'AN' in binary boolean operation."))
                return False
            return True

        elif tokens[0][0] == "NOT":
            # Validate "NOT <x>"
            if len(tokens) < 2:
                result.append((tokens, "ERROR: Insufficient tokens for unary NOT operation."))
                return False
            return True

        elif tokens[0][0] in ["ALL OF", "ANY OF"]:
            # Validate nested boolean operations
            stack = []
            nested_tokens = []
            for token, token_type in tokens:
                if token in ["ALL OF", "ANY OF"]:
                    stack.append(token)
                    nested_tokens.append((token, token_type))
                elif token == "MKAY":
                    if not stack:
                        result.append((tokens, "ERROR: Unmatched 'MKAY' without 'ALL OF' or 'ANY OF'."))
                        return False
                    stack.pop()
                    nested_tokens.append((token, token_type))
                else:
                    nested_tokens.append((token, token_type))
                    if not stack and token != "MKAY":
                        result.append((tokens, "ERROR: Missing 'MKAY' for nested boolean operation."))
                        return False

            if stack:
                result.append((tokens, "ERROR: Missing 'MKAY' for nested boolean operation."))
                return False

            # Check for invalid nesting
            for i, (token, _) in enumerate(nested_tokens):
                if token == "MKAY" and i + 1 < len(nested_tokens) and nested_tokens[i + 1][0] in ["ALL OF", "ANY OF"]:
                    result.append((tokens, "ERROR: Nested 'ALL OF' or 'ANY OF' after 'MKAY' is invalid."))
                    return False
            return True

        else:
            result.append((tokens, "ERROR: Invalid boolean expression."))
            return False

    overall_flag = True
    for line_num, line_tokens in classified_tokens.items():
        if line_tokens and line_tokens[0][0] in ["BOTH OF", "EITHER OF", "WON OF", "NOT", "ALL OF", "ANY OF"]:
            if not validate_bool_expression(line_tokens):
                overall_flag = False
                result.append((f"Line {line_num}: {line_tokens}", "Invalid boolean expression."))
            else:
                result.append((f"Line {line_num}: {line_tokens}", "Valid boolean expression."))

    return overall_flag




def main():
    result = []
    # classified_tokens = classifier(text)
    classified_tokens = {
    1: [["HAI", "KEYWORD"]],  # Program start
    2: [["WAZZUP", "KEYWORD"]],  # Start of variable section
    3: [],  # Comment converted to an empty list
    4: [["I HAS A", "KEYWORD"], ["x", "IDENTIFIER"]],  # Variable declaration x
    5: [["I HAS A", "KEYWORD"], ["y", "IDENTIFIER"]],  # Variable declaration y
    6: [["BUHBYE", "KEYWORD"]],  # End of variable section

    7: [["VISIBLE", "KEYWORD"], ['"x:"', "YARN"], ["WIN", "TROOF"], ['", y:"', "YARN"], ["WIN", "TROOF"]],  # VISIBLE with TROOF literals
    8: [["x", "IDENTIFIER"], ["R", "KEYWORD"], ["WIN", "TROOF"]],  # Assignment
    9: [["y", "IDENTIFIER"], ["R", "KEYWORD"], ["WIN", "TROOF"]],  # Assignment

    10: [["VISIBLE", "KEYWORD"], ["BOTH OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # BOTH OF operation
    11: [["VISIBLE", "KEYWORD"], ["EITHER OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # EITHER OF operation
    12: [["VISIBLE", "KEYWORD"], ["WON OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # WON OF operation
    13: [["VISIBLE", "KEYWORD"], ["NOT", "KEYWORD"], ["x", "IDENTIFIER"]],  # NOT operation
    14: [["VISIBLE", "KEYWORD"], ["ALL OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["MKAY", "KEYWORD"]],  # ALL OF operation
    15: [["VISIBLE", "KEYWORD"], ["ANY OF", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["0", "NUMBR"], ["MKAY", "KEYWORD"]],  # ANY OF operation
    16: [["VISIBLE", "KEYWORD"], ["ANY OF", "KEYWORD"], ["BOTH OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["EITHER OF", "KEYWORD"], ["NOT", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["NOT", "KEYWORD"], ["y", "IDENTIFIER"], ["MKAY", "KEYWORD"]],  # Complex ANY OF operation
    17: [["VISIBLE", "KEYWORD"], ["BOTH OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["EITHER OF", "KEYWORD"], ["NOT", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # Complex BOTH OF operation

    18: [["VISIBLE", "KEYWORD"], ['"x:"', "YARN"], ["FAIL", "TROOF"], ['", y:"', "YARN"], ["WIN", "TROOF"]],  # VISIBLE with mixed TROOF
    19: [["x", "IDENTIFIER"], ["R", "KEYWORD"], ["FAIL", "TROOF"]],  # Assignment to FAIL

    20: [["VISIBLE", "KEYWORD"], ["BOTH OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # Repeat operations
    21: [["VISIBLE", "KEYWORD"], ["EITHER OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],
    22: [["VISIBLE", "KEYWORD"], ["WON OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],
    23: [["VISIBLE", "KEYWORD"], ["NOT", "KEYWORD"], ["x", "IDENTIFIER"]],
    24: [["VISIBLE", "KEYWORD"], ["ALL OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
    25: [["VISIBLE", "KEYWORD"], ["ANY OF", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["0", "NUMBR"], ["MKAY", "KEYWORD"]],
    26: [["VISIBLE", "KEYWORD"], ["ANY OF", "KEYWORD"], ["BOTH OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["EITHER OF", "KEYWORD"], ["NOT", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["NOT", "KEYWORD"], ["y", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
    27: [["VISIBLE", "KEYWORD"], ["BOTH OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["EITHER OF", "KEYWORD"], ["NOT", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],

    28: [["VISIBLE", "KEYWORD"], ['"x:"', "YARN"], ["FAIL", "TROOF"], ['", y:"', "YARN"], ["FAIL", "TROOF"]],  # Mixed TROOFs
    29: [["y", "IDENTIFIER"], ["R", "KEYWORD"], ["FAIL", "TROOF"]],

    30: [["VISIBLE", "KEYWORD"], ["BOTH OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],
    31: [["VISIBLE", "KEYWORD"], ["EITHER OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],
    32: [["VISIBLE", "KEYWORD"], ["WON OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],
    33: [["VISIBLE", "KEYWORD"], ["NOT", "KEYWORD"], ["x", "IDENTIFIER"]],
    34: [["VISIBLE", "KEYWORD"], ["ALL OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
    35: [["VISIBLE", "KEYWORD"], ["ANY OF", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["0", "NUMBR"], ["MKAY", "KEYWORD"]],
    36: [["VISIBLE", "KEYWORD"], ["ANY OF", "KEYWORD"], ["BOTH OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["EITHER OF", "KEYWORD"], ["NOT", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["NOT", "KEYWORD"], ["y", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
    37: [["VISIBLE", "KEYWORD"], ["BOTH OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["EITHER OF", "KEYWORD"], ["NOT", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],

    38: [["KTHXBYE", "KEYWORD"]]  # Program end
}

    program_indices = program_checker(classified_tokens, result)
    if program_indices:
        index_of_HAI, index_of_KTHXBYE = program_indices
        code_block_in_program = {
            k: classified_tokens[k]
            for k in sorted(classified_tokens.keys())
            if index_of_HAI < k < index_of_KTHXBYE
        }

        # Check the program structure and statements
        if statement_checker(code_block_in_program, classified_tokens, result):
            result.append(("", "Program is valid."))
        else:
            result.append(("", "Invalid program structure or statements."))

        # Check VISIBLE statements
        if visible_statement_checker(code_block_in_program, classified_tokens, result):
            result.append(("", "All VISIBLE statements are valid."))
        else:
            result.append(("", "Error/s found in VISIBLE statements."))

        # Check boolean expressions
        bool_checker_result = []
        if bool_checker(code_block_in_program, classified_tokens, bool_checker_result):
            bool_checker_result.append(("", "All boolean expressions are valid."))
        else:
            bool_checker_result.append(("", "Errors found in boolean expressions."))

        # Combine results
        result.extend(bool_checker_result)
    else:
        result.append(("", "ERROR: The program must start with HAI and end with KTHXBYE."))

    # Sort results by line numbers where applicable
    sorted_result = sorted(result, key=lambda x: int(x[0].split()[1].strip(':')) if "Line" in x[0] else float('inf'))

    # Print each result
    for message in sorted_result:
        print(message[0])  # First element of the tuple
        print(message[1])  # Second element of the tuple
        print()  # Blank line for better readability


main()