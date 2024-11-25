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

    """ Check succeeding line and determine the type of statement"""
    for key, value in code_block.items():
        if value == []: #skip the spaces
            continue
        # print(code_block)
        #key - lines; value - tokens
        if visible_statement_checker(key,value, result) == True:
            print("Valid print statement")
    