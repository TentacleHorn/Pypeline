import os
from collections.abc import Iterator
from time import time

from pypeline.graph.operation.operation import operation


@operation
def read(f_list: list[str]):
	results = []
	for p in f_list:
		v = None
		if os.path.splitext(p)[1] == '.py':
			try:
				with open(p) as f:
					v = f.read()
			except Exception as e:
				pass

		results.append(v)
	return results


@operation
def transform(f_contents: list[str]):
	results = []
	for c in f_contents:
		if c:
			c = reversed(c)
		results.append(c)
	return results


def absoluteFilePaths(directory: str) -> Iterator[str]:
	for root, _, filenames in os.walk(directory):
		for f in filenames:
			yield os.path.abspath(os.path.join(root, f))


def test():
	directory = r"C:\Users\User\PycharmProjects\GraphOptimizer\pypeline"

	# flatten to full path list
	f_list = list(absoluteFilePaths(directory))
	s = time()
	f_contents = read(f_list)
	f_contents = transform(f_contents)
	f_contents = f_contents.evaluate()
	duration = time() - s
	print(duration)
