from parameter_checker import parameter_checker
from visible_statement_checker import visible_statement_checker
""" 
Function to check if smoosh (concatenation) is valid
Parameter: tokens for the smoosh
Return value: True - valid smoosh
                False - invalid smoosh
"""




"""
In integrating in statement_checker.py, check this condition:
if token[1][0][0] == 'HOW' and token[1][1][0] == 'IZ' and token[1][2][0] == 'I' and token[3][1] == 'IDENTIFIER':
if true, find the tokens IF U SAY SO 
"""
def function_checker(token):
    print("\nInside function checker")

    ls_of_values = list(token.values()) #3d list 
    print(ls_of_values[0])
    # print(len(ls_of_values[0]))
    parameter_flag = True
    flag = False

    if ls_of_values[0][0][0] == 'HOW' and ls_of_values[0][1][0] == "IZ" and ls_of_values[0][2][0] == "I" and ls_of_values[0][3][1] == "IDENTIFIER":
        #If function has parameter/s, check if the parameters are valid parameters
        if len(ls_of_values[0]) > 4:
            print("Function has multiparameter")
            #check if function header has 'YR'
            if ls_of_values[0][4][0] == "YR":
                parameters = ls_of_values[0][5:]
                if parameter_checker(parameters) == True:
                    print("parameter/s is/are valid")
                    parameter_flag == True
                else:
                    parameter_flag == False
            else:
                print("Invalid function header")
                return False

        
        if parameter_flag == True: 
            #check the function body
            print("function body: " ,ls_of_values[1:])
            for line in ls_of_values[1:]:
                if visible_statement_checker(line) == True: #removethe line parameter in visible_statement_checker
                    print("valid print statement")
                    flag = True
                # elif variable section (VERIFY)

                #elif expression

                #elif assignment

                #elif func_call

                #elif flow control

                #elif input

                elif line[0][0] == "GTFO":
                    print("Valid GTFO")
                    flag = True

    return flag

            # if visible




    
    
    #Check if if start of line is HOW IZ I followed by an identifier
    # if token[2][0][0] == 'HOW' and token[2][1][0] == 'IZ' and token[2][2][0] == 'I' and token[3][1] == 'IDENTIFIER':
    #     print("valid")
    #     #Find the 
    # else:
    #     print("not valid")


    #check if the first 3 tokens is HOW IZ I and 4th token is an identifier
    


code_tokens = {
    1: [["HAI", "KEYWORD"]],
    2: [["HOW", "KEYWORD"], ["IZ", "KEYWORD"], ["I", "KEYWORD"], ["addNum", "IDENTIFIER"], ["YR", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],
    3: [["FOUND", "KEYWORD"], ["YR", "KEYWORD"], ["SUM", "KEYWORD"], ["OF", "KEYWORD"], ["x", "IDENTIFIER"], ["an", "KEYWORD"], ["y", "IDENTIFIER"]],
    4: [["IF", "KEYWORD"], ["U", "KEYWORD"], ["SAY", "KEYWORD"], ["SO", "KEYWORD"]],
    5: [["HOW", "KEYWORD"], ["IZ", "KEYWORD"], ["I", "KEYWORD"], ["printName", "IDENTIFIER"], ["YR", "KEYWORD"], ["person", "IDENTIFIER"]],
    6: [["VISIBLE", "KEYWORD"], ["\"Hello, \"", "STRING"], ["+", "OPERATOR"], ["person", "IDENTIFIER"]],
    7: [["GTFO", "KEYWORD"]],
    8: [["IF", "KEYWORD"], ["U", "KEYWORD"], ["SAY", "KEYWORD"], ["SO", "KEYWORD"]],
    9: [["HOW", "KEYWORD"], ["IZ", "KEYWORD"], ["I", "KEYWORD"], ["printNum", "IDENTIFIER"], ["YR", "KEYWORD"], ["x", "IDENTIFIER"]],
    10: [["FOUND", "KEYWORD"], ["YR", "KEYWORD"], ["x", "IDENTIFIER"]],
    11: [["IF", "KEYWORD"], ["U", "KEYWORD"], ["SAY", "KEYWORD"], ["SO", "KEYWORD"]],
    12: [["WAZZUP", "KEYWORD"]],
    13: [["I", "KEYWORD"], ["HAS", "KEYWORD"], ["A", "KEYWORD"], ["name", "IDENTIFIER"]],
    14: [["I", "KEYWORD"], ["HAS", "KEYWORD"], ["A", "KEYWORD"], ["num1", "IDENTIFIER"]],
    15: [["I", "KEYWORD"], ["HAS", "KEYWORD"], ["A", "KEYWORD"], ["num2", "IDENTIFIER"]],
    16: [["BUHBYE", "KEYWORD"]],
    17: [["GIMMEH", "KEYWORD"], ["num1", "IDENTIFIER"]],
    18: [["GIMMEH", "KEYWORD"], ["num2", "IDENTIFIER"]],
    19: [["I", "KEYWORD"], ["IZ", "KEYWORD"], ["addNuM", "IDENTIFIER"], ["YR", "KEYWORD"], ["num1", "IDENTIFIER"], ["AN", "KEYWORD"], ["num2", "IDENTIFIER"]],
    20: [["VISIBLE", "KEYWORD"], ["IT", "IDENTIFIER"]],
    21: [["GIMMEH", "KEYWORD"], ["name", "IDENTIFIER"]],
    22: [["I", "KEYWORD"], ["IZ", "KEYWORD"], ["printName", "IDENTIFIER"], ["YR", "KEYWORD"], ["name", "IDENTIFIER"]],
    23: [["VISIBLE", "KEYWORD"], ["IT", "IDENTIFIER"]],
    24: [["I", "KEYWORD"], ["IZ", "KEYWORD"], ["printNum", "IDENTIFIER"], ["YR", "KEYWORD"], ["SUM", "KEYWORD"], ["OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["2", "NUMBER"]],
    25: [["VISIBLE", "KEYWORD"], ["IT", "IDENTIFIER"]],
    26: [["KTHXBYE", "KEYWORD"]]
}




for key, value in code_tokens.items():
    if len(value) >= 3:
        # Check if the first 3 tokens are 'HOW IZ I'
        if value[0][0] == 'HOW' and value[1][0] == 'IZ' and value[2][0] == 'I':
            # Find the line/key of 'IF U SAY SO' - end of the function
            end_of_function = None
            for subsequent_key in range(key + 1, len(code_tokens) + 1):
                # Check if line contains 'IF U SAY SO'
                if all(token[0] == word for token, word in zip(code_tokens[subsequent_key], ['IF', 'U', 'SAY', 'SO'])):
                    end_of_function = subsequent_key
                    break
            #Function starts with 'HOW IZ I' and ends with 'IF U SAYO SO'    
            if end_of_function is not None:
                # Create a new dictionary of the contents inside the function starting from 'HOW IZ I'
                function_contents = {k: v for k, v in code_tokens.items() if k >= key and k < end_of_function}
                function_checker(function_contents)
                # for line, tokens in function_contents.items():
                # print(function_contents)
                #     print(f"Line {line}: {tokens}")
            
            else: #function does not end with IF U SAY SO
                print(f"no end for function starting at line {key}")
