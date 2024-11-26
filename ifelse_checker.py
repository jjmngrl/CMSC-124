from lexical_analyzer import lex_main

classified_tokens = lex_main()

"""
Validate the LOLCODE if-then structure based on the dictionary structure.
"""
def ifelse_checker(classified_tokens):

    current_state = "EXPECT_ORLY"
    valid_if_block = True

    for line_num, tokens in classified_tokens.items():
        # Flatten tokens for easier parsing
        flattened_tokens = [token for token, _ in tokens]

        for token in flattened_tokens:
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
                    current_state = "EXPECT_NO_WAI_STATEMENT"
                elif token == "OIC":
                    current_state = "END"
                else:
                    valid_if_block = True  # Process valid statements here

            elif current_state == "EXPECT_NO_WAI_STATEMENT":
                if token == "OIC":
                    current_state = "END"
                else:
                    valid_if_block = True  # Process valid statements here

            elif current_state == "END":
                # No tokens should follow OIC
                valid_if_block = False

            if not valid_if_block:
                return f"Invalid if-then block at line {line_num}"

    # After parsing, ensure we've reached the "END" state
    if current_state != "END":
        return "Invalid if-then block: missing OIC"

    return True


test_case = {
    1: {  # Test Case 1: Basic If-Then Without Else
        1: [("O RLY?", "KEYWORD")],                             # Start of if-else block
        2: [("YA RLY", "KEYWORD")],                             # True branch
        3: [("VISIBLE", "KEYWORD"), ("\"Condition met\"", "YARN")],
        4: [("OIC", "KEYWORD")]                                 # End of block
    },
    2: {  # Test Case 2: If-Then With Else
        1: [("O RLY?", "KEYWORD")],                             # Start of if-else block
        2: [("YA RLY", "KEYWORD")],                             # True branch
        3: [("VISIBLE", "KEYWORD"), ("\"Condition met\"", "YARN")],
        4: [("NO WAI", "KEYWORD")],                             # Else branch
        5: [("VISIBLE", "KEYWORD"), ("\"Condition not met\"", "YARN")],
        6: [("OIC", "KEYWORD")]                                 # End of block
    },
    3: {  # Test Case 3: If-Then with Assignment Statement
        1: [("O RLY?", "KEYWORD")],  # Start of if-else block
        2: [("YA RLY", "KEYWORD")],  # True branch
        3: [("VAR", "IDENTIFIER"), ("R", "KEYWORD"), ("10", "NUMBR")],
        4: [("VAR", "IDENTIFIER"), ("R", "KEYWORD"), ("10", "NUMBR")],  # Assignment
        5: [("VISIBLE", "KEYWORD"), ("\"Variable updated\"", "YARN")],
        6: [("OIC", "KEYWORD")]  # End of block
    },
    4: { # Test Case from sir
        1: [("O RLY?", "KEYWORD")],  # Start of if-else block
        2: [("YA RLY", "KEYWORD")],  # True branch
        3: [("VISIBLE", "KEYWORD"), ("\"Enter birth year: \"", "YARN")],
        4: [("GIMMEH", "KEYWORD"), ("input", "IDENTIFIER")],
        5: [("VISIBLE", "KEYWORD"), ("DIFF OF", "KEYWORD"), ("2022", "NUMBR"), ("AN", "KEYWORD"), ("input", "IDENTIFIER")],
        6: [("OBTW", "KEYWORD")],  # Start of multiline comment
        7: [("BTW", "KEYWORD"), ("uncomment this portion if you have MEBBE", "COMMENT")],
        8: [("BTW", "KEYWORD"), ("else, this portion should be ignored", "COMMENT")],
        9: [("MEBBE", "KEYWORD"), ("BOTH SAEM", "KEYWORD"), ("choice", "IDENTIFIER"), ("AN", "KEYWORD"), ("2", "NUMBR")],
        10: [("VISIBLE", "KEYWORD"), ("\"Enter bill cost: \"", "YARN")],
        11: [("GIMMEH", "KEYWORD"), ("input", "IDENTIFIER")],
        12: [("VISIBLE", "KEYWORD"), ("\"Tip: \"", "YARN"), ("PRODUKT OF", "KEYWORD"), ("input", "IDENTIFIER"), ("AN", "KEYWORD"), ("0.1", "NUMBAR")],
        13: [("MEBBE", "KEYWORD"), ("BOTH SAEM", "KEYWORD"), ("choice", "IDENTIFIER"), ("AN", "KEYWORD"), ("3", "NUMBR")],
        14: [("VISIBLE", "KEYWORD"), ("\"Enter width: \"", "YARN")],
        15: [("GIMMEH", "KEYWORD"), ("input", "IDENTIFIER")],
        16: [("VISIBLE", "KEYWORD"), ("\"Square Area: \"", "YARN"), ("PRODUKT OF", "KEYWORD"), ("input", "IDENTIFIER"), ("AN", "KEYWORD"), ("input", "IDENTIFIER")],
        17: [("MEBBE", "KEYWORD"), ("BOTH SAEM", "KEYWORD"), ("choice", "IDENTIFIER"), ("AN", "KEYWORD"), ("0", "NUMBR")],
        18: [("VISIBLE", "KEYWORD"), ("\"Goodbye\"", "YARN")],
        19: [("TLDR", "KEYWORD")],  # End of multiline comment
        20: [("NO WAI", "KEYWORD")],  # Else branch
        21: [("VISIBLE", "KEYWORD"), ("\"Invalid Input!\"", "YARN")],
        22: [("OIC", "KEYWORD")]  # End of block
    }
}

