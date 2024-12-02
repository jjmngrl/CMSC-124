from syntax_functions.data_type_checker import data_type_checker
# from data_type_checker import data_type_checker
import re

""" 
Function to check if a token is a valid expression
Parameter: Token 
Return value: True - valid expression
                False - invalid expression
"""

def expression_checker(tokens, symbol_table, nested_bool_flag):
    # print(tokens)
    # print()
    # print(symbol_table)
    # print()
    arithmetic_operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']
    boolean_operators = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT']
    nested_boolean_operators = ['ALL OF', 'ANY OF']
    concatenation_operator = ['SMOOSH']
    comparison_operators = ['BOTH SAEM', 'DIFFRINT']
    relational_operators = ['BIGGR OF', 'SMALLR OF']
    explicit_operator = ['MAEK']
    recast_operator = ['IS NOW A']
    expression_operators = (
        arithmetic_operators + 
        boolean_operators + 
        nested_boolean_operators + 
        concatenation_operator + 
        comparison_operators + 
        relational_operators +
        explicit_operator +
        recast_operator
    )

    # Dictionary of operator types and corresponding functions
    operator_functions = {
        'arithmetic': arithmetic_operation,
        'boolean': boolean_operation,
        'nested_boolean': nested_boolean_operation,
        'concatenation': concatenation_operation,
        'comparison': comparison_operation,
        'relational': relational_operation,
        'explicit': explicit_typecast_checker,
        'recast': recast_checker,
    }
    
    # Check if the token is in any of the operator lists
    if tokens[0][0] in arithmetic_operators and tokens[0][1] == "KEYWORD":
        return operator_functions['arithmetic'](arithmetic_operators, tokens, symbol_table)
    elif tokens[0][0] in boolean_operators and tokens[0][1] == "KEYWORD":
        return operator_functions['boolean'](boolean_operators, tokens, expression_operators, nested_bool_flag, [0])
    elif tokens[0][0] in nested_boolean_operators and tokens[0][1] == "KEYWORD":
        return operator_functions['nested_boolean'](nested_boolean_operators, tokens, expression_operators)
    elif tokens[0][0] in concatenation_operator and tokens[0][1] == "KEYWORD":
        return operator_functions['concatenation'](concatenation_operator, tokens, expression_operators)
    elif tokens[0][0] in comparison_operators and tokens[0][1] == "KEYWORD":
        # Check if there's a relational operator with 'AN' before and after it
        return operator_functions['relational'](relational_operators, comparison_operators, tokens, expression_operators) if any(
            token[0] in relational_operators and 
            i > 0 and tokens[i - 1][0] == 'AN'
            for i, token in enumerate(tokens)
        ) else operator_functions['comparison'](comparison_operators, tokens, expression_operators)
    elif tokens[0][0] in explicit_operator and tokens[0][1] == "KEYWORD":
        return operator_functions['explicit'](tokens)
    elif len(tokens)>1 and tokens[1][0] in recast_operator and tokens[1][1] == "KEYWORD":
        return operator_functions['recast'](tokens)
    else:
        print(f"Not an expression")  # If the token does not match any known operator
        return False  # Invalid expression

