"""
    Function to check if GIMMEH statements are valid.
    Rule: The token following GIMMEH must be an IDENTIFIER.
"""
def gimmeh_statement_checker(token):
    flag = True  # Tracks if all GIMMEH statements are valid

    if len(token) == 2 and token[1][1] == "IDENTIFIER":
        return True
    else:
        return False
    # if len(token) < 2:
    #     return False
    # elif token[1][1] != "IDENTIFIER":
    #     flag = False
    # else:
    #     # result.append((f"Line {line_num}: {tokens}", "Valid GIMMEH statement."))
    #     return True
    # return flag