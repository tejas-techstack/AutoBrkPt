import ast
from collections import defaultdict
import sys
import tokenize


def read_file(filename):
    with tokenize.open(filename) as fd:
        return fd.read()
    

class InitialChecker(ast.NodeVisitor):
    vars = {}
    keys = {}
    func_args = {}
    def __init__ (self, filepath):
        tree = ast.parse(read_file(filepath))  
        self.visit(tree)
        
    def visit_Assign(self, node: ast.AST):
        self.vars[node.targets[0].id] =  node.lineno

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
        for violation in self.violations:
            filename, lineno, msg = violation
            print(f"{filename} : {lineno} : {msg}")


class UndefinedReturnValueChecker (BaseChecker, InitialChecker):
    msg = "Possible undefined return value"
    
    def visit_Return(self, node: ast.Return):
        if node.value.id in self.vars and node.lineno < self.vars[node.value.id]:
            self.violations.append((self.filename, node.lineno, self.msg))


class ArgumentNumberChecker (BaseChecker, InitialChecker):
    msg = "Too many or too little arguments for function"

    def visit_Call(self, node: ast.Call):
        if node.func.id in self.func_args and (len(node.args) < self.func_args[node.func.id] 
                                               or (len(node.args) > self.func_args[node.func.id])) :
            self.violations.append((self.filename, node.lineno, self.msg))


if __name__ == '__main__':
    files = ["to_test2.py"]
    initial = InitialChecker(files[0])
    checker = ArgumentNumberChecker()
    checker.check(files)
    checker.report()











# class UndefinedKeyChecker(BaseChecker, InitialChecker):
#     msg = "Possible undefined key inside dictionary"

#     def visit_Assign(self, node: ast.AST):
#         target_ids = []
#         print(node.value.items())
