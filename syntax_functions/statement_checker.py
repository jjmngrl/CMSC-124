from syntax_functions.variable_section_checker import variable_section_checker

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