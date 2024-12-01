from syntax_functions import explicit_typecast_checker
from syntax_functions import data_type_checker

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

    # Case 1: varident IS NOW A <data_type>
    if len(tokens) >= 3 and tokens[1][0] == "IS NOW A" and tokens[1][1] == "KEYWORD":
        if data_type_checker.data_type_checker(tokens[2]):
            print("Valid recast (varident IS NOW A <data_type>)")
            return True
        else:
            return f"Error: Expected data type after 'IS NOW A', found {tokens[2][0]}"

    # Case 2: varident R <explicit_typecast>
    elif len(tokens) >= 2 and tokens[1][0] == "R" and tokens[1][1] == "KEYWORD":
        explicit_typecast_tokens = tokens[2:]  # Extract the tokens after 'R'
        print(explicit_typecast_tokens)
        result = explicit_typecast_checker.explicit_typecast_checker(explicit_typecast_tokens)
        if result == True:
            print("Valid recast (varident R <explicit_typecast>)")
            return True
        else:
            return result

    return "Error: Invalid recast statement"


# Example test cases for recast_checker
test_cases = [
    [("x", "IDENTIFIER"), ("IS NOW A", "KEYWORD"), ("NMBR", "KEYWORD")],  # Valid: x IS NOW A NUMBR
    [("x", "IDENTIFIER"), ("R", "KEYWORD"), ("MAEK", "KEYWORD"), ("y", "IDENTIFIER"), ("A", "KEYWORD"), ("NMBR", "KEYWORD")],  # Valid: x R MAEK y A NUMBR
    [("x", "IDENTIFIER"), ("IS NOW A", "KEYWORD"), ("NOOB", "KEYWORD")],  # Valid: x IS NOW A NOOB
    [("x", "IDENTIFIER"), ("IS NOW A", "KEYWORD")],                       # Invalid: Missing datatype
    [("x", "IDENTIFIER"), ("R", "KEYWORD"), ("MAEK", "KEYWORD"), ("y", "IDENTIFIER"), ("A", "KEYWORD")],  # Invalid: Missing datatype in typecast
    [("x", "IDENTIFIER"), ("R", "KEYWORD"), ("y", "IDENTIFIER")],                                       # Invalid: Missing MAEK keyword for typecast
    [("x", "IDENTIFIER"), ("IS NOW A", "KEYWORD")],                                                     # Invalid: Missing datatype
]

# # Run test cases
# for i, test in enumerate(test_cases, 1):
#     print(i)
#     result = recast_checker(test)
#     print(f"Test Case {i}: {'Valid' if result == True else result}")
