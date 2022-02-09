import os
from collections.abc import Callable
from functools import wraps, partial

from pypeline.perf.profile import benchmark


def with_benchmark(f: Callable, cache_dir: str) -> Callable:
	"""
	Expected to wrap the 'main' method.
	Benchmarking it before execution if benchmark isn't already cached.
	:param f: 'main' method
	:param cache_dir: a directory in which the benchmark will be cached
	"""

	@wraps(f)
	def wrapper(*args, **kwargs):
		# attempt to load from cache
		cached = False
		if os.path.exists(cache_dir) and os.listdir(cache_dir):
			cached = True

		if not cached:
			with benchmark(out_dir=cache_dir):
				return f(*args, **kwargs)
		else:
			return f(*args, **kwargs)

	return wrapper
