from syntax_functions.data_type_checker import data_type_checker
from syntax_functions  import semantics_functions
from syntax_functions import assignment_checker
from syntax_functions.explicit_typecast_checker import to_different_types
import re

""" 
Function to check if a token is a valid expression
Parameter: Token 
Return value: True - valid expression
                False - invalid expression
"""

def expression_checker(tokens, symbol_table, flag=False):
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
    
    # 1. **Concatenation check** 
    if tokens[0][0] in concatenation_operator or any(token[0] == '+' for token in tokens):
        return operator_functions['concatenation'](concatenation_operator, tokens, symbol_table, expression_operators)

    # 2. **Arithmetic operators check**
    elif tokens[0][0] in arithmetic_operators and tokens[0][1] == "KEYWORD":
        return operator_functions['arithmetic'](arithmetic_operators, tokens, symbol_table)
    
    # 3. **Boolean operators check**
    elif tokens[0][0] in boolean_operators and tokens[0][1] == "KEYWORD":
        return operator_functions['boolean'](boolean_operators, tokens, symbol_table, expression_operators, flag, [0])
    
    # 4. **Nested Boolean operators check**
    elif tokens[0][0] in nested_boolean_operators and tokens[0][1] == "KEYWORD":
        return operator_functions['nested_boolean'](nested_boolean_operators, tokens, symbol_table, expression_operators)

    # 5. **Comparison and Relational operators check**
    elif tokens[0][0] in comparison_operators and tokens[0][1] == "KEYWORD":
        # Check if there's a relational operator with 'AN' before and after it
        return operator_functions['relational'](relational_operators, comparison_operators, tokens, symbol_table, expression_operators) if any(
            token[0] in relational_operators and 
            i > 0 and tokens[i - 1][0] == 'AN'
            for i, token in enumerate(tokens)
        ) else operator_functions['comparison'](comparison_operators, tokens, symbol_table, expression_operators, flag)

    # 6. **Explicit typecasting check**
    elif tokens[0][0] in explicit_operator and tokens[0][1] == "KEYWORD":
        return operator_functions['explicit'](tokens)
    
    # 7. **Recasting check**
    elif len(tokens) > 1 and (tokens[1][0] in recast_operator or tokens[2][0] in explicit_operator) and tokens[1][1] == "KEYWORD" and tokens[1][0] == "R":
        return operator_functions['recast'](tokens)

    # If no match, return False (not a valid expression)
    else:
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
        elif token == "AN" and token_type == "KEYWORD":
            stack.append((token, "keyword"))
        elif token_type in ["NUMBR", "NUMBAR", "TROOF", "YARN", "IDENTIFIER"]:
            if token_type == "IDENTIFIER":
                # Check if it's in the symbol table
                if token not in symbol_table:
                    print(f"SEMANTICS ERROR: {token} not declared.")
                    local_flag = False
                    break
                else:
                    # Check if it's typecastable
                    identifier_info = symbol_table[token]
                    val = identifier_info['value']
                    val_type = identifier_info['value_type']

                    if val_type == 'NUMBR':
                        pass
                    elif val_type == 'NUMBAR':
                        numbar_flag = 1
                    elif val_type == 'TROOF':
                        if val == 'FAIL':
                            val = 0
                            val_type = 'NUMBR'
                        elif val == 'WIN':
                            val = 1
                            val_type = 'NUMBR'
                        else:
                            return False
                    elif val_type == 'YARN':
                        val = token.strip('"')
                        if re.match(r'^[\d]+$', val):  # Match digits only
                            val = int(val)  # Convert back to integer after matching
                        elif re.match(r'^[\d]+\.[\d]+$', val):  # Match decimal numbers
                            val = float(val)  # Convert to float
                        else:
                            print("SEMANTICS ERROR: YARN not typecastable")
                            return False
            elif token_type == 'NUMBR':
                val = token
            elif token_type == 'NUMBAR':
                numbar_flag = 1
                val = token
            elif token_type == 'TROOF':
                if token == 'FAIL':
                    val = 0
                elif token == 'WIN':
                    val = 1
                else:
                    print("SEMANTICS ERROR: 2Invalid troof value")
                    return False
            elif token_type == 'YARN':
                val = token.strip('"')
                if re.match(r'^[\d]+$', val):  # Match digits only
                    val = int(val)  # Convert back to integer after matching
                elif re.match(r'^[\d]+\.[\d]+$', val):  # Match decimal numbers
                    val = float(val)  # Convert to float
                else:
                    print("SEMANTICS ERROR: YARN not typecastable")
                    return False
            stack.append((val, "operand"))
        else:
            print(f"ERROR: Invalid arithmetic expression.")
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

                # Evaluate operands
                if len(stack[-3]) == 3:  # Check if operand1 has a value (evaluated)
                    operand1_value = stack[-3][2]
                else:
                    # If operand1 is a raw token (not evaluated), assign it directly
                    if numbar_flag == 1:    # Convert them according to the dominant type
                        operand1_value = float(operand2)
                    else:
                        operand1_value = int(operand1)

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
                        print("SEMANTIC ERROR: Division by zero.")
                        local_flag = False
                    result = operand1_value / operand2_value  # Result will be float if numbar_flag == 1
                elif operation == 'MOD OF':
                    result = operand1_value % operand2_value
                elif operation == 'BIGGR OF':
                    result = max(operand1_value, operand2_value)
                elif operation == 'SMALLR OF':
                    result = min(operand1_value, operand2_value)
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

            # Evaluate operands
            if len(stack[-3]) == 3:  # Check if operand1 has a value (evaluated)
                operand1_value = stack[-3][2]
            else:
                # If operand1 is a raw token (not evaluated), assign it directly
                if numbar_flag == 1:    # Convert them according to the dominant type
                    operand1_value = float(operand2)
                else:
                    operand1_value = int(operand1)

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
                    print("SEMANTIC ERROR: Division by zero.")
                    local_flag = False
                result = operand1_value / operand2_value  # Result will be float if numbar_flag == 1
            elif operation == 'MOD OF':
                result = operand1_value % operand2_value
            elif operation == 'BIGGR OF':
                result = max(operand1_value, operand2_value)
            elif operation == 'SMALLR OF':
                result = min(operand1_value, operand2_value)
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



    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        # print("Valid arithmetic expression.")
        pass
    else:
        print("ERROR: Invalid arithmetic expression.")
        local_flag = False

    return local_flag



