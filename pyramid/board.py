#!/usr/bin/env python3

import sys
import time
from typing import List

from shape import Shape, init_shapes
from helper import print_board


def find_next_pos(board: List[List[str]], empty_char: str) -> (int, int):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == empty_char:
                return (y, x)
    return (-1, -1)


def dfs(
    board: List[List[str]],
    shapes: List[Shape],
    num_shapes: int,
) -> bool:
    if num_shapes == 0:
        return True
    (pos_y, pos_x) = find_next_pos(board, "_")
    print(f"remaining shapes: {num_shapes}, now filling ({pos_y}, {pos_x})")
    print_board(board)
    for item in shapes:
        if item.used > 0:
            continue
        for v_idx in range(len(item.variants)):
            valid = item.fill_board(board, v_idx, pos_y, pos_x, empty_char="_", fixed=True)
            if valid:
                item.used = True
                if dfs(board, shapes, num_shapes - 1):
                    return True
            item.clear_board(board, v_idx, pos_y, pos_x, item.id, "_")
            item.used = False
    return False


def main():
    print("-------- empty board --------")
    board = []
    for y in range(10):
        board.append(["_" for _ in range(y + 1)])
    print_board(board)
    shapes = init_shapes()
    print("\n-------- final board --------")
    dfs(
        board,
        shapes,
        len(shapes),
    )
    print_board(board)


if __name__ == "__main__":
    sys.exit(main())
