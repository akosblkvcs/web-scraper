"""
Processor functions for transforming scraped HTML elements into values.
"""
import re
from collections.abc import Callable
from lxml import html

Processor = Callable[[list[html.HtmlElement], dict[str, object]], str]


def processor_raw_text(
    elements: list[html.HtmlElement],
    _: dict[str, object]
) -> str:
    """
    Returns all text content joined by comma.
    """

    texts: list[str] = [e.text_content().strip() for e in elements]

    return ", ".join(t for t in texts if t)


def processor_min_value(
    elements: list[html.HtmlElement],
    _: dict[str, object]
) -> str:
    """
    Finds minimum numeric value.
    """

    texts: list[str] = [e.text_content().strip() for e in elements]
    prices: list[float] = []

    for t in texts:
        if not t:
            continue

        # Remove non-digit separators except comma/dot
        cleaned = re.sub(r"[^\d,\.]", "", t)
        if not cleaned:
            continue

        # Normalize comma to dot
        cleaned = cleaned.replace(",", ".")

        # Find first number
        match = re.search(r"\d+(\.\d+)?", cleaned)
        if not match:
            continue

        try:
            prices.append(float(match.group(0)))
        except ValueError:
            continue

    if not prices:
        return "-"

    return str(min(prices))


PROCESSORS: dict[str, Processor] = {
    "raw_text": processor_raw_text,
    "min_value": processor_min_value,
}
