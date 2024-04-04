import os
import ast
import igraph

def get_user_input():
    return input("Relative File/Folder Path:")

# Opens up a file and parses into an AST object
def generate_ast_from_file(filepath):
    # Read the source code from the file
    with open(filepath, 'r') as file:
        source_code = file.read()

    # Generate the AST
    ast_object = ast.parse(source_code)
    return ast_object

# Recursively opens files and folders
def recursive_get_files(filepath):
    if os.path.isfile(filepath) and filepath.split('.')[-1] == 'py':
        print("Found File")

        filename = "" # find file name
        if(len(filepath.split('\\')) > 1) : 
            filename = filepath.split('\\')[-1]
        elif(len(filepath.split('/')) > 1) : 
            filename = filepath.split('/')[-1]
        else :
            print("something is terribly wrong")
        
        print("Processing " + filename)
        
        parse_ast(generate_ast_from_file(filepath),filename)
        igraph.plot(graph, filepath.split('.')[0] + '.png', margin=50, layout='reingold_tilford', vertex_label_size=14, vertex_size=34)

        edge_list_string = to_edge_list_names(graph)
        edge_list_dict = create_node_name_to_id(edge_list_string)
        edge_list_numbers = to_edge_list_numbers(edge_list_string, edge_list_dict)
        with open(filepath.split('.')[0] + '.txt', 'w') as f:
            f.write(edge_list_numbers)
        print("Content has been written to", filepath)
        print(edge_list_string)
        print(edge_list_dict)
        print(edge_list_numbers)
        graph.clear()
        print("Dependency Graph Created")

    elif os.path.isdir(filepath):
        print("Found Directory")
        for it in os.scandir(filepath):
            if os.path.isfile(it.path) or os.path.isdir(it.path):
                recursive_get_files(it.path)

def parse_ast(ast_node, filename):

    def recursive_add_nodes(ast_node, filename):
        if str(type(ast_node)) == '<class \'ast.Module\'>':
            graph.add_vertex(name=(filename + '/' + str(type(ast_node))), label=filename.split('\\')[-1], color='red')
        if str(type(ast_node)) == '<class \'ast.FunctionDef\'>':
            graph.add_vertex(name=(filename + '/' + ast_node.name), label=(ast_node.name + '()'), color='green')
        if str(type(ast_node)) == '<class \'ast.ClassDef\'>':
            graph.add_vertex(name=(filename + '/' + ast_node.name), label=(ast_node.name + '()'), color='yellow')

        if hasattr(ast_node, 'body'):
            if str(type(ast_node)) == '<class \'ast.Module\'>':
                filename = filename + '/' + str(type(ast_node))
            elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                filename = filename + '/' + ast_node.name

            for child in ast_node.body:
                recursive_add_nodes(child, filename)

    def recursive_add_children(ast_node, filename):
        if hasattr(ast_node, 'body'):

            if str(type(ast_node)) == '<class \'ast.Module\'>':
                    filename = filename + '/' + str(type(ast_node))
            elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                    filename = filename + '/' + ast_node.name

            for child in ast_node.body:
                if hasattr(child, 'name'):
                    graph.add_edge(filename, (filename + '/' + child.name), color='blue')
                
                recursive_add_children(child, filename)

    def recursive_add_loose_statements(ast_node, filename):
        if str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>' or str(type(ast_node)) == '<class \'ast.Module\'>':
            
            if str(type(ast_node)) == '<class \'ast.Module\'>':
                    filename = filename + '/' + str(type(ast_node))
            elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                    filename = filename + '/' + ast_node.name
            
            for child in ast_node.body:

                if str(type(child)) != '<class \'ast.FunctionDef\'>' or str(type(child)) != '<class \'ast.ClassDef\'>' or str(type(child)) != '<class \'ast.Module\'>':
                    graph.add_vertex(name=(filename + 'loose'), label='loose', color='grey')
                    graph.add_edge(filename, (filename + 'loose'), color='blue')
                    break
            
            for child in ast_node.body:
                recursive_add_loose_statements(child, filename)

    def recursive_add_calls(ast_node, filename):
        if hasattr(ast_node, 'value') and hasattr(ast_node.value, 'func') and hasattr(ast_node.value.func, 'id') and (filename + '/' + ast_node.value.func.id in graph.vs._name_index):
            if str(type(ast_node)) == '<class \'ast.Module\'>':
                graph.add_edge((filename + '/' + str(type(ast_node))), (filename + '/' + ast_node.value.func.id), color='green')
            elif (str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>'):
                graph.add_edge((filename + '/' + ast_node.name), (filename + '/' + ast_node.value.func.id), color='green')
            else:
                graph.add_edge((filename + 'loose'), (filename + '/' + ast_node.value.func.id), color='green')

        if hasattr(ast_node, 'body'):

            if str(type(ast_node)) == '<class \'ast.Module\'>':
                    filename = filename + '/' + str(type(ast_node))
            elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                    filename = filename + '/' + ast_node.name

            for child in ast_node.body:
                recursive_add_calls(child, filename)

    def recursive_add_returns(ast_node, filename):
        if str(type(ast_node)) == '<class \'ast.Return\'>':
            graph.add_edge((filename + 'loose'), (filename), color='red')

        if hasattr(ast_node, 'body'):

            if str(type(ast_node)) == '<class \'ast.Module\'>':
                    filename = filename + '/' + str(type(ast_node))
            elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                    filename = filename + '/' + ast_node.name

            for child in ast_node.body:
                recursive_add_returns(child, filename)
        
    recursive_add_nodes(ast_node, filename)
    recursive_add_children(ast_node, filename)
    recursive_add_loose_statements(ast_node, filename)
    recursive_add_calls(ast_node, filename)
    recursive_add_returns(ast_node, filename)

def to_edge_list_names(graph):
    updated = str(graph)
    updated = updated.split("(vertex names):")[-1].strip()
    updated = updated.replace("<class \'ast.Module\'>", "")
    updated = updated.replace("<class\n\'ast.Module\'>", "")
    updated = updated.replace("//", "/")
    updated = updated.replace(", ", ",\n")
    updated = updated.replace("/->", ",")
    updated = updated.replace("->", ",")
    return updated

def to_edge_list_numbers(names, name_dict):
    for name in reversed(name_dict):
        names = names.replace(name, str(name_dict[name]))
    return names

def create_node_name_to_id(edge_list_string):
    node_name_to_id = {}
    current_id = 0
    lines = edge_list_string.strip().split('\n')
    for line in lines:
        nodes = line.strip().split(',')
        for node in nodes:
            if node not in node_name_to_id and node != "":
                node_name_to_id[node] = current_id
                current_id += 1
    return node_name_to_id

graph = igraph.Graph(directed=True)
user_input = get_user_input()
recursive_get_files(user_input)
