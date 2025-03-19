import ast
import sys
import astpretty  # Install using: pip install astpretty
import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk
import time
import tokenize
import io
from token import tok_name

class SyntaxCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Syntax Checker")
        self.root.geometry("800x600")

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Top frame for file selection
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(top_frame, text="Python File:").pack(side=tk.LEFT, padx=(0, 10))
        self.file_entry = tk.Entry(top_frame, width=50)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        browse_btn = tk.Button(top_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT, padx=(0, 10))

        check_btn = tk.Button(top_frame, text="Check Syntax", command=self.check_syntax)
        check_btn.pack(side=tk.LEFT)

        # Main content area with notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Code tab
        code_frame = tk.Frame(self.notebook)
        self.notebook.add(code_frame, text="Code")

        self.code_text = scrolledtext.ScrolledText(code_frame, wrap=tk.WORD, font=("Courier New", 10))
        self.code_text.pack(fill=tk.BOTH, expand=True)

        # Results tab
        results_frame = tk.Frame(self.notebook)
        self.notebook.add(results_frame, text="Results")

        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, font=("Courier New", 10))
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Tokens tab
        tokens_frame = tk.Frame(self.notebook)
        self.notebook.add(tokens_frame, text="Tokens")

        self.tokens_text = scrolledtext.ScrolledText(tokens_frame, wrap=tk.WORD, font=("Courier New", 10))
        self.tokens_text.pack(fill=tk.BOTH, expand=True)

        # AST tab
        ast_frame = tk.Frame(self.notebook)
        self.notebook.add(ast_frame, text="AST")

        self.ast_text = scrolledtext.ScrolledText(ast_frame, wrap=tk.WORD, font=("Courier New", 10))
        self.ast_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.load_file(file_path)

    def load_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(tk.END, code)
            self.status_var.set(f"Loaded: {file_path}")
        except Exception as e:
            self.status_var.set(f"Error loading file: {str(e)}")

    def tokenize_code(self, code):
        """Tokenize the given code and return a list of tokens."""
        tokens = []
        try:
            # Convert string to bytes for tokenize
            code_bytes = io.BytesIO(code.encode('utf-8'))

            # Tokenize the code
            for tok in tokenize.tokenize(code_bytes.readline):
                token_type = tok_name[tok.type]
                token_string = tok.string
                start_line, start_col = tok.start
                end_line, end_col = tok.end
                line = tok.line

                tokens.append({
                    'type': token_type,
                    'string': token_string,
                    'start': (start_line, start_col),
                    'end': (end_line, end_col),
                    'line': line
                })

        except Exception as e:
            tokens.append({'error': str(e)})

        return tokens

    def check_syntax(self):
        file_path = self.file_entry.get()
        if not file_path:
            self.status_var.set("Please select a Python file first")
            return

        self.results_text.delete(1.0, tk.END)
        self.tokens_text.delete(1.0, tk.END)
        self.ast_text.delete(1.0, tk.END)

        # Reset progress bar
        self.progress["value"] = 0
        self.root.update()

        try:
            # Update status
            self.status_var.set("Reading file...")
            self.progress["value"] = 10
            self.root.update()
            time.sleep(0.3)  # Simulate processing time

            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            # Update status for tokenization
            self.status_var.set("Tokenizing code...")
            self.progress["value"] = 30
            self.root.update()
            time.sleep(0.3)  # Simulate processing time

            # Tokenize the code
            tokens = self.tokenize_code(code)

            # Display tokens
            self.tokens_text.insert(tk.END, "TOKENS:\n")
            self.tokens_text.insert(tk.END, "=" * 80 + "\n\n")

            for token in tokens:
                if 'error' in token:
                    self.tokens_text.insert(tk.END, f"Error during tokenization: {token['error']}\n")
                    continue

                token_info = (
                    f"Type: {token['type']}\n"
                    f"String: {repr(token['string'])}\n"
                    f"Location: Line {token['start'][0]}, Column {token['start'][1]} to "
                    f"Line {token['end'][0]}, Column {token['end'][1]}\n"
                    f"Line: {repr(token['line'])}\n"
                    f"{'-' * 40}\n"
                )
                self.tokens_text.insert(tk.END, token_info)

            # Update status
            self.status_var.set("Parsing code...")
            self.progress["value"] = 50
            self.root.update()
            time.sleep(0.3)  # Simulate processing time

            # Parse the code
            tree = ast.parse(code)

            # Update status
            self.status_var.set("Generating AST visualization...")
            self.progress["value"] = 70
            self.root.update()
            time.sleep(0.3)  # Simulate processing time

            # Display success message
            self.results_text.insert(tk.END, f"✅ No syntax errors found in '{file_path}'.\n\n")
            self.results_text.insert(tk.END, "🔍 Tokenization completed successfully. See the Tokens tab.\n\n")
            self.results_text.insert(tk.END, "🔍 Abstract Syntax Tree (AST) visualization has been generated in the AST tab.\n")

            # Update status
            self.status_var.set("Formatting AST...")
            self.progress["value"] = 90
            self.root.update()
            time.sleep(0.3)  # Simulate processing time

            # Capture AST pretty print output
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                astpretty.pprint(tree)

            ast_output = f.getvalue()

            # Display AST
            self.ast_text.insert(tk.END, ast_output)

            # Switch to tokens tab to show the tokenization results
            self.notebook.select(2)  # Index 2 is the Tokens tab

            # Complete progress
            self.progress["value"] = 100
            self.status_var.set("Syntax check completed successfully")

        except SyntaxError as e:
            self.progress["value"] = 100
            self.status_var.set("Syntax error found")

            self.results_text.insert(tk.END, f"❌ Syntax Error in '{file_path}':\n")
            self.results_text.insert(tk.END, f"   {e.msg}\n")
            self.results_text.insert(tk.END, f"   Line {e.lineno}, Column {e.offset}\n")
            self.results_text.insert(tk.END, f"   {e.text.strip() if e.text else ''}\n")

            # Highlight the error in the code tab
            self.notebook.select(0)
            if e.lineno and e.text:
                try:
                    # Calculate position for highlighting
                    line_start = f"{e.lineno}.0"
                    line_end = f"{e.lineno}.end"

                    self.code_text.tag_configure("error", background="pink", foreground="red")
                    self.code_text.tag_add("error", line_start, line_end)
                    self.code_text.see(line_start)
                except:
                    pass

        except Exception as e:
            self.progress["value"] = 100
            self.status_var.set(f"Error: {str(e)}")
            self.results_text.insert(tk.END, f"❌ Error: {str(e)}\n")

def main():
    root = tk.Tk()
    app = SyntaxCheckerApp(root)

    # If a file was provided as a command-line argument, load it
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        app.file_entry.insert(0, file_path)
        app.load_file(file_path)

    root.mainloop()

if __name__ == "__main__":
    main()
