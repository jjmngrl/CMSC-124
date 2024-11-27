from syntax_functions.switch_checker import switch_checker
from syntax_functions.ifelse_checker import ifelse_checker
from syntax_functions.variable_section_checker import variable_section_checker
from syntax_functions.visible_statement_checker import visible_statement_checker
""" 
Function to check if a statement is valid. Multiple statement_type checker will be called in this function
Parameter: List containing each line of the lol code and the list of tokens
Return value: True - valid variable section
                False - invalid variable section
"""


"""
Dapat andito yung:
    - Print checker
    - variable_section
    - expression checker
    - assignment checker
    - flow_control
    - input



"""
def statement_checker(code_block, classified_tokens, result):
    print("Statement checker function.")
    wazzup_key = None
    buhbye_key = None
    variable_section_exists = False
    print(code_block)

    """Check if there is a variable section"""
    for line_num, tokens in code_block.items():
        for token, token_type in tokens:
            if token_type == "KEYWORD" and token == "WAZZUP":
                variable_section_exists = True
                wazzup_key = line_num
                print("There is a variable section in your program")
            if token_type == "KEYWORD" and token == "BUHBYE":
                variable_section_exists = True
                buhbye_key = line_num


    if variable_section_exists:
        #Check if variable section is valid
        if variable_section_checker(code_block, classified_tokens, result):
        #Create a new dictionary without the variable section to check what kind of statement are the remaining code
            new_code_block = {}
            for key, value in code_block.items():
                if wazzup_key is not None and buhbye_key is not None:
                    if wazzup_key <= key <= buhbye_key:
                        continue #Skip key in the range of WAZZUP to BUHBYE
                new_code_block[key] = value

            code_block =new_code_block
    
    
    else:
        result.append(("Variable section check.", "No variable section found."))
        print("Variable section check.", "No variable section found.")
        # return False

    """Check if there is an if-else block and validate it"""
    # Check if there is an if-else block and validate it
    ifelse_section_exists = False

    # First pass to check if any if-else block exists
    for line_num, tokens in code_block.items():
        for token, token_type in tokens:
            if token_type == "KEYWORD" and token == "O RLY?":
                ifelse_section_exists = True
                break
        if ifelse_section_exists:
            break

    if ifelse_section_exists:
        current_ifelse_block = []
        in_ifelse_block = False
        block_start_line = None
        ifelse_block_counter = 1
        ifelse_blocks = {}

        # Second pass to process the if-else blocks
        for line_num, tokens in code_block.items():
            for token, token_type in tokens:
                if token_type == "KEYWORD" and token == "O RLY?":
                    ifelse_blocks[ifelse_block_counter] = []
                    current_ifelse_block = ifelse_blocks[ifelse_block_counter]
                    current_ifelse_block.append((token, token_type))
                    in_ifelse_block = True
                    block_start_line = line_num
                elif token_type == "KEYWORD" and token == "OIC" and in_ifelse_block:
                    current_ifelse_block.append((token, token_type))
                    in_ifelse_block = False
                    block_start_line = None
                    ifelse_block_counter += 1
                elif in_ifelse_block:
                    current_ifelse_block.append((token, token_type))
        print("\nIf-Else checker")

        for case_id, case in ifelse_blocks.items():
            result = ifelse_checker({case_id: case})
            print(f"If-else block: {ifelse_blocks} \n If-else {case_id}: {'Valid if-else statement' if result == True else result}")
            print("\n")

    else:
        result.append(("If-else section check.", "No if-else section found."))
        print("If-else section check.", "No if-else section found.")

    # """Check if there is an if-else block and validate it"""
# Check if there is an if-else block and validate it
    switch_section_exists = False

    # First pass to check if any if-else block exists
    for line_num, tokens in code_block.items():
        for token, token_type in tokens:
            if token_type == "KEYWORD" and token == "WTF?":
                switch_section_exists = True
                break
        if switch_section_exists:
            break
    
    
    if switch_section_exists:
        switch_blocks = {}
        current_switch_block = []
        is_switch_case = False
        block_start_line = None
        switch_block_counter = 1

        for line_num, tokens in code_block.items():
            for token, token_type in tokens:
                if token_type == "KEYWORD" and token == "WTF?":
                    current_switch_block = [(token, token_type)]
                    is_switch_case = True
                    block_start_line = line_num
                elif token_type == "KEYWORD" and token == "OIC" and is_switch_case:
                    current_switch_block.append((token, token_type))
                    is_switch_case = False
                    switch_blocks[switch_block_counter] = current_switch_block
                    block_start_line = None
                    switch_block_counter += 1
                elif is_switch_case:
                    current_switch_block.append((token, token_type))
        print("\nSwitch checker")

        for case_id, case in switch_blocks.items():
            result = switch_checker({case_id: case})
            print(f"Switch block: {switch_blocks} \n Switch {case_id}: {'Valid switch statement' if result == True else result}")
            print("\n")
    else:
        print("Switch section check.", "No switch section found.")