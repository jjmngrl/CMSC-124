
from parameter_checker import parameter_checker
from identifier_checker import identifier_checker
def function_call_checker(tokens):
    print("\ninside function call checker")
    """
    Validates function calls in LOLCODE based on the specified grammar:
    - I IZ funcident YR <parameter> MKAY
    - I IZ funcident MKAY
    """
    current_state = "EXPECT_I_IZ"
    param_tokens = []  # To collect parameter tokens for validation

    for line_num, tokens_in_line in tokens.items():
        # Flatten tokens for easier parsing
        for idx, (token, token_type) in enumerate(tokens_in_line):  # Unpack token and its type
            if current_state == "EXPECT_I_IZ":
                if token == "I IZ":
                    current_state = "EXPECT_FUNCIDENT"
                else:
                    return f"Error: Expected 'I IZ' at line {line_num}"

            elif current_state == "EXPECT_FUNCIDENT":
                # Check if the type is IDENTIFIER
                if token_type == "IDENTIFIER":
                    func_identifier = token  # Capture the function identifier
                    current_state = "EXPECT_YR_OR_MKAY"
                else:
                    return f"Error: Expected an IDENTIFIER after 'I IZ' at line {line_num}"

            elif current_state == "EXPECT_YR_OR_MKAY":
                if token == "YR":
                    current_state = "EXPECT_PARAMETER"
                elif token == "MKAY":
                    current_state = "END"
                else:
                    return f"Error: Expected 'YR' or 'MKAY' at line {line_num}"

            elif current_state == "EXPECT_PARAMETER":
                # Collect tokens for parameter checking
                param_tokens = tokens_in_line[idx:len(tokens_in_line)-1]  # Slice the remaining tokens
                #catch case that there is no parameter after YR
                if param_tokens == []:
                    return f"Error: Expected 'MKAY' at line {line_num}"
                if parameter_checker(param_tokens):
                    current_state = "EXPECT_MKAY"
                else:
                    return f"Error: Invalid parameter at line {line_num}"

            elif current_state == "EXPECT_MKAY":
                if token == "MKAY":
                    current_state = "END"
                else:
                    return f"Error: Expected 'MKAY' at line {line_num}"

            elif current_state == "END":
                # No tokens should follow a valid function call
                return f"Error: Unexpected token after function call at line {line_num}"

        # Ensure the function call ends in the correct state
        if current_state != "END":
            return f"Error: Incomplete function call at line {line_num}"

    print("Valid function call")
    return True


# Example test cases to validate the modified function_call_checker
test_cases = {
    1: [["I IZ", "KEYWORD"], ["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
    2: [["I IZ", "KEYWORD"], ["anotherFunc", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
    3: [["I IZ", "KEYWORD"], ["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"]],
    4: [["I IZ", "KEYWORD"], ["anotherFunc", "IDENTIFIER"], ["MKAY", "KEYWORD"], ["unexpected", "IDENTIFIER"]],
    5: [["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
    6: [["I IZ", "KEYWORD"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
}

# Run each test case
for case_id, case in test_cases.items():
    result = function_call_checker({1: case})
    print(f"Test Case {case_id}: {'Valid' if result == True else result}")



# Define test cases
test_cases = {
    1: [["I IZ", "KEYWORD"], ["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
    2: [["I IZ", "KEYWORD"], ["anotherFunc", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
    3: [["I IZ", "KEYWORD"], ["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"]],
    4: [["I IZ", "KEYWORD"], ["anotherFunc", "IDENTIFIER"], ["MKAY", "KEYWORD"], ["unexpected", "IDENTIFIER"]],
    5: [["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
    6: [["I IZ", "KEYWORD"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]]
}

# Run each test case
for case_id, case in test_cases.items():
    result = function_call_checker({1: case})
    print(f"Test Case {case_id}: {'Valid' if result == True else result}")

