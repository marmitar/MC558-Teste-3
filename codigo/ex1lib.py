from __future__ import annotations
from dataclasses import dataclass
from graphviz import Graph as UnGraph
from itertools import chain
from math import isfinite
from matplotlib.colors import to_hex, to_rgb
from typing import Callable, Literal, Optional, Union, overload


BLACK = to_hex(to_rgb('k') + (1.0,), keep_alpha=True)
GRAY = to_hex(to_rgb('k') + (0.5,), keep_alpha=True)


class Graph:
    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: dict[Node, dict[Node, float]] = {}

    def node(self, name: str) -> Node:
        node = self._nodes.get(name)
        if node is None:
            node = Node(self, name)
            self._nodes[name] = node
            self._edges[node] = {}
        return node

    def edge(self, a: Union[str, Node], b: Union[str, Node], weight: float) -> tuple[Node, Node, float]:
        assert isfinite(weight) and weight > 0

        if isinstance(a, Node):
            a = a.name
        if isinstance(b, Node):
            b = b.name

        a = self.node(a)
        b = self.node(b)
        self._edges[a][b] = weight
        self._edges[b][a] = weight
        return a, b, weight

    @property
    def nodes(self) -> frozenset[Node]:
        return frozenset(node for node in self._nodes.values())

    @property
    def edges(self) -> frozenset[tuple[Node, Node]]:
        return frozenset((a, b) for a, b, _ in self.edge_weights)

    @property
    def edge_weights(self) -> frozenset[tuple[Node, Node, float]]:
        return frozenset((a, b, w) for a, adj in self._edges.items() for b, w in adj.items() if a.name <= b.name)

    def weight(self, a: Union[str, Node], b: Union[str, Node]) -> Optional[tuple[Node, Node, float]]:
        if isinstance(a, str):
            a: Optional[Node] = self._nodes.get(a)
        if isinstance(b, str):
            b: Optional[Node] = self._nodes.get(b)
        if a is None or b is None:
            return
        weight = self._edges[a].get(b)
        if weight is None:
            return
        return a, b, weight

    @overload
    def __getitem__(self, name: str) -> Node: ...
    @overload
    def __getitem__(self, name: tuple[Node, Node]) -> float: ...
    def __getitem__(self, name: Union[str, tuple[Node, Node]]) -> Union[Node, float]:
        if isinstance(name, tuple):
            a, b = name
            return self._edges[a][b]
        else:
            return self._nodes[name]

    def __str__(self) -> str:
        edges = sum(len(adj) for adj in self._edges.values())
        return f"Graph({len(self._nodes)}, {edges//2})"

    def __repr__(self) -> str:
        nodes = ",".join(str(node) for node in self.nodes)
        edges = ",".join(f"{a!r}{b!r}:{w:.1f}" for a, b, w in self.edge_weights)
        return f"Graph({nodes}; {edges})"

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, name: Union[str, Node, tuple[Node, Node]]) -> bool:
        if isinstance(name, tuple):
            a, b = map(lambda x: self._nodes.get(x.name), name)
            return b in self._edges.get(a, {})
        elif isinstance(name, Node):
            name = name.name
        return name in self._nodes

    def __or__(self, other: Graph) -> Graph:
        out = Graph()
        for a, b, w in chain(self.edge_weights, other.edge_weights):
            out.edge(a, b, w)
        return out

    def viz(self, sub: Optional[Graph] = None, width: Callable[[float], float] = lambda x: x) -> UnGraph:
        dot = UnGraph()

        if sub is not None:
            nodes = sub.nodes
            edges = sub.edges
        else:
            nodes = self.nodes
            edges = self.edges
        def sort(a: Node, b: Node) -> tuple[Node, Node]:
            if a.name < b.name:
                return a, b
            else:
                return b, a

        nodes = frozenset(n.name for n in nodes)
        edges = frozenset((min(a.name, b.name), max(a.name, b.name)) for a, b in edges)

        for node in self.nodes:
            c = BLACK if node.name in nodes else GRAY
            dot.node(node.name, color=c, fontcolor=c)
        for a, b, w in self.edge_weights:
            a, b = sort(a, b)
            c = BLACK if (a.name, b.name) in edges else GRAY
            dot.edge(a.name, b.name, label=f'{w:.0f}', color=c, fontcolor=c, penwidth=f'{width(w):.2f}')
        return dot

    def render(self, sub: Optional[Graph] = None, width: Optional[Callable[[float], float]] = None) -> None:
        if width is not None:
            dot = self.viz(sub, width)
        else:
            dot = self.viz(sub)
        dot.render(_gen_name(), 'out', view=True, cleanup=True, quiet_view=True)


def _gen_name(cnt: list[int] = [0]) -> str:
    n = cnt[0]
    cnt[0] = n + 1
    return f'graph{n:02d}'

@dataclass(frozen=True)
class Node:

    graph: Graph
    name: str

    @overload
    def adjacency(self, weights: Literal[False] = False) -> frozenset[Node]: ...
    @overload
    def adjacency(self, weights: Literal[True]) -> frozenset[tuple[Node, float]]: ...
    def adjacency(self, weights: bool = False) -> Union[frozenset[Node], frozenset[tuple[Node, float]]]:
        if weights:
            return frozenset(self.graph._edges[self].items())
        else:
            return frozenset(self.graph._edges[self].keys())

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other) -> bool:
        return self is other

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        if len(self.name) != 1:
            return repr(self.name)
        else:
            return self.name
