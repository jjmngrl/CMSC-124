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
                raise Exception (f"Invalid if-then block at line {line_num}") 
                # return f"Invalid if-then block at line {line_num}"

    # After parsing, ensure we've reached the "END" state
    if current_state != "END":
        raise Exception ("Invalid if-then block: missing OIC") 
        # return "Invalid if-then block: missing OIC"

    return True


