from typing import Iterable

from src.graph.operation.types.map import map_operation


@map_operation
def classify(data: Iterable[int]):
	return map(lambda x: x + 1, data)


def cascade(data: Iterable):
	models = [1, 2]
	results = []
	for m in models:
		results = classify(results)
		print(results)
		print(results.evaluate())


def main():
	cascade([1, 2])


if __name__ == '__main__':
	main()
