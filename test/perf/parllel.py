from time import sleep, time

from pypeline.graph.operation.operation import operation


@operation
def do(x):
	sleep(1)


@operation
def do_batch(x: list):
	for _ in x:
		sleep(1)


def test():
	data = [0] * 10

	s = time()
	data = do_batch(data)
	data = data.evaluate()
	duration = time() - s
	print(f'duration: {duration}')
