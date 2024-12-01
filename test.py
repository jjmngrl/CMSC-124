# Global variables
declared_variables = []  # List to store declared variables
errors = []  # List to store errors
in_wazzup = False  # Flag to track if inside WAZZUP block

# List of LOLCODE reserved keywords (these should not be treated as variables)
dict_matching = {
        # Keywords
        "KEYWORD": [
            r"I HAS A",
            r"ITZ",
            r"IF U SAY SO",
            r"IM OUTTA YR",
            r"QUOSHUNT OF",
            r"PRODUKT OF",
            r"BOTH SAEM",
            r"EITHER OF",
            r"SMALLR OF",
            r"BIGGR OF",
            r"DIFFRINT",
            r"FOUND YR",
            r"HOW IZ I",
            r"IM IN YR",
            r"IS NOW A",
            r"BOTH OF",
            r"DIFF OF",
            r"KTHXBYE",
            r"VISIBLE",
            r"ALL OF",
            r"ANY OF",
            r"GIMMEH",
            r"MOD OF",
            r"NERFIN",
            r"NO WAI",
            r"NUMBAR",
            "O RLY?",
            r"OMGWTF",
            r"SMOOSH",
            r"SUM OF",
            r"WON OF",
            r"YA RLY",
            r"MEBBE",
            r"NUMBR",
            r"TROOF",
            r"UPPIN",
            r"WAZZUP",
            r"BUHBYE",
            r"GTFO",
            r"MAEK",
            r"MKAY",
            r"NOOB",
            r"WILE",
            "WTF?",
            r"YARN",
            r"HAI",
            r"NOT",
            r"OIC",
            r"OMG",
            r"TIL",
            r"AN",
            r"YR",
            r"R"
        ],
        # Literals
        "NUMBR": r"^-?\d+$",
        "NUMBAR": r"^-?\d+\.\d+$",
        "YARN": r"^\".*\"$",  # Matches complete YARN (strings enclosed in quotes)
        "TROOF": r"\b(WIN|FAIL)\b",
        # Identifiers
        "IDENTIFIER": r"^[a-z][a-z0-9_]*$",
    }

yarn = r'\".*\"'

def variable_checker(test_case):
    global declared_variables, errors, in_wazzup
    for line_number, tokens in enumerate(test_case):
        first_token = tokens[0]
        
        # Start of WAZZUP block
        if first_token == 'WAZZUP':
            in_wazzup = True
            continue

        # Variable declaration (I HAS A)
        if first_token == 'I HAS A':
            in_wazzup = True
            continue

        # ITZ statement (assigns value, but doesn't affect variable tracking)
        if first_token == 'ITZ':
            in_wazzup = True
            continue

        # End of WAZZUP block
        if first_token == 'BUHBYE':
            in_wazzup = False
            continue
        
        # Inside the WAZZUP block, append declared variables
        if in_wazzup:
            declared_variables.append(tokens[0])

        # Check if variable is used before being declared
        if first_token not in dict_matching and first_token not in declared_variables:
            errors.append(f"Error: Variable '{first_token}' used before declaration.")

def visible_checker(test_case):
    global declared_variables, errors
    visible_checker = False
    for tokens in test_case:
        first_token = tokens[0]
        
        if first_token == 'VISIBLE':
            visible_checker = True
            continue

        if first_token not in dict_matching and first_token not in declared_variables:
            continue



            # for token in tokens[0:]:
            #     if token not in reserved_keywords and token not in declared_variables:
            #         errors.append(f"Error: Variable '{token}' used in VISIBLE before declaration.")

def main(test_case):
    global declared_variables, errors
    declared_variables.clear()  # Reset declared variables list
    errors.clear()  # Clear errors from previous runs

    # Run the checkers
    variable_checker(test_case)
    visible_checker(test_case)

    # Output the errors
    if not errors:
        print("No semantic errors found.")
    else:
        for error in errors:
            print(error)

