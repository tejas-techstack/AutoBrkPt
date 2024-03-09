from ast import *
from pygraphviz import AGraph
from re import sub

COLOR_KWD = '#a020f0'
COLOR_VAR = '#6c71c4'
COLOR_STR = '#8b2252'

def colorize(s, col):
    return '<font color="%s">%s</font>' % (col, s)

def kwd(s):
    return colorize(s, COLOR_KWD)

def string(s):
    return colorize(f'&#x27;{s}&#x27;', COLOR_STR)

OPS_HTML = {
    Not : kwd('not'),
    Add : '+',
    Mult : '*',
    Sub : '-',
    USub : '-'
}

OPS_PRECEDENCES = {
    Add : 0,
    Sub : 0,
    Mult : 1
}

def htmlify(node):
    tp = type(node)
    if tp == If:
        return kwd('if') + ' ' + htmlify(node.test)
    elif tp == Assign:
        targets = ', '.join([htmlify(t)  for t in node.targets])
        value = htmlify(node.value)
        return f'{targets} &larr; {value}'
    if tp == BinOp:
        left = node.left
        right = node.right
        left_html = htmlify(left)
        right_html = htmlify(right)
        if type(left) == BinOp and OPS_PRECEDENCES[type(left.op)] == 0:
            left_html = f'({left_html})'
        if type(right) == BinOp:
            right_html = f'({right_html})'
        return ' '.join([
            left_html, htmlify(node.op), right_html
        ])
    elif tp == UnaryOp:
        operand = node.operand
        operand_html = htmlify(operand)
        if type(operand) == BinOp:
            if OPS_PRECEDENCES[type(operand.op)] == 0:
                operand_html = f'({operand_html})'
        op_html = htmlify(node.op)
        if type(node.op) == Not:
            op_html += ' '
        return op_html + operand_html
    elif tp in OPS_HTML:
        return OPS_HTML[tp]
    elif tp == For:
        return ' '.join([
            kwd('for'), htmlify(node.target),
            kwd('in'), htmlify(node.iter)
        ])
    elif tp == While:
        return kwd('while') + ' ' + htmlify(node.test)
    elif tp == Compare:
        assert len(node.ops) == 1
        return ' '.join([
            htmlify(node.left), htmlify(node.ops[0]),
            htmlify(node.comparators[0])
        ])
    elif tp == Expr:
        return htmlify(node.value)
    elif tp == Eq:
        return '='
    elif tp == Lt:
        return '&lt;'
    elif tp == Name:
        id = node.id
        s = f'<i>{id}</i>'
        if '_' in id:
            s = sub(r'(\w+)_(\d+|\?)', r'<i>\1</i><sub>\2</sub>', id)
        return colorize(s, COLOR_VAR)
    elif tp == Constant:
        value = node.value
        if type(value) == str:
            return string(value)
        return str(value)
    elif tp == Num:
        return str(node.n)
    elif tp == Str:
        return string(node.s)
    elif tp == Subscript:
        value_html = htmlify(node.value)
        slice_html = htmlify(node.slice)
        return f'{value_html}&#91;{slice_html}&#93;'
    elif tp == Index:
        return htmlify(node.value)
    elif tp == Call:
        id = node.func.id
        args = ', '.join(htmlify(a) for a in node.args)
        # Phis are so special we pretend that they are keywords
        if id == 'phi':
            return ' '.join([kwd('phi'), args])
        return f'{id}({args})'
    elif tp in (Break, Continue, Pass):
        return kwd(str(tp.__name__).lower())
    elif tp == Return:
        s = kwd('return')
        if node.value:
            return s + ' ' + htmlify(node.value)
        return s
    else:
        assert False

def plot_bbs(bbs, succ):
    G = AGraph(strict = False, directed = True)
    graph_attrs = {
        'dpi' : 300,
        'ranksep' : 0.3,
        'fontname' : 'Inconsolata',
        'bgcolor' : 'transparent'
    }
    G.graph_attr.update(graph_attrs)
    node_attrs = {
        'shape' : 'box',
        'width' : 0.55,
        'style' : 'filled',
        'fillcolor' : 'white'
    }
    G.node_attr.update(node_attrs)
    edge_attrs = {
        'fontsize' : '10pt'
    }
    G.edge_attr.update(edge_attrs)
    names = {bb : i for i, bb in enumerate(bbs)}

    # Add nodes and edges.
    for bb, name in names.items():
        edges = succ[bb]
        peri = 2 if bb == bbs[0] or not edges else 1
        lines = [htmlify(node) for node in bb.insns]
        label = ''.join(l + '<br align="left"/>' for l in lines)
        label = f'<{label}>'
        G.add_node(name, label = label, peripheries = peri)

        colors = ['black'] * len(edges)
        if len(edges) == 2:
            colors = ['#00aa00', '#aa0000']
        for bb2, color in zip(edges, colors):
            G.add_edge(names[bb], names[bb2], color = color)

    G.draw('test.png', prog = 'dot')