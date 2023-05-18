import sys
import argparse

from web import WebClient


def version() -> None:
    print(WebClient.__version__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="nextcord-web")
    parser.add_argument(
        "-v",
        "--version",
        action="store_true"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args: argparse.Namespace = parse_args()
    if args.version:
        version()