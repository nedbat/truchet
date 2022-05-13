"""Helpers for drawing in Jupyter notebooks."""

import io
import itertools

import cairo


class CairoContext:
    def __init__(self):
        self.surface = None
        self.ctx = None

    def _repr_pretty_(self, p, cycle):
        p.text(f"<{self.__class__.__module__}.{self.__class__.__name__}>")

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


class CairoPng(CairoContext):
    def __init__(self, width, height, output):
        self.output = output
        self.pngio = None
        self.surface = cairo.ImageSurface(cairo.Format.RGB24, width, height)
        self.ctx = cairo.Context(self.surface)

    def _repr_html_(self):
        if self.output is not None:
            return f"<b><i>Wrote to {self.output}</i></b>"

    def _repr_png_(self):
        if self.output is None:
            return self.pngio.getvalue()

    def __exit__(self, typ, val, tb):
        if self.output is not None:
            self.surface.write_to_png(self.output)
        else:
            self.pngio = io.BytesIO()
            self.surface.write_to_png(self.pngio)
        super().__exit__(typ, val, tb)


def cairo_context(width, height, format="svg", output=None):
    if format == "svg":
        assert output is None, "No output name allowed for svg"
        return CairoSvg(width, height)
    elif format == "png":
        return CairoPng(width, height, output)


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
            val = tuple(int(val[i:i+2], 16)/ 255 for i in [1, 3, 5])
            return [*val, 1]
