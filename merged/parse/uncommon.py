import ast
from collections import defaultdict
import tokenize

def read_file(filename):
    with tokenize.open(filename) as fd:
        return fd.read()

class InitialChecker(ast.NodeVisitor):
    vars = {}

    def __init__(self, filepath):
        tree = ast.parse(read_file(filepath))
        self.visit(tree)

    def visit_Assign(self, node: ast.AST):
        self.vars[node.targets[0].id] = node.lineno


class BaseChecker(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def check(self, paths):
        for filepath in paths:
            self.filename = filepath
            tree = ast.parse(read_file(filepath))
            self.visit(tree)

    def report(self):
        violations_list = [(lineno, msg) for lineno, msg in self.violations]  # Modified this line
        return(violations_list)


class UndefinedReturnValueChecker(BaseChecker, InitialChecker):
    msg = "Possible undefined return value"

    def visit_Return(self, node: ast.Return):
        if node.value.id in self.vars and node.lineno < self.vars[node.value.id]:
            self.violations.append((node.lineno, self.msg))  # Modified this line


def analyse_files2(files):
    initial = InitialChecker(files[0])
    checker = UndefinedReturnValueChecker()
    checker.check(files)
    checker.report()
