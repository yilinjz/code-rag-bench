import os
import json
import ast

src_dir = "datasets/"
dst_dir = "datasets/post_ast/"

# =============== utils =============== #
def load_json_data(path):
    '''
    Load json data from file path {path}
    '''
    data = []
    with open(path, 'r') as f:
        for line in f:
            json_object = json.loads(line.strip())
            data.append(json_object)
    return data

def write_json_data(path, data):
    '''
    Write json data {data} to file path {path}    
    '''
    with open(path, 'w') as f:
        for line in data:
            json.dump(line, f)
            f.write('\n')

# =============== helper =============== #
def convert_node_to_ast(node):
    '''
    Convert the subtree with root node {node} to the AST structure as a string in A(BC(DE)) format
    - Example input: ast.parse(code_snippet), where code_snippet = """
                                                                def greet(name):
                                                                    return f"Hello, {name}!"

                                                                greet("World")
                                                                """
    - Example output: Module(FunctionDef(arguments(arg)Return(JoinedStr(ConstantFormattedValue(Name(Load))Constant)))Expr(Call(Name(Load)Constant)))
    '''
    # Get the class name of the current node (e.g., Module, FunctionDef)
    node_name = node.__class__.__name__
    # Recursively generate the structure for child nodes
    child_structures = [convert_node_to_ast(child) for child in ast.iter_child_nodes(node)]
    # Combine the current node with its children in the desired format
    if child_structures:
        return f"{node_name}({''.join(child_structures)})"
    else:
        return node_name
    

# Main
if __name__ == "__main__":
    for dir_name in os.listdir(src_dir):
        dir_path = os.path.join(src_dir, dir_name)

        ## select repoeval dir
        if os.path.isdir(dir_path) and dir_name.startswith("repoeval__"):
            query_path = os.path.join(dir_path, "queries.jsonl")
            corpus_path = os.path.join(dir_path, "corpus.jsonl")

            ## read queries and corpus line by line from file
            query_data = load_json_data(query_path)
            corpus_data = load_json_data(corpus_path)

            ## convert code to code + ast
            for i, query in enumerate(query_data):
                try:
                    ## code_snippet format: incomplete_cdoe (i.e. query) + ground_truth (i.e. canonical answer) 
                    code_snippet = f"{query['text']}\n{query['metadata']['ground_truth']}"
                    ## try parsing complete code
                    parsed_tree = ast.parse(code_snippet)
                    ## convert nodes to ast
                    query_ast = convert_node_to_ast(parsed_tree)
                    ## append ast to text
                    query_data[i]['text'] = f"{query_data[i]['text']}\n\nAST={query_ast}"
                except SyntaxError as e:
                    pass
            for i, corpus in enumerate(corpus_data):
                try:
                    code_snippet = corpus['text']
                    ## try parsing complete code
                    parsed_tree = ast.parse(code_snippet)
                    ## convert nodes to ast
                    corpus_ast = convert_node_to_ast(parsed_tree)
                    ## append ast to text
                    corpus_data[i]['text'] = f"""{corpus_data[i]['text']}\n\nAST={corpus_ast}"""
                except SyntaxError as e:
                    pass

            ## dump json to output file
            output_dir = os.path.join(dst_dir, dir_name)
            output_query_path = os.path.join(output_dir, "queries.jsonl")
            output_corpus_path = os.path.join(output_dir, "corpus.jsonl")
            write_json_data(output_query_path, query_data)
            write_json_data(output_corpus_path, corpus_data)
                                                                                                                                                                                                                                                                                                                                                             