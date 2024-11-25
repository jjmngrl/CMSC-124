from syntax_functions.identifier_checker import identifier_checker

""" 
Function to check if a token is a num
Parameter: Token and its type
Return value: True - valid num
                False - invalid num
"""

def num_checker(token):
    print("inside num checker")
    
    #token[1] is the type of the token
    if token[1] == "NUMBR": 
        return True
    elif token[1] == "YARN":
        return True
    elif token[1] == "NUMBAR":
        return True
    elif identifier_checker(token) == True:
        return True
    #elif insert expression checker
    else: 
        return False
