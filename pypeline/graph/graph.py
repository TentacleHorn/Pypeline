from functools import total_ordering
from typing import Any, Callable

import networkx
from matplotlib import pyplot as plt
from pydantic import BaseModel

from pypeline.graph import tokens


@total_ordering
class FutureValue:
    def __init__(self, value: Any):
        token = tokens.create_value_token()
        self.token = token
        self.value = value

    def __hash__(self):
        return self.token

    def evaluate(self):
        return get_default_graph().evaluate(self)

    def __eq__(self, other):
        return self.evaluate() == other

    def __lt__(self, other):
        return self.evaluate() < other


class OperationProperties(BaseModel):
    stateless: bool = False


class Operation:
    def __init__(self, input: Any,
                 output: Any,
                 op: Callable,
                 properties: OperationProperties = None):
        if properties is None:
            properties = OperationProperties()

        self.input = input
        self.output = output
        self.op = op
        self.properties = properties

    def __call__(self, *args, **kwargs):
        pass


class ComputationGraph:
    def __init__(self):
        """
        ComputationGraph is a representation of any "work" that needs to be done.
        Nodes are the variables of the program.
        Edges are the method calls that generate variables.
        """
        self.graph = networkx.DiGraph()

    def add_value(self, future: FutureValue) -> None:
        self.graph.add_node(future)

        if isinstance(future.value, Operation):
            op = future.value
            for inp in op.input:
                self.graph.add_edge(inp, future)

    def show(self) -> None:
        networkx.draw(self.graph)
        plt.savefig("./filename.png")

    def evaluate(self, future: FutureValue) -> Any:
        # todo: no recursion
        if not isinstance(future.value, Operation):
            return future.value

        pre = self.graph.predecessors(future)
        for p in pre:
            p.evaluate()

        op = future.value
        # unwrap inputs
        raw_input = [i.value for i in op.input]
        out = op.op(*raw_input)
        future.value = out

        return future.value


def walk_backwards(g: networkx.DiGraph, node):
    queue = [node]
    while queue:
        c = queue.pop()
        yield c
        pre = g.predecessors(c)
        queue.extend(pre)


_DEFAULT_GRAPH = None


def get_default_graph():
    global _DEFAULT_GRAPH
    if _DEFAULT_GRAPH is None:
        _DEFAULT_GRAPH = ComputationGraph()
    return _DEFAULT_GRAPH
