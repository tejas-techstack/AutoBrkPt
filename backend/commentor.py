import ast
import sys

# Thresholds for method length and nesting level
METHOD_LENGTH_THRESHOLD = 15  # Number of lines
NESTING_LEVEL_THRESHOLD = 3  # Number of nested levels


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.breakpoints = []

    def visit_FunctionDef(self, node):
        method_length = len(node.body)
        if method_length > METHOD_LENGTH_THRESHOLD:
            self.breakpoints.append((node.lineno, f"Method '{node.name}' is too long"))

        nesting_level = self.get_nesting_level(node)
        if nesting_level > NESTING_LEVEL_THRESHOLD:
            self.breakpoints.append(
                (node.lineno, f"Method '{node.name}' has excessive nesting")
            )

        self.generic_visit(node)

    def get_nesting_level(self, node):
        nested_levels = []

        def visit_node(n, level):
            nested_levels.append(level)
            self.generic_visit(n)

        ast.walk(node, visit_node, 0)
        return max(nested_levels)


def analyze_code(file_path):
    with open(file_path, "r") as file:
        code = file.read()

    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    if analyzer.breakpoints:
        print("Detected code issues:")
        for lineno, message in analyzer.breakpoints:
            print(f"- Line {lineno}: {message}")
        print("Consider refactoring the code.")

        # Set breakpoints in the code
        with open(file_path, "r+") as file:
            lines = file.readlines()
            for lineno, _ in analyzer.breakpoints:
                lines.insert(lineno, "# Insert breakpoint here\n")
            file.seek(0)
            file.writelines(lines)
    else:
        print("No code issues detected.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python code_analyzer.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_code(file_path)
