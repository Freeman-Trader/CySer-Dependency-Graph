import ast
import igraph

node_list = list()

# Redefines functions within the NodeVisitor class to print to file in specific format
class NodePrinter(ast.NodeVisitor):
    def __init__(self, output_file):
        self.output_file = output_file

    def generic_visit(self, node):
        # print('\n', file=self.output_file)
        # print('Type: ' + type(node).__name__, file=self.output_file)
        # print('ID: ' + str(id(node)), file=self.output_file)

        dict_entry = {'Type':type(node).__name__, 'ID':str(id(node))}

        if hasattr(node, 'name'):
            # print('Name: ' + str(node.name), file=self.output_file)
            dict_entry['Name'] = str(node.name)

        if hasattr(node, 'body'):
            # print('Children:', file=self.output_file)
            temp_array = list()

            for i in node.body:
                # print(str(id(i)), file=self.output_file)
                temp_array.append([str(id(i)), type(i).__name__])

            dict_entry['Children'] = temp_array

        if type(node).__name__ == "Expr":
            if hasattr(node.value.func, "id"):
                # print('Calling:', file=self.output_file)
                # print(str(node.value.func.id), file=self.output_file)  
                dict_entry['Calling'] = str(node.value.func.id)
            elif hasattr(node.value.func, "attr"):
                # print('Attr:', file=self.output_file)
                # print(str(node.value.func.attr), file=self.output_file)  
                dict_entry['Attr'] = str(node.value.func.attr)

        node_list.append(dict_entry)

        super().generic_visit(node)


# Opens up a file and parses into an AST object
def generate_ast_from_file(filename):
    # Read the source code from the file
    with open(filename, 'r') as file:
        source_code = file.read()

    # Generate the AST
    ast_object = ast.parse(source_code)
    return ast_object


# Opens file in write mode and then starts the AST traversal
def parse_ast(ast_object, filename):
    with open(filename, 'w') as file:
        NodePrinter(file).visit(ast_object)


# def tie_up_loose_statements(graph):
# Needs work

# Traverses through node list and adds each node to the graph
def add_nodes(graph):
    for index in node_list:
        graph.add_vertex(name=index['ID'], label=index['Type'])


# Traverses through node list and adds each edge relationship to the graph
def add_edges(graph):

    # Children relationships
    for index in node_list:
        if 'Children' in index:
            for child in index['Children']:
                graph.add_edge(index['ID'], child[0], color='blue')

    # Calling relationships
    for index in node_list:
        if 'Calling' in index:
            for sIndex in node_list:
                if 'Name' in sIndex and sIndex['Name'] == index['Calling']:
                    graph.add_edge(index['ID'], sIndex['ID'], color='green')


# Reads file and generates graph from file
def visualize_ast():
    newGraph = igraph.Graph(directed=True)
    
    add_nodes(newGraph)
    add_edges(newGraph)

    # Deletes the vertices with degree 0
    newGraph.delete_vertices([v.index for v in newGraph.vs if newGraph.degree()[v.index] == 0])
    # Collects Expr and puts them together
    # newGraph = tie_up_loose_statements(newGraph)
    # Deletes self-loop edges
    #newGraph.simplify(multiple=False, loops=True)

    layout = newGraph.layout('kk')
    igraph.plot(newGraph, 'AST.png', layout=layout)


# Generates AST
ast_object = generate_ast_from_file('test.py')

# Write AST to file and object
parse_ast(ast_object, "AST.txt")

# Visualize the AST
visualize_ast()