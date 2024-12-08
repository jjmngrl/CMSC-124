import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from lexical_analyzer import keyword_classifier
from lexical_analyzer import lex_main
from semantics import process_file_for_semantics  # Import the new function for semantics
from semantics import output

# Create the main application window
root = tk.Tk()
root.title("LOLCode")
root.geometry("950x650")
root.configure(bg="#f0f0f0")

# Define frame styles
frame_style = {"relief": "groove", "borderwidth": 2}

# Define frames for different sections
frame_code_editor = tk.LabelFrame(root, text="Code Editor", **frame_style, bg="#ffffff")
frame_lexemes = tk.LabelFrame(root, text="Lexemes", **frame_style, bg="#ffffff")
frame_symbol_table = tk.LabelFrame(root, text="Symbol Table", **frame_style, bg="#ffffff")
frame_output = tk.LabelFrame(root, text="Output", **frame_style, bg="#ffffff")
frame_execute = tk.Frame(root, bg="#f0f0f0")  # Use tk.Frame instead of ttk.Frame

# Layout frames
frame_code_editor.place(x=10, y=10, width=420, height=350)
frame_lexemes.place(x=440, y=10, width=250, height=350)
frame_symbol_table.place(x=700, y=10, width=240, height=350)
frame_output.place(x=10, y=370, width=930, height=200)
frame_execute.place(x=10, y=580, width=930, height=50)

# Add table headers for Lexemes
lexeme_tree = ttk.Treeview(frame_lexemes, columns=("Lexeme", "Classification"), show="headings")
lexeme_tree.heading("Lexeme", text="Lexeme")
lexeme_tree.heading("Classification", text="Classification")
lexeme_tree.column("Lexeme", width=100, anchor="center", stretch=tk.YES)
lexeme_tree.column("Classification", width=120, anchor="center", stretch=tk.YES)
lexeme_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Add table headers for Symbol Table
symbol_tree = ttk.Treeview(frame_symbol_table, columns=("Identifier", "Value"), show="headings")
symbol_tree.heading("Identifier", text="Identifier")
symbol_tree.heading("Value", text="Value")
symbol_tree.column("Identifier", width=100, anchor="center", stretch=tk.YES)
symbol_tree.column("Value", width=100, anchor="center", stretch=tk.YES)
symbol_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Add a text box for the Code Editor
code_editor = tk.Text(frame_code_editor, wrap="word", font=("Courier", 12))
code_editor.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Add a text box for the Output
output_text = tk.Text(frame_output, wrap="word", font=("Courier", 12))
output_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Add the Execute button
execute_button = ttk.Button(frame_execute, text="EXECUTE", width=20, command=lambda: execute_lexical_analysis())
execute_button.pack(pady=10)

# Improve font and alignment
ttk.Style().configure("TLabel", font=("Arial", 10))

# Declare the file_name_var for displaying selected file path
file_name_var = tk.StringVar()

# Add a label to show the selected file path
file_name_label = tk.Label(root, textvariable=file_name_var, anchor="w", font=("Arial", 10), bg="#f0f0f0")
file_name_label.place(x=700, y=0, width=240, height=20)

# Function to save the code from the Code Editor to a file
def save_code_to_file():
    code = code_editor.get("1.0", tk.END).strip()  # Get the code from the editor
    file_path = "test.lol"  # Save to test.lol
    with open(file_path, 'w') as f:
        f.write(code)  # Write the content to the file

# Function to read the file
def read(file_path):
    with open(file_path, 'r') as f:
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

# Function to perform lexical analysis
def lexical(file_path):
    lines = read(file_path)
    return keyword_classifier(lines)

# Function to choose a file (to load for analysis)
def choose_file():
    file_path = filedialog.askopenfilename(title="Select a LOLCode file", filetypes=[("LOLCode files", "*.lol")])
    if file_path:
        file_name_var.set(file_path)  # Update the file path label
        load_file_into_editor(file_path)

