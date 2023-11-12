#!/usr/bin/env python3

import sys
import yaml
from typing import Dict, List

from color import get_colored_str
from helper import print_board


class Shape:
    def __init__(self, id: str, color: str, shape_config: Dict[int, List[int]]):
        self.id = id
        self.color = color
        self.variants = [{k: shape_config[k] for k in sorted(shape_config)}]
        self.add_variants()
        self.used = False

    def _shift_horizontal(self, variant: Dict[int, List[int]]) -> None:
        offset = variant[0][0]
        for sy in variant:
            for i in range(len(variant[sy])):
                variant[sy][i] -= offset

    def _transpose(self, idx: int) -> Dict[int, List[int]]:
        variant = {}
        offset = 0
        # x may be negative, find the offset to shift it >= 0
        for sy in self.variants[idx]:
            for sx in self.variants[idx][sy]:
                if offset < -sx:
                    offset = -sx
        # transpose
        for sy in self.variants[idx]:
            for sx in self.variants[idx][sy]:
                x = sy
                y = sx + offset
                if y not in variant:
                    variant[y] = []
                variant[y].append(x)
        self._shift_horizontal(variant)
        return variant

    def _flip_up_down(self, idx: int) -> Dict[int, List[int]]:
        variant = {}
        offset = len(self.variants[idx]) - 1
        for sy in reversed(sorted(self.variants[idx])):
            variant[offset - sy] = self.variants[idx][sy].copy()
        self._shift_horizontal(variant)
        return variant

    def _flip_left_right(self, idx: int) -> Dict[int, List[int]]:
        variant = {}
        for sy in sorted(self.variants[idx]):
            variant[sy] = sorted([-x for x in self.variants[idx][sy]])
        self._shift_horizontal(variant)
        return variant

    def add_variants(self) -> None:
        assert len(self.variants) == 1
        # transpose
        variant = self._transpose(0)
        if variant != self.variants[0]:
            self.variants.append(variant)
        # flip up-down
        curr_num = len(self.variants)
        for idx in range(curr_num):
            variant = self._flip_up_down(idx)
            valid = True
            for existing_variant in self.variants:
                if variant == existing_variant:
                    valid = False
            if valid:
                self.variants.append(variant)
        # flip left-right
        curr_num = len(self.variants)
        for idx in range(curr_num):
            variant = self._flip_left_right(idx)
            valid = True
            for existing_variant in self.variants:
                if variant == existing_variant:
                    valid = False
            if valid:
                self.variants.append(variant)
        # verify
        for variant in self.variants:
            assert variant[0][0] == 0

    def clear_board(
        self,
        board: List[List[str]],
        idx: int,
        pos_y: int,
        pos_x: int,
        target_id: str,
        empty_char: str,
    ) -> None:
        variant = self.variants[idx]
        for sy in sorted(variant):
            y = pos_y + sy
            if y < 0 or y >= len(board):
                continue
            for sx in variant[sy]:
                x = sx + pos_x
                if x < 0 or x >= len(board[y]):
                    continue
                if target_id in board[y][x]:
                    board[y][x] = empty_char

    def fill_board(
        self,
        board: List[List[str]],
        idx: int,
        pos_y: int,
        pos_x: int,
        empty_char: str = " ",
        fixed: bool = False,
    ) -> bool:
        variant = self.variants[idx]
        for sy in sorted(variant):
            y = pos_y + sy
            if fixed and (y < 0 or y >= len(board)):
                return False
            while y >= len(board):
                board.append([])
            for sx in variant[sy]:
                x = sx + pos_x
                if fixed and (x < 0 or x >= len(board[y]) or board[y][x] != empty_char):
                    return False
                while x >= len(board[y]):
                    board[y] += empty_char
                # board[y][x] = self.id
                board[y][x] = get_colored_str(self.id, self.color)
        return True

    def print_shapes(self):
        span = 6
        ruler = []
        for _ in range(9):
            ruler += [str(x) for x in range(span)]
        print(" ".join(ruler))
        board = []
        pos_y = 0
        pos_x = span
        for idx in range(len(self.variants)):
            self.fill_board(board, idx, pos_y, pos_x)
            pos_x += span
            # print(board)
        print_board(board)


def init_shapes():
    with open("config_shapes.yaml", "rt") as fp:
        shape_configs = yaml.safe_load(fp)
    shapes = []
    for id, shape_desc in shape_configs.items():
        shapes.append(Shape(id, shape_desc["color"], shape_desc["shape"]))
    return shapes


def main():
    for shape in init_shapes():
        shape.print_shapes()


if __name__ == "__main__":
    sys.exit(main())
