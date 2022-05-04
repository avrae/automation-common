from .models import ValidatedAutomation


def validate(obj: dict) -> ValidatedAutomation:
    """Given an arbitrary dict, either returns the parsed automation or raises a ValidationError."""
    return ValidatedAutomation.parse_obj(obj)