invalid_test_cases = {
    1: {  # Test Case 1: Missing "OIC"
        1: [("O RLY?", "KEYWORD")],  # Start of if-else block
        2: [("YA RLY", "KEYWORD")],  # True branch
        3: [("VISIBLE", "KEYWORD"), ("\"Enter birth year: \"", "YARN")],
        4: [("GIMMEH", "KEYWORD"), ("input", "IDENTIFIER")],
        5: [("VISIBLE", "KEYWORD"), ("DIFF OF", "KEYWORD"), ("2022", "NUMBR"), ("AN", "KEYWORD"), ("input", "IDENTIFIER")]
        # Missing "OIC"
    },
    2: {  # Test Case 2: Missing "YA RLY"
        1: [("O RLY?", "KEYWORD")],  # Start of if-else block
        2: [("VISIBLE", "KEYWORD"), ("\"Condition met\"", "YARN")],
        3: [("OIC", "KEYWORD")]  # End of block
    },
    3: {  # Test Case 3: Extra tokens after "OIC"
        1: [("O RLY?", "KEYWORD")],  # Start of if-else block
        2: [("YA RLY", "KEYWORD")],  # True branch
        3: [("VISIBLE", "KEYWORD"), ("\"Condition met\"", "YARN")],
        4: [("OIC", "KEYWORD")],  # End of block
        5: [("VISIBLE", "KEYWORD"), ("\"This shouldn't be here\"", "YARN")]  # Extra token
    },
    4: {  # Test Case 4: "NO WAI" appears without a preceding "YA RLY"
        1: [("O RLY?", "KEYWORD")],  # Start of if-else block
        2: [("NO WAI", "KEYWORD")],  # Else branch without "YA RLY"
        3: [("VISIBLE", "KEYWORD"), ("\"Invalid Input!\"", "YARN")],
        4: [("OIC", "KEYWORD")]  # End of block
    }
}


# Run the test cases and print results
for case_id, case in test_case.items():
    result = ifelse_checker(case)
    print(f"Test Case {case_id}: {'Valid' if result == True else result}")

for case_id, case in invalid_test_cases.items():
    result = ifelse_checker(case)
    print(f"Test Case {case_id}: {'Valid' if result == True else result}")

