from __future__ import annotations
from dataclasses import dataclass
from random import random, randrange
from typing import TypedDict
from ex2lib import Graph, Node, exemplo, K
from pickle import HIGHEST_PROTOCOL, load, dump



def maiores_bf(g: Graph[K], s: K, k: float) -> dict[Node[K], float]:
    p = {node: float('-inf') for node in g.nodes}

    def visit(n: Node[K], total: float):
        for v, w in n.adjacency.items():
            if total + w <= k and p[v] < max(w, p[n]):
                p[v] = max(w, p[n])
                visit(v, total + w)

    visit(g[s], 0.0)
    return p


def maior_bf(g: Graph[K], s: K, t: K, k: float) -> float:
    return maiores_bf(g, s, k)[g[t]]


@dataclass(frozen=True)
class Vertex:
    n: int

    def __str__(self) -> str:
        return f'v{self.n}'

    def __repr__(self) -> str:
        return str(self)


class State(TypedDict):
    size: int
    start: int
    edges: set[tuple[int, int, float]]


class Test(Graph[Vertex]):
    path = 'test.pickle'

    def __init__(self, size: int, start: int, edges: set[tuple[int, int, float]]) -> None:
        self.size = size
        super().__init__(default_width=self._width)

        for i in range(size):
            self.node(Vertex(i))
        for i, j, w in edges:
            self.edge(Vertex(i), Vertex(j), w)

        self.start = Vertex(start)

    def _width(self, weight: float) -> float:
        return (2 * weight + 1) / self.size

    @staticmethod
    def randdata(size: int, density: float = 0.5) -> State:
        edges: set[tuple[int, int, float]] = set()

        for i in range(size):
            for j in range(size):
                if i != j and random() < density:
                    weight = round(size * random(), 2)
                    edges.add((i, j, weight))

        start = randrange(size)
        return State(size=size, start=start, edges=edges)

    @classmethod
    def load(cls, size: int, density: float = 0.5) -> Test:
        try:
            with open(cls.path, 'rb') as file:
                test: Test = load(file)
            if test.size != size:
                raise ValueError(test)
            return test

        except (FileNotFoundError, ValueError):
            data = cls.randdata(size, density)
            test = cls(**data)
            with open(cls.path, 'wb') as file:
                dump(test, file, HIGHEST_PROTOCOL)
            return test

    def __getstate__(self) -> State:
        edges = {(a.name.n, b.name.n, w) for a, b, w in self.edge_weights}
        return State(size=self.size, start=self.start.n, edges=edges)

    def __setstate__(self, state: State) -> None:
        self.__init__(**state)

    def render(self, remove: Test.SubSet = set(), mark: Test.SubSet = set()) -> None:
        return super().render(remove, mark | {self.start})


test = Test.load(10, 0.3)


if __name__ == "__main__":
    print(maiores_bf(exemplo, 's', 22))

    test.render()
    print(test.start)
    print(maiores_bf(test, test.start, 18))
