import ast
from collections import defaultdict
from types import NoneType
from typing import Optional, Type, Iterable, Iterator


class BasicBlock:
    def __init__(self, insns: list[ast.stmt]) -> None:
        self.insns = insns

    @property
    def last(self) -> Optional[ast.stmt]:
        return self.insns[-1] if self.insns else None

    def matches(self, *types: Type[ast.stmt]) -> bool:
        return isinstance(self.last, types)


TreeNode = tuple[
    BasicBlock,
    list[Iterable['TreeNode']]  # this is recursive - yikes
]


class CFGBuilder:
    def __init__(self) -> None:
        # Basic blocks in program order and a mapping of blocks to
        # their successors.
        self.succ: defaultdict[BasicBlock, list[BasicBlock]] = defaultdict(list)
        self.bbs: list[BasicBlock] = []

    def build_tree(self, nodes: list[ast.stmt]) -> Iterator[TreeNode]:
        buf: list[ast.stmt] = []
        
        for node in nodes:
            match node:
                case ast.For() | ast.While():
                    if buf:
                        yield BasicBlock(buf), []
                    yield BasicBlock([node]), [self.build_tree(node.body)]
                    buf = []
        
                case ast.If():
                    buf.append(node)
                    branches = [self.build_tree(node.body),
                                self.build_tree(node.orelse)]
                    yield BasicBlock(buf), branches
                    buf = []
        
                case ast.Break() | ast.Continue() | ast.Pass() | ast.Return():
                    buf.append(node)
                    yield BasicBlock(buf), []
                    return
        
                case ast.Assign() | ast.Expr():
                    buf.append(node)
        
                case other:
                    raise NotImplementedError()
        if buf:
            yield BasicBlock(buf), []

    def connect(
        self,
        bb_tree: Iterable[TreeNode],
        parent_bb: Optional[BasicBlock],
        loop_bb: Optional[BasicBlock],
    ) -> tuple[
        list[BasicBlock],  # tails
        list[BasicBlock],  # breaks
    ]:
        breaks = []

        if parent_bb and bb_tree:
            tails = [parent_bb]
        else:
            tails = []

        for bb, branches in bb_tree:
            self.bbs.append(bb)

            for tail in tails:
                self.succ[tail].append(bb)

            if bb.matches(ast.If):
                true_branch, false_branch = branches
                true_tails, true_breaks = self.connect(true_branch, bb, loop_bb)
                false_tails, false_breaks = self.connect(false_branch, bb, loop_bb)
                breaks.extend(true_breaks)
                breaks.extend(false_breaks)
                if not (true_tails or false_tails):
                    return [], breaks
                tails = true_tails + false_tails
                if not false_branch:
                    tails.append(bb)

            elif bb.matches(ast.For, ast.While):
                branch, = branches
                tails, loop_breaks = self.connect(branch, bb, bb)
                for tail in tails:
                    self.succ[tail].append(bb)
                tails = [bb] + loop_breaks

            elif bb.matches(ast.Break):
                if loop_bb:
                    return [], breaks + [bb]
                return [bb], []

            elif bb.matches(ast.Continue):
                if loop_bb:
                    self.succ[bb].append(loop_bb)
                    return [], breaks
                return [bb], []

            elif bb.matches(ast.Return):
                return [], []

            elif bb.matches(ast.Assign, ast.Expr, ast.Pass, NoneType):
                tails = [bb]

            else:
                raise NotImplementedError()

        return tails, breaks

    def build(self, nodes: list[ast.stmt]) -> tuple[
        list[BasicBlock],
        defaultdict[BasicBlock, list[BasicBlock]],
    ]:
        # SSA construction requires an entry block.
        bb_tree = [(BasicBlock([]), [])]
        bb_tree.extend(self.build_tree(nodes))

        # If the last block is a block statement, close the cfg with
        # an empty block.
        if bb_tree[-1][1]:
            dummy = BasicBlock([])
            bb_tree.append((dummy, []))
        self.connect(bb_tree, None, None)
        return self.bbs, self.succ


