import ast

class UnusedVariableDetector(ast.NodeVisitor):      
    def __init__(self):
        self.used_variables = set()
        self.unused_variables = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_variables.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.unused_variables.add(node.id)

    def report_unused_variables(self):
        for var in self.unused_variables:
            if var not in self.used_variables:
                print(f"Unused variable: {var}")

def analyze_code(code):
    tree = ast.parse(code)
    detector = UnusedVariableDetector()
    detector.visit(tree)
    detector.report_unused_variables()

# Example Python code to analyze
python_code = """
def example_function():
    x = 1
    y = 2
    z = 3
    print(x, y)
"""

analyze_code(python_code)
