import ast
import traceback

METHOD_LENGTH_THRESHOLD = 5
NESTING_LEVEL_THRESHOLD = 3

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.breakpoints = []

    def visit_FunctionDef(self, node):
        method_length = len(node.body)
        if method_length > METHOD_LENGTH_THRESHOLD:
            self.breakpoints.append((node.lineno, f"Method '{node.name}' is too long"))

        nesting_level = self.get_nesting_level(node)
        if nesting_level > NESTING_LEVEL_THRESHOLD:
            self.breakpoints.append((node.lineno, f"Method '{node.name}' has excessive nesting"))

        self.generic_visit(node)

    def get_nesting_level(self, node):
        nested_levels = [0]
        current_level = 0

        def visit_node(n):
            nonlocal current_level
            if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.If, ast.While, ast.With, ast.Try)):
                current_level += 1
                nested_levels.append(current_level)
                self.generic_visit(n)
                current_level -= 1
            else:
                self.generic_visit(n)

        for child in ast.walk(node):
            visit_node(child)

        return max(nested_levels)

def analyse_files(testcase_file):
    try:
        with open(testcase_file, "r") as file:
            check_code = file.read()

        print("Parsing code...")
        tree = ast.parse(check_code)
        print("Code parsed successfully.")
        
        print("Analyzing code...")
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        print("Code analyzed successfully.")

        return analyzer.breakpoints

    except Exception as e:
        print(f"Error analyzing code: {e}")
        traceback.print_exc()
        return ["error"]
