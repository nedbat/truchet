"""Helpers for drawing in Jupyter notebooks."""

import io
import itertools

import cairo


class CairoContext:
    def __init__(self):
        self.surface = None
        self.ctx = None

    def __enter__(self):
        return self

    def __exit__(self, typ, val, tb):
        self.surface.finish()

    def __getattr__(self, name):
        return getattr(self.ctx, name)


class CairoSvg(CairoContext):
    def __init__(self, width, height):
        super().__init__()
        self.svgio = io.BytesIO()
        self.surface = cairo.SVGSurface(self.svgio, width, height)
        self.ctx = cairo.Context(self.surface)

    def svg(self):
        return self.svgio.getvalue()

    def _repr_svg_(self):
        return self.svg().decode()


def range2d(nx, ny):
    return itertools.product(range(nx), range(ny))
