import functools
from typing import TypeVar, Iterable

from pypeline.graph.operation.operation import Operation, OperationProperties, operation

IN = TypeVar('IN')

filter_operation = functools.partial(operation)


class FilterOperation(Operation):
	input: Iterable[IN]
	output: Iterable[IN]
	properties = OperationProperties(stateless=True)
