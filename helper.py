import networkx as nx
import random

def gen_voltage_digraph(G, gen_type, art_nodes_qty):
    """
    Generate a voltage digraph from a base directed graph.
    
    This function creates a larger directed graph (voltage graph) by replacing each node
    in the original graph with multiple artificial nodes, and connecting them according
    to the specified generation type.
    
    Parameters:
    -----------
    G : networkx.DiGraph
        The base directed graph
    gen_type : str
        The type of voltage graph to generate: "succ" or "pred"
    art_nodes_qty : list
        A list where art_nodes_qty[i] specifies how many artificial nodes to create
        for original node i
        
    Returns:
    --------
    networkx.DiGraph
        The generated voltage digraph
    """
    if not isinstance(G, nx.DiGraph):
        raise ValueError("G must be a directed graph")
    if gen_type != "succ" and gen_type != "pred":
        raise ValueError("Invalid gen_type. Must be one of 'succ' or 'pred'")
    
    # Calculate cumulative sum for node indexing
    cumulate = [0]
    for i in range(G.number_of_nodes()):
        cumulate.append(cumulate[-1] + art_nodes_qty[i])
    
    VG = nx.DiGraph()
    VG.add_nodes_from(range(G.number_of_nodes()))
    for edge in G.edges:
        source, target = edge
        ssize, tsize = art_nodes_qty[source], art_nodes_qty[target]
        
        if gen_type == "succ":
            # For each artificial node of the source, connect to a random artificial node of the target
            for i in range(ssize):
                j = random.randrange(tsize)
                VG.add_edge(cumulate[source] + i, cumulate[target] + j)
        else:  # gen_type == "pred"
            # For each artificial node of the target, connect from a random artificial node of the source
            for i in range(tsize):
                j = random.randrange(ssize)
                VG.add_edge(cumulate[source] + j, cumulate[target] + i)
                    
    return VG

def gen_uniform_voltage_digraph(G, gen_type, nodes_amplification):
    """
    Generate a voltage digraph with uniform node amplification.
    
    A convenience wrapper around gen_voltage_digraph where each node
    is replaced by the same number of artificial nodes.
    
    Parameters:
    -----------
    G : networkx.DiGraph
        The base directed graph
    gen_type : str
        The type of voltage graph to generate: "succ" or "pred"
    nodes_amplification : int
        The number of artificial nodes to create for each original node
        
    Returns:
    --------
    networkx.DiGraph
        The generated voltage digraph
    """
    nq = [nodes_amplification] * G.number_of_nodes()
    return gen_voltage_digraph(G, gen_type, nq)  # Added return statement

def gen_voltage_graph(G, art_nodes_qty):
    """
    Generate a voltage graph from a base undirected graph.
    
    Each edge in the original graph corresponds to a random permutation
    connecting the artificial nodes in the voltage graph.
    
    Parameters:
    -----------
    G : networkx.Graph
        The base undirected graph
    art_nodes_qty : int
        The number of artificial nodes to create for each original node
        
    Returns:
    --------
    networkx.Graph
        The generated voltage graph
    """
    if not isinstance(G, nx.Graph):
        raise ValueError("G must be an undirected graph")
    
    VG = nx.Graph()
    VG.add_nodes_from(range(G.number_of_nodes()))
    for edge in G.edges:
        source, target = edge
        perm = random.sample(range(art_nodes_qty), art_nodes_qty)
        for i in range(art_nodes_qty):
            VG.add_edge(source*art_nodes_qty + i, target*art_nodes_qty + perm[i])
            
    return VG

def gen_strong_voltage_digraph(G, art_nodes_qty):
    """
    Generate a strong voltage digraph from a base directed graph.
    
    Similar to gen_voltage_graph but for directed graphs. Each edge in the original graph 
    corresponds to a random permutation connecting the artificial nodes in the voltage graph.
    
    Parameters:
    -----------
    G : networkx.DiGraph
        The base directed graph
    art_nodes_qty : int
        The number of artificial nodes to create for each original node
        
    Returns:
    --------
    networkx.DiGraph
        The generated strong voltage digraph
    """
    if not isinstance(G, nx.DiGraph):
        raise ValueError("G must be a directed graph")
    
    VG = nx.DiGraph()
    VG.add_nodes_from(range(G.number_of_nodes()))
    for edge in G.edges:
        source, target = edge
        perm = random.sample(range(art_nodes_qty), art_nodes_qty)
        for i in range(art_nodes_qty):
            VG.add_edge(source*art_nodes_qty + i, target*art_nodes_qty + perm[i])
            
    return VG

