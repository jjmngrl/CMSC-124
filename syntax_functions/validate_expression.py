def validate_expression(expression_tokens, classified_tokens):
    valid_operations = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'BIGGR OF', 'SMALLR OF', 'MOD OF', 'BOTH SAEM', 'DIFFRINT', 'BOTH OF', 'EITHER OF', 'WON OF']
    stack = []
    local_flag = True  # Track errors locally within the function

    for token, token_type in expression_tokens:
        print(f"Processing token: {token}, type: {token_type}")
        
        if token in valid_operations and token_type == "KEYWORD":
            stack.append((token, "operation"))
        elif token == "AN" and token_type == "KEYWORD":
            stack.append((token, "keyword"))
        elif token_type in ["NUMBR", "NUMBAR", "TROOF", "YARN", "IDENTIFIER"]:
            if token_type == "IDENTIFIER":
                if not any(
                    token == t and tt == "IDENTIFIER"
                    for line_tokens in classified_tokens.values()
                    for t, tt in line_tokens
                ):
                    print(f"ERROR: Undefined identifier '{token}' in expression.")
                    local_flag = False
            stack.append((token, "operand"))
        else:
            print(f"ERROR: Invalid token '{token}' in expression.")
            local_flag = False

        # Iteratively process the stack for reductions
        while True:
            # Handle BOTH SAEM and DIFFRINT patterns: operation operand keyword operand
            if len(stack) >= 4 and stack[-4][1] == "operation" and stack[-3][1] == "operand" and stack[-2][1] == "keyword" and stack[-1][1] == "operand":
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"
                stack = stack[:-4] + [(reduced_expression, "operand")]
                print(f"Reduced (comparison): {reduced_expression}")

            # Handle other patterns (nested operations, binary operations)
            elif len(stack) >= 5 and stack[-5][1] == "operation" and stack[-4][1] == "operand" and stack[-3][1] == "keyword" and stack[-2][1] == "operand" and stack[-1][1] == "keyword":
                operation = stack[-5][0]
                operand1 = stack[-4][0]
                operand2 = stack[-2][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"
                stack = stack[:-5] + [(reduced_expression, "operand")]
                print(f"Reduced (nested): {reduced_expression}")

            elif len(stack) >= 3 and stack[-3][1] == "operation" and stack[-2][1] == "operand" and stack[-1][1] == "operand":
                operation = stack[-3][0]
                operand1 = stack[-2][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"
                stack = stack[:-3] + [(reduced_expression, "operand")]
                print(f"Reduced (binary): {reduced_expression}")

            else:
                break

        print(f"Current stack: {stack}")

    # Final validation of the stack
    if len(stack) == 1 and stack[0][1] == "operand" and local_flag:
        return "Valid VISIBLE statement.", True
    else:
        print(f"Final stack: {stack}")
        return "ERROR: Malformed expression.", False