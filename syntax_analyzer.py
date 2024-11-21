from lexical_analyzer import *
from syntax_functions.program_checker import program_checker
from syntax_functions.variable_declaration_checker import variable_declaration_checker
from syntax_functions.variable_section_checker import variable_section_checker
from syntax_functions.statement_checker import statement_checker
from syntax_functions.validate_expression import validate_expression
from syntax_functions.visible_statement_checker import visible_statement_checker
from syntax_functions.gimmeh_statement_checker import gimmeh_statement_checker

def main():
    result = []
    # classified_tokens = classifier(text)
    classified_tokens = {
    1: [["HAI", "KEYWORD"]],  # Program start
    2: [["WAZZUP", "KEYWORD"]],  # Start of variable section
    3: [["I HAS A", "KEYWORD"], ["x", "IDENTIFIER"]],  # Variable declaration (NOOB by default)
    4: [["I HAS A", "KEYWORD"], ["y", "IDENTIFIER"]],  # Variable declaration (NOOB by default)
    5: [["BUHBYE", "KEYWORD"]],  # End of variable section
    6: [["VISIBLE", "KEYWORD"], ['"Value 1: "', "YARN"]],  # Print literal
    7: [["GIMMEH", "KEYWORD"], ["x", "IDENTIFIER"]],  # Input for x
    8: [["VISIBLE", "KEYWORD"], ['"Value 2: "', "YARN"]],  # Print literal
    9: [["GIMMEH", "KEYWORD"], ["y", "IDENTIFIER"]],  # Input for y
    10: [],  # Comment converted to an empty list (x == y)
    11: [["VISIBLE", "KEYWORD"], ["BOTH SAEM", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # Comparison (x == y)
    12: [],  # Comment converted to an empty list (x != y)
    13: [["VISIBLE", "KEYWORD"], ["DIFFRINT", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # Comparison (x != y)
    14: [["OBTW", "COMMENT"]],  # Multiline comment start
    15: [["x >= y", "YARN"]],  # Multiline comment content
    16: [["x <= y", "YARN"]],  # Multiline comment content
    17: [["x < y", "YARN"]],  # Multiline comment content
    18: [["x > y", "YARN"]],  # Multiline comment content
    19: [["TLDR", "COMMENT"]],  # Multiline comment end
    20: [["VISIBLE", "KEYWORD"], ["BOTH SAEM", "KEYWORD"], ["BIGGR OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["x", "IDENTIFIER"]],  # BOTH SAEM BIGGR OF x AN y AN x
    21: [["VISIBLE", "KEYWORD"], ["BOTH SAEM", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["SMALLR OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # BOTH SAEM x AN SMALLR OF x AN y
    22: [["VISIBLE", "KEYWORD"], ["DIFFRINT", "KEYWORD"], ["BIGGR OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"], ["AN", "KEYWORD"], ["x", "IDENTIFIER"]],  # DIFFRINT BIGGR OF x AN y AN x
    23: [["VISIBLE", "KEYWORD"], ["DIFFRINT", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["SMALLR OF", "KEYWORD"], ["x", "IDENTIFIER"], ["AN", "KEYWORD"], ["y", "IDENTIFIER"]],  # DIFFRINT x AN SMALLR OF x AN y
    24: [["KTHXBYE", "KEYWORD"]]  # Program end
}

    program_indices = program_checker(classified_tokens, result)
    if program_indices:
        index_of_HAI, index_of_KTHXBYE = program_indices
        code_block_in_program = {
            k: classified_tokens[k]
            for k in sorted(classified_tokens.keys())
            if index_of_HAI < k < index_of_KTHXBYE
        }
        if statement_checker(code_block_in_program, classified_tokens, result):
            result.append(("", "Program is valid."))
        else:
            result.append(("", "Invalid program structure or statements."))

        if gimmeh_statement_checker(code_block_in_program, classified_tokens, result):
            result.append(("", "All GIMMEH statements are valid."))
        else:
            result.append(("", "Error/s found in GIMMEH statements."))

        if visible_statement_checker(code_block_in_program, classified_tokens, result):
            result.append(("", "All VISIBLE statements are valid."))
        else:
            result.append(("", "Error/s found in VISIBLE statements."))
    else:
        result.append(("", "ERROR: The program must start with HAI and end with KTHXBYE."))

    # Sort results by line numbers where applicable and print
    sorted_result = sorted(result, key=lambda x: int(x[0].split()[1].strip(':')) if "Line" in x[0] else float('inf'))
    
    # Print each element of the tuple on a new line
    for message in sorted_result:
        print(message[0])  # First element of the tuple
        print(message[1])  # Second element of the tuple
        print()  # Blank line for better readability

main()