def boolean_operation(operators, tokens, symbol_table, expression_operators, nested_bool_flag, an_count_container, bool_operator = None):
    stack = []
    local_flag = True
    index = 0  # Start processing tokens from the first index
    operation_count = 0  # Counter for operations (though unused when nested_bool_flag is True)
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
            an_count_container[0] = an_count  # Update the count in the container
        elif token_type in ["NUMBR", "NUMBAR", "TROOF", "YARN", "IDENTIFIER"]:
            # Process operands
            if token_type == "IDENTIFIER":
                # Check if it's in the symbol table
                if token not in symbol_table:
                    print(f"SEMANTICS ERROR: {token} not declared.")
                    local_flag = False
                    break
                else:
                    # Handle IDENTIFIER logic
                    identifier_info = symbol_table[token]
                    val = identifier_info['value']
                    val_type = identifier_info['value_type']


                    if val_type == 'NUMBR':
                        val = int(val)  # Convert string to integer for numeric comparison
                        val = 'WIN' if val != 0 else 'FAIL'
                    elif val_type == 'NUMBAR':
                        val = float(val)  # Convert to float if it's a number
                        val = 'WIN' if val != 0 else 'FAIL'
                    elif val_type == 'TROOF':
                        pass  # Handle TROOF if necessary
                    elif val_type == 'YARN':
                        val = 'WIN' if val != "" else 'FAIL'
            # For direct NUMBR types
            elif val_type == 'NUMBR':
                val = int(val)  # Convert string to integer for numeric comparison
                val = 'WIN' if val != 0 else 'FAIL'
            elif val_type == 'NUMBAR':
                val = float(val)  # Convert to float if it's a number
                val = 'WIN' if val != 0 else 'FAIL'
            elif val_type == 'TROOF':
                pass  # Handle TROOF if necessary
            elif val_type == 'YARN':
                val = 'WIN' if val != "" else 'FAIL'

            stack.append((val, "operand", index))
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

            # Update the value of 'IT' in the symbol table
            if 'IT' not in symbol_table:
                symbol_table['IT'] = {
                    'type': 'IDENTIFIER',
                    'value': 'WIN' if operand == 'FAIL' else 'FAIL',
                    'value_type': 'TROOF',
                    'reference_environment': 'GLOBAL'
                }
            else:
                symbol_table['IT']['value'] = 'WIN' if operand == 'FAIL' else 'FAIL'
                symbol_table['IT']['value_type'] = 'TROOF'

            stack.append(('WIN' if operand == 'FAIL' else 'FAIL', "operand", reduced_index))  # Add the reduced expression

            while True:
                if len(stack) > 1 and stack[-2][0] == "NOT" and stack[-2][1] == "operation" and stack[-1][1] == "operand":
                        # Perform the reduction of "NOT operand"
                        operand = stack[-1][0]
                        reduced_expression = f"NOT {operand}"
                        reduced_index = (stack[-2][2], stack[-1][2][1])  # Use the indices of the "NOT" and the operand

                        stack = stack[:-2]  # Remove the "NOT" and the operand

                        # Update the value of 'IT' in the symbol table
                        if 'IT' not in symbol_table:
                            symbol_table['IT'] = {
                                'type': 'IDENTIFIER',
                                'value': 'WIN' if operand == 'FAIL' else 'FAIL',
                                'value_type': 'TROOF',
                                'reference_environment': 'GLOBAL'
                            }
                        else:
                            symbol_table['IT']['value'] = 'WIN' if operand == 'FAIL' else 'FAIL'
                            symbol_table['IT']['value_type'] = 'TROOF'

                        stack.append(('WIN' if operand == 'FAIL' else 'FAIL', "operand", reduced_index))  # Add the reduced expression

                        # Update the value of 'IT' in the symbol table
                        if 'IT' not in symbol_table:
                            symbol_table['IT'] = {
                                'type': 'IDENTIFIER',
                                'value': 'WIN' if operand == 'FAIL' else 'FAIL',
                                'value_type': 'TROOF',
                                'reference_environment': 'GLOBAL'
                            }
                        else:
                            symbol_table['IT']['value'] = 'WIN' if operand == 'FAIL' else 'FAIL'
                            symbol_table['IT']['value_type'] = 'TROOF'


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

                # Perform the reduction (operation operand AN operand)
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operation} {operand1} AN {operand2}"

                # Capture the indices of the reduced tokens
                reduced_index = (stack[-4][2], stack[-1][2])  # Ensure this is a tuple with start and end indices

                if operand1 == 'WIN':
                    operand1 = True
                else:
                    operand1 = False

                if operand2 == 'WIN':
                    operand2 = True
                else:
                    operand2 = False
                    

                if operation == 'BOTH OF':
                    result = operand1 and operand2
                elif operation == 'EITHER OF':
                    result = operand1 or operand2
                elif operation == 'WON OF':
                    result = operand1 ^ operand2
                else:
                    print(f"SEMANTIC ERROR: Invalid operation '{operation}'.")
                    local_flag = False
                    return local_flag

                # Update the value of 'IT' in the symbol table
                if 'IT' not in symbol_table:
                    symbol_table['IT'] = {
                        'type': 'IDENTIFIER',
                        'value': 'WIN' if result else 'FAIL',
                        'value_type': 'TROOF',
                        'reference_environment': 'GLOBAL'
                    }
                else:
                    symbol_table['IT']['value'] = 'WIN' if result else 'FAIL'
                    symbol_table['IT']['value_type'] = 'TROOF'

                # Replace the reduced portion of the stack with the new expression
                stack = stack[:-4] + [('WIN' if result else 'FAIL', "operand", reduced_index)]  # Replace the reduced tokens with the new expression

                # Now, let's work with the reduced tokens for further validation
                reduced_tokens = tokens[reduced_index[0]:reduced_index[1] + 1]  # Correctly slice the tokens list

                while True:
                    if len(stack) > 1 and stack[-2][0] == "NOT" and stack[-2][1] == "operation" and stack[-1][1] == "operand":
                            # Perform the reduction of "NOT operand"
                            operand = stack[-1][0]
                            reduced_expression = f"NOT {operand}"
                            reduced_index = (stack[-2][2], stack[-1][2][1])  # Use the indices of the "NOT" and the operand
                            stack = stack[:-2]  # Remove the "NOT" and the operand

                            # Update the value of 'IT' in the symbol table
                            if 'IT' not in symbol_table:
                                symbol_table['IT'] = {
                                    'type': 'IDENTIFIER',
                                    'value': 'WIN' if operand == 'FAIL' else 'FAIL',
                                    'value_type': 'TROOF',
                                    'reference_environment': 'GLOBAL'
                                }
                            else:
                                symbol_table['IT']['value'] = 'WIN' if operand == 'FAIL' else 'FAIL'
                                symbol_table['IT']['value_type'] = 'TROOF'

                            stack.append(('WIN' if operand == 'FAIL' else 'FAIL', "operand", reduced_index))  # Add the reduced expression

                            # Update the value of 'IT' in the symbol table
                            if 'IT' not in symbol_table:
                                symbol_table['IT'] = {
                                    'type': 'IDENTIFIER',
                                    'value': 'WIN' if operand == 'FAIL' else 'FAIL',
                                    'value_type': 'TROOF',
                                    'reference_environment': 'GLOBAL'
                                }
                            else:
                                symbol_table['IT']['value'] = 'WIN' if operand == 'FAIL' else 'FAIL'
                                symbol_table['IT']['value_type'] = 'TROOF'

                            # Skip the remaining processing for this token (as it's been reduced)
                            index = reduced_index[1] + 1  # Skip to the next token after reduction
                    else:
                        break 
                    # Skip validation if the first token is part of the reduced tokens
                    if tokens[0] in reduced_tokens:
                        # Move the index to the token after the reduced portion
                        index = reduced_index[1] + 1
                        continue

                # **Backward Check**: We now perform a backward check to see if further reductions are possible.
                if len(stack) >= 4 and (stack[-4][1] == "operation" and
                                         stack[-3][1] == "operand" and
                                         stack[-2][1] == "keyword" and
                                         stack[-1][1] == "operand"):
                    # Perform the reduction (operation operand AN operand)
                    operation = stack[-4][0]
                    operand1 = stack[-3][0]
                    operand2 = stack[-1][0]
                    reduced_expression = f"{operation} {operand1} AN {operand2}"
                    # Capture the indices of the reduced tokens
                    reduced_index = (stack[-4][2], stack[-1][2][1])  # Ensure this is a tuple with start and end indices

                    if operand1 == 'WIN':
                        operand1 = True
                    else:
                        operand1 = False

                    if operand2 == 'WIN':
                        operand2 = True
                    else:
                        operand2 = False
                        
                    if operation == 'BOTH OF':
                        result = operand1 and operand2
                    elif operation == 'EITHER OF':
                        result = operand1 or operand2
                    elif operation == 'WON OF':
                        result = operand1 ^ operand2
                    else:
                        print(f"SEMANTIC ERROR: Invalid operation '{operation}'.")
                        local_flag = False
                        return local_flag

                    # Update the value of 'IT' in the symbol table
                    if 'IT' not in symbol_table:
                        symbol_table['IT'] = {
                            'type': 'IDENTIFIER',
                            'value': 'WIN' if result else 'FAIL',
                            'value_type': 'TROOF',
                            'reference_environment': 'GLOBAL'
                        }
                    else:
                        symbol_table['IT']['value'] = 'WIN' if result else 'FAIL'
                        symbol_table['IT']['value_type'] = 'TROOF'

                    # Replace the reduced portion of the stack with the new expression
                    stack = stack[:-4] + [('WIN' if result else 'FAIL', "operand", reduced_index)]  # Replace the reduced tokens with the new expression

                    # Now, let's work with the reduced tokens for further validation
                    reduced_tokens = tokens[reduced_index[0]:reduced_index[1] + 1]  # Correctly slice the tokens list

                # After the backward check, **update the index** to skip the reduced portion
                index = reduced_index[1] + 1
                continue  # Skip the remaining processing of the current token

        # If no operation, check for the pattern operand AN operand (special case for nested)
        if nested_bool_flag and len(stack) == 3 and bool_operator != None:
            if (stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):
                # Reduce the expression to a single operand
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]
                reduced_expression = f"{operand1} AN {operand2}"

                # Replace the reduced portion of the stack with the reduced expression
                reduced_index = (stack[-3][2], stack[-1][2])

                if operand1 == 'WIN':
                    operand1 = True
                else:
                    operand1 = False

                if operand2 == 'WIN':
                    operand2 = True
                else:
                    operand2 = False
                    
                if bool_operator == 'ALL OF':
                    result = operand1 and operand2
                elif bool_operator == 'ANY OF':
                    result = operand1 or operand2
                else:
                    print(f"SEMANTIC ERROR: Invalid operation '{operation}'.")
                    local_flag = False
                    return local_flag

                # Update the value of 'IT' in the symbol table
                if 'IT' not in symbol_table:
                    symbol_table['IT'] = {
                        'type': 'IDENTIFIER',
                        'value': 'WIN' if result else 'FAIL',
                        'value_type': 'TROOF',
                        'reference_environment': 'GLOBAL'
                    }
                else:
                    symbol_table['IT']['value'] = 'WIN' if result else 'FAIL'
                    symbol_table['IT']['value_type'] = 'TROOF'

                stack = stack[:-3] + [('WIN' if result else 'FAIL', "operand", reduced_index)]

                # No need to validate since it's just the reduction of two operands
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

    if remaining_tokens:
        remaining_tokens = remaining_tokens[0]

    # If nested_bool_flag is True, return the reduced expression along with the remaining tokens
    if nested_bool_flag:
        return reduced_expression, remaining_tokens, True
    
    if len(remaining_tokens)>0:
        local_flag = False

    # If nested_bool_flag is False, return the local_flag
    if local_flag != True:
        print("ERROR: Invalid Boolean Expression")
    return local_flag

