from __future__ import annotations
from random import shuffle
from typing import Iterable
from ex1lib import Graph, Node
from ex1krus import kruskal


def partition(G: Graph) -> tuple[Graph, Graph, set[tuple[str, str, float]]]:
    G1, G2 = Graph(), Graph()

    for i, node in enumerate(G.nodes):
        if i % 2 == 0:
            G1.node(node.name)
        else:
            G2.node(node.name)

    cut: set[tuple[str, str, float]] = set()
    for sub in (G1, G2):
        for new in sub.nodes:
            old = G[new.name]
            for adj, weight in old.adjacency(weights=True):
                if adj in sub:
                    sub.edge(new, adj.name, weight)
                else:
                    cut.add((new.name, adj.name, weight))
    return G1, G2, cut


def maybeMST(G: Graph) -> Graph:
    if len(G) <= 2:
        return G

    G1, G2, cut = partition(G)
    print(repr(G1), repr(G2), cut)
    T1 = maybeMST(G1)
    T2 = maybeMST(G2)

    v1, v2, weight = min(cut, key=lambda s: s[2])
    T = T1 | T2
    T.edge(v1, v2, weight)
    return T


class CompleteGraph(Graph):
    def __init__(self, nodes: Iterable[str], initial: float = 1.0) -> None:
        super().__init__()

        nodes = list(nodes)
        pairs: list[tuple[Node, Node]] = []
        for i, node in enumerate(nodes):
            for adj in nodes[i+1:]:
                pairs.append((node, adj))

        shuffle(pairs)
        weight = iter(range(len(pairs)))
        for a, b in pairs:
            self.edge(a, b, initial + next(weight))

if __name__ == "__main__":
    G = CompleteGraph('abc')

    print(G)
    T = maybeMST(G)
    G.render(T, width=lambda x: (x + 1)/3)
    G.render(kruskal(G), width=lambda x: (x + 1)/3)
