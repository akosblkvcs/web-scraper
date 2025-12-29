"""
Main entry point for the web scraper application.
"""

from .scraper import run_all_active_targets


def main() -> None:
    """
    Run all active watch targets once.
    """

    run_all_active_targets()


if __name__ == "__main__":
    main()
