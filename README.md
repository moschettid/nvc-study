# Naive Vertex Classification Algorithm Benchmarking

This project implements and compares different algorithms for vertex classification in the context of graph isomorphism testing. The study focuses on three main approaches:

1. **Cardon-Crochemore Algorithm** - An implementation of the partition refinement algorithm for naive vertex classification
2. **1-WL (Weisfeiler-Lehman)** - Using NetworkX's implementation of the 1-dimensional Weisfeiler-Lehman graph hash
3. **Color Refinement** - A basic implementation of the iterative color refinement procedure

## Overview

Graph isomorphism testing is a fundamental problem in graph theory with applications in chemistry, network analysis, and pattern recognition. This project explores algorithms that classify vertices into equivalence classes, which can be used to detect isomorphism or distinguish non-isomorphic graphs.

## Features

- Voltage graph generation from base graphs (directed and undirected)
- Implementation of Cardon-Crochemore's partition refinement algorithm
- Graph comparison utilities
- Performance benchmarking across different graph sizes
- Support for various graph representations (adjacency lists, neighborhood structures)

## Requirements

- Python 3.x
- NetworkX
- Jupyter Notebook (for running experiments)

## Example Usage

```python
# Generate test graphs
G = nx.gnp_random_graph(10, 0.5)  # Random undirected graph
VG1 = gen_voltage_graph(G, 3)     # First voltage graph
VG2 = gen_voltage_graph(G, 3)     # Second voltage graph from same base

# Test for possible isomorphism
result_cc = could_be_isomorphic_cc(VG1, VG2)  # Cardon-Crochemore
result_wl = could_be_isomorphic_wl(VG1, VG2)  # Weisfeiler-Lehman

# Run benchmarks on increasing graph sizes
for n in [100, 1000, 10000]:
    G = nx.gnp_random_graph(n, 0.4)
    # Measure and compare performance...
```

## Implementation Details

The project implements various graph generation functions:

- `gen_voltage_digraph` - Creates voltage digraphs with configurable node amplification
- `gen_voltage_graph` - Generates voltage graphs using random permutations
- `gen_strong_voltage_digraph` - Similar to voltage graph but for directed graphs

The key algorithms are:

- `labeled_cc_partition_refinement` - Implementation of Cardon-Crochemore's algorithm
- `color_refinement` - A direct implementation of iterative color refinement
- Integration with NetworkX's Weisfeiler-Lehman implementation

## References

- Cardon, A., & Crochemore, M. (1982). Partitioning a graph in O(|A|log₂|V|)
- Weisfeiler, B., & Lehman, A. (1968). A reduction of a graph to a canonical form and an algebra arising during this reduction
