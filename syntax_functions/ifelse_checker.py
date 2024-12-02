
"""
Validate the LOLCODE if-then structure based on the dictionary structure.
"""
def ifelse_checker(classified_tokens):
    from syntax_functions.statement_checker import statement_checker
    print("\nIn if else checker")
    current_state = "EXPECT_ORLY"
    valid_if_block = True

    if_body = {}
    else_body = {}
    current_body = None

    for line_num, tokens_in_line in classified_tokens.items():
        # Flatten tokens for easier parsing
        # flattened_tokens = [token for token, _ in tokens]

        for i, (token, token_type) in enumerate(tokens_in_line):
            print("Token: ", token)
            if current_state == "EXPECT_ORLY":
                if token == "O RLY?":
                    current_state = "EXPECT_YARLY"
                else:
                    valid_if_block = False

            elif current_state == "EXPECT_YARLY":
                if token == "YA RLY":
                    current_state = "EXPECT_STATEMENT"
                else:
                    valid_if_block = False

            elif current_state == "EXPECT_STATEMENT":
                if token == "NO WAI":
                    #validate if body before collecting else body
                    print("IF BODY: ", if_body)
                    result_if_body = statement_checker(if_body, if_body)
                    if result_if_body != True:
                        raise Exception(f"ERROR at line {line_num}: Invalid if body")
                    current_state = "EXPECT_NO_WAI_STATEMENT"
                    print("valid if body")

                    current_body = else_body #Switch to collecting the ele body
                elif token == "OIC":
                    current_state = "END"
                else:
                    #record tokens in current body (if)
                    if line_num not in if_body:
                        if_body[line_num] = []
                    if_body[line_num].append([token, token_type])


            elif current_state == "EXPECT_NO_WAI_STATEMENT":
                if token == "OIC":
                    #validate else block first
                    print("else BODY: ", else_body)
                    result_else_body = statement_checker(else_body, else_body)
                    if result_else_body != True:
                        raise Exception(f"ERROR at line {line_num}: Invalid else body")
                    print("valid else body")

                    current_state = "END"
                else:
                    #collect else body
                    if line_num not in else_body:
                        else_body[line_num] = []
                    else_body[line_num].append([token, token_type])
                    

            elif current_state == "END":
                # No tokens should follow OIC
                valid_if_block = False

            if not valid_if_block:
                raise Exception (f"Invalid if-then block at line {line_num}") 
                # return f"Invalid if-then block at line {line_num}"

    # After parsing, ensure we've reached the "END" state
    if current_state != "END":
        raise Exception ("Invalid if-then block: missing OIC") 
        # return "Invalid if-then block: missing OIC"

    return True


