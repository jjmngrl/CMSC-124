from syntax_functions import explicit_typecast_checker
from syntax_functions import data_type_checker
from syntax_functions  import semantics_functions
from syntax_functions import explicit_typecast_checker
from syntax_functions  import data_type_checker
from syntax_functions import assignment_checker

def recast_checker(tokens):
    """
    Validates recast statements in LOLCODE based on the specified grammar:
    - varident IS NOW A <data_type>
    - varident R <explicit_typecast>
    
    Arguments:
        tokens: A list of tokens, where each token is a tuple (value, type).
                Example: [("x", "IDENTIFIER"), ("IS NOW A", "KEYWORD"), ("NUMBR", "DATATYPE")]

    Returns:
        True if the recast statement is valid, or an error message if invalid.
    """
    # print("\nInside recast_checker")
    # print("Tokens to check:", tokens)

    if len(tokens) < 3:
        return "Error: Incomplete recast statement"

    # Check the variable identifier
    if tokens[0][1] != "IDENTIFIER":
        return f"Error: Expected variable identifier at the start, found {tokens[0][0]}"
    
    #check if variable is declared
    var_declared = semantics_functions.symbol_exists(tokens[0][0])
    if not var_declared:
        raise Exception(f"Semantic Error in line: Variable {tokens[0][0]} is not declared")
    
    token_to_change = tokens[0][0]
    type_of_tok_to_change = tokens[0][1]

    # Case 1: varident IS NOW A <data_type>
    if len(tokens) >= 3 and tokens[1][0] == "IS NOW A" and tokens[1][1] == "KEYWORD":
        
        data_type_to_check = tokens[2] 
        if data_type_checker.data_type_checker(data_type_to_check):
            print("Valid recast (varident IS NOW A <data_type>)")

            token_name = tokens[2][0]
            token_type = tokens[2][1]
            #Semantic check 
            print("semantic evaluation\n")
            explicit_typecast_checker.to_different_types(token_name, token_type, line_num, token_to_change, type_of_tok_to_change)


            return True
        else:
            return f"Error: Expected data type after 'IS NOW A', found {tokens[2][0]}"

    # Case 2: varident R <explicit_typecast>
    elif len(tokens) >= 2 and tokens[1][0] == "R" and tokens[1][1] == "KEYWORD":
        explicit_typecast_tokens = tokens[2:]  # Extract the tokens after 'R'
        line_num = 2
        retain_token_val = semantics_functions.get_symbol(explicit_typecast_tokens[1][0])["value"] 
        retain_token_type = semantics_functions.get_symbol(explicit_typecast_tokens[1][0])["value_type"]
        var_name_in_explicit = explicit_typecast_tokens[1][0]
        var_type_in_explicit = explicit_typecast_tokens[1][1]
        print(explicit_typecast_tokens)
        result = explicit_typecast_checker.explicit_typecast_checker(explicit_typecast_tokens)
        if result == True:
            print("Valid recast (varident R <explicit_typecast>)")

            #Semantics check
            explicit_typecast_checker.evaluate_explicit_typecast(line_num, explicit_typecast_tokens)
            print(explicit_typecast_tokens[1][0])
            to_assign = semantics_functions.get_symbol(var_name_in_explicit)["value"]
            to_assign_type = semantics_functions.get_symbol(var_name_in_explicit)["value_type"]
            
            #Assign explicit typecast to variable
            print(f"assigning explicit to variable")
            assignment_checker.assignment_semantics(line_num, [[token_to_change,type_of_tok_to_change],['R', "KEYWORD"], [to_assign, to_assign_type]])

            #return the original value and type of the variable in the explicit typecast part
            assignment_checker.assignment_semantics(line_num, [[var_name_in_explicit,var_type_in_explicit],['R', "KEYWORD"], [retain_token_val, retain_token_type]])
            
            explicit_typecast_checker.evaluate_explicit_typecast(line_num, [["MAEK", "KEYWORD"],[var_name_in_explicit, var_type_in_explicit],["A", "KEYWORD"], [retain_token_type, "KEYWORD"]])
            
            print("\nAFTER RECAST\n",semantics_functions.symbols)
            return True
        else:
            return result

    return "Error: Invalid recast statement"