def nested_boolean_operation(operators, tokens, symbol_table, expression_operators):
    an_count_container = [0]  # Initialize an_count as a list to simulate pass-by-reference

    # Check if the first token is a valid operator and the last token is 'MKAY'
    if tokens[0][0] not in operators:
        print("ERROR: Nested boolean operation must start with a valid operator.")
        return False
    if tokens[-1] != ['MKAY', 'KEYWORD']:
        print("ERROR: Nested boolean operation must end with 'MKAY'.")
        return False

    nested_operator = tokens[0][0]
    nested_operator = str(nested_operator)
    # Slice the tokens to exclude the first (operator) and last ('MKAY') token
    inner_tokens = tokens[1:-1]

    # Process the tokens by calling boolean_operation iteratively
    remaining_tokens = inner_tokens
    while remaining_tokens:  # Continue until no remaining tokens
        # Pass the container to the boolean_operation function
        reduced_expression, remaining_tokens, local_flag = boolean_operation(
            operators, remaining_tokens, symbol_table, expression_operators, nested_bool_flag=True, an_count_container=an_count_container, bool_operator=nested_operator
        )

        if not local_flag:
            print("ERROR: Invalid boolean expression in the current iteration.")
            return False

        # If no more tokens remain, it means we've reduced everything successfully
        if not remaining_tokens:
            print("Valid Boolean operation.")
            return True

        # If there are remaining tokens, and the first one is 'AN', continue processing
        if len(remaining_tokens) > 1 and remaining_tokens[0] == ['AN', 'KEYWORD']:
            # Recurse with the remaining tokens
            remaining_tokens = remaining_tokens[1:]  # Skip the first 'AN' token
        else:
            # If we cannot process the remaining tokens, return False
            print("ERROR: Remaining tokens after reduction do not form a valid boolean operation.")
            return False

