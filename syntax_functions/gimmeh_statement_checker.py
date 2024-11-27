def gimmeh_statement_checker(code_block, classified_tokens, result):
    """
    Function to check if GIMMEH statements are valid.
    Rule: The token following GIMMEH must be an IDENTIFIER.
    """
    flag = True  # Tracks if all GIMMEH statements are valid

    for line_num, tokens in code_block.items():
        if not tokens:
            continue

        # Check if the statement starts with GIMMEH
        if tokens[0][0] == "GIMMEH" and tokens[0][1] == "KEYWORD":
            if len(tokens) < 2:
                result.append((f"Line {line_num}: {tokens}", "ERROR: Missing identifier after 'GIMMEH'."))
                flag = False
            elif tokens[1][1] != "IDENTIFIER":
                result.append((f"Line {line_num}: {tokens}", f"ERROR: Expected IDENTIFIER after 'GIMMEH', found '{tokens[1][0]}' instead."))
                flag = False
            else:
                result.append((f"Line {line_num}: {tokens}", "Valid GIMMEH statement."))

    return flag