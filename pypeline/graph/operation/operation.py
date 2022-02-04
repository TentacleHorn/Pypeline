from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable

from pypeline.graph.graph import OperationProperties, Operation, FutureValue, get_default_graph


@dataclass
class Input:
    args: Iterable
    kwargs: dict


def operation(f: Callable,
              properties: OperationProperties = None):
    if properties is None:
        properties = OperationProperties()

    def wrap(*args, **kwargs):
        graph = get_default_graph()
        i = Input(args, kwargs)

        op = Operation(input=i, output=None, op=f, properties=properties)
        out = FutureValue(op)
        graph.add_value(out)
        return out

    return wrap
