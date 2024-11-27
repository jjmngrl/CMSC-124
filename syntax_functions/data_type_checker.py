
"""
Function to check if type of keyword is valid
Parameter:
Return Value:
    -> True - valid data type
    -> False - invalid data type
"""
def data_type_checker(token):
    """
    Validate data type declarations in LOLCODE.

    :param tokens: List of tokens (e.g., [("NUMBAR", "DATATYPE"), ("x", "IDENTIFIER")]).
    :return: True if all data types are valid, otherwise an error message.
    """
    # print("\ninside data_type checker")
    valid_data_types = {"NUMBAR", "YARN", "NMBR", "TROOF", "NOOB"}

    if token[0] in valid_data_types:
        return True
    else:
        return False

    


