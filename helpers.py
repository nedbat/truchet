"""Helpers for drawing in Jupyter notebooks with PyCairo."""

import colorsys
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


def make_bgfg(hs, ls, ss):
    hslsss = [[v,v] if isinstance(v, (int, float)) else v for v in [hs, ls, ss]]
    return dict(zip(["bg", "fg"], [colorsys.hls_to_rgb(*hls) for hls in zip(*hslsss)]))


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
    return min(values, key=lambda v: abs(v - x))
