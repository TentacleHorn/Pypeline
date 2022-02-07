from pypeline.graph.operation.operation import operation


@operation
def double(x):
    return [v * 2 for v in x]


@operation
def multiply(x, y):
    return x * y


def test_single():
    data = [1, 3, 5]
    data = double(data)
    data = double(data)
    assert data == [4, 12, 20]


def test_two():
    x = multiply(1, 3)
    x = multiply(x, 3)
    assert x == 9
