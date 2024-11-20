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
    valid_operations = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'BIGGR OF', 'SMALLR OF', 'MOD OF', 'BOTH SAEM', 'DIFFRINT', 'BOTH OF', 'EITHER OF', 'WON OF']
    stack = []
    local_flag = True  # Track errors locally within the function

    for token, token_type in expression_tokens:
        print(f"Processing token: {token}, type: {token_type}")
        
        if token in valid_operations and token_type == "KEYWORD":
            stack.append((token, "operation"))
        elif token == "AN" and token_type == "KEYWORD":
            stack.append((token, "keyword"))
        elif token_type in ["NUMBR", "NUMBAR", "TROOF", "YARN", "IDENTIFIER"]:
            if token_type == "IDENTIFIER":
                if not any(
                    token == t and tt == "IDENTIFIER"
                    for line_tokens in classified_tokens.values()
                    for t, tt in line_tokens
                ):
                    print(f"ERROR: Undefined identifier '{token}' in expression.")
                    local_flag = False
            stack.append((token, "operand"))
        else:
            print(f"ERROR: Invalid token '{token}' in expression.")
            local_flag = False

        # Iteratively process the stack for reductions
        while True:
            # Handle BOTH SAEM and DIFFRINT patterns: operation operand keyword operand
            if len(stack) >= 4 and stack[-4][1] == "operation" and stack[-3][1] == "operand" and stack[-2][1] == "keyword" and stack[-1][1] == "operand":
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"
                stack = stack[:-4] + [(reduced_expression, "operand")]
                print(f"Reduced (comparison): {reduced_expression}")

            # Handle other patterns (nested operations, binary operations)
            elif len(stack) >= 5 and stack[-5][1] == "operation" and stack[-4][1] == "operand" and stack[-3][1] == "keyword" and stack[-2][1] == "operand" and stack[-1][1] == "keyword":
                operation = stack[-5][0]
                operand1 = stack[-4][0]
                operand2 = stack[-2][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"
                stack = stack[:-5] + [(reduced_expression, "operand")]
                print(f"Reduced (nested): {reduced_expression}")

            elif len(stack) >= 3 and stack[-3][1] == "operation" and stack[-2][1] == "operand" and stack[-1][1] == "operand":
                operation = stack[-3][0]
                operand1 = stack[-2][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"
                stack = stack[:-3] + [(reduced_expression, "operand")]
                print(f"Reduced (binary): {reduced_expression}")

            else:
                break

        print(f"Current stack: {stack}")

    # Final validation of the stack
    if len(stack) == 1 and stack[0][1] == "operand" and local_flag:
        return "Valid VISIBLE statement.", True
    else:
        print(f"Final stack: {stack}")
        return "ERROR: Malformed expression.", False


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

def gimmeh_statement_checker(code_block, classified_tokens, result):
    """
    Function to check if GIMMEH statements are valid.
    Rule: The token following GIMMEH must be an IDENTIFIER.
    """
    flag = True  # Tracks if all GIMMEH statements are valid

    for line_num, tokens in code_block.items():
        if not tokens:
            continue

        # Check if the statement starts with GIMMEH
        if tokens[0][0] == "GIMMEH" and tokens[0][1] == "KEYWORD":
            if len(tokens) < 2:
                result.append((f"Line {line_num}: {tokens}", "ERROR: Missing identifier after 'GIMMEH'."))
                flag = False
            elif tokens[1][1] != "IDENTIFIER":
                result.append((f"Line {line_num}: {tokens}", f"ERROR: Expected IDENTIFIER after 'GIMMEH', found '{tokens[1][0]}' instead."))
                flag = False
            else:
                result.append((f"Line {line_num}: {tokens}", "Valid GIMMEH statement."))

    return flag


def main():
    result = []
    # classified_tokens = classifier(text)
    classified_tokens = {
    1: [["HAI", "KEYWORD"]],  # Program start
    2: [["WAZZUP", "KEYWORD"]],  # Start of variable section
    3: [["I HAS A", "KEYWORD"], ["x", "IDENTIFIER"]],  # Variable declaration (NOOB by default)
    4: [["I HAS A", "KEYWORD"], ["y", "IDENTIFIER"]],  # Variable declaration (NOOB by default)
    5: [["BUHBYE", "KEYWORD"]],  # End of variable section
    6: [["VISIBLE", "KEYWORD"], ['"Value 1: "', "YARN"]],  # Print literal
    7: [["GIMMEH", "KEYWORD"], ["x", "IDENTIFIER"]],  # Input for x
    8: [["VISIBLE", "KEYWORD"], ['"Value 2: "', "YARN"]],  # Print literal
    9: [["GIMMEH", "KEYWORD"], ["y", "IDENTIFIER"]],  # Input for y
    10: [],  # Comment converted to an empty list (x == y)
    11: [["VISIBLE", "KEYWORD"], ["BOTH SAEM", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # Comparison (x == y)
    12: [],  # Comment converted to an empty list (x != y)
    13: [["VISIBLE", "KEYWORD"], ["DIFFRINT", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # Comparison (x != y)
    14: [["OBTW", "COMMENT"]],  # Multiline comment start
    15: [["x >= y", "YARN"]],  # Multiline comment content
    16: [["x <= y", "YARN"]],  # Multiline comment content
    17: [["x < y", "YARN"]],  # Multiline comment content
    18: [["x > y", "YARN"]],  # Multiline comment content
    19: [["TLDR", "COMMENT"]],  # Multiline comment end
    20: [["VISIBLE", "KEYWORD"], ["BOTH SAEM", "KEYWORD"], ["BIGGR OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["x", "IDENTIFIER"]],  # BOTH SAEM BIGGR OF x AN y AN x
    21: [["VISIBLE", "KEYWORD"], ["BOTH SAEM", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["SMALLR OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # BOTH SAEM x AN SMALLR OF x AN y
    22: [["VISIBLE", "KEYWORD"], ["DIFFRINT", "KEYWORD"], ["BIGGR OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["x", "IDENTIFIER"]],  # DIFFRINT BIGGR OF x AN y AN x
    23: [["VISIBLE", "KEYWORD"], ["DIFFRINT", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["SMALLR OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # DIFFRINT x AN SMALLR OF x AN y
    24: [["KTHXBYE", "KEYWORD"]]  # Program end
}

    program_indices = program_checker(classified_tokens, result)
    if program_indices:
        index_of_HAI, index_of_KTHXBYE = program_indices
        code_block_in_program = {
            k: classified_tokens[k]
            for k in sorted(classified_tokens.keys())
            if index_of_HAI < k < index_of_KTHXBYE
        }
        if statement_checker(code_block_in_program, classified_tokens, result):
            result.append(("", "Program is valid."))
        else:
            result.append(("", "Invalid program structure or statements."))

        if gimmeh_statement_checker(code_block_in_program, classified_tokens, result):
            result.append(("", "All GIMMEH statements are valid."))
        else:
            result.append(("", "Error/s found in GIMMEH statements."))

        if visible_statement_checker(code_block_in_program, classified_tokens, result):
            result.append(("", "All VISIBLE statements are valid."))
        else:
            result.append(("", "Error/s found in VISIBLE statements."))
    else:
        result.append(("", "ERROR: The program must start with HAI and end with KTHXBYE."))

    # Sort results by line numbers where applicable and print
    sorted_result = sorted(result, key=lambda x: int(x[0].split()[1].strip(':')) if "Line" in x[0] else float('inf'))
    
    # Print each element of the tuple on a new line
    for message in sorted_result:
        print(message[0])  # First element of the tuple
        print(message[1])  # Second element of the tuple
        print()  # Blank line for better readability

main()
