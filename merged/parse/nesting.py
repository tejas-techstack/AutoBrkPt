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
            self.breakpoints.append(node.lineno)

        nesting_level = self.get_nesting_level(node)
        if nesting_level > NESTING_LEVEL_THRESHOLD:
            self.breakpoints.append(node.lineno)

    def get_nesting_level(self, node):
        nested_levels = []

        def visit_node(n, level):
            if isinstance(
                n, (ast.FunctionDef, ast.ClassDef, ast.If, ast.While, ast.With, ast.Try)
            ):
                level += 1
            nested_levels.append(level)
            for child in ast.iter_child_nodes(n):
                visit_node(child, level)

        visit_node(node, 0)
        return max(nested_levels)

def analyse_files(testcase_file, check1):
    try:
        with open(check1, "r") as file:
            code = file.read()

        tree = ast.parse(code)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)

        return analyzer.breakpoints

    except Exception as e:
        print(f"Error analyzing code: {e}")
        traceback.print_exc()
        return []
