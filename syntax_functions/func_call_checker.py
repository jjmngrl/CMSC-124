
from syntax_functions.parameter_checker import parameter_checker
from syntax_functions.identifier_checker import identifier_checker

def function_call_checker(tokens, line_num):
    print("\ninside function call checker")
    print(tokens)
    """
    Validates function calls in LOLCODE based on the specified grammar:
    - I IZ funcident YR <parameter> MKAY
    - I IZ funcident MKAY
    """
    current_state = "EXPECT_I_IZ"
    param_tokens = []  # To collect parameter tokens for validation

    for idx, token in enumerate(tokens):
        print("idx: ",idx)
        print(current_state)
        # print(tokens_in_line)
        
        # # Flatten tokens for easier parsing
        # for idx, (token, token_type) in enumerate(tokens_in_line):  # Unpack token and its type
        if current_state == "EXPECT_I_IZ":
            if token[0] == "I IZ":
                current_state = "EXPECT_FUNCIDENT"
            else:
                raise f"ERROR at line {line_num}: Expected 'I IZ'"

        elif current_state == "EXPECT_FUNCIDENT":
            # Check if the type is IDENTIFIER
            if token[1] == "IDENTIFIER":
                func_identifier = token  # Capture the function identifier
                current_state = "EXPECT_YR_OR_MKAY"
            else:
                return f"ERROR at line {line_num}: Expected an IDENTIFIER after 'I IZ'"

        elif current_state == "EXPECT_YR_OR_MKAY":
            if token[0] == "YR":
                current_state = "EXPECT_PARAMETER"
            elif token[0] == "MKAY":
                current_state = "END"
            else:
                return f"ERROR at line {line_num}: Expected 'YR' or 'MKAY' "

        elif current_state == "EXPECT_PARAMETER":
            # Collect tokens for parameter checking
            param_tokens = tokens[idx:-1]  # Slice the remaining tokens
            #catch case that there is no parameter after YR
            if param_tokens == []:
                return f"ERROR at line {line_num}: Expected 'MKAY'"
            if parameter_checker(param_tokens, line_num):
                current_state = "EXPECT_MKAY"
            else:
                return f"ERROR at line {line_num}: Invalid parameter"

        elif current_state == "EXPECT_MKAY":
            if tokens[len(tokens)-1][0] == "MKAY":
                current_state = "END"
            else:
                return f"ERROR at line {line_num}: Expected 'MKAY'"

        elif current_state == "END":
            print("Valid function call")
            return True
    # Ensure the function call ends in the correct state
    if current_state != "END":
        return f"ERROR at line {line_num}: Incomplete function call"

    return True
    


# Example test cases to validate the modified function_call_checker
# test_cases = {
#     1: [["I IZ", "KEYWORD"], ["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
#     2: [["I IZ", "KEYWORD"], ["anotherFunc", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
#     3: [["I IZ", "KEYWORD"], ["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"]],
#     4: [["I IZ", "KEYWORD"], ["anotherFunc", "IDENTIFIER"], ["MKAY", "KEYWORD"], ["unexpected", "IDENTIFIER"]],
#     5: [["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
#     6: [["I IZ", "KEYWORD"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
# }

# # Run each test case
# for case_id, case in test_cases.items():
#     result = function_call_checker({1: case})
#     print(f"Test Case {case_id}: {'Valid' if result == True else result}")



# # Define test cases
# test_cases = {
#     1: [["I IZ", "KEYWORD"], ["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
#     2: [["I IZ", "KEYWORD"], ["anotherFunc", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
#     3: [["I IZ", "KEYWORD"], ["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"]],
#     4: [["I IZ", "KEYWORD"], ["anotherFunc", "IDENTIFIER"], ["MKAY", "KEYWORD"], ["unexpected", "IDENTIFIER"]],
#     5: [["myFunc", "IDENTIFIER"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]],
#     6: [["I IZ", "KEYWORD"], ["YR", "KEYWORD"], ["param1", "IDENTIFIER"], ["MKAY", "KEYWORD"]]
# }

# # Run each test case
# for case_id, case in test_cases.items():
#     result = function_call_checker({1: case})
#     print(f"Test Case {case_id}: {'Valid' if result == True else result}")

