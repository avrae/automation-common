from typing import Optional

import pydantic.fields


def str_is_identifier(value: Optional[str], field: pydantic.fields.ModelField):
    """If a str is given, it must be an identifier."""
    if value is None:
        if field.allow_none:
            return value
        raise ValueError("None is not an allowed value")
    if not value.isidentifier():
        raise ValueError("value must be a valid identifier")
    return value
