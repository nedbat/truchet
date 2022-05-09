"""Helpers for drawing in Jupyter notebooks."""

import contextlib
import io
import itertools
import math
import random

import cairo
import IPython.display

THINGS = {}

@contextlib.contextmanager
def svg_surface(w, h):
    svgio = io.BytesIO()
    with cairo.SVGSurface(svgio, w, h) as surface:
        THINGS[surface] = svgio
        yield surface

@contextlib.contextmanager
def svg_context(w, h):
    with svg_surface(w, h) as surface:
        context = cairo.Context(surface)
        THINGS[context] = surface
        yield context

def show_svg(thing):
    while thing in THINGS:
        thing = THINGS[thing]
    svg = thing.getvalue()
    return IPython.display.SVG(data=svg)

def range2d(nx, ny):
    return itertools.product(range(nx), range(ny))
