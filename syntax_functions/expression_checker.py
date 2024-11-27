""" 
Function to check if a token is a valid expression
Parameter: Token 
Return value: True - valid expression
                False - invalid expression
"""

def expression_checker(tokens, nested_bool_flag):
    print()
    print("You are now in expression checker")
    print(tokens)
    print()
    arithmetic_operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']
    boolean_operators = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT']
    nested_boolean_operators = ['ALL OF', 'ANY OF']
    concatenation_operator = ['SMOOSH']
    comparison_operators = ['BOTH SAEM', 'DIFFRINT']
    relational_operators = ['BIGGR OF', 'SMALLR OF']
    expression_operators = (
        arithmetic_operators + 
        boolean_operators + 
        nested_boolean_operators + 
        concatenation_operator + 
        comparison_operators + 
        relational_operators
    )

    # Dictionary of operator types and corresponding functions
    operator_functions = {
        'arithmetic': arithmetic_operation,
        'boolean': boolean_operation,
        'nested_boolean': nested_boolean_operation,
        'concatenation': concatenation_operation,
        'comparison': comparison_operation,
        'relational': relational_operation,
    }
    
    # Check if the token is in any of the operator lists
    if tokens[0][0] in arithmetic_operators and tokens[0][1] == "KEYWORD":
        return operator_functions['arithmetic'](arithmetic_operators, tokens)
    elif tokens[0][0] in boolean_operators and tokens[0][1] == "KEYWORD":
        return operator_functions['boolean'](boolean_operators, tokens, expression_operators, nested_bool_flag, [0])
    elif tokens[0][0] in nested_boolean_operators and tokens[0][1] == "KEYWORD":
        return operator_functions['nested_boolean'](nested_boolean_operators, tokens, expression_operators)
    elif tokens[0][0] in concatenation_operator and tokens[0][1] == "KEYWORD":
        return operator_functions['concatenation'](concatenation_operator, tokens, expression_operators)
    elif tokens[0][0] in comparison_operators and tokens[0][1] == "KEYWORD":
        # Check for relational operators in the tokens
        if any(token[0] in relational_operators for token in tokens):
            # Call the 'relational' function if relational operators are found
            return operator_functions['relational'](relational_operators, comparison_operators, tokens, expression_operators)
        else:
            # Otherwise, call the 'comparison' function
            return operator_functions['comparison'](comparison_operators, tokens, expression_operators)
    else:
        print(f"Invalid token: {tokens[0][0]}")  # If the token does not match any known operator
        return False  # Invalid expression

def arithmetic_operation(operators, tokens):
    print()
    print("You're now in arithmetic operation function")
    print(f"Tokens: {tokens}")
    print()
    stack = []
    local_flag = True

    # Iteratively process the stack for reductions
    for token_info in tokens:
        token, token_type = token_info  # Unpack the token and its type
        
        # Check if the token is an operator
        if token in operators and token_type == "KEYWORD":
            stack.append((token, "operation"))
            # print(f"Added to stack as operation: {stack}")
        elif token == "AN" and token_type == "KEYWORD":
            stack.append((token, "keyword"))
            # print(f"Added to stack as keyword: {stack}")
        elif token_type in ["NUMBR", "NUMBAR", "TROOF", "YARN", "IDENTIFIER"]:
            stack.append((token, "operand"))
            # print(f"Added to stack as operand: {stack}")
        else:
            print(f"ERROR: Invalid token '{token}' in arithmetic.")
            local_flag = False
        
        # Check for the pattern (operation operand AN operand)
        if len(stack) >= 4:
            if (stack[-4][1] == "operation" and
                stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):
                
                # Reduce the stack
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"
                
                # Replace the reduced portion of the stack with the reduced expression
                stack = stack[:-4] + [(reduced_expression, "operand")]
                
                # print(f"Reduced to: {reduced_expression}")
    
    # After all reductions, check for the final step
    if len(stack) == 4:
        if (stack[-4][1] == "operation" and
            stack[-3][1] == "operand" and
            stack[-2][1] == "keyword" and
            stack[-1][1] == "operand"):
            
            operation = stack[-4][0]
            operand1 = stack[-3][0]
            operand2 = stack[-1][0]
            reduced_expression = f"{operation} {operand1} AN {operand2}"
            
            # Final reduction
            stack = stack[:-4] + [(reduced_expression, "operand")]
            # print(f"Final reduction: {reduced_expression}")

    # Final state of the stack
    print(f"Final stack: {stack}")

    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        print("Valid arithmetic expression.")
    else:
        print("ERROR: Malformed arithmetic expression.")
        local_flag = False

    return local_flag

