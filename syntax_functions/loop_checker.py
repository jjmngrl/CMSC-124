from syntax_functions.identifier_checker import identifier_checker



"""
Use this checker when a statement or line of code has the keyword 'IM IN YR'
and 'IM OUTTA YR'. 
"""
def loop_checker(token):
    """
    Validates LOLCODE loop blocks with 'IM IN YR' and 'IM OUTTA YR'.
    Handles both 'TIL' and 'WILE' conditions.
    """
    current_state = "EXPECT_IM_IN_YR"
    valid_loop_block = True
    loop_identifier = None

    for line_num, tokens_in_line in token.items():
        for token, token_type in tokens_in_line:
            print("Token: ",token)

            if current_state == "EXPECT_IM_IN_YR":
                if token == "IM IN YR":
                    current_state = "EXPECT_LOOPIDENT"
                else:
                    return f"Error: Expected 'IM IN YR' at line {line_num}"

            elif current_state == "EXPECT_LOOPIDENT":
                if token_type == "IDENTIFIER":
                    loop_identifier = token  # Capture the loop identifier
                    current_state = "EXPECT_OPERATION"
                else:
                    return f"Error: Expected an identifier after 'IM IN YR' at line {line_num}"

            elif current_state == "EXPECT_OPERATION":
                if token in ["UPPIN", "NERFIN"]:
                    current_state = "EXPECT_YR"
                else:
                    return f"Error: Expected 'UPPIN' or 'NERFIN' at line {line_num}"

            elif current_state == "EXPECT_YR":
                if token == "YR":
                    current_state = "EXPECT_VARIDENT"
                else:
                    return f"Error: Expected 'YR' at line {line_num}"

            elif current_state == "EXPECT_VARIDENT":
                if token_type == "IDENTIFIER":
                    current_state = "EXPECT_TIL_OR_WILE"
                else:
                    return f"Error: Expected an identifier after 'YR' at line {line_num}"

            elif current_state == "EXPECT_TIL_OR_WILE":
                if token in ["TIL", "WILE"]:
                    current_state = "EXPECT_EXPRESSION"
                else:
                    return f"Error: Expected 'TIL' or 'WILE' at line {line_num}"

            elif current_state == "EXPECT_EXPRESSION":
                # Assume valid expressions for now; enhance with proper validation as needed
                
                current_state = "EXPECT_FLOW_CONTROL_STATEMENT"

            elif current_state == "EXPECT_FLOW_CONTROL_STATEMENT":
                if token == "IM OUTTA YR":
                    current_state = "EXPECT_LOOPIDENT_END"
                else:
                    # Assume this is the loop body; no explicit validation for now
                    valid_loop_block = True

            elif current_state == "EXPECT_LOOPIDENT_END":
                if token == loop_identifier:
                    current_state = "END"
                else:
                    return f"Error: Expected matching loop identifier '{loop_identifier}' at line {line_num}"

            elif current_state == "END":
                # No tokens should follow a valid loop block
                return f"Error: Unexpected token after loop end at line {line_num}"

    # After parsing, ensure we've reached the "END" state
    if current_state != "END":
        return "Error: Invalid loop block: missing 'IM OUTTA YR' or loop identifier"

    return True






