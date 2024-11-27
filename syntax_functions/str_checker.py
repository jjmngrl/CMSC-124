from literal_checker import literal_checker
from identifier_checker import identifier_checker


""" 
Function to check if valid str - this is from the grammar. 
This is to handle recursive concatenations/smoosh
Parameter: tokens for the smoosh
Return value: True - valid str
                False - invalid str
"""


def str_checker(tokens):
    print("inside str_checker")
    print(tokens)
    """
    Algo:
        - check if length of tokens is of 1 or 3
        - if 3, recursion
        - else (1) - check if valid literal
    """
    if len(tokens) == 1:
        if(literal_checker(tokens[0])) == True or identifier_checker(tokens[0]) == True:
            print("Valid")
            return True
    else:
        #check if first token is a literal
        #Algo: check if literal, check if an, call back to str_checker function
        if(literal_checker(tokens[0])) == True or identifier_checker(tokens[0]) == True:
            #check if next is AN
            if tokens[1][0] == "AN":
                if(str_checker(tokens[2:]) == True):
                    return True
                
    return False
    #check if length of tokens is of size 1 or 3

