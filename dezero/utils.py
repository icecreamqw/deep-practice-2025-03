import os
import subprocess

def get_dot_graph(output, verbose=True):
    txt = ''
    funcs = []
    seen_set = set()

    def add_func(f):
        if f not in seen_set:
            funcs.append(f)
            seen_set.add(f)

    def _dot_var(v):
        name = '' if v.name is None else v.name
        return f'"{id(v)}" [label="{name}: {v.data.shape}", color=orange, style=filled]\n'

    def _dot_func(f):
        txt = f'"{id(f)}" [label="{f.__class__.__name__}", color=lightblue, style=filled, shape=box]\n'
        for x in f.inputs:
            txt += f'"{id(x)}" -> "{id(f)}"\n'
        for y in f.outputs:
            txt += f'"{id(f)}" -> "{id(y)}"\n'  # 수정 완료: y() → y
        return txt

    txt += _dot_var(output)

    add_func(output.creator)
    while funcs:
        f = funcs.pop()
        txt += _dot_func(f)
        for x in f.inputs:
            txt += _dot_var(x)
            if x.creator is not None:
                add_func(x.creator)

    return 'digraph g {\n' + txt + '}'

def plot_dot_graph(output, verbose=True, to_file='graph.png'):
    dot_graph = get_dot_graph(output, verbose)
    tmp_path = 'tmp_graph.dot'
    with open(tmp_path, 'w') as f:
        f.write(dot_graph)
    cmd = f'dot {tmp_path} -T png -o {to_file}'
    subprocess.run(cmd, shell=True)