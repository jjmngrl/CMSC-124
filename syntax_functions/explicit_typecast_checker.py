
# from syntax_functions.data_type_checker import data_type_checker
# from syntax_functions import semantics_functions
from syntax_functions.data_type_checker import data_type_checker
from syntax_functions import semantics_functions








#Accept token of this format [token, token_type]
def to_nmbr_numbar(line_num,token_param):
# symbol_table.update_symbol("num", value="42", value_type="NUMBR") #can be used for expression, typecast, changing value of IT and other vars
    print("to number or numbar")
    token = token_param[0]
    token_type = semantics_functions.get_symbol(token)['value_type']
    print("token: ", token_type)

    if token_type == "TROOF":
        #if win, value is 1. else 0
        if token == "WIN":
            semantics_functions.update_symbol(token, value_type="NUMBR", value=1)
        else:
            semantics_functions.update_symbol(token, value_type="NUMBR", value=0)
    elif token_type == "NUMBR" or token_type == "NUMBAR":
        return
    else: #type is not troof
        value_of_token = semantics_functions.get_symbol(token)['value']
        
        try:
            value_of_token = value_of_token.strip('"')
            print("Value of token: ", value_of_token.strip('"'))
            if '.' in value_of_token:
                #change to numbar
                val = float(value_of_token)
                semantics_functions.update_symbol(token, value_type="NUMBAR", value=val)
            else:
                val = int(value_of_token)
                semantics_functions.update_symbol(token, value_type="NUMBR", value=val)

        except:
            raise  Exception(f"ERROR in line {line_num}: Cannot cast token {token} with value {value_of_token} to NUMBR or NUMBAR")
        

def to_numbar(line_num,token_param):
# symbol_table.update_symbol("num", value="42", value_type="NUMBR") #can be used for expression, typecast, changing value of IT and other vars
    print("to numbar")
    token = token_param[0]
    token_type = semantics_functions.get_symbol(token)['value_type']
    print("token: ", token_type)

    if token_type == "TROOF":
        #if win, value is 1. else 0
        if token == "WIN":
            semantics_functions.update_symbol(token, value_type="NUMBAR", value=1.0)
        else:
            semantics_functions.update_symbol(token, value_type="NUMBAR", value=0)
    elif token_type == "NUMBR":
        value_of_token = semantics_functions.get_symbol(token)['value']
        semantics_functions.update_symbol(token, value_type="NUMBAR", value=float(value_of_token))
        
    elif token_type == "NUMBAR":
        print("Do nothing since token is already a numbar")
        return
    else: #type is not troof
        value_of_token = semantics_functions.get_symbol(token)['value']
        
        try:
            value_of_token = value_of_token.strip('"')
            print("Value of token: ", value_of_token.strip('"'))
            if '.' in value_of_token:
                #change to numbar
                val = float(value_of_token)
                semantics_functions.update_symbol(token, value_type="NUMBAR", value=val)
            else:
                val = int(value_of_token)
                semantics_functions.update_symbol(token, value_type="NUMBR", value=val)

        except:
            raise  Exception(f"ERROR in line {line_num}: Cannot cast token {token} with value {value_of_token} to NUMBR or NUMBAR")
        
def to_numbr(line_num,token_param):
# symbol_table.update_symbol("num", value="42", value_type="NUMBR") #can be used for expression, typecast, changing value of IT and other vars
    print("to numbr")
    token = token_param[0]
    token_type = semantics_functions.get_symbol(token)['value_type']
    print("token: ", token_type)

    if token_type == "TROOF":
        #if win, value is 1. else 0
        if token == "WIN":
            semantics_functions.update_symbol(token, value_type="NUMBR", value=1)
        else:
            semantics_functions.update_symbol(token, value_type="NUMBR", value=0)
    elif token_type == "NUMBAR":
        value_of_token = semantics_functions.get_symbol(token)['value']
        print(int(value_of_token))
        semantics_functions.update_symbol(token, value_type="NUMBR", value=int(value_of_token))
        
    elif token_type == "NUMBR":
        print("do nothing since NUMBR already")
        return
    else: #type is not troof
        value_of_token = semantics_functions.get_symbol(token)['value']
        
        try:
            value_of_token = value_of_token.strip('"')
            print("Value of token: ", value_of_token.strip('"'))
            if '.' in value_of_token:
                #change to numbar
                val = float(value_of_token)
                semantics_functions.update_symbol(token, value_type="NUMBAR", value=val)
            else:
                val = int(value_of_token)
                semantics_functions.update_symbol(token, value_type="NUMBR", value=val)

        except:
            raise  Exception(f"ERROR in line {line_num}: Cannot cast token {token} with value {value_of_token} to NUMBR or NUMBAR")



