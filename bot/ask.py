import questionary


def _validate_float(value: str, min: float = None, max: float = None):
    try:
        float_val = float(value)
        if min is not None and float_val < min:
            return f"The value must be no less than {min}!"
        if max is not None and float_val > max:
            return f"The value must be no greater than {max}!"
        return True
    except ValueError:
        return "Please enter a valid floating-point number!"


def _validate_int(value: str, min: int = None, max: int = None):
    try:
        int_val = int(value)
        if min is not None and int_val < min:
            return f"The value must be no less than {min}!"
        if max is not None and int_val > max:
            return f"The value must be no greater than {max}!"
        return True
    except ValueError:
        return "Please enter a valid integer!"


async def ask_float(
        message: str = "Enter value (float)",
        min: float = None,
        max: float = None,
        default: float = None,
) -> float:
    value = await questionary.text(
        message,
        validate=lambda text: _validate_float(text, min, max),
        default=str(default) if default else "",
    ).ask_async()
    return float(value)


async def ask_int(
        message: str = "Enter value (int)",
        min: int = None,
        max: int = None,
        default: int = None,
) -> int:
    value = await questionary.text(
        message,
        validate=lambda text: _validate_int(text, min, max),
        default=str(default) if default else "",
    ).ask_async()
    return int(value)
