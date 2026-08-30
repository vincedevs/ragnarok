import re


def tokenize(text: str) -> list[str]:
    """Return normalized words suitable for lightweight lexical retrieval."""
    return re.findall(r"[a-z0-9]+", text.casefold())
