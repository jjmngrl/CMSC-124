
# gui.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from lexical_analyzer import keyword_classifier
from lexical_analyzer import lex_main
import re

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
lexeme_tree.column("Lexeme", width=100, anchor="center")
lexeme_tree.column("Classification", width=120, anchor="center")
lexeme_tree.pack(expand=True, fill="both", padx=5, pady=5)

# Add table headers for Symbol Table
symbol_tree = ttk.Treeview(frame_symbol_table, columns=("Identifier", "Value"), show="headings")
symbol_tree.heading("Identifier", text="Identifier")
symbol_tree.heading("Value", text="Value")
symbol_tree.column("Identifier", width=100, anchor="center")
symbol_tree.column("Value", width=100, anchor="center")
symbol_tree.pack(expand=True, fill="both", padx=5, pady=5)

# Add a text box for the Code Editor
code_editor = tk.Text(frame_code_editor, wrap="word", font=("Courier", 12))
code_editor.pack(expand=True, fill="both", padx=5, pady=5)

# Add a text box for the Output
output_text = tk.Text(frame_output, wrap="word", font=("Courier", 12))
output_text.pack(expand=True, fill="both", padx=5, pady=5)

# Add the Execute button
execute_button = ttk.Button(frame_execute, text="EXECUTE", width=20, command=lambda: execute_lexical_analysis())
execute_button.pack(pady=10)

# Improve font and alignment
ttk.Style().configure("TLabel", font=("Arial", 10))

# File chooser function
def choose_file():
    file_path = filedialog.askopenfilename(title="Select a LOLCode file", filetypes=[("LOLCode files", "*.lol")])
    if file_path:
        file_name_var.set(file_path)  # Update file name label

# Add a label to show the selected file
file_name_var = tk.StringVar()
file_name_label = tk.Label(root, textvariable=file_name_var, anchor="w", font=("Arial", 10), bg="#f0f0f0")
file_name_label.place(x=700, y=0, width=240, height=20)

# Add the File menu with a button to choose file
file_menu_button = ttk.Button(root, text="Choose File", command=choose_file)
file_menu_button.place(x=820, y=0, width=100, height=20)

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

def lexical(file_path):
    lines = read(file_path)
    return keyword_classifier(lines)

def execute_lexical_analysis():
    """Runs the lexical analysis and updates the output."""
    file_path = file_name_var.get()
    if not file_path:
        output_text.insert(tk.END, "No file selected.\n")
        return
    
    try:
        classified_tokens = lexical(file_path)  # Get the classified tokens
    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}\n")
        return
    
    # Clear the Lexemes table
    for row in lexeme_tree.get_children():
        lexeme_tree.delete(row)
    
    # Populate Lexemes table with classified tokens
    for line_num, classifications in sorted(classified_tokens.items()):
        for token, classification in classifications:
            lexeme_tree.insert("", "end", values=(token, classification))  # Insert token and classification
    
    # Clear the output text widget
    output_text.delete(1.0, tk.END)
    
    # Update output with the lexical analysis result
    for line_num, classifications in sorted(classified_tokens.items()):
        formatted_classifications = ', '.join(
            [f"[{repr(token)}, {repr(classification)}]" for token, classification in classifications]
        )
        output_text.insert(tk.END, f"Line {line_num}: {formatted_classifications}\n")

# Ensure you have this at the end of the script
root.mainloop()