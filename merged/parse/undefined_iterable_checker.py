import ast
from collections import defaultdict
import sys
import tokenize


def read_file(filename):
    with tokenize.open(filename) as fd:
        return fd.read()
    

class InitialChecker(ast.NodeVisitor):
    iterable = []
    def __init__ (self, filepath):
        tree = ast.parse(read_file(filepath))  
        self.visit(tree)
        
    def visit_Assign(self, node: ast.AST):
        if isinstance(node.value, ast.Call):
            self.iterable.append(node.targets[0].id)
        elif node.value.elts == []:
            self.iterable.append(node.targets[0].id)


class BaseChecker(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def check(self, paths):
        for filepath in paths:
            self.filename = filepath
            tree = ast.parse(read_file(filepath))
            self.visit(tree)

    def report(self):
        for violation in self.violations:
            filename, lineno, msg = violation
            print(f"{filename} : {lineno} : {msg}")


class PossibleUndefinedIterable (BaseChecker, InitialChecker):
    msg = "Possibly returning empty iterable"

    def visit_For(self, node: ast.For):
        if node.iter.id in self.iterable:
            self.violations.append((self.filename, node.lineno, self.msg))


if __name__ == '__main__':
    files = ["to_test2.py"]
    initial = InitialChecker(files[0])
    checker = PossibleUndefinedIterable()
    checker.check(files)
    checker.report()