def concatenation_operation(operators, tokens, symbol_table, expression_operators):
    stack = []
    temp_operand = []  # List to temporarily hold operands for processing
    local_flag = True
    index = 0  # Start processing tokens from the first index

    # Iteratively process the stack for reductions
    while index < len(tokens):
        token_info = tokens[index]
        token, token_type = token_info  # Unpack the token and its type

        # Check if the token is an operator (from either operators or expression_operators)
        if token in operators or (token in expression_operators and token_type == "KEYWORD"):
            stack.append((token, "operation", index))  # Add token with index
        elif (token == "AN" or token == "+") and token_type == "KEYWORD":
            stack.append((token, "keyword", index))  # Add keyword with index
        elif token_type in ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB", "IDENTIFIER"]:
            # If it's an IDENTIFIER, check if it exists in the symbol table
            if token_type == "IDENTIFIER":
                if token not in symbol_table:
                    print(f"SEMANTICS ERROR: {token} not declared.")
                    local_flag = False
                    break
                else:
                    val = symbol_table[token]['value']
                    val_type = symbol_table[token]['value_type']
            else:
                val = token
                val_type = token_type

            # Add to temp_operand (don't check symbol table here, add directly)
            temp_operand.append((val, type, index))

            # Add operand to stack
            stack.append((val, "operand", index))
        else:
            print(f"ERROR: Invalid token '{token}' in concatenation.")
            local_flag = False

        # Check for the 3-element pattern (operand AN operand)
        if len(stack) == 3:
            if (stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and stack[-2][0] == "+" and
                stack[-1][1] == "operand"):

                # Concatenate the two operands
                operand1 = stack[-3][0]
                operand2 = stack[-1][0]

                # Concatenate the values of the operands
                reduced_val = operand1 + operand2
                reduced_expression = f"{operand1}{operand2}"

                # Update the IT value with the concatenated result
                if 'IT' not in symbol_table:
                    symbol_table['IT'] = {
                        'type': 'IDENTIFIER',
                        'value': reduced_expression,
                        'value_type': 'TROOF',
                        'reference_environment': 'GLOBAL'
                    }
                else:
                    symbol_table['IT']['value'] = reduced_expression
                    symbol_table['IT']['value_type'] = 'TROOF'

                # Replace the reduced portion of the stack with the concatenated result
                start_index = stack[-3][2][0] if isinstance(stack[-3][2], tuple) else stack[-3][2]
                end_index = stack[-1][2][0] if isinstance(stack[-1][2], tuple) else stack[-1][2]
                reduced_index = (start_index, end_index)  # Capture the indices of the reduced tokens
                stack = [(reduced_expression, "operand", reduced_index)]  # Replace the tokens with the reduced expression

                # Now validate the reduced expression
                reduced_tokens = tokens[:reduced_index[1]]
                if expression_checker(reduced_tokens, symbol_table, False) == False:
                    print("ERROR: Reduced expression is invalid.")
                    local_flag = False
                    break
                else:
                    index = reduced_index[1] + 1

                    expression_value = symbol_table['IT']['value']
                continue

        # Check for the pattern (operation operand AN operand)
        elif len(stack) >= 4:
            # Look for a valid reduction pattern: operation operand AN operand
            if (stack[-4][1] == "operation" and
                stack[-3][1] == "operand" and
                (stack[-2][1] == "keyword" and stack[-2][0] == "AN") and
                stack[-1][1] == "operand"):

                # Perform the reduction (operation operand AN operand)
                operation = stack[-4][0]
                # Check if stack[-3][2] is an integer or a tuple
                if isinstance(stack[-3][2], tuple):  # If it's a tuple
                    operand1 = expression_value
                else:  # Otherwise, treat it as a value from the stack
                    operand1 = stack[-3][0]

                # Check if stack[-1][2] is an integer or a tuple
                if isinstance(stack[-1][2], tuple):  # If it's a tuple
                    operand2 = expression_value
                else:  # Otherwise, treat it as a value from the stack
                    operand2 = stack[-1][0]


                # Fetch the actual values of the operands
                val1 = symbol_table[operand1]['value'] if operand1 in symbol_table else operand1
                val2 = symbol_table[operand2]['value'] if operand2 in symbol_table else operand2

                # Concatenate the values of the operands (since we're dealing with "SMOOSH" operation)
                reduced_val = val1 + val2
                reduced_expression = f"{operand1}{operand2}"  # Store the reduced expression

                # Update the IT value with the concatenated result
                if 'IT' not in symbol_table:
                    symbol_table['IT'] = {
                        'type': 'IDENTIFIER',
                        'value': reduced_expression,
                        'value_type': 'YARN',
                        'reference_environment': 'GLOBAL'
                    }
                else:
                    symbol_table['IT']['value'] = reduced_expression
                    symbol_table['IT']['value_type'] = 'YARN'


                # Replace the reduced portion of the stack with the concatenated result
                reduced_index = (stack[-3][2], stack[-1][2])  # Capture the indices of the reduced tokens
                stack = stack[:-3] + [(reduced_expression, "operand", reduced_index)]  # Replace the reduced tokens with the new expression

                # Now, let's work with the reduced tokens for further validation
                reduced_tokens = tokens[reduced_index[0]:reduced_index[1] + 1]  # Slice the original tokens list

                # Skip validation if the first token is part of the reduced tokens
                if tokens[0] in reduced_tokens:
                    # Move the index to the token after the reduced portion
                    index = reduced_index[1] + 1
                    continue

                # Validate the reduced expression by passing the reduced tokens to expression_checker
                if expression_checker(reduced_tokens, symbol_table, False) == False:
                    print("ERROR: Reduced expression is invalid.")
                    local_flag = False
                    break
                else:
                    index = reduced_index[1] + 1

                    expression_value = symbol_table['IT']['value']
                    continue

        # Increment the index to move to the next token
        index += 1

    # After all reductions, check for the final step (outside of the loop)
    if len(stack) == 4:
        if (stack[-4][1] == "operation" and
            stack[-3][1] == "operand" and
            (stack[-2][1] == "keyword" and stack[-2][0] == "AN") and
            stack[-1][1] == "operand"):

            operation = stack[-4][0]
            # Check if stack[-3][2] is an integer or a tuple
            if isinstance(stack[-3][2], tuple):  # If it's a tuple
                operand1 = expression_value
            else:  # Otherwise, treat it as a value from the stack
                operand1 = stack[-3][0]

            # Check if stack[-1][2] is an integer or a tuple
            if isinstance(stack[-1][2], tuple):  # If it's a tuple
                operand2 = expression_value
            else:  # Otherwise, treat it as a value from the stack
                operand2 = stack[-1][0]

            reduced_expression = f"{operand1}{operand2}"

            # Final reduction
            stack = stack[:-4] + [(reduced_expression, "operand")]

    # After all reductions, check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        # Update the value of 'IT' in the symbol table
        if 'IT' not in symbol_table:
            symbol_table['IT'] = {
                'type': 'IDENTIFIER',
                'value': stack[0][0],
                'value_type': 'YARN',
                'reference_environment': 'GLOBAL'
            }
        else:
            symbol_table['IT']['value'] = stack[0][0]
            symbol_table['IT']['value_type'] = 'YARN' 
    else:
        print("ERROR: Invalid concatenation expression.")
        local_flag = False

    return local_flag


