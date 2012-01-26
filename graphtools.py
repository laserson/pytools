import pygraphviz as pgv

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
            
            G.add_node(node,size=size)
            if parent != '0':
                G.add_edge(parent,node,mut=muts)
    
    return G

