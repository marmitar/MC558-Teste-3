from __future__ import annotations
from queue import Queue
from ex2lib import Graph, Node, exemplo, K
from ex2test import test



def maiores_bf(g: Graph[K], s: K, k: float) -> dict[Node[K], float]:
    p = {node: float('-inf') for node in g.nodes}
    Q = [(g[s], 0.0, p[g[s]])]

    while Q:
        u, total, maxw = Q.pop()

        for v, w in u.adjacency.items():
            if total + w <= k:
                p[v] = max(p[v], w, maxw)
                Q.append((v, total + w, max(w, maxw)))

    return p


def maior_bf(g: Graph[K], s: K, t: K, k: float) -> float:
    return maiores_bf(g, s, k)[g[t]]


if __name__ == "__main__":
    print(maiores_bf(exemplo, 's', 22))

    test.render()
    print(test.start, test.end)
    print(maiores_bf(test, test.start, 18))
