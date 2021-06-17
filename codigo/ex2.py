from __future__ import annotations
from ex2lib import Graph, exemplo, dijkstra, K


def maior_preco(g: Graph[K], start: K, end: K, k: float) -> float:
    raise NotImplementedError()


if __name__ == "__main__":
    exemplo.render()
    print(maior_preco(exemplo, 's', 't', k=22))
