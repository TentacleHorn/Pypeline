from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
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

    def __iter__(self):
        return iter(self.evaluate())


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


class GraphExecutioner(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def execute(self, future: FutureValue, graph: ComputationGraph, ):
        pass


class NaiveExecutioner(GraphExecutioner):
    def execute(self, future: FutureValue, graph: ComputationGraph):
        # todo: no recursion
        if not isinstance(future.value, Operation):
            return future.value

        pre = graph.graph.predecessors(future)
        for p in pre:
            p.evaluate()

        op = future.value

        unwrapped_args = [i.value if isinstance(i, FutureValue) else i
                          for i in op.input.args]
        unwrapped_kwargs = {k: (i.value if isinstance(i, FutureValue) else i)
                            for k, i in op.input.kwargs.items()}

        out = op.op(*unwrapped_args, **unwrapped_kwargs)
        future.value = out


class ComputationGraph:
    def __init__(self, executioner=None):
        """
        ComputationGraph is a representation of any "work" that needs to be done.
        Nodes are the variables of the program.
        Edges are the method calls that generate variables.
        """
        self.graph = networkx.DiGraph()

        if executioner is None:
            executioner = NaiveExecutioner()
        self.executioner: GraphExecutioner = executioner

    def add_value(self, future: FutureValue) -> None:
        self.graph.add_node(future)

        if isinstance(future.value, Operation):
            op = future.value
            for inp in itertools.chain(op.input.args, op.input.kwargs.values()):
                if isinstance(inp, FutureValue):
                    self.graph.add_edge(inp, future)

    def show(self) -> None:
        networkx.draw(self.graph)
        plt.savefig("./filename.png")

    def evaluate(self, future: FutureValue) -> Any:
        self.executioner.execute(future, self)
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
