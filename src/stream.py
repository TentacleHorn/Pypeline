from typing import List


class LazyStream:
	def __init__(self, values: List):
		self.values = None

	def __iter__(self):
		pass
