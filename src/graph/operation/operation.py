from typing import Any, Callable

from src.graph.graph import OperationProperties, Operation, FutureValue, get_default_graph


def operation(f: Callable,
              properties: OperationProperties = None):
    if properties is None:
        properties = OperationProperties()

    def wrap(*args, **kwargs):
        graph = get_default_graph()
        wrapped_args = []
        for arg in args:
            if not isinstance(arg, FutureValue):
                arg = FutureValue(arg)
                graph.add_value(arg)
            wrapped_args.append(arg)

        op = Operation(input=wrapped_args, output=None, op=f, properties=properties)
        out = FutureValue(op)
        graph.add_value(out)
        return out

    return wrap
