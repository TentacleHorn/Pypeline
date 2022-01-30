from src import constant


def test_auto_evaluate():
	x = constant(5)
	assert x == 5
	assert 5 == x
	x = constant(5)
	assert not 4 == x
	assert not x == 4


def test_auto_compare():
	x = constant(5)
	assert 4 < x
	assert 6 > x
	assert not x > 6
	assert not x < 4
