#import sys
import os
import ast
import igraph
import pickle

reports_folder_name = 'igraph_reports'
reports_folder_abs_path = os.path.abspath('AST.py') + '\\..\\' + reports_folder_name
graph = igraph.Graph(directed=True)

def get_user_input():
    return input("File or Folder Path:")

def build_report_folder():
    os.chdir(os.path.abspath('AST.py') + '\\..')
    if not os.path.isdir(reports_folder_abs_path):
        os.mkdir(reports_folder_name)

# Opens up a file and parses into an AST object
def generate_ast_from_file(filename):
    # Read the source code from the file
    with open(filename, 'r', encoding='utf-8') as file:
        source_code = file.read()

    # Generate the AST
    ast_object = ast.parse(source_code)
    return ast_object

# Recursively opens files and folders
def recursive_get_files(name):
    if os.path.isfile(name) and name.split('.')[-1] == 'py':
        print("Found File")
        parse_ast(generate_ast_from_file(name), os.getcwd() + "\\" + name)
        #igraph.plot(graph, name.split('.')[0] + '.png', margin=50, layout='reingold_tilford', vertex_label_size=14, vertex_size=34)
        igraph.write(graph, reports_folder_abs_path + '\\' + name.split('.')[0].split('\\')[-1] + '.graphml')
        graph.clear()
        print("Dependency Graph Created")

    elif os.path.isdir(name): 
        print("Found Directory")
        for dir in os.scandir(name):
            #if os.path.isfile(dir.path) or os.path.isdir(dir.path):
            if os.path.isdir(dir.path):
                if not os.path.isdir(reports_folder_abs_path + '\\' + name):
                    os.mkdir(reports_folder_abs_path + '\\' + name)
                
            recursive_get_files(dir.path)



def get_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                #graph = create_igraph(file_path)
                parse_ast(generate_ast_from_file(file), file_path)
                
                class_name = os.path.basename(root)
                output_dir = os.path.join(os.path.dirname(directory), "igraph_reports", class_name)
                os.makedirs(output_dir, exist_ok=True)
                graph_file_name = os.path.join(output_dir, f"{file.split('.')[0]}.pkl")
                with open(graph_file_name, 'wb') as f:
                    pickle.dump(graph, f)

def parse_ast(ast_node, location):
    def recursive_add_nodes(ast_node, location):
        if str(type(ast_node)) == '<class \'ast.Module\'>':
            graph.add_vertex(name=(location + '\\' + str(type(ast_node))), label=location.split('\\')[-1], color='red')
        if str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.AsyncFunctionDef\'>':
            graph.add_vertex(name=(location + '\\' + ast_node.name), label=(ast_node.name + '()'), color='green')
        if str(type(ast_node)) == '<class \'ast.ClassDef\'>':
            graph.add_vertex(name=(location + '\\' + ast_node.name), label=(ast_node.name + '()'), color='yellow')

        if hasattr(ast_node, 'body'):
            if str(type(ast_node)) == '<class \'ast.Module\'>':
                location = location + '\\' + str(type(ast_node))
            elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                location = location + '\\' + ast_node.name

            for child in ast_node.body:
                recursive_add_nodes(child, location)

    def recursive_add_children(ast_node, location):
        if hasattr(ast_node, 'body'):

            if str(type(ast_node)) == '<class \'ast.Module\'>':
                    location = location + '\\' + str(type(ast_node))
            elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                    location = location + '\\' + ast_node.name

            for child in ast_node.body:
                if hasattr(child, 'name'):
                    graph.add_edge(location, (location + '\\' + child.name), color='blue')
                
                recursive_add_children(child, location)

    def recursive_add_loose_statements(ast_node, location):
        if str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>' or str(type(ast_node)) == '<class \'ast.Module\'>':
            
            if str(type(ast_node)) == '<class \'ast.Module\'>':
                    location = location + '\\' + str(type(ast_node))
            elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                    location = location + '\\' + ast_node.name
            
            for child in ast_node.body:

                if str(type(child)) != '<class \'ast.FunctionDef\'>' or str(type(child)) != '<class \'ast.ClassDef\'>' or str(type(child)) != '<class \'ast.Module\'>':
                    graph.add_vertex(name=(location + 'loose'), label='loose', color='grey')
                    graph.add_edge(location, (location + 'loose'), color='blue')
                    break
            
            for child in ast_node.body:
                recursive_add_loose_statements(child, location)

    def recursive_add_calls(ast_node, location):
        if hasattr(ast_node, 'value') and hasattr(ast_node.value, 'func') and hasattr(ast_node.value.func, 'id') and (location + '/' + ast_node.value.func.id in graph.vs._name_index):
            if str(type(ast_node)) == '<class \'ast.Module\'>':
                graph.add_edge((location + '\\' + str(type(ast_node))), (location + '\\' + ast_node.value.func.id), color='green')
            elif (str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>'):
                graph.add_edge((location + '\\' + ast_node.name), (location + '\\' + ast_node.value.func.id), color='green')
            else:
                graph.add_edge((location + 'loose'), (location + '\\' + ast_node.value.func.id), color='green')

        if hasattr(ast_node, 'body'):

            if str(type(ast_node)) == '<class \'ast.Module\'>':
                    location = location + '\\' + str(type(ast_node))
            elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                    location = location + '\\' + ast_node.name

            for child in ast_node.body:
                recursive_add_calls(child, location)

    def recursive_add_returns(ast_node, location):
        if str(type(ast_node)) == '<class \'ast.Return\'>':
            graph.add_edge((location + 'loose'), (location), color='red')

        if hasattr(ast_node, 'body'):

            if str(type(ast_node)) == '<class \'ast.Module\'>':
                    location = location + '\\' + str(type(ast_node))
            elif str(type(ast_node)) == '<class \'ast.FunctionDef\'>' or str(type(ast_node)) == '<class \'ast.ClassDef\'>':
                    location = location + '\\' + ast_node.name

            for child in ast_node.body:
                recursive_add_returns(child, location)
        
    recursive_add_nodes(ast_node, location)
    recursive_add_children(ast_node, location)
    recursive_add_loose_statements(ast_node, location)
    recursive_add_calls(ast_node, location)
    recursive_add_returns(ast_node, location)

def main():
    user_input = get_user_input()
    build_report_folder()
    recursive_get_files(user_input)
    #get_files(user_input)

    # if len(sys.argv) > 1:
    #     build_report_folder()
    #     for arg in sys.argv:
    #         recursive_get_files(arg[1:])
    # else:
    #     print('No Arguments Entered')

if __name__ == '__main__':
    main()