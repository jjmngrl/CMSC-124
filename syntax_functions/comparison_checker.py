from syntax_functions.num_checker import num_checker
""" 
Function to check if a comparison is valid
Parameter: list of tokens for the comparison (ex: pag ginamit sa visible, ang parameter ay yung 2d list pero di kasama si VISIBLE)
Return value: True - valid comparison
                False - invalid comparison
"""
def comparison_checker(token):
    #list of accepted keywords in comparison
    comparison_keywords = ['BOTH SAEM', 'DIFFRINT']

    #check if first token is keyword sa comparison
    if token[0][0] in comparison_keywords and token[0][1] == 'KEYWORD':
        # return True
        #check if next token is <num> (numbr, numbar, varident, expression, yar)
        if num_checker(token[1]) == True:
        #     #check if next token is AN
            if token[2][0] == "AN":
                if num_checker(token[3]) == True:
                    return True
    else:
        return False




# tokens = {
#     1: [['VISIBLE', 'KEYWORD'], ['BOTH SAEM', 'KEYWORD'], ['BIGGR OF', 'KEYWORD'], ['x', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['y', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['x', 'IDENTIFIER']],
#     2: [['VISIBLE', 'KEYWORD'], ['BOTH SAEM', 'KEYWORD'], ['x', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['SMALLR OF', 'KEYWORD'], ['x', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['y', 'IDENTIFIER']],
#     3: [['VISIBLE', 'KEYWORD'], ['DIFFRINT', 'KEYWORD'], ['BIGGR OF', 'KEYWORD'], ['x', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['y', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['x', 'IDENTIFIER']],
#     4: [['VISIBLE', 'KEYWORD'], ['DIFFRINT', 'KEYWORD'], ['x', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['SMALLR OF', 'KEYWORD'], ['x', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['y', 'IDENTIFIER']]
# }


# filtered = {key: value[1:] for key, value in tokens.items()}
# print(filtered)
#visible checker

""" Use this as a guide sa pagpasa ng parameter"""
# for i in tokens:
#     #check if first token is 'VISIBLE'
#     if tokens[i][0][0] == 'VISIBLE' and tokens[i][0][1] == 'KEYWORD':
#         print("valid")
        
#         #remove the first list of the token
#         filtered = tokens[i][1:]
#         # print(filtered)
#         #Check next token if comparison
#         if comparison_checker(filtered) == True:
#             print("Next token is a comparison")
#     else:
#         print("not valid")
    