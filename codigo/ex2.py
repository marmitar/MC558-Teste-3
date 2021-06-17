from __future__ import annotations
from ex2lib import Graph, Node, exemplo, dijkstra, K
from ex2bf import test, maiores_bf


def transpose(g: Graph[K]) -> Graph[K]:
    gt = Graph[K](g.default_width)
    for v in g.nodes:
        gt.node(v.name)
    for u, v, w in g.edge_weights:
        gt.edge(v.name, u.name, w)
    return gt


def tdijkstra(g: Graph[K], s: K) -> dict[Node[K], float]:
    d = dijkstra(transpose(g), s)
    return {g[node.name]: dist for node, dist in d.items()}



def maior_preco(g: Graph[K], s: K, t: K, k: float) -> float:
    ds = dijkstra(g, s)
    dt = tdijkstra(g, t)

    maxw = float('-inf')

    for u, v, w in g.edge_weights:
        if ds[u] + w + dt[v] <= k and w > maxw:
            maxw = w
    return maxw


def maiores_precos(g: Graph[K], s: K, k: float) -> dict[Node[K], float]:
    return {v: maior_preco(g, s, v.name, k) for v in g.nodes}



if __name__ == "__main__":
    exemplo.render()
    print(maiores_precos(exemplo, 's', k=22))
    print(maiores_bf(exemplo, 's', k=22))
    print()

    test.render()
    print(maiores_precos(test, test.start, k=10))
    print(maiores_bf(test, test.start, k=10))
