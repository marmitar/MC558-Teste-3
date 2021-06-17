from __future__ import annotations
from math import isfinite
from random import randrange
from graphviz import Digraph
from matplotlib.colors import to_hex, to_rgb
from typing import Callable, Container, Generic, Hashable, Literal, Optional, TypeVar, Union


BLACK = to_hex(to_rgb('k') + (1.0,), keep_alpha=True)
GRAY = to_hex(to_rgb('k') + (0.5,), keep_alpha=True)
RED = '#8c251d'


K = TypeVar('K', bound=Hashable)
Width = Callable[[float], float]

def identity(x: float) -> float:
    return x


class Graph(Generic[K]):
    def __init__(self, default_width: Width = identity) -> None:
        self._nodes: dict[K, Node[K]] = {}
        self.default_width = default_width

    def node(self, name: K) -> Node[K]:
        if (node := self._nodes.get(name)) is None:
            node = Node(self, name)
            self._nodes[name] = node
        return node

    def edge(self, tail: K, head: K, weight: Union[float, int]) -> None:
        weight = float(weight)
        assert isfinite(weight) and weight >= 0

        a = self.node(tail)
        b = self.node(head)
        a.adjacency[b] = weight

    @property
    def nodes(self) -> frozenset[Node[K]]:
        return frozenset(self._nodes.values())

    @property
    def edges(self) -> frozenset[tuple[Node[K], Node[K]]]:
        return frozenset((head, tail) for head, tail, _ in self.edge_weights)

    @property
    def edge_weights(self) -> frozenset[tuple[Node[K], Node[K], float]]:
        return frozenset(
            (tail, head, weight)
            for tail in self._nodes.values()
            for head, weight in tail.adjacency.items()
        )

    def __contains__(self, name: K) -> bool:
        return name in self._nodes

    def __getitem__(self, name: K) -> Node[K]:
        return self._nodes[name]

    def __str__(self) -> str:
        nodes = map(str, self._nodes.keys())
        return "{" + ", ".join(nodes) + "}"

    def __repr__(self) -> str:
        return f"Graph({str(self)})"

    SubSet = Container[Union[K, tuple[K, K]]]

    def viz(self, remove: SubSet = set(), mark: SubSet = set()) -> Digraph:
        dot = Digraph()

        def color(elem: Union[K, tuple[K, K]]):
            if elem in remove:
                return GRAY
            if elem in mark:
                return RED
            else:
                return BLACK

        for node in self.nodes:
            c = color(node.name)
            dot.node(str(node), color=c, fontcolor=c)
        for a, b, w in self.edge_weights:
            c = color((a.name, b.name))
            width = str(self.default_width(w))
            dot.edge(str(a), str(b), label=str(w), color=c, fontcolor=c, penwidth=width)
        return dot

    def render(self, remove: SubSet = set(), mark: SubSet = set()) -> None:
        dot = self.viz(remove, mark)
        dot.render(_gen_name(), 'out', view=True, cleanup=True, quiet_view=True)


def _gen_name(cnt: set[int] = set()) -> str:
    n = randrange(2**30)
    while n in cnt:
        n += 1
    cnt.add(n)
    return f'graph{n:x}'


class Node(Generic[K]):
    def __init__(self, graph: Graph[K], name: K) -> None:
        self.graph = graph
        self.name = name
        self.adjacency: dict[Node[K], float] = {}

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other) -> bool:
        return self is other

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return repr(self.name)


def dijkstra(g: Graph[K], s: K) -> dict[Node[K], float]:
    d = {node: float('+inf') for node in g.nodes}
    d[g[s]] = 0

    Q = set(g.nodes)
    while Q:
        u = min(Q, key=lambda n: d[n])
        Q.remove(u)

        for v, w in u.adjacency.items():
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return d


exemplo = Graph[str](lambda w: w/5)
exemplo.edge('s', 'u', 7)
exemplo.edge('s', 'x', 6)
exemplo.edge('s', 'p', 5)
exemplo.edge('u', 'v', 10)
exemplo.edge('x', 'y', 9)
exemplo.edge('p', 'q', 8)
exemplo.edge('v', 't', 6)
exemplo.edge('y', 't', 7)
exemplo.edge('q', 't', 6)


if __name__ == "__main__":
    d = dijkstra(exemplo, 's')
    for n, d in sorted(d.items(), key=lambda x: x[1]):
        print(n, d)
    exemplo.render()
