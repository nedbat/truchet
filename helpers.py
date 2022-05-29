"""Helpers for drawing in Jupyter notebooks with PyCairo."""

import itertools


def range2d(nx, ny):
    return itertools.product(range(nx), range(ny))


def color(val):
    """Create an RGBA color tuple from a variety of inputs."""
    if isinstance(val, (int, float)):
        return (val, val, val, 1)
    elif isinstance(val, (list, tuple)):
        if len(val) == 3:
            return (*val, 1)
        else:
            return tuple(val)
    elif isinstance(val, str):
        if val[0] == "#":
            val = tuple(int(val[i : i + 2], 16) / 255 for i in [1, 3, 5])
            return (*val, 1)


def ffffx(start, f):
    allfx = set()
    to_call = [start]
    while to_call:
        next_to_call = []
        for v in to_call:
            for vv in f(v):
                if vv not in allfx:
                    allfx.add(vv)
                    next_to_call.append(vv)
        to_call = next_to_call
    return allfx

def all_subclasses(cls):
    """Return a set of all subclasses of `cls`, including subclasses of subclasses."""
    return ffffx(cls, lambda c: c.__subclasses__())

def closest(x, values):
    return min(values, lambda v: abs(v - x))


if 0:
    # https://bpa.st/4UHA
    import numpy as np


    def nearest(a, b):
        """Find the values in a closest to the values in b"""
        return a[np.argmin(np.abs(a[:, np.newaxis] - b[np.newaxis, :]), axis=0)]


    floats = np.array((1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    x = np.array((3.2, 1.8, 7.6, 9.9))
    print(nearest(floats, x))
