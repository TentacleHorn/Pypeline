from src.graph.operation.operation import operation


@operation
def my_op(x):
    return [v * 2 for v in x]


@operation
def two_vars(x, y):
    return x * y


def test_single():
    data = [1, 3, 5]
    data = my_op(data)
    data = my_op(data)
    data = data.evaluate()
    assert data == [4, 12, 20]


def test_two():
    x = two_vars(1, 3)
    x = two_vars(x, 3)
    x = x.evaluate()
    assert x == 9
