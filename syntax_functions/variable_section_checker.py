from syntax_functions.variable_declaration_checker import variable_declaration_checker

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