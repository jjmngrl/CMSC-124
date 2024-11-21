"""
Function to check if the lol code starts with HAI and ends with KTHXBYE
Parameter: List containing each line of the lol code
Return value: If true, will call the function to check the code block
                else, return false
"""
def program_checker(code, result):
    line_numbers = sorted(code.keys())

    index_of_HAI = None
    for line_num in line_numbers:
        for token, token_type in code[line_num]:
            if token_type == 'KEYWORD' and token == 'HAI':
                index_of_HAI = line_num
                result.append((f"Line {line_num}: {code[line_num]}", "HAI found, program starts here."))
                break
        if index_of_HAI is not None:
            break

    index_of_KTHXBYE = None
    for line_num in reversed(line_numbers):
        for token, token_type in code[line_num]:
            if token_type == 'KEYWORD' and token == 'KTHXBYE':
                index_of_KTHXBYE = line_num
                result.append((f"Line {line_num}: {code[line_num]}", "KTHXBYE found, program ends here."))
                break
        if index_of_KTHXBYE is not None:
            break

    if index_of_HAI is not None and index_of_KTHXBYE is not None and index_of_HAI < index_of_KTHXBYE:
        return index_of_HAI, index_of_KTHXBYE
    else:
        result.append(("Program structure validation.", "ERROR: The program must start with HAI and end with KTHXBYE."))
        return False