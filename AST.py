import os
import ast
import igraph

graph = igraph.Graph(directed=True)
debugfile = open('debug.txt', 'w')

# Opens up a file and parses into an AST object
def generate_ast_from_file(filename):
    # Read the source code from the file
    with open(filename, 'r') as file:
        source_code = file.read()

    # Generate the AST
    ast_object = ast.parse(source_code)
    return ast_object

def parse_ast(ast_node, location):

    def recursive_add_nodes(ast_node, location):
        if str(type(ast_node)) == '<class \'ast.Module\'>':
            graph.add_vertex(name=(location + '/' + str(type(ast_node))), label=location.split('\\')[-1], color='red')
        if str(type(ast_node)) == '<class \'ast.FunctionDef\'>':
            graph.add_vertex(name=(location + '/' + ast_node.name), label=(ast_node.name + '()'), color='green')
        if str(type(ast_node)) == '<class \'ast.ClassDef\'>':
            graph.add_vertex(name=(location + '/' + ast_node.name), label=(ast_node.name + '()'), color='yellow')

        if hasattr(ast_node, 'body'):
            for child in ast_node.body:
                recursive_add_nodes(child, location)

    def recursive_add_children(ast_node, location):
        if hasattr(ast_node, 'body'):
            for child in ast_node.body:
                if hasattr(ast_node, 'name') and hasattr(child, 'name'):
                    graph.add_edge((location + '/' + ast_node.name), (location + '/' + child.name), color='blue')
                elif hasattr(child, 'name'):
                    graph.add_edge((location + '/' + str(type(ast_node))), (location + '/' + child.name), color='blue')  
                
                recursive_add_children(child, location)

    def recursive_add_loose_statements(ast_node, location):
        if str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>' or str(type(ast_node)) == '<class \'ast.Module\'>':
            for child in ast_node.body:
                if str(type(child)) != '<class \'ast.FunctionDef\'>' or str(type(child)) != '<class \'ast.ClassDef\'>' or str(type(child)) != '<class \'ast.Module\'>':
                    if str(type(ast_node)) == '<class \'ast.Module\'>':
                        graph.add_vertex(name=(location + '/' + str(type(ast_node)) + 'loose'), label='loose', color='grey')
                        graph.add_edge((location + '/' + str(type(ast_node))), (location + '/' + str(type(ast_node)) + 'loose'), color='blue')
                    elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                        graph.add_vertex(name=(location + '/' + ast_node.name + 'loose'), label='loose', color='grey')
                        graph.add_edge((location + '/' + ast_node.name), (location + '/' + ast_node.name + 'loose'), color='blue')
                    break
            
            for child in ast_node.body:
                recursive_add_loose_statements(child, location)

    def recursive_add_calls(ast_node, location, parent):
        if hasattr(ast_node, 'value') and hasattr(ast_node.value, 'func') and hasattr(ast_node.value.func, 'id') and (location + '/' + ast_node.value.func.id in graph.vs._name_index):
            if str(type(ast_node)) == '<class \'ast.Module\'>':
                graph.add_edge((location + '/' + str(type(ast_node))), (location + '/' + ast_node.value.func.id), color='green')
            elif (str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>'):
                graph.add_edge((location + '/' + ast_node.name), (location + '/' + ast_node.value.func.id), color='green')
            else:
                graph.add_edge((location + '/' + parent + 'loose'), (location + '/' + ast_node.value.func.id), color='green')

        if hasattr(ast_node, 'body'):
            for child in ast_node.body:
                if str(type(ast_node)) == '<class \'ast.Module\'>':
                    recursive_add_calls(child, location, str(type(ast_node)))
                elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                    recursive_add_calls(child, location, ast_node.name)
                else:
                    recursive_add_calls(child, location, parent)

    recursive_add_nodes(ast_node, location)
    recursive_add_children(ast_node, location)
    recursive_add_loose_statements(ast_node, location)
    recursive_add_calls(ast_node, location, '')

# Input name of folder here, folder must be in res
# current_file = str()
# folder_name = "data"
# path = os.getcwd() + "\\" + folder_name
# for filename in os.listdir(path):
#     # Check for python file extensions
#     if filename.endswith('.py'):  
#         current_file = os.path.join(path, filename)
#         # Generates AST then writes AST to file and object
#         print(generate_ast_from_file(current_file))
    
ast_object = generate_ast_from_file("AST.py")
parse_ast(ast_object, os.getcwd() + "\\" + "AST.py")

# Deletes the vertices with degree 0
graph.delete_vertices([v.index for v in graph.vs if graph.degree()[v.index] == 0])
# Deletes self-loop edges
graph.simplify(multiple=False, loops=True)

# Visualize the AST

    # My favorite layouts
    #igraph.plot(newGraph, 'AST.png', layout='reingold_tilford', vertex_label_size=14, vertex_size=34)
    #igraph.plot(newGraph, 'AST.png', layout='sugiyama')
    #igraph.plot(newGraph, 'AST.png', vertex_label_size=14, vertex_size=34)
    #igraph.plot(newGraph, 'AST.png', layout='davidson_harel')
    #igraph.plot(newGraph, 'AST.png', layout='fruchterman_reingold')

igraph.plot(graph, 'AST.png', layout='reingold_tilford', vertex_label_size=14, vertex_size=34)
#igraph.plot(graph, 'AST.png', vertex_label_size=14, vertex_size=34)
debugfile.close()