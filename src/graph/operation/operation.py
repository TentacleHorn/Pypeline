import functools
from typing import Any, Dict, Callable, Optional

from pydantic import ByteSize, BaseModel

from src.graph import tokens
from src.graph.graph import OperationProperties, Operation, FutureValue, get_default_graph, FutureValueTuple


class PerformanceSpecs:
    duration: float  # seconds
    utilization: float  # 0 < x < 1
    memory: ByteSize


class DeviceSpecs:
    memory: ByteSize
    utilization: float


def operation(f: Callable,
              input: Any = None,
              output: Any = None,
              properties: OperationProperties = None,
              cls=Operation):
    if properties is None:
        properties = OperationProperties()

    def wrap(*args, **kwargs):
        graph = get_default_graph()
        vis = []
        for arg in args:
            if not isinstance(arg, FutureValue):
                arg = FutureValue(arg)
                graph.add_value(arg)
            vis.append(arg)

        if len(vis) > 1:
            arg = FutureValueTuple(vis)
        else:
            arg = vis[0]
        op = cls(input=arg, output=None, op=f, properties=properties)
        out = FutureValue(op)
        op.output = out
        graph.add_value(out, parent_operation=op)
        return out

    return wrap
