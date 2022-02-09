from time import sleep, time

import pytest

from pypeline.graph.operation.operation import operation
from .helper import with_benchmark_unit


@operation
def do(x):
	sleep(1)


@operation
def do_batch(x: list):
	for _ in x:
		sleep(0.1)


@with_benchmark_unit
def test():
	data = [0] * 10

	s = time()
	data = do_batch(data)
	data = data.evaluate()
	duration = time() - s
	print(f'duration: {duration}')
	assert duration < 0.2
