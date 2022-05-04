def str_is_identifier(value: str):
    if not value.isidentifier():
        raise ValueError("value must be a valid identifier")
    return value
