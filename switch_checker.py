from lexical_analyzer import lex_main

classified_tokens = lex_main()

"""
Validate the LOLCODE switch-case structure (WTF?).
Supports multiple OMG blocks, validates literals after OMG, and ensures proper use of GTFO, OMGWTF, and OIC.
"""

def switch_checker(classified_tokens):
    current_state = "EXPECT_WTF"
    # valid_switch_block = True
    omg_case_found = False

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
                    current_state = "EXPECT_LITERAL"
                    omg_case_found = True
                elif token == "OMGWTF":
                    if not omg_case_found:
                        return f"Error: OMGWTF without any OMG cases at line {line_num}"
                    current_state = "EXPECT_DEFAULT_STATEMENT"
                elif token == "OIC":
                    if not omg_case_found:
                        return f"Error: No OMG case found before OIC at line {line_num}"
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
                    current_state = "EXPECT_OMG_OR_END"
                elif token == "OMG":
                    current_state = "EXPECT_LITERAL"  # Allow transition to the next OMG case
                elif token == "OMGWTF":
                    current_state = "EXPECT_DEFAULT_STATEMENT"  # Allow transition to OMGWTF
                elif token == "OIC":
                    current_state = "END"
                else:
                    # Allow valid statements to continue
                    continue

            elif current_state == "EXPECT_OMG_OR_END":
                if token == "OMG":
                    current_state = "EXPECT_LITERAL"
                elif token == "OMGWTF":
                    current_state = "EXPECT_DEFAULT_STATEMENT"
                elif token == "OIC":
                    current_state = "END"
                else:
                    return f"Error: Expected OMG, OMGWTF, or OIC at line {line_num}"

            elif current_state == "EXPECT_DEFAULT_STATEMENT":
                if token == "OIC":
                    current_state = "END"
                # Allow other valid statements
                else:
                    continue

            elif current_state == "END":
                # No tokens should follow OIC
                return f"Error: Unexpected token after OIC at line {line_num}"

    # If the loop ends without reaching the END state
    if current_state != "END":
        return "Error: Incomplete switch-case block, missing OIC"

    return True



test_case = {
    1: {  # Test Case 1: Valid switch-case
        1: [("WTF?", "KEYWORD")],
        2: [("OMG", "KEYWORD"), ("42", "NUMBR")],
        3: [("VISIBLE", "KEYWORD"), ("\"Matched 42\"", "YARN")],
        4: [("GTFO", "KEYWORD")],
        5: [("OMG", "KEYWORD"), ("\"Hello\"", "YARN")],
        6: [("VISIBLE", "KEYWORD"), ("\"Matched Hello\"", "YARN")],
        7: [("OMGWTF", "KEYWORD")],
        8: [("VISIBLE", "KEYWORD"), ("\"Default case\"", "YARN")],
        9: [("OIC", "KEYWORD")]
    },
    2: {  # Test Case 1: Switch-case with multiple OMG and OMGWTF
        1: [("WTF?", "KEYWORD")],                                # Start of switch-case block
        2: [("OMG", "KEYWORD"), ("1", "NUMBR")],                 # First case
        3: [("VISIBLE", "KEYWORD"), ("\"Enter birth year: \"", "YARN")],
        4: [("GIMMEH", "KEYWORD"), ("input", "IDENTIFIER")],
        5: [("VISIBLE", "KEYWORD"), ("DIFF OF", "KEYWORD"), ("2022", "NUMBR"), ("AN", "KEYWORD"), ("input", "IDENTIFIER")],
        6: [("GTFO", "KEYWORD")],                                # Exit first case
        7: [("OMG", "KEYWORD"), ("2", "NUMBR")],                 # Second case
        8: [("VISIBLE", "KEYWORD"), ("\"Enter bill cost: \"", "YARN")],
        9: [("GIMMEH", "KEYWORD"), ("input", "IDENTIFIER")],
        10: [("VISIBLE", "KEYWORD"), ("\"Tip: \"", "YARN"), ("PRODUCKT OF", "KEYWORD"), ("input", "IDENTIFIER"), ("AN", "KEYWORD"), ("0.1", "NUMBAR")],
        11: [("GTFO", "KEYWORD")],                               # Exit second case
        12: [("OMG", "KEYWORD"), ("3", "NUMBR")],                # Third case
        13: [("VISIBLE", "KEYWORD"), ("\"Enter width: \"", "YARN")],
        14: [("GIMMEH", "KEYWORD"), ("input", "IDENTIFIER")],
        15: [("VISIBLE", "KEYWORD"), ("\"Square Area: \"", "YARN"), ("PRODUCKT OF", "KEYWORD"), ("input", "IDENTIFIER"), ("AN", "KEYWORD"), ("input", "IDENTIFIER")],
        16: [("GTFO", "KEYWORD")],                               # Exit third case
        17: [("OMG", "KEYWORD"), ("0", "NUMBR")],                # Fourth case
        18: [("VISIBLE", "KEYWORD"), ("\"Goodbye\"", "YARN")],
        19: [("OMGWTF", "KEYWORD")],                             # Default case
        20: [("VISIBLE", "KEYWORD"), ("\"Invalid Input!\"", "YARN")],
        21: [("OIC", "KEYWORD")]                                 # End of block
    }
}


# Run the test cases and print results
for case_id, case in test_case.items():
    result = switch_checker(case)
    print(f"Test Case {case_id}: {'Valid' if result == True else result}")

