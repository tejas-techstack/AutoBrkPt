import ast
import sys
import traceback

# counter = 0
METHOD_LENGTH_THRESHOLD = 5  # Number of lines
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

    def visit_If(self, node):
        nesting_level = self.get_nesting_level(node)
        if nesting_level > NESTING_LEVEL_THRESHOLD:
            self.breakpoints.append((node.lineno, f"If block has excessive nesting"))

    def visit_While(self, node):
        nesting_level = self.get_nesting_level(node)
        if nesting_level > NESTING_LEVEL_THRESHOLD:
            self.breakpoints.append((node.lineno, f"While block has excessive nesting"))

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


def analyze_code(file_path):
    counter = 0
    try:
        with open(file_path, "r") as file:
            code = file.read()

        tree = ast.parse(code)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)

        if analyzer.breakpoints:
            print("Detected code issues:")
            for lineno, message in analyzer.breakpoints:
                print(f"- Line {lineno}: {message}")
                print("Calling breakpoint()")
                breakpoint()

            with open(file_path, "r+") as file:
                lines = file.readlines()
                for lineno, _ in analyzer.breakpoints:
                    lineno += counter
                    lines.insert(lineno, "    server.debugpy.breakpoint()\n")
                    counter += 1
                file.seek(0)
                file.writelines(lines)
            print("Consider refactoring the code.")
        else:
            print("No code issues detected.")
    except Exception as e:
        print(f"Error analyzing code: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python addbreaks.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_code(file_path)
