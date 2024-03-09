import sys
import ast
import pdb
import graphviz

code="""
def example_function():
    x = 1
    y = 2
    z = x + y
    print(z)
example_function()
"""

def generate_ast_graph(code):
    # Parse the code into an AST
    tree = ast.parse(code)

    # Create a Graphviz graph
    dot = graphviz.Digraph()

    # Define a recursive function to traverse the AST and add nodes and edges to the graph
    def traverse(node):
        # Add a node for the current AST node
        node_id = str(id(node))
        node_label = type(node).__name__
        dot.node(node_id, label=node_label)

        # Recursively process child nodes
        for child_name, child_node in ast.iter_fields(node):
            if isinstance(child_node, ast.AST):
                child_node_id = traverse(child_node)
                dot.edge(node_id, child_node_id, label=child_name)

        return node_id

    # Traverse the AST starting from the root node
    traverse(tree)

    return dot

# Generate the graph
graph = generate_ast_graph(code)

# Render and display the graph (requires Graphviz installed)
graph.render(filename='ast_graph', format='png', cleanup=True)