# code_tokens = {
#     1: {
#         1: [["IM IN YR", "KEYWORD"], ["asc", "IDENTIFIER"], ["UPPIN", "KEYWORD"], ["YR", "KEYWORD"], ["num2", "IDENTIFIER"], ["WILE", "KEYWORD"], ["BOTH", "KEYWORD"], ["SAEM", "KEYWORD"], ["num2", "IDENTIFIER"], ["AN", "KEYWORD"], ["SMALLR", "KEYWORD"], ["OF", "KEYWORD"], ["num2", "IDENTIFIER"], ["AN", "KEYWORD"], ["num1", "IDENTIFIER"]],
#         2: [["VISIBLE", "KEYWORD"], ["num2", "IDENTIFIER"]],
#         3: [["IM OUTTA YR", "KEYWORD"], ["asc", "IDENTIFIER"]],
#     },
#     2: {
#         1: [["IM IN YR", "KEYWORD"], ["desc", "IDENTIFIER"], ["NERFIN", "KEYWORD"], ["YR", "KEYWORD"], ["num2", "IDENTIFIER"], ["TIL", "KEYWORD"], ["BOTH", "KEYWORD"], ["SAEM", "KEYWORD"], ["num2", "IDENTIFIER"], ["AN", "KEYWORD"], ["0", "NUMBER"]],
#         2: [["VISIBLE", "KEYWORD"], ["num2", "IDENTIFIER"]],
#         3: [["IM OUTTA YR", "KEYWORD"], ["desc", "IDENTIFIER"]]
#     },
#     #invalid test cases
#     3: { #missing  IM OUTTA YR
#         1: [["IM IN YR", "KEYWORD"], ["loop1", "IDENTIFIER"], ["UPPIN", "KEYWORD"], ["YR", "KEYWORD"], ["var1", "IDENTIFIER"], ["TIL", "KEYWORD"], ["BOTH", "KEYWORD"], ["SAEM", "KEYWORD"], ["var1", "IDENTIFIER"], ["AN", "KEYWORD"], ["10", "NUMBER"]],
#         2: [["VISIBLE", "KEYWORD"], ["var1", "IDENTIFIER"]],
#         # Missing "IM OUTTA YR loop1"
#     },   
#     4: { #Mismatched loop identifier in IM OUTTA YR
#         1: [["IM IN YR", "KEYWORD"], ["loop2", "IDENTIFIER"], ["NERFIN", "KEYWORD"], ["YR", "KEYWORD"], ["var2", "IDENTIFIER"], ["WILE", "KEYWORD"], ["BOTH", "KEYWORD"], ["SAEM", "KEYWORD"], ["var2", "IDENTIFIER"], ["AN", "KEYWORD"], ["5", "NUMBER"]],
#         2: [["VISIBLE", "KEYWORD"], ["var2", "IDENTIFIER"]],
#         3: [["IM", "KEYWORD"], ["OUTTA", "KEYWORD"], ["YR", "KEYWORD"], ["wrong_loop", "IDENTIFIER"]],
#     },
#     5: { #missing til or while
#         1: [["IM IN YR", "KEYWORD"], ["loop3", "IDENTIFIER"], ["UPPIN", "KEYWORD"], ["YR", "KEYWORD"], ["var3", "IDENTIFIER"]],
#         2: [["VISIBLE", "KEYWORD"], ["var3", "IDENTIFIER"]],
#         3: [["IM", "KEYWORD"], ["OUTTA", "KEYWORD"], ["YR", "KEYWORD"], ["loop3", "IDENTIFIER"]],
#     },
#     6: { #Missing YR
#         1: [["IM IN YR", "KEYWORD"], ["loop4", "IDENTIFIER"], ["UPPIN", "KEYWORD"], ["var4", "IDENTIFIER"], ["TIL", "KEYWORD"], ["BOTH", "KEYWORD"], ["SAEM", "KEYWORD"], ["var4", "IDENTIFIER"], ["AN", "KEYWORD"], ["3", "NUMBER"]],
#         2: [["VISIBLE", "KEYWORD"], ["var4", "IDENTIFIER"]],
#         3: [["IM", "KEYWORD"], ["OUTTA", "KEYWORD"], ["YR", "KEYWORD"], ["loop4", "IDENTIFIER"]],
#     },
#     7: { #Missing IM OUTTA YR
#         1: [["IM IN YR", "KEYWORD"], ["loop5", "IDENTIFIER"], ["NERFIN", "KEYWORD"], ["YR", "KEYWORD"], ["var5", "IDENTIFIER"], ["WILE", "KEYWORD"], ["BOTH", "KEYWORD"], ["SAEM", "KEYWORD"], ["var5", "IDENTIFIER"], ["AN", "KEYWORD"], ["1", "NUMBER"]],
#         2: [["VISIBLE", "KEYWORD"], ["var5", "IDENTIFIER"]],
#         3: [["IM", "KEYWORD"], ["OUTTA", "KEYWORD"], ["YR", "KEYWORD"], ["loop5", "IDENTIFIER"]],
#         4: [["VISIBLE", "KEYWORD"], ["var5", "IDENTIFIER"]],  # Extra token after loop end
#     }
    
# }


# #run test cases

# #valid test cases
# for case_id, case in code_tokens.items():
#     result = loop_checker(case)
#     print(f"Test Case {case_id}: {'Valid' if result == True else result}")


#invalid test cases
