

from syntax_functions.data_type_checker import data_type_checker

def explicit_typecast_checker(tokens):
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
    print("\nInside explicit_typecast_checker")
    print("Tokens to check:", tokens)
    
    if len(tokens) < 3:
        return "Error: Incomplete typecasting statement"

    if tokens[0][0] != "MAEK" or tokens[0][1] != "KEYWORD":
        return "Error: Expected 'MAEK' at the start of typecasting statement"

    # Check the variable identifier
    if tokens[1][1] != "IDENTIFIER":
        return f"Error: Expected variable identifier after 'MAEK', found {tokens[1][0]}"

    # Case 1: MAEK varident A <data_type>
    if len(tokens) == 4:
        if tokens[2][0] != "A" or tokens[2][1] != "KEYWORD":
            return f"Error: Expected 'A' keyword for typecasting, found {tokens[2][0]}"
        if not data_type_checker(tokens[3]):
            return f"Error: Expected data type after 'A', found {tokens[3][0]}"
        print("Valid explicit typecasting (MAEK varident A <data_type>)")
        return True

    # Case 2: MAEK varident <data_type>
    elif len(tokens) == 3:
        if not data_type_checker(tokens[2]):
            return f"Error: Expected data type after variable identifier, found {tokens[2][0]}"
        print("Valid explicit typecasting (MAEK varident <data_type>)")
        return True

    return "Error: Invalid typecasting statement"


# Test cases for explicit_typecast_checker
test_cases = [
    [("MAEK", "KEYWORD"), ("x", "IDENTIFIER"), ("A", "KEYWORD"), ("NMBR", "KEYWORD")],  # Valid: MAEK x A NUMBR
    [("MAEK", "KEYWORD"), ("x", "IDENTIFIER"), ("NMBR", "KEYWORD")],                  # Valid: MAEK x NUMBR
    [("MAEK", "KEYWORD"), ("x", "IDENTIFIER"), ("A", "KEYWORD"), ("NOOB", "KEYWORD")], # Valid: MAEK x A NOOB
    [("MAEK", "KEYWORD"), ("x", "IDENTIFIER"), ("MKAY", "KEYWORD")],                   # Invalid: No datatype
    [("I IZ", "KEYWORD"), ("x", "IDENTIFIER"), ("A", "KEYWORD"), ("NMBR", "KEYWORD")],# Invalid: Wrong start keyword
    [("MAEK", "KEYWORD"), ("x", "IDENTIFIER"), ("A", "KEYWORD")],                      # Invalid: Missing datatype
]

# Run test cases
for i, test in enumerate(test_cases, 1):
    result = explicit_typecast_checker(test)
    print(f"Test Case {i}: {'Valid' if result == True else result}")


