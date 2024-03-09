import re
from math import log2

# with open('to_test2.py') as f:
#     lines = [line.rstrip() for line in f]

# lines = [line.strip() for line in lines if line != ""]

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

    volume = 1
    if operators:
        volume = (total_operators + total_operands) * (log2(len(operators)) + log2(len(operands)))
    # difficulty = (len(operators) / 2) * (total_operands / len(operands))
    # effort = difficulty * volume
    
    return volume

# Calculate Halstead metrics for the example code
def calculate(lines):
    hal_line_str = ''
    for line in lines:
        hal_line_str += line
    halstead_metrics = calculate_halstead_metrics(hal_line_str)
    return halstead_metrics