def arithmetic_operation(operators, tokens, symbol_table):
    stack = []
    local_flag = True
    numbar_flag = 0

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
            if token_type == "IDENTIFIER":
                # Check if it's in the symbol table
                if token not in symbol_table:
                    print(f"SEMANTICS ERROR: {token} not declared.")
                    local_flag = False
                    break
                else:
                    # Check if it's typecastable
                    # print("token: ", token)
                    # print("symbol_table[token]: ", symbol_table[token])
                    identifier_info = symbol_table[token]
                    val = identifier_info['value']
                    type = identifier_info['value_type']

                    if type == 'NUMBR':
                        pass
                    elif type == 'NUMBAR':
                        numbar_flag = 1
                    elif type == 'TROOF':
                        if val == 'FAIL':
                            val = 0
                            type = 'NUMBR'
                        elif val == 'WIN':
                            val = 1
                            type = 'NUMBR'
                        else:
                            print("SEMANTICS ERROR: Invalid troof value")
                    elif type == 'YARN':
                        if not re.match(r'^[\d]+$', val):  # The regex matches only numbers
                            print("SEMANTICS ERROR: YARN not typecastable")

            if token_type == 'NUMBR':
                val = token
            elif token_type == 'NUMBAR':
                numbar_flag = 1
                val = token
            elif token_type == 'TROOF':
                if val == 'FAIL':
                    val = 0
                elif val == 'WIN':
                    val = 1
                else:
                    print("SEMANTICS ERROR: Invalid troof value")
            elif token_type == 'YARN':
                if not re.match(r'^[\d]+$', val):  # The regex matches only numbers
                    print("SEMANTICS ERROR: YARN not typecastable")
            # print(val)
            stack.append((val, "operand"))
            # print(f"Added to stack as operand: {stack}")
        else:
            print(f"ERROR: Invalid arithmetic expression.")
            local_flag = False
                    
        # Check for the pattern (operation operand AN operand)
        if len(stack) >= 4:
            if (stack[-4][1] == "operation" and
                stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):
                
                # print("stack: ", stack)
                # Reduce the stack
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                # print("operand1: ", operand1)
                operand2 = stack[-1][0]
                # print("operand2: ", operand2)
                reduced_expression = f"{operation} {operand1} AN {operand2}"

                # print("stack[-3]: ", stack[-3])
                # Evaluate operands
                if len(stack[-3]) == 3:  # Check if operand1 has a value (evaluated)
                    operand1_value = stack[-3][2]
                else:
                    # If operand1 is a raw token (not evaluated), assign it directly
                    if numbar_flag == 1:    # Convert them according to the dominant type
                        operand1_value = float(operand2)
                    else:
                        operand1_value = int(operand1)

                # print("stack[-1]: ", stack[-1])
                if len(stack[-1]) == 3:  # Check if operand2 has a value (evaluated)
                    operand2_value = stack[-1][2]
                else:
                    # If operand2 is a raw token (not evaluated), assign it directly
                    if numbar_flag == 1:    # Convert them according to the dominant type
                        operand2_value = float(operand2)
                    else:
                        operand2_value = int(operand2)

                # Perform the operation and get the result
                if operation == 'SUM OF':
                    result = operand1_value + operand2_value
                elif operation == 'DIFF OF':
                    result = operand1_value - operand2_value
                elif operation == 'PRODUKT OF':
                    result = operand1_value * operand2_value
                elif operation == 'QUOSHUNT OF':
                    # Division with zero-checking
                    if operand2_value == 0:
                        print("ERROR: Division by zero.")
                        local_flag = False
                    result = operand1_value / operand2_value  # Result will be float if numbar_flag == 1
                else:
                    print(f"ERROR: Invalid operation '{operation}'.")
                    local_flag = False

                # Update the value of 'IT' in the symbol table
                if 'IT' not in symbol_table:
                    symbol_table['IT'] = {
                        'type': 'IDENTIFIER',
                        'value': result,
                        'value_type': 'NUMBAR' if numbar_flag == 1 else 'NUMBR',
                        'reference_environment': 'GLOBAL'
                    }
                else:
                    symbol_table['IT']['value'] = result
                    symbol_table['IT']['value_type'] = 'NUMBAR' if numbar_flag == 1 else 'NUMBR'

                # Replace the reduced portion of the stack with both the reduced expression and evaluated value
                stack = stack[:-4] + [(reduced_expression, "operand", result)]

                # print(f"Reduced to: {reduced_expression} with result {result}")
    
    # After all reductions, check for the final step
    if len(stack) == 4:
        if (stack[-4][1] == "operation" and
            stack[-3][1] == "operand" and
            stack[-2][1] == "keyword" and
            stack[-1][1] == "operand"):
            
            # print("stack: ", stack)
            operation = stack[-4][0]
            operand1 = stack[-3][0]
            operand2 = stack[-1][0]
            reduced_expression = f"{operation} {operand1} AN {operand2}"

            # print("stack[-3]: ", stack[-3])
            # Evaluate operands
            if len(stack[-3]) == 3:  # Check if operand1 has a value (evaluated)
                operand1_value = stack[-3][2]
            else:
                # If operand1 is a raw token (not evaluated), assign it directly
                if numbar_flag == 1:    # Convert them according to the dominant type
                    operand1_value = float(operand2)
                else:
                    operand1_value = int(operand1)

            # print("stack[-1]: ", stack[-1])
            if len(stack[-1]) == 3:  # Check if operand2 has a value (evaluated)
                operand2_value = stack[-1][2]
            else:
                # If operand2 is a raw token (not evaluated), assign it directly
                if numbar_flag == 1:    # Convert them according to the dominant type
                    operand2_value = float(operand2)
                else:
                    operand2_value = int(operand2)


            # Perform the operation and get the result
            if operation == 'SUM OF':
                result = operand1_value + operand2_value
            elif operation == 'DIFF OF':
                result = operand1_value - operand2_value
            elif operation == 'PRODUKT OF':
                result = operand1_value * operand2_value
            elif operation == 'QUOSHUNT OF':
                # Division with zero-checking
                if operand2_value == 0:
                    print("ERROR: Division by zero.")
                    local_flag = False
                result = operand1_value / operand2_value  # Result will be float if numbar_flag == 1
            else:
                print(f"ERROR: Invalid operation '{operation}'.")
                local_flag = False

            # Update the value of 'IT' in the symbol table
            if 'IT' not in symbol_table:
                symbol_table['IT'] = {
                    'type': 'IDENTIFIER',
                    'value': result,
                    'value_type': 'NUMBAR' if numbar_flag == 1 else 'NUMBR',
                    'reference_environment': 'GLOBAL'
                }
            else:
                symbol_table['IT']['value'] = result
                symbol_table['IT']['value_type'] = 'NUMBAR' if numbar_flag == 1 else 'NUMBR'

            # Replace the reduced portion of the stack with both the reduced expression and evaluated value
            stack = stack[:-4] + [(reduced_expression, "operand", result)]

            # print(f"Reduced to: {reduced_expression} with result {result}")

    # Final state of the stack
    # print(f"Final stack: {stack}")

    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        print("Valid arithmetic expression.")
    else:
        print("ERROR: Invalid arithmetic expression.")
        local_flag = False

    return local_flag


