"""
Web scraper module for fetching and processing web pages.
"""

import time
from datetime import datetime, timezone

import requests
from lxml import html

from .db import get_session
from .models import WatchTarget, WatchLog
from .processors import Processor, PROCESSORS, processor_raw_text


def fetch_and_parse(url: str) -> html.HtmlElement:
    """
    Fetch a URL and parse the response body into an lxml HTML element tree.
    """

    headers: dict[str, str] = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    resp: requests.Response = requests.get(url, timeout=20, headers=headers)
    resp.raise_for_status()

    return html.fromstring(resp.content)


def run_watch_target(target: WatchTarget) -> None:
    """
    Run a single watch target:
    - fetch page
    - select elements
    - run processor
    - write WatchLog + update WatchTarget
    """

    start: float = time.perf_counter()
    status: str = "ok"
    raw_text: str = ""
    processed_text: str = ""
    error_message: str | None = None

    try:
        tree: html.HtmlElement = fetch_and_parse(target.url)
        elements: list[html.HtmlElement] = list(
            tree.cssselect(target.selector)
        )

        raw_text = processor_raw_text(elements, {})

        processor: Processor = PROCESSORS.get(
            target.processor_type,
            processor_raw_text
        )

        config: dict[str, object] = target.processor_config or {}
        processed_text = processor(elements, config)

        if not processed_text:
            status = "empty"
    except requests.RequestException as ex:
        status = "error"
        error_message = f"HTTP error: {ex}"
    except (ValueError, TypeError) as ex:
        status = "error"
        error_message = f"processing error: {ex}"

    duration_ms: int = int((time.perf_counter() - start) * 1000)

    with get_session() as session:
        target_w: WatchTarget | None = session.get(WatchTarget, target.id)

        if target_w is None:
            return

        target_w.last_run_at = datetime.now(timezone.utc)
        target_w.last_status = status
        target_w.last_raw_text = raw_text
        target_w.last_processed_text = processed_text

        log = WatchLog(
            watch_target_id=target_w.id,
            status=status,
            raw_text=raw_text,
            processed_text=processed_text,
            error_message=error_message,
            duration_ms=duration_ms,
        )

        session.add(log)


def run_all_active_targets() -> None:
    """
    Load all active WatchTarget rows and run them one by one.
    """

    with get_session() as session:
        targets: list[WatchTarget] = (
            session.query(WatchTarget)
            .filter(WatchTarget.active.is_(True))
            .order_by(WatchTarget.id)
            .all()
        )

    for t in targets:
        run_watch_target(t)
