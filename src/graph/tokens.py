
_value_token = -1
_op_token = -1


def create_value_token():
    global _value_token
    _value_token += 1
    return _value_token


def create_op_token():
    global _op_token
    _op_token += 1
    return _op_token