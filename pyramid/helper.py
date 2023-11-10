#!/usr/bin/env python3

from typing import List


def print_board(board: List[List[str]]):
    for row in board:
        print(" ".join(row))