def comparison_operation(operators, tokens, symbol_table, expression_operators, relational_flag):
    stack = []
    local_flag = True
    index = 0  # Start processing tokens from the first index
    numbar_flag = 0
    numbr_flag = 0

    # Iteratively process the stack for reductions
    while index < len(tokens):
        token_info = tokens[index]
        if len(token_info) == 2:
            token, token_type = token_info  # Unpack the token and its type
        elif len(token_info) == 3 and relational_flag == True:
            token, token_type, index = token_info
            #change token type based on its data type
            if type(token) == float:
                token_type = "NUMBAR"
            elif type(token) == int:
                token_type = "NUMBR"

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
                    val_type = identifier_info['value_type']
                    if val_type == 'NUMBR':
                        numbr_flag = 1
                    elif val_type == 'NUMBAR':
                        numbar_flag = 1
                    else:
                        print(f"SEMANTICS ERROR: {val} is not a NUMBR/NUMBAR variable")
                        local_flag = False
                        break
            else:
                if token_type == 'NUMBR':
                    val = int(token)
                    numbr_flag = 1
                elif token_type == 'NUMBAR':
                    val = float(token)
                    numbar_flag = 1
                else: 
                    print(f"SEMANTICS ERROR: {val} is not a NUMBR/NUMBAR literal")
                    local_flag = False
                    break

            stack.append((val, "operand", index))  # Add operand to stack
        elif relational_flag == True and len(token_info) == 3:
                stack.append((token, token_type, index))
        else:
            print(f"ERROR: Invalid token '{token}' in comparison.")
            local_flag = False
            break

        
        
        if numbar_flag == 1 and numbr_flag == 1:
            print(f"SEMANTICS ERROR: Operands should be all NUMBRs or all NUMBARs")
            local_flag = False
            break

        # Check for the pattern (operation operand AN operand)
        stack_for_final_check = stack
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
                if isinstance(stack[-1][2], tuple):
                    reduced_index = (stack[-4][2], stack[-1][2][1])
                else:
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
    if len(stack_for_final_check) == 4:
        stack = stack_for_final_check
        if (stack[-4][1] == "operation" and
            stack[-3][1] == "operand" and
            stack[-2][1] == "keyword" and
            stack[-1][1] == "operand"):
            
            operation = stack[-4][0]
            operand1 = stack[-3][0]
            operand2 = stack[-1][0]
            reduced_expression = f"{operation} {operand1} AN {operand2}"
            if operation == 'BOTH SAEM':
                # If operand1_value is equal to operand2_value, result is 'WIN', otherwise 'FAIL'
                result = 'WIN' if operand1 == operand2 else 'FAIL'
            elif operation == 'DIFFRINT':
                # If operand1_value is not equal to operand2_value, result is 'WIN', otherwise 'FAIL'
                result = 'WIN' if operand1!= operand2 else 'FAIL'
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

    
    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        pass
    else:
        print("ERROR: Invalid comparison expression.")
        local_flag = False

    return local_flag