def boolean_operation(operators, tokens, expression_operators, nested_bool_flag, an_count_container):
    stack = []
    local_flag = True
    index = 0  # Start processing tokens from the first index
    operation_count = 0  # Counter for operations (though unused when nested_bool_flag is True)
    an_count = an_count_container[0]  # Unwrap the count from the container

    # Iteratively process the stack for reductions
    while index < len(tokens):
        token_info = tokens[index]
        token, token_type = token_info  # Unpack the token and its type

        # print(f"Processing token at index {index}: {token_info}")

        # Check if the token is an operator (from either operators or expression_operators)
        if token in operators or token in expression_operators and token_type == "KEYWORD":
            # print(f"Token '{token}' is an operator.")
            stack.append((token, "operation", index))  # Add token with index
            operation_count += 1  # Increment operation count
        elif token == "AN" and token_type == "KEYWORD":
            # print(f"Token '{token}' is an 'AN' keyword.")
            stack.append((token, "keyword", index))  # Add keyword with index
            an_count += 1  # Increment AN count
            an_count_container[0] = an_count  # Update the count in the container
        elif token_type in ["NUMBR", "NUMBAR", "TROOF", "YARN", "IDENTIFIER"]:
            # print(f"Token '{token}' is an operand.")
            stack.append((token, "operand", index))
        else:
            # Exception (f"ERROR: Invalid token '{token}' in boolean operation.")
            print(f"ERROR: Invalid token '{token}' in boolean operation.")
            local_flag = False

        # Check if there's a "NOT" at the top of the stack before an operand
        if len(stack)>1 and stack[-2][0] == "NOT" and stack[-2][1] == "operation" and (stack[-1][1] == "operand"):
            # Perform the reduction of "NOT operand"
            operand = token
            reduced_expression = f"NOT {operand}"
            reduced_index = (stack[-2][2], index)  # Use the indices of the "NOT" and the operand
            stack = stack[:-2]  # Remove the "NOT" and the operand
            stack.append((reduced_expression, "operand", reduced_index))  # Add the reduced expression

            # Print the reduction of "NOT"
            # print(f"Reduced 'NOT' expression: {reduced_expression}")

            while True:
                if len(stack) > 1 and stack[-2][0] == "NOT" and stack[-2][1] == "operation" and stack[-1][1] == "operand":
                        # Perform the reduction of "NOT operand"
                        # print("\nNOT found after reduction\n")
                        operand = stack[-1][0]
                        reduced_expression = f"NOT {operand}"
                        reduced_index = (stack[-2][2], stack[-1][2][1])  # Use the indices of the "NOT" and the operand
                        stack = stack[:-2]  # Remove the "NOT" and the operand
                        stack.append((reduced_expression, "operand", reduced_index))  # Add the reduced expression

                        # Print the reduction of "NOT"
                        # print(f"Reduced 'NOT' expression: {reduced_expression}")

                        # Skip the remaining processing for this token (as it's been reduced)
                        index = reduced_index[1] + 1  # Skip to the next token after reduction
                else:
                    break 

            index += 1  # Skip to the next token after reduction
            continue  # Skip the remaining processing for this token (as it's been reduced)

        elif len(stack) >= 4:
            # Look for a valid reduction pattern: operation operand AN operand
            if (stack[-4][1] == "operation" and
                stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):

                # print("Pattern found: operation operand AN operand.")
                # Perform the reduction (operation operand AN operand)
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"

                # Capture the indices of the reduced tokens
                reduced_index = (stack[-4][2], stack[-1][2])  # Ensure this is a tuple with start and end indices

                # Replace the reduced portion of the stack with the new expression
                stack = stack[:-4] + [(reduced_expression, "operand", reduced_index)]  # Replace the reduced tokens with the new expression

                # Now, let's work with the reduced tokens for further validation
                reduced_tokens = tokens[reduced_index[0]:reduced_index[1] + 1]  # Correctly slice the tokens list
                # print(f"After reduction, stack: {stack}")
                # print(f"Reduced tokens for validation: {reduced_tokens}")
                # print(f"Reduced index: {reduced_index}")

                while True:
                    if len(stack) > 1 and stack[-2][0] == "NOT" and stack[-2][1] == "operation" and stack[-1][1] == "operand":
                            # Perform the reduction of "NOT operand"
                            # print("\nNOT found after reduction\n")
                            operand = stack[-1][0]
                            reduced_expression = f"NOT {operand}"
                            reduced_index = (stack[-2][2], stack[-1][2][1])  # Use the indices of the "NOT" and the operand
                            stack = stack[:-2]  # Remove the "NOT" and the operand
                            stack.append((reduced_expression, "operand", reduced_index))  # Add the reduced expression

                            # Print the reduction of "NOT"
                            # print(f"Reduced 'NOT' expression: {reduced_expression}")

                            # Skip the remaining processing for this token (as it's been reduced)
                            index = reduced_index[1] + 1  # Skip to the next token after reduction
                    else:
                        break 
                    # Skip validation if the first token is part of the reduced tokens
                    if tokens[0] in reduced_tokens:
                        # print("Skipping validation since the first token is part of the reduced tokens.")
                        # Move the index to the token after the reduced portion
                        index = reduced_index[1] + 1
                        continue

                # **Backward Check**: We now perform a backward check to see if further reductions are possible.
                if len(stack) >= 4 and (stack[-4][1] == "operation" and
                                         stack[-3][1] == "operand" and
                                         stack[-2][1] == "keyword" and
                                         stack[-1][1] == "operand"):
                    # print("Backward check found another valid pattern: operation operand AN operand.")
                    # Perform the reduction (operation operand AN operand)
                    operation = stack[-4][0]
                    operand1 = stack[-3][0]
                    operand2 = stack[-1][0]
                    reduced_expression = f"{operation} {operand1} AN {operand2}"
                    # Capture the indices of the reduced tokens
                    reduced_index = (stack[-4][2], stack[-1][2][1])  # Ensure this is a tuple with start and end indices
                    # print("reduced_index: ", reduced_index)
                    # Replace the reduced portion of the stack with the new expression
                    stack = stack[:-4] + [(reduced_expression, "operand", reduced_index)]  # Replace the reduced tokens with the new expression

                    # Now, let's work with the reduced tokens for further validation
                    reduced_tokens = tokens[reduced_index[0]:reduced_index[1] + 1]  # Correctly slice the tokens list
                    # print(f"After reduction, stack: {stack}")
                    # print(f"Reduced tokens for validation: {reduced_tokens}")
                    # print(f"Reduced index: {reduced_index}")

                # After the backward check, **update the index** to skip the reduced portion
                index = reduced_index[1] + 1
                continue  # Skip the remaining processing of the current token

        # If no operation, check for the pattern operand AN operand (special case for nested)
        if nested_bool_flag and len(stack) == 3:
            if (stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):
                # print("Nested pattern found: operand AN operand.")
                # Reduce the expression to a single operand
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operand1} AN {operand2}"

                # Replace the reduced portion of the stack with the reduced expression
                reduced_index = (stack[-3][2], stack[-1][2])
                stack = stack[:-3] + [(reduced_expression, "operand", reduced_index)]

                # No need to validate since it's just the reduction of two operands
                # print(f"After reduction, stack: {stack}")
                index += 1  # Move index to next token after reduction
                continue

        # Increment the index to move to the next token
        index += 1

    # After processing all tokens, check if there's any "extra AN" or invalid tokens
    remaining_tokens = []

    if len(stack) > 1:
        # Check for any extra tokens that shouldn't be in the stack (invalid state)
        if stack[-1][1] != "operand":
            # print(f"Extra token detected: {stack[-1]}. Returning False immediately.")
            return False  # If the last token in the stack is not an operand, return False immediately

        # If we have more than one element in the stack and everything seems valid,
        # we append all unreduced tokens to the remaining_tokens list
        # This should include tokens that are still in the stack but couldn't be reduced
        for token_info in stack:
            # For each token in the stack, we check if it's an operand, operation, or keyword
            # that hasn't been reduced yet and add it to remaining_tokens
            if isinstance(token_info[-1], int):
                remaining_tokens.append(tokens[token_info[2]:])  # Append the token from original `tokens` list using its index

    # Return the final reduced expression and remaining tokens
    reduced_expression = stack[0][0] if stack else ""  # If stack is not empty, return the reduced expression
    # print(f"Final stack: {stack}")

    if remaining_tokens:
        remaining_tokens = remaining_tokens[0]

    # print(f"BOOLEAN | Remaining tokens after reductions: {remaining_tokens}")
    # If nested_bool_flag is True, return the reduced expression along with the remaining tokens
    if nested_bool_flag:
        return reduced_expression, remaining_tokens, True
    
    if len(remaining_tokens)>0:
        local_flag = False

    # If nested_bool_flag is False, return the local_flag
    if local_flag == True:
        print("Valid Boolean Expression")
    else:
        print("ERROR: Invalid Boolean Expression")
    return local_flag

