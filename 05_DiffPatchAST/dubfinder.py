import sys
import importlib
import inspect
import difflib
import ast
import textwrap

def get_func_list(entity, prev_name):
    result_func_list = []
    for entity_name, entity_data in inspect.getmembers(entity):
        if inspect.isclass(entity_data) and entity_name.startswith("__"):
            continue
        if inspect.ismethod(entity_data) or inspect.isfunction(entity_data):
            result_func_list.append((f"{prev_name}.{entity_name}", entity_data))
        elif inspect.isclass(entity_data):
            result_func_list.extend(get_func_list(entity_data, f"{prev_name}.{entity_name}"))
    return result_func_list

def process_func(func):
    func_ast = ast.parse(textwrap.dedent(inspect.getsource(func)))
    for node in ast.walk(func_ast):
        for attr_name in ['name', 'id', 'arg', 'attr']:
            if hasattr(node, attr_name):
                setattr(node, attr_name, "_")
    return ast.unparse(func_ast)

argv = sys.argv[1:]
func_list = []
for module_name in argv:
    func_list.extend(get_func_list(importlib.import_module(module_name), module_name))

functions = {name: process_func(func) for name, func in func_list}
result = []

for key1, value1 in functions.items():
    for key2, value2 in functions.items():
        if key1 >= key2:
            continue
        if difflib.SequenceMatcher(None, value1, value2).ratio() > 0.95:
            result.append((key1, key2))

for item in result:
    print(item[0] + " " + item[1])