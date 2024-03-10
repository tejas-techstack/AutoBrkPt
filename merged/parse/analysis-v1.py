import ast
from pylint.lint import Run


class UnusedDetector(ast.NodeVisitor):      
    def __init__(self):
        self.used_variables = set()
        self.unused_variables = set()
        self.used_functions = set()
        self.unused_functions = set()
        self.imported_modules = set()
        self.unused_imports = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_variables.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.unused_variables.add(node.id)

    def visit_Import(self, node):
        for alias in node.names:
            self.imported_modules.add(alias.name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imported_modules.add(node.module + '.' + alias.name)

    def report_unused_variables(self):
        for var in self.unused_variables:
            if var not in self.used_variables:
                print(f"Unused variable: {var}")

    def report_unused_functions(self):
        for func in self.used_functions:
            if func not in self.used_functions:
                print(f"Unused function: {func}")

    def report_unused_imports(self):
        for imp in self.imported_modules:
            if imp not in self.used_variables:
                print(f"Unused import: {imp}")


    def report_used_variable_count(self):
        print(f"Number of used variables: {len(self.used_variables)}")

def analyze_code(code):
    tree = ast.parse(code)
    detector = UnusedDetector()
    detector.visit(tree)
    detector.report_unused_variables()
    detector.report_unused_functions()
    detector.report_unused_imports()
    detector.report_used_variable_count()

# Example Python code to analyze

filename = input("Enter name of the python file you want to analyze:")

def analyze_file(filepath):
    try:
        with open(filepath, 'r') as file:
            code = file.read()
            analyze_code(code)
    except FileNotFoundError:
        print("File not found!")
    except Exception as e:
        print("An error occurred:", e)


def run_pylint(file_path):
    try:
        # Run pylint on the specified file
        results = Run([file_path])
        
        # Print the output
        for message_id, occurrences in results.linter.stats["by_msg"].items():
            print(f"{message_id}: {occurrences}")
    except Exception as e:
        print("An error occurred:", e)





if __name__ == "__main__":
    python_file_path = filename
    analyze_file(python_file_path)

    run_pylint(python_file_path)

