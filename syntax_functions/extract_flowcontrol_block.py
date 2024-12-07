"""
    Extracts a single if-else block starting from a given line number.
    
    Parameters:
        code_block (dict): Dictionary containing lines of LOLCODE as line number -> tokens
        start_line (int): The line number where "O RLY?" is encountered
    
    Returns:
        tuple: (extracted_block, next_line) where
            - extracted_block: The extracted if-else block as a dictionary {line_num: tokens}
            - next_line: The line number after "OIC" for further processing
    """
def extract_ifelse_block(code_block, start_line):
    
    extracted_block = {}
    in_ifelse_block = False

    for line_num, tokens in code_block.items():
        if line_num < start_line:  # Skip lines before the start
            continue

        for token, token_type in tokens:
            if token == "O RLY?" and token_type == "KEYWORD" and line_num == start_line:
                in_ifelse_block = True  # Mark the start of the block
                extracted_block[line_num] = tokens
            elif token == "OIC" and token_type == "KEYWORD" and in_ifelse_block:
                extracted_block[line_num] = tokens  # Add the closing line
                in_ifelse_block = False
                return extracted_block, line_num + 1  # Return the block and next line
            elif in_ifelse_block:
                extracted_block[line_num] = tokens  # Add lines within the block

    raise Exception("OIC not found after O RLY?")  # Handle missing OIC



"""
Extracts a single switch-case block starting from a given line number.

Parameters:
    code_block (dict): Dictionary containing lines of LOLCODE as line number -> tokens
    start_line (int): The line number where "WTF?" is encountered

Returns:
    tuple: (extracted_block, next_line) where
        - extracted_block: The extracted switch-case block as a dictionary {line_num: tokens}
        - next_line: The line number after "OIC" for further processing
"""
def extract_switch_block(code_block, start_line):
    extracted_block = {}
    in_switch_block = False

    for line_num, tokens in code_block.items():
        if line_num < start_line:  # Skip lines before the start
            continue

        for token, token_type in tokens:
            if token_type == "KEYWORD" and token == "WTF?" and line_num == start_line:
                in_switch_block = True  # Mark the start of the switch block
                extracted_block[line_num] = tokens
            elif token_type == "KEYWORD" and token == "OIC" and in_switch_block:
                extracted_block[line_num] = tokens  # Add the closing line
                in_switch_block = False
                return extracted_block, line_num + 1  # Return the block and the next line
            elif in_switch_block:
                extracted_block[line_num] = tokens  # Add lines within the switch block

    raise Exception("OIC not found after WTF?")  # Handle missing OIC

"""
Extracts a single loop block starting from a given line number.

Parameters:
    code_block (dict): Dictionary containing lines of LOLCODE as line number -> tokens
    start_line (int): The line number where "IM IN YR" is encountered

Returns:
    tuple: (extracted_block, next_line) where
        - extracted_block: The extracted loop block as a dictionary {line_num: tokens}
        - next_line: The line number after "IM OUTTA YR" for further processing
"""
def extract_loop_block(code_block, start_line):
   
    extracted_block = {}
    in_loop_block = False

    for line_num, tokens in code_block.items():
        if line_num < start_line:  # Skip lines before the start
            continue

        for token, token_type in tokens:
            if token == "IM IN YR" and token_type == "KEYWORD" and line_num == start_line:
                in_loop_block = True  # Mark the start of the loop block
                extracted_block[line_num] = tokens
            elif token == "IM OUTTA YR" and token_type == "KEYWORD" and in_loop_block:
                extracted_block[line_num] = tokens  # Add the closing line
                in_loop_block = False
                return extracted_block, line_num + 1  # Return the block and the next line
            elif in_loop_block:
                extracted_block[line_num] = tokens  # Add lines within the loop block

    raise Exception("IM OUTTA YR not found after IM IN YR")  # Handle missing loop end