# Function to load file contents into the code editor
def load_file_into_editor(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
        code_editor.delete(1.0, tk.END)  # Clear the editor
        code_editor.insert(tk.END, code)  # Insert the file content

# Function to execute lexical analysis and semantics
# Function to execute lexical analysis and semantics
# Update the output display in the execute_lexical_analysis function
def execute_lexical_analysis():
    save_code_to_file()  # Save the code from the editor into a file

    file_path = "test.lol"  # Use the saved test.lol file as input
    if not file_path:
        output_text.insert(tk.END, "No file selected.\n")
        return
    
    try:
        # Call the new function in semantics.py with the file path to get the symbol table
        symbol_table = process_file_for_semantics(file_path)  # Get the symbol table after semantic checks
        
        # Clear and populate the Symbol Table Treeview with the updated symbol table
        for row in symbol_tree.get_children():
            symbol_tree.delete(row)

        # Insert identifiers and values into the Symbol Table Treeview
        for identifier, value in symbol_table.items():
            symbol_tree.insert("", "end", values=(identifier, value))

    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}\n")
        return
    
    # Clear the Lexemes table
    for row in lexeme_tree.get_children():
        lexeme_tree.delete(row)

    # Populate Lexemes table with classified tokens (already available from `lexical` function)
    try:
        classified_tokens = lexical(file_path)  # Perform lexical analysis with the file path
    except Exception as e:
        output_text.insert(tk.END, f"Error during lexical analysis: {e}\n")
        return

    for line_num, classifications in sorted(classified_tokens.items()):
        for token, classification in classifications:
            lexeme_tree.insert("", "end", values=(token, classification))  # Insert token and classification
    
    # Clear the output text widget
    output_text.delete(1.0, tk.END)
    
    # Update output with the semantic analysis result (output from semantics)
    try:
        # Assuming output is a dictionary and we need to format it for display
        print(output)  # Check the structure of the output
        for line_num, classifications in output.items():
            # Ensure we unpack correctly: check if classifications is a list of tuples or something else
            if isinstance(classifications, list):
                for item in classifications:
                    if isinstance(item, tuple) and len(item) == 2:
                        token, classification = item
                        formatted_classifications = f"[{repr(token)}, {repr(classification)}]"
                        output_text.insert(tk.END, f"Line {line_num}: {formatted_classifications}\n")
                    else:
                        output_text.insert(tk.END, f" {item}\n")
            else:
                output_text.insert(tk.END, f"Error: Expected a list, got {type(classifications)}\n")
    except Exception as e:
        output_text.insert(tk.END, f"Error displaying output: {e}\n")




# Add horizontal scrollbar to Lexemes table
horizontal_scrollbar_lexemes = ttk.Scrollbar(frame_lexemes, orient="horizontal", command=lexeme_tree.xview)
lexeme_tree.configure(xscrollcommand=horizontal_scrollbar_lexemes.set)
horizontal_scrollbar_lexemes.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

# Add vertical scrollbar to Lexemes table
vertical_scrollbar_lexemes = ttk.Scrollbar(frame_lexemes, orient="vertical", command=lexeme_tree.yview)
lexeme_tree.configure(yscrollcommand=vertical_scrollbar_lexemes.set)
vertical_scrollbar_lexemes.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

# Add horizontal scrollbar to Symbol Table
horizontal_scrollbar_symbol = ttk.Scrollbar(frame_symbol_table, orient="horizontal", command=symbol_tree.xview)
symbol_tree.configure(xscrollcommand=horizontal_scrollbar_symbol.set)
horizontal_scrollbar_symbol.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

# Add vertical scrollbar to Symbol Table
vertical_scrollbar_symbol = ttk.Scrollbar(frame_symbol_table, orient="vertical", command=symbol_tree.yview)
symbol_tree.configure(yscrollcommand=vertical_scrollbar_symbol.set)
vertical_scrollbar_symbol.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

# Ensure frames expand with window resizing
frame_code_editor.grid_rowconfigure(0, weight=1)
frame_code_editor.grid_columnconfigure(0, weight=1)

frame_lexemes.grid_rowconfigure(0, weight=1)
frame_lexemes.grid_columnconfigure(0, weight=1)

frame_symbol_table.grid_rowconfigure(0, weight=1)
frame_symbol_table.grid_columnconfigure(0, weight=1)

frame_output.grid_rowconfigure(0, weight=1)
frame_output.grid_columnconfigure(0, weight=1)

frame_execute.grid_rowconfigure(0, weight=1)
frame_execute.grid_columnconfigure(0, weight=1)

# Add a button to choose a file
choose_file_button = ttk.Button(root, text="Choose File", command=choose_file)
choose_file_button.place(x=700, y=30, width=240, height=30)

# Main loop to run the GUI
root.mainloop()
