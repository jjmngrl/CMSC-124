# from syntax_functions.flow_control_body_checker import flow_control_body_checker

"""
Validate the LOLCODE switch-case structure (WTF?).
Supports multiple OMG blocks, validates literals after OMG, and ensures proper use of GTFO, OMGWTF, and OIC.
"""

def switch_checker(classified_tokens):
    print("\n In switch checker")
    current_state = "EXPECT_WTF"
    omg_stack = []  # Stack to track `OMG` cases
    valid_switch_block = True
    flow_control_statements = {} 
    current_block = []
    omgwtf_body = {}

    for line_num, tokens_in_line in classified_tokens.items():
        for i, (token, token_type) in enumerate(tokens_in_line):
            print(f"Token: {token}, State: {current_state}")
            if current_state == "EXPECT_WTF":
                if token == "WTF?":
                    current_state = "EXPECT_OMG"
                else:
                    raise Exception (f"Error: Missing WTF? at line {line_num}")
                    # return f"Error: Missing WTF? at line {line_num}"

            elif current_state == "EXPECT_OMG":
                if token == "OMG":
                    omg_stack.append("OMG")  # Push to stack
                    current_state = "EXPECT_LITERAL"
                elif token == "OMGWTF":
                    if omg_stack and omg_stack[-1] == "OMG":
                        omg_stack.pop()  # Final `OMG` does not require `GTFO`
                    current_state = "EXPECT_DEFAULT_STATEMENT"
                elif token == "OIC":
                    if omg_stack:
                        raise Exception (f"Error: Missing GTFO for one or more OMG cases before OIC at line {line_num}") 
                        # return f"Error: Missing GTFO for one or more OMG cases before OIC at line {line_num}"
                    current_state = "END"
                else:
                    raise Exception(f"Error: Expected OMG, OMGWTF, or OIC at line {line_num}")
                    # return f"Error: Expected OMG, OMGWTF, or OIC at line {line_num}"

            elif current_state == "EXPECT_LITERAL":
                # Any literal type is acceptable
                if token in ["NUMBR", "NUMBAR", "YARN", "TROOF"] or isinstance(token, str):
                    current_state = "EXPECT_STATEMENT"
                else:
                    raise Exception (f"Error: Expected literal after OMG at line {line_num}")
                    # return f"Error: Expected literal after OMG at line {line_num}"

            elif current_state == "EXPECT_STATEMENT":
                if token == "GTFO":
                    #check if statement is valid
                    if omg_stack:
                        omg_stack.pop()  # GTFO clears the current `OMG` case
                    current_state = "EXPECT_OMG_OR_END"
                    # print("OMG BODY:", current_block)
                    # result = flow_control_body_checker(current_block)
                    # if result != True:
                    #     raise Exception(f"ERROR at line {line_num}: Invalid OMG body")
                    # print("valid OMG body")
                    
                elif token == "OMG":
                    #check if statement is valid
                    if omg_stack:
                        raise Exception (f"Error: Missing GTFO before next OMG at line {line_num}")
                elif token == "OMGWTF":
                    #check if statement is valid
                    if omg_stack and omg_stack[-1] == "OMG":
                        omg_stack.pop()  # Clear stack for OMG before OMGWTF
                    current_state = "EXPECT_DEFAULT_STATEMENT"
                    # print("OMGWTF BODY:", current_block)
                    # result = flow_control_body_checker(current_block)
                    # if result != True:
                    #     raise Exception(f"ERROR at line {line_num}: Invalid OMGWTF body")
                    # print("valid OMGWTF body")
                elif token == "OIC":
                    if omg_stack:
                        raise Exception (f"Error: Missing GTFO for one or more OMG cases before OIC at line {line_num}")
                    current_state = "END"
                else:
                    #Store flow control statement
                    if token != "GTFO" and token != "OIC" \
                    and token != "OMG" and token != "OMGWTF":
                        if line_num not in flow_control_statements:
                            flow_control_statements[line_num] = []
                        flow_control_statements[line_num].append([token, token_type])
                    continue

            elif current_state == "EXPECT_OMG_OR_END":
                if token == "OMG":
                    omg_stack.append("OMG")  # Push to stack for the next case
                    current_state = "EXPECT_LITERAL"
                elif token == "OMGWTF":
                    if omg_stack and omg_stack[-1] == "OMG":
                        omg_stack.pop()  # Final OMG does not require GTFO
                    current_state = "EXPECT_DEFAULT_STATEMENT"
                elif token == "OIC":
                    if omg_stack:
                        raise Exception (f"Error: Missing GTFO for one or more OMG cases before OIC at line {line_num}")
                        # return f"Error: Missing GTFO for one or more OMG cases before OIC at line {line_num}"
                    current_state = "END"
                else:
                    raise Exception (f"Error: Expected OMG, OMGWTF, or OIC at line {line_num}")
                    # return f"Error: Expected OMG, OMGWTF, or OIC at line {line_num}"

            elif current_state == "EXPECT_DEFAULT_STATEMENT":
                if token == "OIC":
                    #check if OMGWTF is valid
                    current_state = "END"       
                # Allow valid statements in the default case
                else:
                    if line_num not in omgwtf_body:
                        omgwtf_body[line_num] = []
                    omgwtf_body[line_num].append([token, token_type])
                    continue

            elif current_state == "END":
                # No tokens should follow OIC
                raise Exception (f"Error: Unexpected token after OIC at line {line_num}")
                # return f"Error: Unexpected token after OIC at line {line_num}"

    # After processing all lines, ensure the block is correctly closed
    if current_state != "END":
        raise Exception ("Error: Incomplete switch-case block, missing OIC")
        # return "Error: Incomplete switch-case block, missing OIC"

    return True
