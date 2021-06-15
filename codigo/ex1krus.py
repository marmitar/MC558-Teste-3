from __future__ import annotations
from itertools import chain
from ex1lib import Graph, Node


def kruskal(g: Graph) -> Graph:
    T = Graph()

    s: dict[Node, set[Node]] = {}
    for v in g.nodes:
        s[v] = {v}
        T.node(v.name)

    edges = sorted(g.edge_weights, key=lambda e: e[2])
    for a, b, w in edges:
        if s[a] is not s[b]:
            joined = s[a] | s[b]
            for n in chain(s[a], s[b]):
                s[n] = joined
            T.edge(a, b, w)

    return T


if __name__ == "__main__":
    g = Graph()
    g.edge('a', 'b', 4)
    g.edge('a', 'h', 8)
    g.edge('b', 'c', 8)
    g.edge('b', 'h', 11)
    g.edge('c', 'd', 7)
    g.edge('c', 'f', 4)
    g.edge('c', 'i', 2)
    g.edge('d', 'e', 9)
    g.edge('d', 'f', 14)
    g.edge('e', 'f', 10)
    g.edge('f', 'g', 2)
    g.edge('g', 'h', 1)
    g.edge('g', 'i', 6)
    g.edge('h', 'i', 7)

    print(g.edges)
    g.render(kruskal(g))
