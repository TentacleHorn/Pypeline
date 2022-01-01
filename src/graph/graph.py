from typing import Any, Callable, Iterable

import networkx
from matplotlib import pyplot as plt
from pydantic import BaseModel

from src.graph import tokens


class FutureValue:
    def __init__(self, value: Any, token: int = None):
        if token is None:
            token = tokens.create_value_token()
        self.token = token
        self.value = value

    def __hash__(self):
        return self.token

    def evaluate(self):
        return get_default_graph().evaluate(self)


class FutureValueTuple(FutureValue):
    def __init__(self, value: Iterable, token: int = None):
        super().__init__(value, token)


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

    def add_value(self, future: FutureValue, parent_operation: Operation = None) -> None:
        if parent_operation:
            self.graph.add_edge(parent_operation.input, parent_operation.output)
        else:
            self.graph.add_node(future)

    def show(self) -> None:
        networkx.draw(self.graph)
        plt.savefig("./filename.png")

    def evaluate(self, future: FutureValue) -> Any:
        # todo: no recursion
        if not isinstance(future.value, (FutureValue, Operation)):
            return future.value

        pre = self.graph.predecessors(future)
        for p in pre:
            self.evaluate(p)

        if not isinstance(future.value, Operation):
            raise NotImplemented

        op = future.value
        out = op.op(op.input.value)
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