def relational_operation(relational_operators, comparison_operators, tokens, symbol_table, expression_operators):
    first_part = []
    second_part = []
    found_relational = False
    fPartOperand = None
    variables = []

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
    if first_part:
        fPartOperand = first_part[0][0]

    # Process the second part
    stack = []
    local_flag = True
    index = 0  # Start processing tokens from the first index

    numbr_flag = 0
    numbar_flag = 0

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
                    val_type = identifier_info['value_type']

                    if val_type == 'NUMBR':
                        numbr_flag = 1
                    elif val_type == 'NUMBAR':
                        numbar_flag = 1
                    else:
                        print(f"SEMANTICS ERROR: {val} is not a NUMBR/NUMBAR variable")
                        local_flag = False
                        break
            
            else:
                if token_type == 'NUMBR':
                    val = int(token)
                    numbr_flag = 1
                elif token_type == 'NUMBAR':
                    val = float(token)
                    numbar_flag = 1
                else: 
                    print(f"SEMANTICS ERROR: {val} is not a NUMBR/NUMBAR literal")
                    local_flag = False
                    break

            if numbar_flag == 1 and numbr_flag == 1:
                print(f"SEMANTICS ERROR: Operands should be all NUMBRs or all NUMBARs")
                local_flag = False
                break
            else:
                stack.append((val, "operand", index))  # Add operand to stack
        
        else:
            # Exception(f"ERROR: Invalid token '{token}' in relational processing.")
            print(f"ERROR: Invalid token '{token}' in relational processing.")
            local_flag = False
            break
        
        stack_for_final_check = stack
        if len(stack) >= 4:
            # Look for a valid reduction pattern: operation operand AN operand
            if (stack[-4][1] == "operation" and
                stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):

                # Perform the reduction (operation operand AN operand)
                operation = stack[-4][0]
                operand1 = stack[-3][0]
                token1 = operand1
                operand2 = stack[-1][0]
                token2 = operand2
                reduced_expression = f"{operation} {operand1} AN {operand2}"

                if len(stack[-3]) == 3:  # Check if operand1 has a value (evaluated)
                    operand1_value = stack[-3][2]
                    token1 = operand1
                else:
                    operand1_value = operand1
                    token1 = operand1

                if len(stack[-1]) == 3:  # Check if operand2 has a value (evaluated)
                    operand2_value = stack[-1][2]
                else:
                    operand2_value = operand2

               
                if operation == 'BIGGR OF':
                    # If operand1_value is greater to operand2_value, result is 'WIN', otherwise 'FAIL'
                    result = token1 if operand1_value > operand2_value else token2
                elif operation == 'SMALLR OF':
                    # If operand1_value is less to operand2_value, result is 'WIN', otherwise 'FAIL'
                    result = token1 if operand1_value < operand2_value else token2
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
                stack = stack[:-4] + [(result, "operand", reduced_index)]  # Replace the reduced tokens with the new expression


                # Move the index to the token after the reduced portion
                index = reduced_index[1] + 1
                continue

        # Increment the index to move to the next token
        index += 1

    # After all reductions, check for the final step
    if len(stack_for_final_check) == 4:
        stack = stack_for_final_check
        if (stack[-4][1] == "operation" and
                stack[-3][1] == "operand" and
                stack[-2][1] == "keyword" and
                stack[-1][1] == "operand"):

            # Perform the reduction (operation operand AN operand)
            operation = stack[-4][0]
            operand1 = stack[-3][0]
            token1 = operand1
            operand2 = stack[-1][0]
            token2 = operand2
            reduced_expression = f"{operation} {operand1} AN {operand2}"

            if operation == 'BIGGR OF':
                # If operand1_value is greater to operand2_value, result is 'WIN', otherwise 'FAIL'
                result = token1 if operand1 > operand2 else token2
            elif operation == 'SMALLR OF':
                # If operand1_value is less to operand2_value, result is 'WIN', otherwise 'FAIL'
                result = token1 if operand1 < operand2 else token2
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
            stack = stack[:-4] + [(result, "operand", reduced_index)]  # Replace the reduced tokens with the new expression

            # Move the index to the token after the reduced portion
            index = reduced_index[1] + 1

    # Check if the final stack is valid
    if local_flag and len(stack) == 1 and stack[0][1] == "operand":
        if comparison_operation(comparison_operators, first_part + stack, symbol_table, expression_operators, True) == False:  # Assuming `expression_checker` is the comparison validator
            # Exception("ERROR: Tokens do not form a valid comparison.")
            print("ERROR: Tokens do not form a valid comparison.")
            local_flag = False
        
    else:
        print("ERROR: Invalid relational expression.")
        local_flag = False

    
    return local_flag

