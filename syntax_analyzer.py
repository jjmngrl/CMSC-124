from lexical_analyzer import lex_main
from syntax_functions import program_checker
# from syntax_functions import variable_declaration_checker
# from syntax_functions import variable_section_checker
from syntax_functions import statement_checker
from syntax_functions import validate_expression
from syntax_functions import visible_statement_checker
from syntax_functions import gimmeh_statement_checker

def main():
    print("-"*5,"in syntax analyzer",5*"-")
    # result = []
    classified_tokens = lex_main()
    # print("tokens from lexical: \n",classified_tokens)

    program_indices = program_checker.program_checker(classified_tokens)
    if program_indices:
        #program is valid

        index_of_HAI, index_of_KTHXBYE = program_indices
        #dictionary that does not contain "HAI" and "KBYETHX"
        code_block_in_program = {
            k: classified_tokens[k]
            for k in sorted(classified_tokens.keys())
            if index_of_HAI < k < index_of_KTHXBYE
        }
        # print("code block in program\n",code_block_in_program)
        #Check if a statement is valid:
        if statement_checker.statement_checker(code_block_in_program, classified_tokens):
        #     # result.append(("", "Program is valid."))
            print("\n\n","-"*10,"Program is valid","-"*10)
        else:
            raise SyntaxError(f"Invalid Program")
            # result.append(("", "Invalid program structure or statements."))

        # if gimmeh_statement_checker(code_block_in_program, classified_tokens, result):
        #     result.append(("", "All GIMMEH statements are valid."))
        # else:
        #     result.append(("", "Error/s found in GIMMEH statements."))

        # if visible_statement_checker(code_block_in_program, classified_tokens, result):
        #     result.append(("", "All VISIBLE statements are valid."))
        # else:
        #     result.append(("", "Error/s found in VISIBLE statements."))
    else:
        # result.append(("", "ERROR: The program must start with HAI and end with KTHXBYE."))
        # print("ERROR: The program must start with HAI and end with KTHXBYE.")
        raise SyntaxError ("The program must start with HAI and end with KTHXBYE.")
    # Sort results by line numbers where applicable and print
    # sorted_result = sorted/(result, key=lambda x: int(x[0].split()[1].strip(':')) if "Line" in x[0] else float('inf'))
    
    # Print each element of the tuple on a new line
    # for message in sorted_result:
    #     print(message[0])  # First element of the tuple (e.g., "HAI found")
    #     print(message[1])  # Second element of the tuple (e.g., "Program starts here.")
    #     print()  # Blank line for better readability


main()
