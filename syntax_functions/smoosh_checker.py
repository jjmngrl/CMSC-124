from syntax_functions.literal_checker import literal_checker
from syntax_functions.str_checker import str_checker
from syntax_functions.identifier_checker import identifier_checker

""" 
Function to check if smoosh (concatenation) is valid
Parameter: tokens for the smoosh
Return value: True - valid smoosh
                False - invalid smoosh
"""


def smoosh_checker(token):
    
    #check if first token is 'SMOOSH'
    if token[0][0] in 'SMOOSH' and token[0][1] == 'KEYWORD':
        # return True
        #check if next token is a literal
        if literal_checker(token[1]) == True or identifier_checker(token[1]) == True:
        #     #check if next token is AN
            print("valid literal")
            if token[2][0] == "AN":
                print(token[3:])
                if str_checker(token[3:]) == True:
                    return True
    else:
        return False





additional_tokens = {
    5: [['VISIBLE', 'KEYWORD'], ['SMOOSH', 'KEYWORD'], ['x', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['y', 'IDENTIFIER']],
    6: [['VISIBLE', 'KEYWORD'], ['SMOOSH', 'KEYWORD'], ['x', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['x', 'IDENTIFIER'], 
        ['AN', 'KEYWORD'], ['x', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['y', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['y', 'IDENTIFIER']]
}

for i in additional_tokens:
    filtered = additional_tokens[i][1:]
    print("FIltered: ", filtered)
    if smoosh_checker(filtered) == True:
        print("valid smoosh")
    else: print("invalid")