def boolean_operation(operators, tokens, expression_operators, nested_bool_flag, an_count_container): 
    print()
    print("You're now in boolean operation function")
    print(f"Tokens: {tokens}")
    print()

    stack = []
    local_flag = True
    index = 0  # Start processing tokens from the first index
    operation_count = 0  # Counter for operations
    an_count = an_count_container[0]  # Unwrap the count from the container

    # Iteratively process the stack for reductions
    while index < len(tokens):
        token_info = tokens[index]
        token, token_type = token_info  # Unpack the token and its type

        # Check if the token is an operator (from either operators or expression_operators)
        if token in operators or token in expression_operators and token_type == "KEYWORD":
            stack.append((token, "operation", index))  # Add token with index
            operation_count += 1  # Increment operation count
        elif token == "AN" and token_type == "KEYWORD":
            stack.append((token, "keyword", index))  # Add keyword with index
            an_count += 1  # Increment AN count
        elif token_type in ["NUMBR", "NUMBAR", "TROOF", "YARN", "IDENTIFIER"]:
            stack.append((token, "operand", index))  # Add operand to stack
        else:
            print(f"ERROR: Invalid token '{token}' in boolean operation.")
            local_flag = False

        # Check for the pattern (operation operand AN operand)
        if len(stack) >= 4:
            # Look for a valid reduction pattern: operation operand AN operand
            if (stack[-4][1] == "operation" and
                stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):

                # Perform the reduction (operation operand AN operand)
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"

                # Replace the reduced portion of the stack with the reduced expression
                reduced_index = (stack[-4][2], stack[-1][2])  # Capture the indices of the reduced tokens
                stack = stack[:-4] + [(reduced_expression, "operand", reduced_index)]  # Replace the reduced tokens with the new expression

                # Now, let's work with the reduced tokens for further validation
                reduced_tokens = tokens[reduced_index[0]:reduced_index[1] + 1]  # Slice the original tokens list

                # Skip validation if the first token is part of the reduced tokens
                if tokens[0] in reduced_tokens:
                    print("Skipping validation since the first token is part of the reduced tokens.")
                    # Move the index to the token after the reduced portion
                    index = reduced_index[1] + 1
                    continue

                # Print for debugging
                print(f"After reduction, stack: {stack}")
                print(f"Reduced tokens for validation: {reduced_tokens}")
                print(f"Reduced index: {reduced_index}")

                # Validate the reduced expression by passing the reduced tokens to expression_checker
                if expression_checker(reduced_tokens, False) == False:
                    print("ERROR: Reduced expression is invalid.")
                    local_flag = False
                    break
                else:
                    # Move index to the token after the reduced portion
                    index = reduced_index[1] + 1
                    continue

        # Increment the index to move to the next token
        index += 1

    # After all reductions, check for the final step
    if len(stack) == 4:
        if (stack[-4][1] == "operation" and
            stack[-3][1] == "operand" and
            stack[-2][1] == "keyword" and
            stack[-1][1] == "operand"):
            
            operation = stack[-4][0]
            operand1 = stack[-3][0]
            operand2 = stack[-1][0]
            reduced_expression = f"{operation} {operand1} AN {operand2}"
            
            # Final reduction
            stack = stack[:-4] + [(reduced_expression, "operand")]

    # Final state of the stack
    print(f"Final stack: {stack}")
    
    # Print the final an_count and operation_count for debugging
    print(f"Final an_count: {an_count}")
    print(f"Final operation_count: {operation_count}")
    
    # Check if the number of "AN" keywords equals the number of operations
    if nested_bool_flag:
        # Allow for one extra "AN" if nested_bool_flag is True
        if an_count > operation_count + 1:
            print(f"ERROR: Too many 'AN' keywords. Expected at most {operation_count + 1} but got {an_count}.")
            local_flag = False
    else:
        if an_count != operation_count:
            print(f"ERROR: Number of 'AN' keywords ({an_count}) does not match number of operations ({operation_count}).")
            local_flag = False

    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        print("Valid boolean expression.")
    else:
        print("ERROR: Malformed boolean expression.")
        local_flag = False

    # Update the an_count in the container
    an_count_container[0] = an_count

    return local_flag

