#!/usr/bin/env python3

import sys


def _get_all_colors():
    return {
        "red": "[31;1m",
        "orange": "[31;3m",
        "light-green": "[32;1m",
        "dark-green": "[32;2m",
        "yellow": "[33;1m",
        "blue": "[34;1m",
        "light-blue": "[36;1m",
        "pink": "[35;1m",
        "light-pink": "[35;3m",
        "purple": "[35;2m",
        "white": "[37;1m",
        "grey": "[37;2m",
    }


def get_colored_str(payload: str, color: str):
    color_code = _get_all_colors()[color]
    return f"\033{color_code}{payload}\033[0m"


def main():
    for color in _get_all_colors():
        print(get_colored_str("A", color))


if __name__ == "__main__":
    sys.exit(main())
