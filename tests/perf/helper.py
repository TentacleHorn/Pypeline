import os.path
from collections.abc import Callable

from pypeline.perf.util import with_benchmark

OUT_DIR = r"C:\Users\User\PycharmProjects\GraphOptimizer\out"
TEST_DIR = r"C:\Users\User\PycharmProjects\GraphOptimizer\tests"


def with_benchmark_unit(f: Callable):
	import inspect
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	suffix = mod.__file__.removeprefix(TEST_DIR + "\\perf\\")
	name = os.path.splitext(suffix)[0]

	return with_benchmark(f, cache_dir=os.path.join(OUT_DIR, name))
