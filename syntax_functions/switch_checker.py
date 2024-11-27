"""
Validate the LOLCODE switch-case structure (WTF?).
Supports multiple OMG blocks, validates literals after OMG, and ensures proper use of GTFO, OMGWTF, and OIC.
"""

def switch_checker(classified_tokens):

    current_state = "EXPECT_WTF"
    omg_stack = []  # Stack to track `OMG` cases
    valid_switch_block = True

    for line_num, tokens in classified_tokens.items():
        # Flatten tokens for easier parsing
        flattened_tokens = [token for token, _ in tokens]

        for token in flattened_tokens:
            if current_state == "EXPECT_WTF":
                if token == "WTF?":
                    current_state = "EXPECT_OMG"
                else:
                    return f"Error: Missing WTF? at line {line_num}"

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
                        return f"Error: Missing GTFO for one or more OMG cases before OIC at line {line_num}"
                    current_state = "END"
                else:
                    return f"Error: Expected OMG, OMGWTF, or OIC at line {line_num}"

            elif current_state == "EXPECT_LITERAL":
                # Any literal type is acceptable
                if token in ["NUMBR", "NUMBAR", "YARN", "TROOF"] or isinstance(token, str):
                    current_state = "EXPECT_STATEMENT"
                else:
                    return f"Error: Expected literal after OMG at line {line_num}"

            elif current_state == "EXPECT_STATEMENT":
                if token == "GTFO":
                    if omg_stack:
                        omg_stack.pop()  # GTFO clears the current `OMG` case
                    current_state = "EXPECT_OMG_OR_END"
                elif token == "OMG":
                    if omg_stack:
                        return f"Error: Missing GTFO before next OMG at line {line_num}"
                elif token == "OMGWTF":
                    if omg_stack and omg_stack[-1] == "OMG":
                        omg_stack.pop()  # Clear stack for OMG before OMGWTF
                    current_state = "EXPECT_DEFAULT_STATEMENT"
                elif token == "OIC":
                    if omg_stack:
                        return f"Error: Missing GTFO for one or more OMG cases before OIC at line {line_num}"
                    current_state = "END"
                else:
                    # Allow valid statements to continue
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
                        return f"Error: Missing GTFO for one or more OMG cases before OIC at line {line_num}"
                    current_state = "END"
                else:
                    return f"Error: Expected OMG, OMGWTF, or OIC at line {line_num}"

            elif current_state == "EXPECT_DEFAULT_STATEMENT":
                if token == "OIC":
                    current_state = "END"
                # Allow valid statements in the default case
                else:
                    continue

            elif current_state == "END":
                # No tokens should follow OIC
                return f"Error: Unexpected token after OIC at line {line_num}"

    # After processing all lines, ensure the block is correctly closed
    if current_state != "END":
        return "Error: Incomplete switch-case block, missing OIC"

    return True