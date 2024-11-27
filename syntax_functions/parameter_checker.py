# from syntax_functions.literal_checker import literal_checker
# from syntax_functions.identifier_checker import identifier_checker

from literal_checker import literal_checker
from identifier_checker import identifier_checker

def parameter_checker(token):
    # print("\ninside parameter checker function")
    # print("token to check: ",token)
    """
    Algo:
        - check if length of tokens is of 1 or more
        - if more than 1:
            - check if next token is 'AN'
            - recursively check the remaining tokens after AN
        - else (1) - check if valid literal
    """
    if(len(token)) == 1:
        if literal_checker(token[0]) == True or identifier_checker(token[0]) == True: #insert expression checker
            print("Valid  parameter")
            return True
        else:
            print("invalid parameter: ", token[0])
            return False

    else:
        #recursive case
        if literal_checker(token[0]) == True or identifier_checker(token[0]) == True: #insert expression checker
            if token[1][0] == "AN":
                
                return parameter_checker(token[2:])

