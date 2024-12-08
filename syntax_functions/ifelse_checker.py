from syntax_functions import semantics_functions
from syntax_functions import explicit_typecast_checker
from syntax_functions import evaluate_ifthen_body
"""
Validate the LOLCODE if-then structure based on the dictionary structure.
"""
def ifelse_checker(classified_tokens):

    from syntax_functions.statement_checker import statement_checker
    
    def evaluate_condition(line_num):
        #Typecast IT to TROOF if not already TROOF
        if semantics_functions.get_symbol("IT")["value_type"] != "TROOF":
            explicit_typecast_checker.to_troof(line_num, ["IT", "KEYWORD"])
        # Get the value of IT after typecasting

        return semantics_functions.get_symbol("IT")["value"]

    def check_for_OIC(classified_tokens):
        line_of_oic = list(classified_tokens.keys())[-1]
        possible_oic = classified_tokens[line_of_oic][0][0]
        if possible_oic == 'OIC':
            return True
        else:
            return False

    print("\nIn if-else checker")
    current_state = "EXPECT_ORLY"
    valid_if_block = True
    print("if-else body: ", classified_tokens)

    if_body = {}
    else_body = {}
    current_body = None
    no_wai_flag = False
    start_collecting_else = False
    for line_num, tokens_in_line in classified_tokens.items():
        # Check for empty lines
        if not tokens_in_line:  # If the line is empty
            print(f"Empty line at line {line_num}")
            if current_state == "EXPECT_STATEMENT":
                if line_num not in current_body:
                    current_body[line_num] = []
            elif start_collecting_else == True and current_state ==  "EXPECT_NO_WAI_STATEMENT":
                if line_num not in current_body:
                    current_body[line_num] = []
            continue  # Skip further processing for this line

        print(f"line_num: {line_num}")

        for i, (token, token_type) in enumerate(tokens_in_line):
            print("Token: ", token)
            print("state: ",current_state)
            if current_state == "EXPECT_ORLY":
                if token == "O RLY?":
                    # Check value of IT
                    try:
                        it_value = evaluate_condition(line_num)
                        print("VALUE OF IT: ", it_value)
                        if it_value == "WIN":
                            execute_if = True  # True if YA RLY should execute, False otherwise
                        else:
                            execute_if = False
                        current_state = "EXPECT_YARLY"
                    except Exception:
                        print(f"ERROR at line {line_num}: IT cannot be typecast to TROOF")
                        # current_state = "END"
                else:
                    valid_if_block = False

            elif current_state == "EXPECT_YARLY":
                if token == "YA RLY":
                    if execute_if:
                        current_state = "EXPECT_STATEMENT"
                        current_body = if_body  # Assign current_body to if_body
                    else:
                        # Skip YA RLY and wait for NO WAI or OIC
                        current_state = "EXPECT_NO_WAI_STATEMENT"
                        current_body = else_body
                        no_wai_flag = True
                else:
                    valid_if_block = False

            elif current_state == "EXPECT_STATEMENT":
                if token == "NO WAI":
                    no_wai_flag = True
                    if execute_if:
                        # Skip NO WAI since YA RLY executed
                        print("IF BODY: ", if_body)
                        
                        print("Execute if body")
                        result_if_body = evaluate_ifthen_body.evaluate_body(if_body)
                        if result_if_body != True:
                            raise Exception(f"ERROR at line {line_num}: Invalid if body")
                        # current_state = "END"
                        no_wai_flag = True
                        if check_for_OIC(classified_tokens) == True:
                            print("\nUpdated symbol table after if-then statement: \n", semantics_functions.symbols)
                            return True
                        else:
                            return False
                    else:
                        current_state = "EXPECT_NO_WAI_STATEMENT"
                        current_body = else_body  # Switch to collecting the else body
                elif token == "OIC" and no_wai_flag == False:
                    # End the block if YA RLY executed without NO WAI
                    print("IF BODY: ", if_body)
                    if execute_if:
                        print("Execute if body")
                        result_if_body = evaluate_ifthen_body.evaluate_body(if_body)
                        if result_if_body != True:
                            raise Exception(f"ERROR at line {line_num}: Invalid if body")
                        # current_state = "END"
                        if check_for_OIC(classified_tokens) == True:
                            print("\nUpdated symbol table after if-then statement: \n", semantics_functions.symbols)
                            return True
                        else:
                            return False
                # elif token == "OIC" and no_wai_flag == True:
                #     current_state = "END"
                else:
                    # Record tokens in current body (if)
                    if line_num not in if_body:
                        if_body[line_num] = []
                    if_body[line_num].append([token, token_type])

            elif current_state == "EXPECT_NO_WAI_STATEMENT":
                if token == "OIC":
                    # Validate the else block if it was executed
                    if not execute_if:
                        print("Execute else body")
                        print("ELSE BODY: ", else_body)
                        result_else_body = evaluate_ifthen_body.evaluate_body(else_body)
                        if result_else_body != True:
                            raise Exception(f"ERROR at line {line_num}: Invalid else body")
                        if check_for_OIC(classified_tokens) == True:
                            print("\nUpdated symbol table after if-then statement: \n", semantics_functions.symbols)
                            return True
                        else:
                            return False
                    # current_state = "END"
                if token == "NO WAI":
                    start_collecting_else = True
                else:
                    # Collect else body only if YA RLY did not execute
                    if not execute_if and start_collecting_else == True:
                        if line_num not in else_body:
                            else_body[line_num] = []
                        else_body[line_num].append([token, token_type])

            elif current_state == "END":
                # No tokens should follow OIC
                valid_if_block = False

            if not valid_if_block:
                raise Exception(f"Invalid if-then block at line {line_num}")

    # After parsing, ensure we've reached the "END" state
    if current_state != "END":
        raise Exception("Invalid if-then block: missing OIC")

    return True

