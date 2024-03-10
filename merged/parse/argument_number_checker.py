import ast
from collections import defaultdict
import sys
import tokenize


def read_file(filename):
    with tokenize.open(filename) as fd:
        return fd.read()
    

class InitialChecker(ast.NodeVisitor):
    func_args = {}
    def __init__ (self, filepath):
        tree = ast.parse(read_file(filepath))  
        self.visit(tree)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        counter = len(node.args.args)
        self.func_args[node.name] = counter


class BaseChecker(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def check(self, paths):
        for filepath in paths:
            self.filename = filepath
            tree = ast.parse(read_file(filepath))
            self.visit(tree)

    def report(self):
        report_list = []  # Initialize an empty list to store report items
        for violation in self.violations:
            filename, lineno, msg = violation
            report_list.append((lineno, msg))  # Append each violation as a tuple to the list
        return report_list  # Return the list of violations

class ArgumentNumberChecker (BaseChecker, InitialChecker):
    msg = "Too many or too little arguments for function"

    def visit_Call(self, node: ast.Call):
        if node.func.id in self.func_args and (len(node.args) < self.func_args[node.func.id] 
                                               or (len(node.args) > self.func_args[node.func.id])) :
            self.violations.append((self.filename, node.lineno, self.msg))

def analyse_files3(files):
    initial = InitialChecker(files[0])
    checker = ArgumentNumberChecker()
    checker.check(files)
    return checker.report()  # Return the generated report

# class UndefinedKeyChecker(BaseChecker, InitialChecker):
#     msg = "Possible undefined key inside dictionary"

#     def visit_Assign(self, node: ast.AST):
#         target_ids = []
#         print(node.value.items())
