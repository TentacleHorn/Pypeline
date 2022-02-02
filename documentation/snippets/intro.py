from pypeline.graph.operation.operation import operation


@operation
def hello_world():
	print('hello world! This is Pypeline')


x = hello_world()
print('nothing Yet!...')
x.evaluate()