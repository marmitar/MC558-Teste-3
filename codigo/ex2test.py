from __future__ import annotations
from dataclasses import dataclass
from random import random, randrange
from typing import TypedDict
from ex2lib import Graph
from pickle import HIGHEST_PROTOCOL, load, dump


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
    end: int
    edges: set[tuple[int, int, float]]


class Test(Graph[Vertex]):
    path = 'test.pickle'

    def __init__(self, size: int, start: int, end: int, edges: set[tuple[int, int, float]]) -> None:
        self.size = size
        super().__init__(default_width=self._width)

        for i in range(size):
            self.node(Vertex(i))
        for i, j, w in edges:
            self.edge(Vertex(i), Vertex(j), w)

        self.start, self.end = Vertex(start), Vertex(end)

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

        start, end = randrange(size), randrange(size)
        start, end = min(start, end), max(start, end)
        return State(size=size, start=start, end=end, edges=edges)

    def save(self) -> Test:
        with open(self.path, 'wb') as file:
            dump(self, file, HIGHEST_PROTOCOL)
        return self


    @classmethod
    def load(cls, size: int, density: float = 0.5) -> Test:
        try:
            with open(cls.path, 'rb') as file:
                if (obj := load(file)).size == size:
                    return obj

        except FileNotFoundError:
            pass

        data = cls.randdata(size, density)
        return cls(**data).save()

    def __getstate__(self) -> State:
        edges = {(a.name.n, b.name.n, w) for a, b, w in self.edge_weights}
        return State(size=self.size, start=self.start.n, end=self.end.n, edges=edges)

    def __setstate__(self, state: State) -> None:
        self.__init__(**state)

    def render(self, remove: Test.SubSet = set(), mark: Test.SubSet = set()) -> None:
        return super().render(remove, mark | {self.start, self.end})


test = Test.load(10, 0.3)


if __name__ == "__main__":
    test.render()
    print(test.start, test.end)
