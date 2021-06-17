from __future__ import annotations
from math import isfinite
from graphviz import Digraph
from matplotlib.colors import to_hex, to_rgb
from typing import Callable, Generic, Hashable, Optional, TypeVar, Union


BLACK = to_hex(to_rgb('k') + (1.0,), keep_alpha=True)
GRAY = to_hex(to_rgb('k') + (0.5,), keep_alpha=True)


K = TypeVar('K', bound=Hashable)
Width = Callable[[float], float]


class Graph(Generic[K]):
    def __init__(self, default_width: Width = lambda x: x) -> None:
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
        return f"Graph({str(self)}"

    def viz(self, sub: Optional[Graph[K]] = None, width: Optional[Width] = None) -> Digraph:
        dot = Digraph()
        width = width or self.default_width

        if sub is not None:
            nodes = sub.nodes
            edges = sub.edges
        else:
            nodes = self.nodes
            edges = self.edges

        nodes = frozenset(n.name for n in nodes)
        edges = frozenset((a.name, b.name) for a, b in edges)

        for node in self.nodes:
            c = BLACK if node.name in nodes else GRAY
            dot.node(str(node), color=c, fontcolor=c)
        for a, b, w in self.edge_weights:
            c = BLACK if (a.name, b.name) in edges else GRAY
            dot.edge(str(a), str(b), label=str(w), color=c, fontcolor=c, penwidth=str(width(w)))
        return dot

    def render(self, sub: Optional[Graph[K]] = None, width: Optional[Width] = None) -> None:
        if width is not None:
            dot = self.viz(sub, width)
        else:
            dot = self.viz(sub)
        dot.render(_gen_name(), 'out', view=True, cleanup=True, quiet_view=True)


def _gen_name(cnt: list[int] = [0]) -> str:
    n = cnt[0]
    cnt[0] = n + 1
    return f'graph{n:02d}'


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


exemplo: Graph[str] = Graph(lambda w: w/5)
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