def nested_boolean_operation(operators, tokens, expression_operators):
    an_count_container = [0]  # Initialize an_count as a list to simulate pass-by-reference

    # Check if the first token is a valid operator and the last token is 'MKAY'
    if tokens[0][0] not in operators:
        # print("ERROR: Nested boolean operation must start with a valid operator.")
        return False
    if tokens[-1] != ['MKAY', 'KEYWORD']:
        # print("ERROR: Nested boolean operation must end with 'MKAY'.")
        return False

    # Slice the tokens to exclude the first (operator) and last ('MKAY') token
    inner_tokens = tokens[1:-1]

    # Process the tokens by calling boolean_operation iteratively
    remaining_tokens = inner_tokens
    while remaining_tokens:  # Continue until no remaining tokens
        # Pass the container to the boolean_operation function
        reduced_expression, remaining_tokens, local_flag = boolean_operation(
            operators, remaining_tokens, expression_operators, nested_bool_flag=True, an_count_container=an_count_container
        )

        if not local_flag:
            print("ERROR: Invalid boolean expression in the current iteration.")
            return False

        # print(f"Updated an_count: {an_count_container[0]}")
        # print(f"Reduced expression: {reduced_expression}")
        # print(f"Remaining tokens after reduction: {remaining_tokens}")

        # If no more tokens remain, it means we've reduced everything successfully
        if not remaining_tokens:
            print("Valid Boolean operation.")
            return True

        # If there are remaining tokens, and the first one is 'AN', continue processing
        if len(remaining_tokens) > 1 and remaining_tokens[0] == ['AN', 'KEYWORD']:
            # print(f"Passing remaining tokens {remaining_tokens[1:]} to boolean_operation for further processing.")
            # Recurse with the remaining tokens
            remaining_tokens = remaining_tokens[1:]  # Skip the first 'AN' token
        else:
            # If we cannot process the remaining tokens, return False
            print("ERROR: Remaining tokens after reduction do not form a valid boolean operation.")
            return False


