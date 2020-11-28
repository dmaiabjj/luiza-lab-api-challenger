import re


def sanitize(value):
    if value is None:
        return ""
    value = value.strip()
    # Remove all non-word characters (everything except numbers and letters)
    value = re.sub(r"[^\w\s]", '', str(value))

    # Replace all runs of whitespace with a single dash
    value = re.sub(r"\s+", '-', value)

    return value.lower()

