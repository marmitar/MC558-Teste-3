from __future__ import annotations
from ex2lib import Graph, Node, exemplo, dijkstra, K


def maior_preco(g: Graph[K], start: K, end: K, k: float) -> float:
    ds, dt = dijkstra(g, start), dijkstra(g, end)
    raise NotImplementedError(ds, dt, k)


if __name__ == "__main__":
    print(maior_preco(exemplo, 's', 't', k=22))