def nested_boolean_operation(operators, tokens, expression_operators):
    print()
    print("You're now in nested boolean operation function")
    print(f"Tokens: {tokens}")
    print()

    an_count_container = [0]  # Initialize an_count as a list to simulate pass-by-reference

    # Check if the first and last tokens meet the criteria
    if tokens[0][0] not in operators or tokens[-1] != ['MKAY', 'KEYWORD']:
        print("ERROR: Nested boolean operation must start with a valid operator and end with MKAY.")
        return False

    # Pass the container to the boolean_operation function
    if boolean_operation(operators, tokens[1:-1], expression_operators, nested_bool_flag=True, an_count_container=an_count_container):
        print("Valid structure: Starts with a valid operator and ends with MKAY.")
        # Now that boolean_operation has executed, the an_count_container has the updated count
        print(f"Updated an_count: {an_count_container[0]}")
        return True
    else:
        return False

def concatenation_operation(operators, tokens, expression_operators):
    print()
    print("You're now in concatenation operation function")
    print(f"Tokens: {tokens}")
    print()
    stack = []
    local_flag = True
    index = 0  # Start processing tokens from the first index

    # Iteratively process the stack for reductions
    while index < len(tokens):
        token_info = tokens[index]
        token, token_type = token_info  # Unpack the token and its type

        # Check if the token is an operator (from either operators or expression_operators)
        if token in operators or token in expression_operators and token_type == "KEYWORD":
            stack.append((token, "operation", index))  # Add token with index
        elif token == "AN" and token_type == "KEYWORD":
            stack.append((token, "keyword", index))  # Add keyword with index
        elif token_type in ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB", "IDENTIFIER"]:
            stack.append((token, "operand", index))  # Add operand to stack
        else:
            print(f"ERROR: Invalid token '{token}' in concatenation.")
            local_flag = False

        # Check for the pattern (operation operand AN operand)
        if len(stack) >= 4:
            # Look for a valid reduction pattern: operation operand AN operand
            if (stack[-4][1] == "operation" and
                stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):

                # Perform the reduction (operation operand AN operand)
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"

                # Replace the reduced portion of the stack with the reduced expression
                reduced_index = (stack[-4][2], stack[-1][2])  # Capture the indices of the reduced tokens
                stack = stack[:-4] + [(reduced_expression, "operand", reduced_index)]  # Replace the reduced tokens with the new expression

                # Now, let's work with the reduced tokens for further validation
                reduced_tokens = tokens[reduced_index[0]:reduced_index[1] + 1]  # Slice the original tokens list

                # Skip validation if the first token is part of the reduced tokens
                if tokens[0] in reduced_tokens:
                    print("Skipping validation since the first token is part of the reduced tokens.")
                    # Move the index to the token after the reduced portion
                    index = reduced_index[1] + 1
                    continue

                # Print for debugging
                print(f"After reduction, stack: {stack}")
                print(f"Reduced tokens for validation: {reduced_tokens}")
                print(f"Reduced index: {reduced_index}")

                # Validate the reduced expression by passing the reduced tokens to expression_checker
                if expression_checker(reduced_tokens, False) == False:
                    print("ERROR: Reduced expression is invalid.")
                    local_flag = False
                    break
                else:
                    # Move index to the token after the reduced portion
                    index = reduced_index[1] + 1
                    continue

        # Increment the index to move to the next token
        index += 1

    # After all reductions, check for the final step
    if len(stack) == 4:
        if (stack[-4][1] == "operation" and
            stack[-3][1] == "operand" and
            stack[-2][1] == "keyword" and
            stack[-1][1] == "operand"):
            
            operation = stack[-4][0]
            operand1 = stack[-3][0]
            operand2 = stack[-1][0]
            reduced_expression = f"{operation} {operand1} AN {operand2}"
            
            # Final reduction
            stack = stack[:-4] + [(reduced_expression, "operand")]

    # Final state of the stack
    print(f"Final stack: {stack}")
    
    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        print("Valid concatenation expression.")
    else:
        print("ERROR: Malformed concatenation expression.")
        local_flag = False

    return local_flag

