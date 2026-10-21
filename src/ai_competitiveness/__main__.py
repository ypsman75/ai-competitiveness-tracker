"""Command-line entry point: ``python -m ai_competitiveness``."""

import argparse

from ai_competitiveness import GEOS, __version__

COMMANDS = """commands:
  python -m ai_competitiveness.validate_data   validate data/processed/indicators.csv
  python -m ai_competitiveness.build_data      fetch sources and rebuild the dataset
                                               (--dry-run to validate without writing)
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ai_competitiveness",
        description="AI competitiveness tracker comparing EU27, US and China.",
        epilog=COMMANDS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.parse_args(argv)
    print(f"ai_competitiveness {__version__} — geographies: {', '.join(GEOS)}")
    print(COMMANDS, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