def to_troof(line_num,token_param):
    print("to troof")
    token = token_param[0]
    token_type = semantics_functions.get_symbol(token)['value_type']
    value_of_token = semantics_functions.get_symbol(token)['value']
    #if current type is numbr or numbar:
    if token_type == "NUMBR" or token_type == "NUMBAR":
        
        # 0 - FAIL, else, WIN
        if value_of_token == 0 or value_of_token == 0.0:
            semantics_functions.update_symbol(token, value_type="TROOF", value="FAIL")
        else:
            semantics_functions.update_symbol(token, value_type="TROOF", value="WIN")

    #if current type is yarn
    elif token_type == "YARN":
        print(token_type)
        if value_of_token == "":
            semantics_functions.update_symbol(token, value_type="TROOF", value="FAIL")
        else:
            semantics_functions.update_symbol(token, value_type="TROOF", value="WIN")

    #cannot be typecasted to troof
    else:
        raise Exception(f"Error in line {line_num}: Cannot cast the token {token} with value of {value_of_token} to Troof")


def troof_to_bool(line_num, token_param):
    print("troof to boolean")
    token = token_param[0]
    token_type = token_param[1]
    value_of_token = semantics_functions.get_symbol(token)['value'].strip('"')

    if value_of_token == "WIN":
        return True
    else:
        return False

def to_yarn(line_num, token_param):
    print("casting to yarn")
    token = token_param[0]
    token_type = token_param[1]
    value_of_token = semantics_functions.get_symbol(token)['value']

    semantics_functions.update_symbol(token, value_type="YARN", value=str(value_of_token))


def to_noob(line_num, token_param):
    print("to noob")
    token = token_param[0]
    token_type = token_param[1]
    semantics_functions.update_symbol(token, value_type="NOOB", value=None)


def to_different_types(token_name, line_num, token_to_change, type_of_tok_to_change):
    print("token name: ", token_name)
    #to numbar
    if token_name == "NUMBAR":
    # #call to numbr or numbar
        print("casting to numbar")
        to_numbar(line_num, [token_to_change, type_of_tok_to_change])
        print(semantics_functions.symbols)

    #to numbr
    if token_name == "NUMBR":
        print("casting to numbr")
        to_numbr(line_num, [token_to_change, type_of_tok_to_change])
        print(semantics_functions.symbols)

    #to yarn
    if token_name == "YARN":
        print("CASting to yarn")
        to_yarn(line_num, [token_to_change, type_of_tok_to_change])
        print(semantics_functions.symbols)

    #call to troof
    if token_name == "TROOF":
        print("cast to troof")
        to_troof(line_num, [token_to_change, type_of_tok_to_change])
        print(semantics_functions.symbols)

    #call to noob
    if token_name == "NOOB":
        print("Cast to Noob")
        to_noob(line_num, [token_to_change, type_of_tok_to_change])
        print(semantics_functions.symbols)

# def evaluate_explicit_typecast(line_num, token_param):
#     print("evaluating explicit typecast")
#     idx = 0
#     while idx < len(token_param):
#         token_name = token_param[idx][0]
#         token_type = token_param[idx][1]
        
