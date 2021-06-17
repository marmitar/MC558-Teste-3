from __future__ import annotations
from dataclasses import dataclass
from random import random, randrange
from ex2lib import Graph, Node, exemplo, K



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


class Test(Graph[Vertex]):
    def __init__(self, size: int, density: float = 0.5) -> None:
        super().__init__(default_width=lambda x: (2*x + 1)/size)

        for i in range(size):
            for j in range(size):
                if i != j and random() < density:
                    weight = round(size * random(), 2)
                    self.edge(Vertex(i), Vertex(j), weight)

        start = randrange(size)
        self.start = Vertex(start)


if __name__ == "__main__":
    print(maiores_bf(exemplo, 's', 22))

    test = Test(10, 0.3)
    test.render()
    print(test.start)
    print(maiores_bf(test, test.start, 28))
