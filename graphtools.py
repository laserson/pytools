import pygraphviz as pgv

import scale

def load_immunitree_nodes(infile):
    G = pgv.AGraph(strict=True,directed=True)
    with open(infile,'r') as ip:
        ip.next()   # burn header
        for line in ip:
            data = [d.strip() for d in line.split(',')]
            
            node = data[0]
            parent = data[1]
            size = int(data[2])
            muts = len(data[-1].split('-'))
            
            G.add_node(node,xlabel="[%s] %i" % (node,size),size=size)
            if parent != '0':
                G.add_edge(parent,node,label=muts)
    
    return G

def format_immunitree_graph(G):
    min_size = max(min([int(node.attr['size']) for node in G.nodes_iter()]),1)
    max_size = max([int(node.attr['size']) for node in G.nodes_iter()])
    min_area = 0.3
    max_area = 1.3
    area_scale = scale.root(min_size,max_size).range(min_area,max_area).power(2)
    for node in G.nodes_iter():
        node.attr['fixedsize'] = True
        if int(node.attr['size']) == 0:
            node.attr['shape'] = 'point'
        else:
            node.attr['shape'] = 'circle'
            node.attr['height'] = area_scale(int(node.attr['size']))
    
    for edge in G.edges_iter():
        pass
    
    G.graph_attr['forcelabels'] = True
    G.layout(prog='dot')