#         #if token is of type IDENTIFIER, check if it is declared
#         if token_type == "IDENTIFIER":
#             result = semantics_functions.symbol_exists(token_name)
#             token_to_change = token_name
#             type_of_tok_to_change = token_type
#             #if result != True, var is not declared
#             if not result:
#                 raise Exception(f"Semantic Error in line {line_num}: Variable {token_name} is not declared")
#             idx += 1

#         #check if valid data type
#         elif data_type_checker([token_name,token_type]):
#             print("token type: ", token_name)
#             to_different_types(token_name, token_type, line_num, token_to_change, type_of_tok_to_change)

#             idx += 1
#         else:
#             idx += 1

additional_tokens = {
    5: [['MAEK', 'KEYWORD'], ['var1', 'IDENTIFIER'], ['A', 'KEYWORD'], ['NUMBAR', 'KEYWORD']],
    6: [['MAEK', 'KEYWORD'], ['var1', 'IDENTIFIER'], ['A', 'KEYWORD'], ['NUMBR', 'KEYWORD']],
    7: [['MAEK', 'KEYWORD'], ['var1', 'IDENTIFIER'], ['A', 'KEYWORD'], ['YARN', 'KEYWORD']],
    8: [['MAEK', 'KEYWORD'], ['var1', 'IDENTIFIER'], ['A', 'KEYWORD'], ['TROOF', 'KEYWORD']]

}

# evaluate_explicit_typecast(5, additional_tokens[5])
# print(additional_tokens[6])
# evaluate_explicit_typecast(6, additional_tokens[6])
# evaluate_explicit_typecast(7, additional_tokens[7])
# evaluate_explicit_typecast(8, additional_tokens[8])

"""
    Validates explicit typecasting in LOLCODE based on the specified grammar:
    - MAEK varident A <data_type>
    - MAEK varident <data_type>
    
    Arguments:
        tokens: A list of tokens, where each token is a tuple (value, type).
                Example: [("MAEK", "KEYWORD"), ("x", "IDENTIFIER"), ("A", "KEYWORD"), ("NUMBR", "DATATYPE")]
    
    Returns:
        True if the explicit typecasting is valid, or an error message if invalid.
"""
def explicit_typecast_checker(tokens):
    
    print("\nInside explicit_typecast_checker")
    print("Tokens to check:", tokens)
    syntax_flag = False
    if len(tokens) < 3:
        return "Error: Incomplete typecasting statement"

    if tokens[0][0] != "MAEK" or tokens[0][1] != "KEYWORD":
        return "Error: Expected 'MAEK' at the start of typecasting statement"

    # Check the variable identifier
    if tokens[1][1] != "IDENTIFIER":
        return f"Error: Expected variable identifier after 'MAEK', found {tokens[1][0]}"

    token_name = tokens[1][0]
    token_type = tokens[1][1]
    #check if variable is declared
    result = semantics_functions.symbol_exists(token_name)
    if not result:
        raise Exception(f"Semantic Error in line: Variable {token_name} is not declared")
            
    # Case 1: MAEK varident A <data_type>
    if len(tokens) == 4:
        if tokens[2][0] != "A" or tokens[2][1] != "KEYWORD":
            return f"Error: Expected 'A' keyword for typecasting, found {tokens[2][0]}"
        if not data_type_checker(tokens[3]):
            return f"Error: Expected data type after 'A', found {tokens[3][0]}"
        print("Valid explicit typecasting (MAEK varident A <data_type>)")
        data_type = tokens[3]
        syntax_flag =  True

    # Case 2: MAEK varident <data_type>
    elif len(tokens) == 3:
        if not data_type_checker(tokens[2]):
            return f"Error: Expected data type after variable identifier, found {tokens[2][0]}"
        print("Valid explicit typecasting (MAEK varident <data_type>)")
        data_type = tokens[2][0]

        syntax_flag =  True


    if syntax_flag == True:
        print("Token type: ", data_type )
        to_different_types(data_type, 5, token_name, token_type)


        return True

    else:
        return "Error: Invalid typecasting statement"

