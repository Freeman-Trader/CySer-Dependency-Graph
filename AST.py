import ast, copy
import igraph


# Opens up a file and parses into an AST
def generate_ast_from_file(filename):
    # Read the source code from the file
    with open(filename, 'r') as file:
        source_code = file.read()

    # Generate the AST
    tree = ast.parse(source_code)
    return tree


# Opens file in write mode and then starts the AST traversal
def write_ast_to_file(ast_object, filename):
    
    with open(filename, 'w') as file:
        file.write('0: Modules\n')
        file.write(str(id(ast_object)) + '\n')
        rTraverseAST(ast_object, file, 1)


# Recursively goes through the AST and writes the level and element to file 
def rTraverseAST(ast_object, file, level):
    if hasattr(ast_object, 'body'):
        for i in ast_object.body:
            if(str(type(i)) == "<class 'ast.FunctionDef'>"):
                file.write(str(level) + ': Function Definition: ' + str(i.name) + '\n')
                #file.write(str(level) + ': Function Body\n')
                file.write(str(id(i)) + '\n')
            elif(str(type(i)) == "<class 'ast.Expr'>"):
                file.write(str(level) + ': Expr\n')
                file.write(str(id(i)) + '\n')
            rTraverseAST(i, file, level+1)

# Seperated for one it gets to the end of a branch of the AST
    else:
        if(str(type(ast_object.value)) == "<class 'ast.FunctionDef'>"):
            file.write(str(level) + ': Function Definition: ' + str(ast_object.name) + '\n')
            file.write(str(id(ast_object)) + '\n')
        elif(str(type(ast_object.value)) == "<class 'ast.Call'>"):
            file.write(str(level) + ': Function Call: ' + str(ast_object.value.func.id) + '\n')
            file.write(str(id(ast_object)) + '\n')
            #if hasattr(ast_object.value, 'args') and ast_object.value.args != None:
                #file.write(str(level) + ': Function Args\n')
                #for i in ast_object.value.args:
                #    file.write(str(level) + ': Value: ' + i.value + '\n')


# Reads file and generates graph from file
def visualize_ast(filename):
    newGraph = igraph.Graph(directed=True)
    
    with open(filename, 'r') as file0:
        line0 = file0.readline()
        while line0:
            parentLevel = int(line0.strip().split(":")[0])
            parentData = line0.strip().split(":")[1]
            parentID = file0.readline()
            newGraph.add_vertex(name=parentID, label=parentData)

            with open('AST.txt', 'r') as file1:
                file1.seek(file0.tell())
                for line1 in file1:
                    childLevel = int(line1.strip().split(":")[0])
                    childData = line1.strip().split(":")[1]
                    childID = file1.readline()

                    if (parentLevel == (childLevel - 1)):
                        newGraph.add_vertex(name=childID, label=childData)
                        newGraph.add_edge(parentID, childID)
                    elif(parentLevel == childLevel):
                        break
            line0 = file0.readline()

    # Deletes the vertices with degree 0
    newGraph.delete_vertices([v.index for v in newGraph.vs if newGraph.degree()[v.index] == 0])
    # Deletes self-loop edges
    newGraph.simplify(multiple=False, loops=True)

    layout = newGraph.layout('kk')
    igraph.plot(newGraph, 'ast.png', layout=layout)


# Generates AST
tree = generate_ast_from_file('test.py')

# Write AST to file
write_ast_to_file(tree, "AST.txt")

# Visualize the AST
visualize_ast("AST.txt")