def comparison_operation(operators, tokens, expression_operators):
    print()
    print("You're now in comparison operation function")
    print(f"Tokens: {tokens}")
    print()
    stack = []
    local_flag = True
    index = 0  # Start processing tokens from the first index

    # Iteratively process the stack for reductions
    while index < len(tokens):
        token_info = tokens[index]
        token, token_type = token_info  # Unpack the token and its type

        # Check if the token is an operator (from either operators or expression_operators)
        if token in operators or token in expression_operators and token_type == "KEYWORD":
            stack.append((token, "operation", index))  # Add token with index
        elif token == "AN" and token_type == "KEYWORD":
            stack.append((token, "keyword", index))  # Add keyword with index
        elif token_type in ["NUMBR", "NUMBAR", "YARN", "IDENTIFIER"]:
            stack.append((token, "operand", index))  # Add operand to stack
        else:
            print(f"ERROR: Invalid token '{token}' in comparison.")
            local_flag = False

        # Check for the pattern (operation operand AN operand)
        if len(stack) >= 4:
            # Look for a valid reduction pattern: operation operand AN operand
            if (stack[-4][1] == "operation" and
                stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):

                # Perform the reduction (operation operand AN operand)
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"

                # Replace the reduced portion of the stack with the reduced expression
                reduced_index = (stack[-4][2], stack[-1][2])  # Capture the indices of the reduced tokens
                stack = stack[:-4] + [(reduced_expression, "operand", reduced_index)]  # Replace the reduced tokens with the new expression

                # Now, let's work with the reduced tokens for further validation
                reduced_tokens = tokens[reduced_index[0]:reduced_index[1] + 1]  # Slice the original tokens list

                # Skip validation if the first token is part of the reduced tokens
                if tokens[0] in reduced_tokens:
                    print("Skipping validation since the first token is part of the reduced tokens.")
                    # Move the index to the token after the reduced portion
                    index = reduced_index[1] + 1
                    continue

                # Print for debugging
                print(f"After reduction, stack: {stack}")
                print(f"Reduced tokens for validation: {reduced_tokens}")
                print(f"Reduced index: {reduced_index}")

                # Validate the reduced expression by passing the reduced tokens to expression_checker
                if expression_checker(reduced_tokens, False) == False:
                    print("ERROR: Reduced expression is invalid.")
                    local_flag = False
                    break
                else:
                    # Move index to the token after the reduced portion
                    index = reduced_index[1] + 1
                    continue

        # Increment the index to move to the next token
        index += 1

    # After all reductions, check for the final step
    if len(stack) == 4:
        if (stack[-4][1] == "operation" and
            stack[-3][1] == "operand" and
            stack[-2][1] == "keyword" and
            stack[-1][1] == "operand"):
            
            operation = stack[-4][0]
            operand1 = stack[-3][0]
            operand2 = stack[-1][0]
            reduced_expression = f"{operation} {operand1} AN {operand2}"
            
            # Final reduction
            stack = stack[:-4] + [(reduced_expression, "operand")]

    # Final state of the stack
    print(f"Final stack: {stack}")
    
    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        print("Valid comparison expression.")
    else:
        print("ERROR: Malformed comparison expression.")
        local_flag = False

    return local_flag