def concatenation_operation(operators, tokens, expression_operators):
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
            # Exception(f"ERROR: Invalid token '{token}' in concatenation.")
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
                    # print("Skipping validation since the first token is part of the reduced tokens.")
                    # Move the index to the token after the reduced portion
                    index = reduced_index[1] + 1
                    continue

                # Print for debugging
                # print(f"After reduction, stack: {stack}")
                # print(f"Reduced tokens for validation: {reduced_tokens}")
                # print(f"Reduced index: {reduced_index}")

                # Validate the reduced expression by passing the reduced tokens to expression_checker
                if expression_checker(reduced_tokens, False) == False:
                    # Exception("ERROR: Reduced expression is invalid.")
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
    # print(f"Final stack: {stack}")
    
    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        print("Valid concatenation expression.")
    else:
        print("ERROR: Invalid concatenation expression.")
        local_flag = False

    return local_flag

def comparison_operation(operators, tokens, expression_operators):
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
            if token_type == "IDENTIFIER":
                # Check if it's in the symbol table
                if token not in symbol_table:
                    print(f"SEMANTICS ERROR: {token} not declared.")
                    local_flag = False
                    break
                else:
                    # Only accepts NUMBR and NUMBAR
                    identifier_info = symbol_table[token]
                    val = identifier_info['value']
                    type = identifier_info['value_type']

                    if type == 'NUMBR' or type == 'NUMBAR':
                        pass
                    else:
                        print(f"SEMANTICS ERROR: {val} is not a NUMBR/NUMBAR variable")
                        local_flag = False
                        break
            else:
                if token_type == 'NUMBR' or token_type == 'NUMBAR':
                    val = token
                else: 
                    print(f"SEMANTICS ERROR: {val} is not a NUMBR/NUMBAR literal")
                    local_flag = False
                    break

            stack.append((token, "operand", index))  # Add operand to stack
        else:
            print(f"ERROR: Invalid token '{token}' in comparison.")
            local_flag = False
            break

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

                if len(stack[-3]) == 3:  # Check if operand1 has a value (evaluated)
                    operand1_value = stack[-3][2]
                else:
                    operand1_value = operand1

                if len(stack[-1]) == 3:  # Check if operand2 has a value (evaluated)
                    operand2_value = stack[-1][2]
                else:
                    operand2_value = operand2

                if operation == 'BOTH SAEM':
                    # If operand1_value is equal to operand2_value, result is 'WIN', otherwise 'FAIL'
                    result = 'WIN' if operand1_value == operand2_value else 'FAIL'
                elif operation == 'DIFFRINT':
                    # If operand1_value is not equal to operand2_value, result is 'WIN', otherwise 'FAIL'
                    result = 'WIN' if operand1_value != operand2_value else 'FAIL'
                else:
                    print(f"ERROR: Invalid operation '{operation}'.")
                    local_flag = False
                    break

                # Update the value of 'IT' in the symbol table
                if 'IT' not in symbol_table:
                    symbol_table['IT'] = {
                        'type': 'IDENTIFIER',
                        'value': result,
                        'value_type': 'TROOF',
                        'reference_environment': 'GLOBAL'
                    }
                else:
                    symbol_table['IT']['value'] = result
                    symbol_table['IT']['value_type'] = 'TROOF' 

                # Replace the reduced portion of the stack with the reduced expression
                reduced_index = (stack[-4][2], stack[-1][2])  # Capture the indices of the reduced tokens
                stack = stack[:-4] + [(reduced_expression, "operand", reduced_index)]  # Replace the reduced tokens with the new expression

                # print("stack: ", stack)
                # print("symbol_table: ", symbol_table)
                # Now, let's work with the reduced tokens for further validation
                reduced_tokens = tokens[reduced_index[0]:reduced_index[1] + 1]  # Slice the original tokens list

                # Skip validation if the first token is part of the reduced tokens
                if tokens[0] in reduced_tokens:
                    # print("Skipping validation since the first token is part of the reduced tokens.")
                    # Move the index to the token after the reduced portion
                    index = reduced_index[1] + 1
                    continue

                # Print for debugging
                # print(f"After reduction, stack: {stack}")
                # print(f"Reduced tokens for validation: {reduced_tokens}")
                # print(f"Reduced index: {reduced_index}")

                # Validate the reduced expression by passing the reduced tokens to expression_checker
                if expression_checker(reduced_tokens, False) == False:
                    # Exception("ERROR: Reduced expression is invalid.")
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
            
            if len(stack[-3]) == 3:  # Check if operand1 has a value (evaluated)
                operand1_value = stack[-3][2]
            else:
                operand1_value = operand1

            if len(stack[-1]) == 3:  # Check if operand2 has a value (evaluated)
                operand2_value = stack[-1][2]
            else:
                operand2_value = operand2

            if operation == 'BOTH SAEM':
                # If operand1_value is equal to operand2_value, result is 'WIN', otherwise 'FAIL'
                result = 'WIN' if operand1_value == operand2_value else 'FAIL'
            elif operation == 'DIFFRINT':
                # If operand1_value is not equal to operand2_value, result is 'WIN', otherwise 'FAIL'
                result = 'WIN' if operand1_value != operand2_value else 'FAIL'
            else:
                print(f"ERROR: Invalid operation '{operation}'.")
                local_flag = False

            # Update the value of 'IT' in the symbol table
            if 'IT' not in symbol_table:
                symbol_table['IT'] = {
                    'type': 'IDENTIFIER',
                    'value': result,
                    'value_type': 'TROOF',
                    'reference_environment': 'GLOBAL'
                }
            else:
                symbol_table['IT']['value'] = result
                symbol_table['IT']['value_type'] = 'TROOF' 

            # Replace the reduced portion of the stack with the reduced expression
            reduced_index = (stack[-4][2], stack[-1][2])  # Capture the indices of the reduced tokens
            stack = stack[:-4] + [(reduced_expression, "operand", reduced_index)]  # Replace the reduced tokens with the new expression


    # Final state of the stack
    # print(f"Final stack: {stack}")
    
    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        print("Valid comparison expression.")
    else:
        print("ERROR: Invalid comparison expression.")
        local_flag = False

    # print()
    # print("symbol table: ", symbol_table)
    return local_flag