def gen_adj_list(G, reverse=False):
    """
    Generate an adjacency list representation of a directed graph.
    
    Parameters:
    -----------
    G : networkx.DiGraph
        The directed graph
    reverse : bool, default=False
        If True, generate the reverse adjacency list (incoming edges)
        
    Returns:
    --------
    list
        A list of lists where adj_list[i] contains the nodes adjacent to node i
    """
    if not isinstance(G, nx.DiGraph):
        raise ValueError("G must be a directed graph")
    
    adj_list = [[] for _ in range(G.number_of_nodes())]
    if not reverse:
        for e in sorted(G.edges):
            adj_list[e[0]].append(e[1])
    else:
        for e in sorted(G.edges, key=lambda x: (x[1], x[0])):
            adj_list[e[1]].append(e[0])
    return adj_list

def gen_neighbourhood(G):
    """
    Generate a neighborhood list for an undirected graph.
    
    Parameters:
    -----------
    G : networkx.Graph
        The undirected graph
        
    Returns:
    --------
    list
        A list of lists where neighbourhood[i] contains the neighbors of node i,
        sorted in ascending order
    """
    if not isinstance(G, nx.Graph):
        raise ValueError("G must be an undirected graph")
    
    neighbourhood = [[] for _ in range(G.number_of_nodes())]
    for e in G.edges:
        neighbourhood[e[0]].append(e[1])
        neighbourhood[e[1]].append(e[0])
    for i in range(len(neighbourhood)):
        neighbourhood[i] = sorted(neighbourhood[i])
    return neighbourhood

def combine_graphs(G0, G1):
    """
    Combine two graphs into a single larger graph.
    
    This function creates a new graph by placing G0 and G1 side by side (disjoint union).
    The nodes from G1 are renumbered to avoid conflicts with G0's nodes.
    
    Parameters:
    -----------
    G0 : networkx.Graph or networkx.DiGraph
        The first graph
    G1 : networkx.Graph or networkx.DiGraph
        The second graph (should be the same type as G0)
        
    Returns:
    --------
    networkx.Graph or networkx.DiGraph
        A new graph containing all nodes and edges from both input graphs
        
    Notes:
    ------
    - The type of the returned graph (directed or undirected) is determined by G0
    - Nodes from G1 are renumbered by adding the number of nodes in G0 to their indices
    """
    # Validate that both graphs are the same type
    if isinstance(G0, nx.DiGraph) != isinstance(G1, nx.DiGraph):
        raise ValueError("Both graphs must be of the same type (both directed or both undirected)")
    
    N0 = G0.number_of_nodes()
    
    # Create a new graph of the same type as the input graphs
    if isinstance(G0, nx.DiGraph):
        G = nx.DiGraph()
    else:
        G = nx.Graph()
        
    # Add all edges from G0
    for e in G0.edges:
        G.add_edge(e[0], e[1])
    
    # Add all edges from G1, with node indices shifted
    for e in G1.edges:
        G.add_edge(e[0] + N0, e[1] + N0)
        
    return G

#TODO: substitute with lexicographic sort
"""
k = max([len(S[v]) for v in S.keys()])
m = maxr - minr + 2 #ex. 0-5 -> void + [0,1,2,3,4,5] (7 classes)
elements = deque(S.items())
Q = [[] for _ in range(m)]
for j in range(k,0,-1):
    while elements:
        A = elements.popleft()
        if len(A[1]) < j:
            Q[0].append(A)
        else:
            Q[A[1][j-1]-minr+1].append(A)
    for l in range(m):
        while Q[l]:
            elements.extend(Q[l])
            Q[l] = []
S_sorted = list(elements)"""