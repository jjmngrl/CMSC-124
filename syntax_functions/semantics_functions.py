# Symbol Table using functions and a dictionary without a class

# Dictionary to store symbol data
symbols = {}

def get_symbol(symbol_name):
    """Retrieve a specific symbol from the symbol table."""
    if symbol_name in symbols:
        return symbols[symbol_name]
    raise KeyError(f"Symbol '{symbol_name}' does not exist.")

def get_all_symbols():
    """Retrieve all symbols from the symbol table."""
    return symbols

def add_symbol(symbol_name, symbol_info):
    """
    Add a new symbol to the table.
    :param symbol_name: Name of the symbol (key).
    :param symbol_info: A dictionary containing type, value, value_type, and reference_environment.
    """
    if symbol_name in symbols:
        raise KeyError(f"Symbol '{symbol_name}' already exists.")
    symbols[symbol_name] = symbol_info

def symbol_exists(symbol_name):
    """Check if a symbol exists in the table."""
    return symbol_name in symbols

def update_symbol(symbol_name, **updates):
    """
    Update the attributes of an existing symbol.
    :param symbol_name: Name of the symbol to update.
    :param updates: Keyword arguments for the attributes to update (e.g., value='new_value').
    """
    if symbol_name not in symbols:
        raise KeyError(f"Symbol '{symbol_name}' does not exist.")
    symbols[symbol_name].update(updates)


# Example usage
# Initialize the table with the given data
# initial_symbols = {
#     "monde": {"type": "identifier", "value": None, "value_type": "NOOB", "reference_environment": "GLOBAL"},
#     "num": {"type": "identifier", "value": "17", "value_type": "NUMBR", "reference_environment": "GLOBAL"},
#     "name": {"type": "identifier", "value": '"seventeen"', "value_type": "YARN", "reference_environment": "GLOBAL"},
#     "fnum": {"type": "identifier", "value": "17.0", "value_type": "NUMBR", "reference_environment": "GLOBAL"},
#     "flag": {"type": "identifier", "value": "WIN", "value_type": "YARN", "reference_environment": "GLOBAL"},
#     "sum": {"type": "identifier", "value": "SUM OF", "value_type": "KEYWORD", "reference_environment": "GLOBAL"},
#     "diff": {"type": "identifier", "value": "DIFF OF", "value_type": "KEYWORD", "reference_environment": "GLOBAL"},
#     "prod": {"type": "identifier", "value": "PRODUKT OF", "value_type": "KEYWORD", "reference_environment": "GLOBAL"},
#     "quo": {"type": "identifier", "value": "QUOSHUNT OF", "value_type": "KEYWORD", "reference_environment": "GLOBAL"}
# }

# symbols = {
#     "IT": {"type": "identifier", "value": 0, "value_type": "NOOB", "reference_environment": "main"}
# }

symbols = {
    "IT": {"type": "identifier", "value": None, "value_type": "NOOB", "reference_environment": "main"},
}