# Example test case
test_case = [
    ['HAI', 'KEYWORD'],
    ['WAZZUP', 'KEYWORD'],
    ['I HAS A', 'KEYWORD'], ['monde', 'IDENTIFIER'],
    ['I HAS A', 'KEYWORD'], ['num', 'IDENTIFIER'], ['ITZ', 'KEYWORD'], ['17', 'NUMBR'],
    ['I HAS A', 'KEYWORD'], ['name', 'IDENTIFIER'], ['ITZ', 'KEYWORD'], ['"seventeen"', 'YARN'],
    ['I HAS A', 'KEYWORD'], ['fnum', 'IDENTIFIER'], ['ITZ', 'KEYWORD'], ['17.0', 'NUMBR'],
    ['I HAS A', 'KEYWORD'], ['flag', 'IDENTIFIER'], ['ITZ', 'KEYWORD'], ['WIN', 'YARN'],
    
    ['I HAS A', 'KEYWORD'], ['sum', 'IDENTIFIER'], ['ITZ', 'KEYWORD'], ['SUM OF', 'KEYWORD'], ['num', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['13', 'NUMBR'],
    ['I HAS A', 'KEYWORD'], ['diff', 'IDENTIFIER'], ['ITZ', 'KEYWORD'], ['DIFF OF', 'KEYWORD'], ['sum', 'IDENTIFIER'], ['AN', 'KEYWORD'], ['17', 'NUMBR'],
    ['I HAS A', 'KEYWORD'], ['prod', 'IDENTIFIER'], ['ITZ', 'KEYWORD'], ['PRODUKT OF', 'KEYWORD'], ['3', 'NUMBR'], ['AN', 'KEYWORD'], ['4', 'NUMBR'],
    ['I HAS A', 'KEYWORD'], ['quo', 'IDENTIFIER'], ['ITZ', 'KEYWORD'], ['QUOSHUNT OF', 'KEYWORD'], ['4', 'NUMBR'], ['AN', 'KEYWORD'], ['5', 'NUMBR'],
    
    ['BUHBYE', 'KEYWORD'],
    
    ['VISIBLE', 'KEYWORD'], ['"declarations"', 'YARN'],
    ['VISIBLE', 'KEYWORD'], ['monde', 'IDENTIFIER'],
    ['VISIBLE', 'KEYWORD'], ['num', 'IDENTIFIER'],
    ['VISIBLE', 'KEYWORD'], ['name', 'IDENTIFIER'],
    ['VISIBLE', 'KEYWORD'], ['fnum', 'IDENTIFIER'],
    ['VISIBLE', 'KEYWORD'], ['flag', 'IDENTIFIER'],
    
    ['VISIBLE', 'KEYWORD'], ['sum', 'IDENTIFIER'],
    ['VISIBLE', 'KEYWORD'], ['diff', 'IDENTIFIER'],
    ['VISIBLE', 'KEYWORD'], ['prod', 'IDENTIFIER'],
    ['VISIBLE', 'KEYWORD'], ['quo', 'IDENTIFIER'],
    
    ['VISIBLE', 'KEYWORD'], ['SUM OF', 'KEYWORD'], ['PRODUKT OF', 'KEYWORD'], ['3', 'NUMBR'], ['AN', 'KEYWORD'], ['5', 'NUMBR'], ['AN', 'KEYWORD'], ['BIGGR OF', 'KEYWORD'], ['DIFF OF', 'KEYWORD'], ['17', 'NUMBR'], ['AN', 'KEYWORD'], ['2', 'NUMBR'], ['AN', 'KEYWORD'], ['5', 'NUMBR'],
    ['VISIBLE', 'KEYWORD'], ['BIGGR OF', 'KEYWORD'], ['PRODUKT OF', 'KEYWORD'], ['11', 'NUMBR'], ['AN', 'KEYWORD'], ['2', 'NUMBR'], ['AN', 'KEYWORD'], ['QUOSHUNT OF', 'KEYWORD'], ['SUM OF', 'KEYWORD'], ['3', 'NUMBR'], ['AN', 'KEYWORD'], ['5', 'NUMBR'], ['AN', 'KEYWORD'], ['2', 'NUMBR'],
    
    ['KTHXBYE', 'KEYWORD']
]

# Run the main function with the provided test case
main(test_case)
# print(declared_variables)
