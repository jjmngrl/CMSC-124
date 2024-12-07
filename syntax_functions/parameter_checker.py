from syntax_functions.literal_checker import literal_checker
from syntax_functions.identifier_checker import identifier_checker
from syntax_functions.expression_checker import expression_checker

# from literal_checker import literal_checker
# from identifier_checker import identifier_checker

def parameter_checker(token, line_num):
    print("\ninside parameter checker function")
    print("token to check: ",len(token))
    print(token)
    """
    Algo:
        - check if length of tokens is of 1 or more
        - if more than 1:
            - check if next token is 'AN'
            - recursively check the remaining tokens after AN
        - else (1) - check if valid literal
    """
    
    #check if token is an expression
    arithmetic_operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']
    boolean_operators = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT']
    nested_boolean_operators = ['ALL OF', 'ANY OF']
    concatenation_operator = ['SMOOSH']
    comparison_operators = ['BOTH SAEM', 'DIFFRINT']
    relational_operators = ['BIGGR OF', 'SMALLR OF']
    explicit_operator = ['MAEK']
    recast_operator = ['IS NOW A']

    if token[0][0] in arithmetic_operators or token[0][0] in boolean_operators \
    or token[0][0] in nested_boolean_operators or token[0][0] in concatenation_operator \
    or token[0][0] in comparison_operators or token[0][0] in relational_operators \
    or token[0][0] in explicit_operator or token[0][0] in recast_operator:
        if expression_checker(token, False) == True:
            print("Valid Parameter - expression")
            return True
        else:
            return f"ERROR at line {line_num}: Invalid parameter (expression)"




    if(len(token)) == 1:
        if literal_checker(token[0]) == True or identifier_checker(token[0]) == True: #insert expression checker
            print("Valid  parameter")
            return True
        else:
            print("invalid parameter: ", token[0])
            return f"ERROR at line {line_num}: Invalid parameter. Must be of type (1) literal, (2) identifier, (3) expression only"
    elif (len(token)) > 1:
        #recursive case
        if literal_checker(token[0]) == True or identifier_checker(token[0]) == True: #insert expression checker
            if token[1][0] == "AN" and token[2][0] == "YR":
                
                return parameter_checker(token[3:], line_num)
    else:
         raise Exception( f"ERROR at line {line_num}: No Parameter after YR")
        

