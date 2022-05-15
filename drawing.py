"""Helpers for drawing in Jupyter notebooks with PyCairo."""

import io
import os.path

import cairo


class _CairoContext:
    """Base class for Cairo contexts that can display in Jupyter, or write to a file."""

    def __init__(self, width: int, height: int, output: str | None = None):
        self.width = width
        self.height = height
        if isinstance(output, str):
            self.output = os.path.expandvars(os.path.expanduser(output))
        else:
            self.output = output
        self.surface = None
        self.ctx = None

    def _repr_pretty_(self, p, cycle_unused):
        """Plain text repr for the context."""
        # This is implemented just to limit needless changes in notebook files.
        # This gets written to the .ipynb file, and the default includes the
        # memory address, which changes each time.  This string does not.
        p.text(f"<{self.__class__.__module__}.{self.__class__.__name__}>")

    def _repr_html_(self):
        """
        HTML display in Jupyter.

        If output went to a file, display a message saying so.  If output
        didn't go to a file, do nothing and the derived class will implement a
        method to display the output in Jupyter.
        """
        if self.output is not None:
            return f"<b><i>Wrote to {self.output}</i></b>"

    def __enter__(self):
        return self

    def __getattr__(self, name):
        """Proxy to the cairo context, so that we have all the same methods."""
        return getattr(self.ctx, name)


class _CairoSvg(_CairoContext):
    """For creating an SVG drawing in Jupyter."""

    def __init__(self, width: int, height: int, output: str | None = None):
        super().__init__(width, height, output)
        self.svgio = io.BytesIO()
        self.surface = cairo.SVGSurface(self.svgio, self.width, self.height)
        self.ctx = cairo.Context(self.surface)

    def __exit__(self, typ, val, tb):
        self.surface.finish()
        if self.output is not None:
            with open(self.output, "wb") as svgout:
                svgout.write(self.svgio.getvalue())

    def _repr_svg_(self):
        if self.output is None:
            return self.svgio.getvalue().decode()


class _CairoPng(_CairoContext):
    """For creating a PNG drawing in Jupyter."""

    def __init__(self, width: int, height: int, output: str | None = None):
        super().__init__(width, height, output)
        self.pngio = None
        self.surface = cairo.ImageSurface(cairo.Format.RGB24, self.width, self.height)
        self.ctx = cairo.Context(self.surface)

    def __exit__(self, typ, val, tb):
        if self.output is not None:
            self.surface.write_to_png(self.output)
        else:
            self.pngio = io.BytesIO()
            self.surface.write_to_png(self.pngio)
        self.surface.finish()

    def _repr_png_(self):
        if self.output is None:
            return self.pngio.getvalue()


def cairo_context(
    width: int, height: int, format: str = "svg", output: str | None = None
):
    """
    Create a PyCairo context for use in Jupyter.

    Arguments:
        width (int), height (int): the size of the drawing in pixels.
        format (str): either "svg" or "png".
        output (optional str): if provided, the output will be written to this
            file.  If None, the output will be displayed in the Jupyter notebook.

    Returns:
        A PyCairo context proxy.
    """

    if format == "svg":
        cls = _CairoSvg
    elif format == "png":
        cls = _CairoPng
    else:
        raise ValueError(f"Unknown format: {format!r}")
    return cls(width, height, output)