def relational_operation(relational_operators, comparison_operators, tokens, expression_operators):
    # Split tokens into two parts: comparison and relational
    print("You're in relational")
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
    # print(f"First Part (Comparison): {first_part}")
    # print(f"Second Part (Relational): {second_part}")

    # Process the second part
    # print("\nProcessing the second part (Relational Operations):")
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
            # Exception(f"ERROR: Invalid token '{token}' in relational processing.")
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
                # print(f"After reduction, stack: {stack}")
                # print(f"Reduced tokens for validation: {second_part[reduced_index[0]:reduced_index[1] + 1]}")
                # print(f"Reduced index: {reduced_index}")

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
    # print(f"Final stack: {stack}")
    
    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        print("Valid relational expression.")
        
        # Validate the original tokens as a comparison expression
        # print("\nChecking if tokens are a valid comparison...")
        if not comparison_operation(comparison_operators, tokens, expression_operators):  # Assuming `expression_checker` is the comparison validator
            # Exception("ERROR: Tokens do not form a valid comparison.")
            print("ERROR: Tokens do not form a valid comparison.")
            local_flag = False
        else:
            print("Tokens are a valid comparison expression.")
    else:
        print("ERROR: Invalid relational expression.")
        local_flag = False

    if local_flag == True:
        print("Valid relational expression")
    return local_flag

