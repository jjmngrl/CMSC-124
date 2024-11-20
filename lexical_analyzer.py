"""
Lexical Analyzer for LOLCODE
"""

import re

def read():
    """
    Reads a LOLCODE file and removes comments and empty lines.
    :return: List of cleaned lines from the LOLCODE file.
    """
    file = r"test code/01_variables.lol"
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
                    continue
                elif line.startswith("TLDR"):
                    in_multiline_comment = False
                    continue
                if in_multiline_comment:
                    continue
                
                # Handle single-line comments
                if "BTW" in line:
                    line = line.split("BTW")[0].strip()
                
                # Add non-empty lines to data
                data.append(line)  # Keep empty lines to track them
            return data


def classifier(lines):
    """
    Classifies tokens in LOLCODE lines into various types.
    :param lines: List of cleaned LOLCODE lines.
    :return: Dictionary where keys are line numbers and values are lists of token classifications.
    """
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
            "O RLY\?",
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
            "WTF\?",
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

    classified_lines = {}

    for line_num, line in enumerate(lines, start=1):
        tokens_with_classifications = []
        tokens = line.split()  # Split the line into tokens in order

        for token in tokens:
            # Match token with defined patterns
            matched = False
            for lexeme_type, pattern in dict_matching.items():
                if lexeme_type == "KEYWORD":
                    # Match multi-word keywords
                    for keyword in pattern:
                        if re.fullmatch(keyword, token):
                            tokens_with_classifications.append([token, "KEYWORD"])
                            matched = True
                            break
                elif re.fullmatch(pattern, token):
                    tokens_with_classifications.append([token, lexeme_type])
                    matched = True
                    break

            # If token is not matched, classify as TROOF or IDENTIFIER or UNCLASSIFIED
            if not matched:
                if re.fullmatch(dict_matching["TROOF"], token):
                    tokens_with_classifications.append([token, "TROOF"])
                elif re.fullmatch(dict_matching["IDENTIFIER"], token):
                    tokens_with_classifications.append([token, "IDENTIFIER"])
                else:
                    tokens_with_classifications.append([token, "UNCLASSIFIED"])

        classified_lines[line_num] = tokens_with_classifications

    return classified_lines


def main():
    """
    Main function to execute the lexical analyzer.
    """
    text = read()
    classified_tokens = classifier(text)
    # print(classified_tokens)
    # Print the classified tokens dictionary
    for line_num, classifications in sorted(classified_tokens.items()):
        formatted_classifications = ', '.join(
            [f"[{repr(token)}, {repr(classification)}]" for token, classification in classifications]
        )
        print(f"Line {line_num}: {formatted_classifications}")

if __name__ == "__main__":
    main()