def relational_operation(relational_operators, comparison_operators, tokens, expression_operators):
    print()
    print("You're now in relational operation function")
    print(f"Tokens: {tokens}")
    print()
    
    # Split tokens into two parts: comparison and relational
    first_part = []
    second_part = []
    found_relational = False

    # Divide tokens into first_part and second_part
    for token in tokens:
        if not found_relational:
            if token[0] in comparison_operators:
                first_part.append(token)
            elif token[0] in relational_operators:
                found_relational = True
                second_part.append(token)
            else:
                first_part.append(token)
        else:
            second_part.append(token)

    # Debugging output for token splitting
    print(f"First Part (Comparison): {first_part}")
    print(f"Second Part (Relational): {second_part}")

    # Process the second part
    print("\nProcessing the second part (Relational Operations):")
    stack = []
    local_flag = True
    index = 0  # Start processing tokens from the first index

    # Iteratively process the stack for reductions
    while index < len(second_part):
        token_info = second_part[index]
        token, token_type = token_info  # Unpack the token and its type

        # Check if the token is an operator (from relational_operators or expression_operators)
        if token in relational_operators or token in comparison_operators and token_type == "KEYWORD":
            stack.append((token, "operation", index))  # Add token with index
        elif token == "AN" and token_type == "KEYWORD":
            stack.append((token, "keyword", index))  # Add keyword with index
        elif token_type in ["NUMBR", "NUMBAR", "YARN", "IDENTIFIER"]:
            stack.append((token, "operand", index))  # Add operand to stack
        else:
            print(f"ERROR: Invalid token '{token}' in relational processing.")
            local_flag = False

        # Check for the pattern (operation operand AN operand)
        if len(stack) >= 4:
            # Look for a valid reduction pattern: operation operand AN operand
            if (stack[-4][1] == "operation" and
                stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):

                # Perform the reduction (operation operand AN operand)
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"

                # Replace the reduced portion of the stack with the reduced expression
                reduced_index = (stack[-4][2], stack[-1][2])  # Capture the indices of the reduced tokens
                stack = stack[:-4] + [(reduced_expression, "operand", reduced_index)]  # Replace the reduced tokens with the new expression

                # Print for debugging
                print(f"After reduction, stack: {stack}")
                print(f"Reduced tokens for validation: {second_part[reduced_index[0]:reduced_index[1] + 1]}")
                print(f"Reduced index: {reduced_index}")

                # Move the index to the token after the reduced portion
                index = reduced_index[1] + 1
                continue

        # Increment the index to move to the next token
        index += 1

    # After all reductions, check for the final step
    if len(stack) == 4:
        if (stack[-4][1] == "operation" and
            stack[-3][1] == "operand" and
            stack[-2][1] == "keyword" and
            stack[-1][1] == "operand"):
            
            operation = stack[-4][0]
            operand1 = stack[-3][0]
            operand2 = stack[-1][0]
            reduced_expression = f"{operation} {operand1} AN {operand2}"
            
            # Final reduction
            stack = stack[:-4] + [(reduced_expression, "operand")]

    # Final state of the stack
    print(f"Final stack: {stack}")
    
    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        print("Valid relational expression.")
        
        # Validate the original tokens as a comparison expression
        print("\nChecking if tokens are a valid comparison...")
        if not comparison_operation(comparison_operators, tokens, expression_operators):  # Assuming `expression_checker` is the comparison validator
            print("ERROR: Tokens do not form a valid comparison.")
            local_flag = False
        else:
            print("Tokens are a valid comparison expression.")
    else:
        print("ERROR: Malformed relational expression.")
        local_flag = False

    return local_flag

tokens = [
    ['ANY OF', 'KEYWORD'],
    ['BOTH OF', 'KEYWORD'],
    ['X', 'IDENTIFIER'],
    ['AN', 'KEYWORD'],
    ['EITHER OF', 'KEYWORD'],
    ['NOT', 'KEYWORD'],
    ['X', 'IDENTIFIER'],
    ['AN', 'KEYWORD'],
    ['Y', 'IDENTIFIER'],
    ['AN', 'KEYWORD'],
    ['Y', 'IDENTIFIER'],
    ['AN', 'KEYWORD'],
    ['NOT', 'KEYWORD'],
    ['Y', 'IDENTIFIER'],
    ['MKAY', 'KEYWORD']
]


expression_checker(tokens, False)