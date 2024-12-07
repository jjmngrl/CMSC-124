from syntax_functions.semantics_functions import *

"""
    Function to check if GIMMEH statements are valid.
    Rule: The token following GIMMEH must be an IDENTIFIER.
"""
def gimmeh_statement_checker(token):
    flag = True  # Tracks if all GIMMEH statements are valid

    if len(token) == 2 and token[1][1] == "IDENTIFIER":
        #semantics
    
        #check if token exists in the symbol table
        result = symbol_exists(token[1][0])

        #Insert logic to accept input of user
        print(result)
        return True
    else:
        return False
    


# test_case = {
#     7: [['GIMMEH', 'KEYWORD'], ['monde', 'IDENTIFIER']],
#     10: [['GIMMEH', 'KEYWORD'], ['num', 'IDENTIFIER']],
#     11: [['GIMMEH', 'KEYWORD'], ['monde', 'IDENTIFIER']],
# }

# # Run test cases
# for i, (line_num, tokens) in enumerate(test_case.items()):
#     # print(i)
#     result = gimmeh_statement_checker(tokens)
#     print(f"Test Case {i}: {'Valid' if result == True else result}")