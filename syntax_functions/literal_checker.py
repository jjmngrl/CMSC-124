""" 
Function to check if a token is a valid literal
Parameter: Token and its type
Return value: True - valid literal
                False - invalid literal
"""


def literal_checker(token):
    valid_literals = ["YARN", "NUMBR", "NUMBAR", "TROOF"]
    
    print("In literal_checker function, checking token: ", token)
    if token[1] in valid_literals: 
        return True
    else: return False