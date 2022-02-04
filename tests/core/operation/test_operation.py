from pypeline.graph.operation.operation import operation


@operation
def mult_args(a, b):
	return a * b


@operation
def multi_kwargs(a=None, b=None):
	return a * b


def multi(a, b, optional=True):
	return a * b


def test_args():
	x = mult_args(1, 3)
	x = mult_args(x, 3)
	assert x == 9


def test_kwargs():
	x = multi_kwargs(a=1, b=3)
	x = multi_kwargs(x, b=3)
	assert x == 9


def test_multi():
	x = multi(1, 3)
	x = multi(x, b=3)
	x = multi(x, 3, optional=True)
	assert x == 27