def plot():
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
        ast.Not: kwd('not'),
        ast.Add: '+',
        ast.Mult: '*',
        ast.Sub: '-',
        ast.USub: '-'
    }

    OPS_PRECEDENCES = {
        ast.Add: 0,
        ast.Sub: 0,
        ast.Mult: 1
    }

    def htmlify(node):
        tp = type(node)
        if tp == ast.If:
            return kwd('if') + ' ' + htmlify(node.test)
        elif tp == ast.Assign:
            targets = ', '.join([htmlify(t) for t in node.targets])
            value = htmlify(node.value)
            return f'{targets} &larr; {value}'
        if tp == ast.BinOp:
            left = node.left
            right = node.right
            left_html = htmlify(left)
            right_html = htmlify(right)
            if type(left) == ast.BinOp and OPS_PRECEDENCES[type(left.op)] == 0:
                left_html = f'({left_html})'
            if type(right) == ast.BinOp:
                right_html = f'({right_html})'
            return ' '.join([
                left_html, htmlify(node.op), right_html
            ])
        elif tp == ast.UnaryOp:
            operand = node.operand
            operand_html = htmlify(operand)
            if type(operand) == ast.BinOp:
                if OPS_PRECEDENCES[type(operand.op)] == 0:
                    operand_html = f'({operand_html})'
            op_html = htmlify(node.op)
            if type(node.op) == ast.Not:
                op_html += ' '
            return op_html + operand_html
        elif tp in OPS_HTML:
            return OPS_HTML[tp]
        elif tp == ast.For:
            return ' '.join([
                kwd('for'), htmlify(node.target),
                kwd('in'), htmlify(node.iter)
            ])
        elif tp == ast.While:
            return kwd('while') + ' ' + htmlify(node.test)
        elif tp == ast.Compare:
            assert len(node.ops) == 1
            return ' '.join([
                htmlify(node.left), htmlify(node.ops[0]),
                htmlify(node.comparators[0])
            ])
        elif tp == ast.Expr:
            return htmlify(node.value)
        elif tp == ast.Eq:
            return '='
        elif tp == ast.Lt:
            return '&lt;'
        elif tp == ast.Name:
            id = node.id
            s = f'<i>{id}</i>'
            if '_' in id:
                s = sub(r'(\w+)_(\d+|\?)', r'<i>\1</i><sub>\2</sub>', id)
            return colorize(s, COLOR_VAR)
        elif tp == ast.Constant:
            value = node.value
            if type(value) == str:
                return string(value)
            return str(value)
        elif tp == ast.Num:
            return str(node.n)
        elif tp == ast.Str:
            return string(node.s)
        elif tp == ast.Subscript:
            value_html = htmlify(node.value)
            slice_html = htmlify(node.slice)
            return f'{value_html}&#91;{slice_html}&#93;'
        elif tp == ast.Index:
            return htmlify(node.value)
        elif tp == ast.Call:
            id = node.func.id
            args = ', '.join(htmlify(a) for a in node.args)
            # Phis are so special we pretend that they are keywords
            if id == 'phi':
                return ' '.join([kwd('phi'), args])
            return f'{id}({args})'
        elif tp in (ast.Break, ast.Continue, ast.Pass):
            return kwd(str(tp.__name__).lower())
        elif tp == ast.Return:
            s = kwd('return')
            if node.value:
                return s + ' ' + htmlify(node.value)
            return s
        else:
            assert False

    def plot_bbs(bbs, succ):
        G = AGraph(strict=False, directed=True)
        graph_attrs = {
            'dpi': 300,
            'ranksep': 0.3,
            'fontname': 'Inconsolata',
            'bgcolor': 'transparent'
        }
        G.graph_attr.update(graph_attrs)
        node_attrs = {
            'shape': 'box',
            'width': 0.55,
            'style': 'filled',
            'fillcolor': 'white'
        }
        G.node_attr.update(node_attrs)
        edge_attrs = {
            'fontsize': '10pt'
        }
        G.edge_attr.update(edge_attrs)
        names = {bb: i for i, bb in enumerate(bbs)}

        # Add nodes and edges.
        for bb, name in names.items():
            edges = succ[bb]
            peri = 2 if bb == bbs[0] or not edges else 1
            lines = [htmlify(node) for node in bb.insns]
            label = ''.join(l + '<br align="left"/>' for l in lines)
            label = f'<{label}>'
            G.add_node(name, label=label, peripheries=peri)

            colors = ['black'] * len(edges)
            if len(edges) == 2:
                colors = ['#00aa00', '#aa0000']
            for bb2, color in zip(edges, colors):
                G.add_edge(names[bb], names[bb2], color=color)

        G.draw('test.png', prog='dot')

    return plot_bbs


def main() -> None:
    root = ast.parse('''
for i in range (0, x):
    for j in range (0, i):
        print(i, j)
''')
    builder = CFGBuilder()
    bbs, succ = builder.build(root.body)
    plot()(bbs, succ)


if __name__ == '__main__':
    main()