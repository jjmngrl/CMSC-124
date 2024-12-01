""" 
Function to check if a token is a valid IDENTIFIER
Parameter: Token and its type
Return value: True - valid identifier
                False - invalid identifier
"""

def identifier_checker(token):
    
    if token[1] == "IDENTIFIER": return True
    else: return False


"""Original code from previous file:"""

# elif first_type == "IDENTIFIER":
    #             if not any(
    #                 first_value == token
    #                 for line_tokens in classified_tokens.values()
    #                 for token, token_type in line_tokens
    #                 if token_type == "IDENTIFIER"
    #             ):
    #                 prompt = f"ERROR: Undefined identifier '{first_value}' used in 'VISIBLE'."
    #                 flag = False
    #             else:
    #                 prompt = "Valid VISIBLE statement."