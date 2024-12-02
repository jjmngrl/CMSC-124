"""
-----------------------------------------------------------------------------------------
THIS IS A PYTHON IMPLEMENTATION OF A LEXICAL ANALYZER FOR LOLCODE.
-----------------------------------------------------------------------------------------
"""

import re

"""
-----------------------------------------------------------------------------------------
Reads a LOLCODE file and removes comments and empty lines.
@return: 
    List of cleaned lines from the LOLCODE file.
-----------------------------------------------------------------------------------------
"""

def read():
    file = r"test case/03_arith.lol"
    if file.endswith(".lol"):
        with open(file, 'r') as f:
            lines = f.readlines()
            data = []
            in_multiline_comment = False
            for line in lines:
                line = line.strip()
                
                # Handle multi-line comments
                if line.startswith("OBTW"):
                    in_multiline_comment = True
                    data.append("")
                    continue
                elif line.startswith("TLDR"):
                    data.append("")
                    in_multiline_comment = False
                    continue
                if in_multiline_comment:
                    data.append("")
                    continue
                
                # Handle single-line comments
                if "BTW" in line:
                    line = line.split("BTW")[0].strip()
                                 
                # Add non-empty lines to data
                data.append(line)  # Keep empty lines to track them
            return data

"""
-----------------------------------------------------------------------------------------
Classifies tokens in LOLCODE lines into various types.
@param: 
    List of cleaned LOLCODE lines.
@return: 
    Dictionary where keys are line numbers and values are lists of token classifications.
-----------------------------------------------------------------------------------------
"""
def classifier(lines):
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
            r"I IZ",
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
            r"IT",
            r"R",
            r"A"
        ],
        # Literals
        "NUMBR": r"^-?\d+$",
        "NUMBAR": r"^-?\d+\.\d+$",
        "YARN": r"^\".*\"$",  # Matches complete YARN (strings enclosed in quotes)
        "TROOF": r"\b(WIN|FAIL)\b",
        # Identifiers
        "IDENTIFIER": r"^[a-z][a-z0-9_]*$",
    }

    classified_lines = {}

    for line_num, line in enumerate(lines, start=1):
        tokens_with_classifications = []
        tokens = line.split()  # Split the line into tokens

        index = 0
        while index < len(tokens):
            token = tokens[index]
            matched = False

            # Handle YARN literals
            if token.startswith('"'):
                yarn_buffer = token
                while not token.endswith('"') and index + 1 < len(tokens):
                    index += 1
                    token = tokens[index]
                    yarn_buffer += f" {token}"
                tokens_with_classifications.append([yarn_buffer.strip(), "YARN"])
                index += 1
                continue

            # Match multi-word keywords first
            for keyword in dict_matching["KEYWORD"]:
                keyword_parts = keyword.split()
                if tokens[index:index + len(keyword_parts)] == keyword_parts:
                    tokens_with_classifications.append([" ".join(keyword_parts), "KEYWORD"])
                    index += len(keyword_parts)
                    matched = True
                    break

            if matched:
                continue

            # Match single-word patterns
            for lexeme_type, pattern in dict_matching.items():
                if lexeme_type == "KEYWORD":
                    continue  # Skip multi-word keywords; already handled
                if re.fullmatch(pattern, token):
                    tokens_with_classifications.append([token, lexeme_type])
                    matched = True
                    break

            # If no match, classify as TROOF, IDENTIFIER, or UNCLASSIFIED
            if not matched:
                if re.fullmatch(dict_matching["TROOF"], token):
                    tokens_with_classifications.append([token, "TROOF"])
                elif re.fullmatch(dict_matching["IDENTIFIER"], token):
                    tokens_with_classifications.append([token, "IDENTIFIER"])
                else:
                    tokens_with_classifications.append([token, "UNCLASSIFIED"])

            index += 1

        classified_lines[line_num] = tokens_with_classifications

    return classified_lines


"""
-----------------------------------------------------------------------------------------
Main function to execute the lexical analyzer.
-----------------------------------------------------------------------------------------
"""
def lex_main():
    text = read()
    classified_tokens = classifier(text)
    
    # Print the classified tokens dictionary
    for line_num, classifications in sorted(classified_tokens.items()):
        formatted_classifications = ', '.join(
            [f"[{repr(token)}, {repr(classification)}]" for token, classification in classifications]
        )
        # print(f"Line {line_num}: {formatted_classifications}") 
        
    return classified_tokens

lex_main()