def evaluate_recast(line_num, tokens):
    print("evaluating recast")
    

    if len(tokens) < 3:
        return "Error: Incomplete recast statement"

    # Check the variable identifier
    if tokens[0][1] != "IDENTIFIER":
        return f"Error: Expected variable identifier at the start, found {tokens[0][0]}"

    #check if variable is declared
    var_declared = semantics_functions.symbol_exists(tokens[0][0])
    if not var_declared:
        raise Exception(f"Semantic Error in line {line_num}: Variable {token_name} is not declared")
    
    token_to_change = tokens[0][0]
    type_of_tok_to_change = tokens[0][1]
    # Case 1: varident IS NOW A <data_type>
    if len(tokens) >= 3 and tokens[1][0] == "IS NOW A" and tokens[1][1] == "KEYWORD":
        data_type_to_check = tokens[2] 
        if data_type_checker.data_type_checker(data_type_to_check):
            print("Valid recast (varident IS NOW A <data_type>)")


            token_name = tokens[2][0]
            token_type = tokens[2][1]

            #Semantic check 
            print("semantic evaluation\n")
            explicit_typecast_checker.to_different_types(token_name, token_type, line_num, token_to_change, type_of_tok_to_change)


            return True
        else:
            return f"Error: Expected data type after 'IS NOW A', found {tokens[2][0]}"

    # Case 2: varident R <explicit_typecast>
    elif len(tokens) >= 2 and tokens[1][0] == "R" and tokens[1][1] == "KEYWORD":

        explicit_typecast_tokens = tokens[2:]  # Extract the tokens after 'R'
        
        retain_token_val = semantics_functions.get_symbol(explicit_typecast_tokens[1][0])["value"] 
        retain_token_type = semantics_functions.get_symbol(explicit_typecast_tokens[1][0])["value_type"]
        var_name_in_explicit = explicit_typecast_tokens[1][0]
        var_type_in_explicit = explicit_typecast_tokens[1][1]
        print(explicit_typecast_tokens)
        result = explicit_typecast_checker.explicit_typecast_checker(explicit_typecast_tokens)
        if result == True:
            print("Valid recast (varident R <explicit_typecast>)")

            #Semantics check
            explicit_typecast_checker.evaluate_explicit_typecast(line_num, explicit_typecast_tokens)
            print(explicit_typecast_tokens[1][0])
            to_assign = semantics_functions.get_symbol(var_name_in_explicit)["value"]
            to_assign_type = semantics_functions.get_symbol(var_name_in_explicit)["value_type"]
            
            #Assign explicit typecast to variable
            print(f"assigning explicit to variable")
            assignment_checker.assignment_semantics(line_num, [[token_to_change,type_of_tok_to_change],['R', "KEYWORD"], [to_assign, to_assign_type]])

            #return the original value and type of the variable in the explicit typecast part
            assignment_checker.assignment_semantics(line_num, [[var_name_in_explicit,var_type_in_explicit],['R', "KEYWORD"], [retain_token_val, retain_token_type]])
            
            explicit_typecast_checker.evaluate_explicit_typecast(line_num, [["MAEK", "KEYWORD"],[var_name_in_explicit, var_type_in_explicit],["A", "KEYWORD"], [retain_token_type, "KEYWORD"]])
            
            # print( [[token_to_change,type_of_tok_to_change],['R', "KEYWORD"], [to_assign, to_assign_type]])
            # idx = 0
            # while idx < len(explicit_typecast_tokens):
            #     token_name = explicit_typecast_tokens[idx][0]
            #     token_type = explicit_typecast_tokens[idx][1]
            #     print(f"token {token_name} with type {token_type}")                
            #     #if token is of type IDENTIFIER, check if it is declared
            #     if token_type == "IDENTIFIER":
            #         result = semantics_functions.symbol_exists(token_name)
            #         #if result != True, var is not declared
            #         if not result:
            #             raise Exception(f"Semantic Error in line {line_num}: Variable {token_name} is not declared")
            #         idx += 1

            #     #check if valid data type
            #     elif data_type_checker.data_type_checker([token_name,token_type]):
            #         print("token type: ", token_name)
            #         print(f"token to change {token_to_change} with type {type_of_tok_to_change}")
            #         explicit_typecast_checker.to_different_types(token_name, token_type, line_num, token_to_change, type_of_tok_to_change)

            #         idx += 1
            #     else:
            #         idx += 1

           


            print("\nAFTER RECAST\n",semantics_functions.symbols)
            return True
        else:
            return result

    return "Error: Invalid recast statement"

# # Example test cases for recast_checker
# test_cases = {
#     # 1: [("x", "IDENTIFIER"), ("IS NOW A", "KEYWORD"), ("NUMBR", "KEYWORD")],  # Valid: x IS NOW A NUMBR
#     2: [("x", "IDENTIFIER"), ("R", "KEYWORD"), ("MAEK", "KEYWORD"), ("y", "IDENTIFIER"), ("A", "KEYWORD"), ("NUMBR", "KEYWORD")],  # Valid: x R MAEK y A NUMBR
#     # 3: [("x", "IDENTIFIER"), ("IS NOW A", "KEYWORD"), ("NOOB", "KEYWORD")],  # Valid: x IS NOW A NOOB
#     # 4: [("x", "IDENTIFIER"), ("IS NOW A", "KEYWORD")],                       # Invalid: Missing datatype
#     # 5: [("x", "IDENTIFIER"), ("R", "KEYWORD"), ("MAEK", "KEYWORD"), ("y", "IDENTIFIER"), ("A", "KEYWORD")],  # Invalid: Missing datatype in typecast
#     # 6: [("x", "IDENTIFIER"), ("R", "KEYWORD"), ("y", "IDENTIFIER")],                                       # Invalid: Missing MAEK keyword for typecast
#     # 7: [("x", "IDENTIFIER"), ("IS NOW A", "KEYWORD")],                                                     # Invalid: Missing datatype
# }
# # for i in additional_tokens:
#     # filtered = additional_tokens[i][1:]
#     # print("FIltered: ", filtered)
#     # if smoosh_checker(filtered) == True:
#     #     print("valid smoosh")
#     # else: print("invalid")
# # # Run test cases
# for i in test_cases:
#     filtered = test_cases[i]
#     print(i)
#     result = evaluate_recast(i, filtered)
#     print(f"Test Case {i}: {'Valid' if result == True else result}")
