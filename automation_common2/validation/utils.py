import re

from pydantic import ValidationError


def format_validation_error(err: ValidationError) -> str:
    """Minor ValidationError formatting changes to make it a little easier to read in Automation-specific contexts."""
    # impl adapted from ValidationError.__str__()
    errors = err.errors()
    no_errors = len(errors)
    return (
        f'{no_errors} validation error{"" if no_errors == 1 else "s"} for {err.model.__name__}\n'
        f"{_display_errors(errors)}"
    )


def _display_errors(errors):
    return "\n".join(f'{_display_error_loc(e)}\n  {e["msg"]} ({_display_error_type_and_ctx(e)})' for e in errors)


def _display_error_loc(error) -> str:
    out = ""
    for e in error["loc"]:
        if e == "__root__":
            continue
        elif isinstance(e, int):
            out += f"[{e}]"
        elif isinstance(e, str) and re.match(r"[A-Z]", e):
            out += f" -> {e}"
        else:
            out += f".{e}"
    return out.removeprefix(".")


def _display_error_type_and_ctx(error) -> str:
    t = "type=" + error["type"]
    ctx = error.get("ctx")
    if ctx:
        return t + "".join(f"; {k}={v}" for k, v in ctx.items())
    else:
        return t
