import ast
import re
from math import log2
from math import log
from halstead import calculate

line_nos = []


def calculate_cyclomatic_complexity(func_ast):
    complexity = 1
    
    for node in ast.walk(func_ast):
        if isinstance(node, ast.If) or isinstance(node, ast.While) or isinstance(node, ast.For):
            complexity += 1
        elif isinstance(node, ast.Try) or isinstance(node, ast.ExceptHandler):
            complexity += 1
        elif isinstance(node, ast.With):
            complexity += 1
        elif isinstance(node, ast.AsyncWith):
            complexity += 1
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            continue
    
    return [func_ast.lineno, func_ast.end_lineno], complexity


def extract_function(ast_tree, func_name):
    for node in ast_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return node
    return None



def get_operators_and_operands(code):
    operators = set()
    operands = set()
    
    operator_pattern = r'(\+|\-|\*|\/|\=\=|\!|\>|\<|\&\&|\|\||\=)'
    operand_pattern = r'([a-zA-Z_]\w*|\d+)'
    
    operator_matches = re.findall(operator_pattern, code)
    operand_matches = re.findall(operand_pattern, code)
    
    operators.update(operator_matches)
    operands.update(operand_matches)
    
    return operators, operands

def calculate_halstead_metrics(code):
    operators, operands = get_operators_and_operands(code)
    
    total_operators = len(re.findall(r'(\+|\-|\*|\/|\=\=|\!|\>|\<|\&\&|\|\||\=)', code))
    total_operands = len(re.findall(r'([a-zA-Z_]\w*|\d+)', code))

    volume = (total_operators + total_operands) * (log2(len(operators)) + log2(len(operands)))
    difficulty = (len(operators) / 2) * (total_operands / len(operands))
    effort = difficulty * volume
    
    return volume


file_path = 'to_test2.py'
with open(file_path, 'r') as file:
    code = file.read()
parsed_ast = ast.parse(code)

for node in parsed_ast.body:
    if isinstance(node, ast.FunctionDef):
        target_function_name = node.name 
        target_function_ast = extract_function(parsed_ast, target_function_name)

        if target_function_ast:
            line_nos, complexity = calculate_cyclomatic_complexity(target_function_ast)
            with open('to_test2.py') as f:
                    lines = [line.rstrip() for line in f]
                    # lines = [line.strip() for line in lines if line != ""]
            hal_lines = []
            for line in range(line_nos[0], line_nos[1]):
                hal_lines.append(lines[line])
            hal_metrics = calculate(hal_lines)
            # mi = abs((log(hal_metrics) - 9.2 * (complexity) - 16.2 * log(len(lines))))
            mi = max(0,(171 - 5.2 * log(hal_metrics) - 0.23 * (complexity) - 16.2 * log(len(lines)))*100 / 171)
            print(target_function_name, mi)
        else:
            print(f"Function '{target_function_name}' not found in the code.")
