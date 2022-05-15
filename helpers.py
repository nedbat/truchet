"""Helpers for drawing in Jupyter notebooks with PyCairo."""

import itertools


def range2d(nx, ny):
    return itertools.product(range(nx), range(ny))


def color(val):
    if isinstance(val, (int, float)):
        return [val, val, val, 1]
    elif isinstance(val, (list, tuple)):
        if len(val) == 3:
            return [*val, 1]
        else:
            return val
    elif isinstance(val, str):
        if val[0] == "#":
            val = tuple(int(val[i : i + 2], 16) / 255 for i in [1, 3, 5])
            return [*val, 1]
