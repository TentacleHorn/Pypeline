from src.graph.graph import get_default_graph
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
    get_default_graph().show()
    data = data.evaluate()
    print(f'final result {data}')
    assert data == [4, 12, 20]


def test_two():
    x = two_vars(1, 3)
    x = two_vars(x, 3)
    print(f'final result {x}')
    assert x == 9