def explicit_typecast_checker(tokens):
    """
    Validates explicit typecasting in LOLCODE based on the specified grammar:
    - MAEK varident A <data_type>
    - MAEK varident <data_type>
    
    Arguments:
        tokens: A list of tokens, where each token is a tuple (value, type).
                Example: [("MAEK", "KEYWORD"), ("x", "IDENTIFIER"), ("A", "KEYWORD"), ("NUMBR", "DATATYPE")]
    
    Returns:
        True if the explicit typecasting is valid, or an error message if invalid.
    """
    # print("\nInside explicit_typecast_checker")
    # print("Tokens to check:", tokens)
    
    if len(tokens) < 3:
        return "Error: Incomplete typecasting statement"

    if tokens[0][0] != "MAEK" or tokens[0][1] != "KEYWORD":
        return "Error: Expected 'MAEK' at the start of typecasting statement"

    # Check the variable identifier
    if tokens[1][1] != "IDENTIFIER":
        return f"Error: Expected variable identifier after 'MAEK', found {tokens[1][0]}"

    # Case 1: MAEK varident A <data_type>
    if len(tokens) == 4:
        if tokens[2][0] != "A" or tokens[2][1] != "KEYWORD":
            return f"Error: Expected 'A' keyword for typecasting, found {tokens[2][0]}"
        if not data_type_checker(tokens[3]):
            return f"Error: Expected data type after 'A', found {tokens[3][0]}"
        print("Valid explicit typecasting (MAEK varident A <data_type>)")
        return True

    # Case 2: MAEK varident <data_type>
    elif len(tokens) == 3:
        if not data_type_checker(tokens[2]):
            return f"Error: Expected data type after variable identifier, found {tokens[2][0]}"
        print("Valid explicit typecasting (MAEK varident <data_type>)")
        return True

    return "Error: Invalid typecasting statement"

