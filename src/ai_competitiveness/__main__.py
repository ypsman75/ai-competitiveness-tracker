"""Command-line entry point: ``python -m ai_competitiveness``."""

import argparse

from ai_competitiveness import GEOS, __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ai_competitiveness",
        description="AI competitiveness tracker comparing EU27, US and China.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.parse_args(argv)
    print(f"ai_competitiveness {__version__} — geographies: {', '.join(GEOS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