def explicit_typecast_checker(tokens):
    syntax_flag = False
    if len(tokens) < 3:
        print( "Error: Incomplete typecasting statement")

    if tokens[0][0] != "MAEK" or tokens[0][1] != "KEYWORD":
        print( "Error: Expected 'MAEK' at the start of typecasting statement")

    # Check the variable identifier
    if tokens[1][1] != "IDENTIFIER":
        return f"semantics Error: Expected variable identifier after 'MAEK', found {tokens[1][0]}"

    token_name = tokens[1][0]
    token_type = tokens[1][1]
    #check if variable is declared
    result = semantics_functions.symbol_exists(token_name)
    if not result:
        raise Exception(f"Semantic Error in line: Variable {token_name} is not declared")
            
    # Case 1: MAEK varident A <data_type>
    if len(tokens) == 4:
        if tokens[2][0] != "A" or tokens[2][1] != "KEYWORD":
            print (f"Error: Expected 'A' keyword for typecasting, found {tokens[2][0]}")
        if not data_type_checker(tokens[3]):
            print( f"Error: Expected data type after 'A', found {tokens[3][0]}")
        data_type = tokens[3]
        syntax_flag =  True

    # Case 2: MAEK varident <data_type>
    elif len(tokens) == 3:
        if not data_type_checker(tokens[2]):
            return( f"Error: Expected data type after variable identifier, found {tokens[2][0]}")
        data_type = tokens[2][0]

        syntax_flag =  True


    if syntax_flag == True:
        to_different_types(data_type[0], 5, token_name, token_type)


        return True

    else:
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

    if len(tokens) < 3:
        return "Error: Incomplete recast statement"

    # Check the variable identifier
    if tokens[0][1] != "IDENTIFIER":
        return f"Error: Expected variable identifier at the start, found {tokens[0][0]}"
    
    #check if variable is declared
    var_declared = semantics_functions.symbol_exists(tokens[0][0])
    if not var_declared:
        raise Exception(f"Semantic Error in line: Variable {tokens[0][0]} is not declared")
    
    token_to_change = tokens[0][0]
    type_of_tok_to_change = tokens[0][1]

    # Case 1: varident IS NOW A <data_type>
    if len(tokens) >= 3 and tokens[1][0] == "IS NOW A" and tokens[1][1] == "KEYWORD":
        
        data_type_to_check = tokens[2] 
        if data_type_checker.data_type_checker(data_type_to_check):

            token_name = tokens[2][0]
            token_type = tokens[2][1]
            #Semantic check 
            explicit_typecast_checker.to_different_types(token_name, token_type, line_num, token_to_change, type_of_tok_to_change)


            return True
        else:
            return f"Error: Expected data type after 'IS NOW A', found {tokens[2][0]}"

    # Case 2: varident R <explicit_typecast>
    elif len(tokens) >= 2 and tokens[1][0] == "R" and tokens[1][1] == "KEYWORD":
        explicit_typecast_tokens = tokens[2:]  # Extract the tokens after 'R'
        line_num = 2
        retain_token_val = semantics_functions.get_symbol(explicit_typecast_tokens[1][0])["value"] 
        retain_token_type = semantics_functions.get_symbol(explicit_typecast_tokens[1][0])["value_type"]
        var_name_in_explicit = explicit_typecast_tokens[1][0]
        var_type_in_explicit = explicit_typecast_tokens[1][1]
        result = explicit_typecast_checker(explicit_typecast_tokens)
        if result == True:

            #Semantics check
            explicit_typecast_checker(explicit_typecast_tokens)
            to_assign = semantics_functions.get_symbol(var_name_in_explicit)["value"]
            to_assign_type = semantics_functions.get_symbol(var_name_in_explicit)["value_type"]
            
            #Assign explicit typecast to variable
            assignment_checker.assignment_semantics(line_num, [[token_to_change,type_of_tok_to_change],['R', "KEYWORD"], [to_assign, to_assign_type]])

            #return the original value and type of the variable in the explicit typecast part
            assignment_checker.assignment_semantics(line_num, [[var_name_in_explicit,var_type_in_explicit],['R', "KEYWORD"], [retain_token_val, retain_token_type]])
            
            explicit_typecast_checker( [["MAEK", "KEYWORD"],[var_name_in_explicit, var_type_in_explicit],["A", "KEYWORD"], [retain_token_type, "KEYWORD"]])
            
            return True
        else:
            return result

    return "Error: Invalid recast statement"