def recast_checker(tokens):
    """
    Validates recast statements in LOLCODE based on the specified grammar:
    - varident IS NOW A <data_type>
    - varident R <explicit_typecast>
    
    Arguments:
        tokens: A list of tokens, where each token is a tuple (value, type).
                Example: [("x", "IDENTIFIER"), ("IS NOW A", "KEYWORD"), ("NUMBR", "DATATYPE")]

    Returns:
        True if the recast statement is valid, or an error message if invalid.
    """
    # print("\nInside recast_checker")
    # print("Tokens to check:", tokens)

    if len(tokens) < 3:
        return "Error: Incomplete recast statement"

    # Check the variable identifier
    if tokens[0][1] != "IDENTIFIER":
        return f"Error: Expected variable identifier at the start, found {tokens[0][0]}"

    # Case 1: varident IS NOW A <data_type>
    if len(tokens) >= 3 and tokens[1][0] == "IS NOW A" and tokens[1][1] == "KEYWORD":
        if data_type_checker(tokens[2]):
            print("Valid recast (varident IS NOW A <data_type>)")
            return True
        else:
            return f"Error: Expected data type after 'IS NOW A', found {tokens[2][0]}"

    # Case 2: varident R <explicit_typecast>
    elif len(tokens) >= 2 and tokens[1][0] == "R" and tokens[1][1] == "KEYWORD":
        explicit_typecast_tokens = tokens[2:]  # Extract the tokens after 'R'
        # print(explicit_typecast_tokens)
        result = explicit_typecast_checker(explicit_typecast_tokens)
        if result == True:
            print("Valid recast (varident R <explicit_typecast>)")
            return True
        else:
            return result

    return "Error: Invalid recast statement"

