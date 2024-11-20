"""
Lexical Analyzer for LOLCODE
"""

import re

def read():
    """
    Reads a LOLCODE file and removes comments and empty lines.
    :return: List of cleaned lines from the LOLCODE file.
    """
    file = "01_variables.lol"
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
            r"\bI HAS A\b",
            r"\bITZ\b",
            r"\bIF U SAY SO\b",
            r"\bIM OUTTA YR\b",
            r"\bQUOSHUNT OF\b",
            r"\bPRODUKT OF\b",
            r"\bBOTH SAEM\b",
            r"\bEITHER OF\b",
            r"\bSMALLR OF\b",
            r"\bBIGGR OF\b",
            r"\bDIFFRINT\b",
            r"\bFOUND YR\b",
            r"\bHOW IZ I\b",
            r"\bIM IN YR\b",
            r"\bIS NOW A\b",
            r"\bBOTH OF\b",
            r"\bDIFF OF\b",
            r"\bKTHXBYE\b",
            r"\bVISIBLE\b",
            r"\bALL OF\b",
            r"\bANY OF\b",
            r"\bGIMMEH\b",
            r"\bMOD OF\b",
            r"\bNERFIN\b",
            r"\bNO WAI\b",
            r"\bNUMBAR\b",
            "O RLY\?",
            r"\bOMGWTF\b",
            r"\bSMOOSH\b",
            r"\bSUM OF\b",
            r"\bWON OF\b",
            r"\bYA RLY\b",
            r"\bMEBBE\b",
            r"\bNUMBR\b",
            r"\bTROOF\b",
            r"\bUPPIN\b",
            r"\bWAZZUP\b",
            r"\bBUHBYE\b",
            r"\bGTFO\b",
            r"\bMAEK\b",
            r"\bMKAY\b",
            r"\bNOOB\b",
            r"\bWILE\b",
            "WTF\?",
            r"\bYARN\b",
            r"\bHAI\b",
            r"\bNOT\b",
            r"\bOIC\b",
            r"\bOMG\b",
            r"\bTIL\b",
            r"\bAN\b",
            r"\bYR\b",
            r"\bR\b"
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
        yarn_literal = False  # Tracks if we are inside a YARN literal
        yarn_buffer = ""  # Buffer for multi-token YARNs

        # Check for multi-word keywords first
        for keyword in dict_matching["KEYWORD"]:
            matches = re.findall(keyword, line)
            if matches:
                for match in matches:
                    tokens_with_classifications.append([match, "KEYWORD"])
                    line = line.replace(match, "").strip()  # Remove matched keyword from line

        # Split the remaining line into tokens
        tokens = line.split()
        for token in tokens:
            # Syntax error check for tokens that are all uppercase letters but not keywords
            if re.fullmatch(r"[A-Z]+", token):  # Match one or more uppercase letters
                if token not in dict_matching["KEYWORD"]:  # Check if it's not a valid keyword
                    if not re.fullmatch(dict_matching["TROOF"], token):  # Exclude TROOF literals
                        print(f"Syntax error in Line {line_num}: '{token}' is a typo or not a keyword")
                        return classified_lines  # Stop processing and return the results so far

            # Handle YARN literals
            if token.startswith('"') or yarn_literal:
                # Start or continuation of a YARN literal
                yarn_buffer += f" {token}" if yarn_literal else token
                yarn_literal = not token.endswith('"')  # Flip flag if it ends with a closing quote
                if not yarn_literal:  # Completed YARN literal
                    tokens_with_classifications.append([yarn_buffer.strip(), "YARN"])
                    yarn_buffer = ""
                continue

            # Match token with defined patterns
            matched = False
            for lexeme_type, pattern in dict_matching.items():
                if lexeme_type == "KEYWORD":
                    # Match multi-word keywords (already handled separately)
                    for keyword in pattern:
                        if re.fullmatch(keyword, token):
                            tokens_with_classifications.append([token, "KEYWORD"])
                            matched = True
                            break
                    if matched:
                        break  # Exit if keyword matched
                elif re.fullmatch(pattern, token):  # Match single regex patterns
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
    for line_num, classifications in classified_tokens.items():
        print(f"Line {line_num}: {classifications}")

if __name__ == "__main__":
    main()
