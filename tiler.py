import itertools
import math
import random

from drawing import cairo_context
from helpers import color, range2d


def tile_value(tile):
    pic = multiscale(tiles=[tile], width=10, height=10, tilew=10, nlayers=1, format="png")
    import numpy as np
    from PIL import Image

    a = np.array(Image.open(pic.pngio).convert("L"))
    value = np.sum(a) / a.size
    return value / 255


def value_chart(tiles, inverted=False):
    marg = 50
    width = 800
    mid = 50

    def tick(x, h):
        v = (width - 2 * marg) * x + marg
        ctx.move_to(v, mid - h / 2)
        ctx.line_to(v, mid + h / 2)
        ctx.stroke()

    with cairo_context(width, mid * 2) as ctx:
        ctx.set_line_width(0.5)
        ctx.move_to(marg, mid)
        ctx.line_to(width - marg, mid)
        ctx.stroke()
        tick(0, 20)
        tick(1, 20)
        for i in range(10):
            tick(i / 10, 10)
        for t in tiles:
            value = tile_value(t)
            tick(value, 50)
            if inverted:
                tick(1 - value, 50)
    return ctx


def show_tiles(tiles, size=100, frac=.6, width=950, with_value=False, with_name=False, only_one=False, sort=True):
    if only_one:
        # Keep only one of each class
        classes = {tile.__class__ for tile in tiles}
        tiles = [cls() for cls in classes]
    if sort:
        tiles = sorted(tiles, key=lambda t: t.__class__.__name__)
    wh = size * frac
    gap = size / 10
    per_row = (width + gap) // (size + gap)
    nrows = len(tiles) // per_row + (1 if len(tiles) % per_row else 0)
    ncols = per_row if nrows > 1 else len(tiles)
    totalW = (size + gap) * ncols - gap
    totalH = (size + gap) * nrows - gap
    with cairo_context(totalW, totalH) as ctx:
        ctx.select_font_face("Sans")
        ctx.set_font_size(10)
        for i, tile in enumerate(tiles):
            r, c = divmod(i, per_row)
            ctx.save()
            ctx.translate((size + gap) * c, (size + gap) * r)
            ctx.rectangle(0, 0, size, size)
            ctx.set_source_rgb(0.85, 0.85, 0.85)
            ctx.fill()

            ctx.save()
            ctx.translate((size - wh) / 2, (size - wh) / 2)

            g = tile.G(wh)
            tile.init_tile(ctx, g)
            tile.draw(ctx, g)

            ctx.rectangle(0, 0, wh, wh)
            ctx.set_source_rgba(0.5, 0.5, 0.5, 0.75)
            ctx.set_line_width(1)
            ctx.set_dash([5, 5], 7.5)
            ctx.stroke()
            ctx.restore()

            if with_value:
                ctx.move_to(2, 10)
                ctx.set_source_rgba(0, 0, 0, 1)
                ctx.show_text(f"{tile_value(tile):.2f}")

            if with_name:
                ctx.move_to(2, size - 2)
                ctx.set_source_rgba(0, 0, 0, 1)
                ctx.show_text(tile.__class__.__name__)

            ctx.restore()

    return ctx


def rotations(cls, num_rots):
    return map(cls, range(num_rots))

def show_overlap(tile):
    W = 200
    bgfg = [color(1), color(0)]
    with cairo_context(W, W) as ctx:
        ctx.rectangle(0, 0, W, W)
        ctx.set_source_rgb(.75, .75, .75)
        ctx.fill()
        ctx.save()
        ctx.translate(W/4, W/4)
        tile.draw(ctx, W/2, bgfg)
        ctx.restore()
        offset = 0
        bgfg = [color((0, 0, .7)), color((1, .5, .5))]
        for x, y in itertools.product([0, 1], repeat=2):
            ctx.save()
            ctx.translate(W/4 + x * W/4 + offset, W/4 + y * W/4 + offset)
            tile.draw(ctx, W/4, bgfg)
            ctx.restore()
    return ctx


def multiscale_truchet(
    tiles,
    width=400,
    height=200,
    tilew=40,
    nlayers=2,
    chance=0.5,
    bg=1,
    fg=0,
    seed=None,
    format="svg",
    output=None,
    grid=False,
):
    all_boxes = []

    if isinstance(chance, float):
        _chance = chance
        chance = lambda *a, **k: _chance

    def one_tile(x, y, size):
        ctx.save()
        ctx.translate(x, y)
        tile = rand.choice(tiles)
        g = tile.G(size, bgfg)
        tile.init_tile(ctx, g)
        tile.draw(ctx, g)
        ctx.restore()
        boxes.append((x, y, size))
        if grid:
            all_boxes.append((x, y, size))

    rand = random.Random(seed)
    with cairo_context(width, height, format=format, output=output) as ctx:
        boxes = []
        size = tilew
        bgfg = [color(bg), color(fg)]
        for ox, oy in range2d(int(width / size), int(height / size)):
            one_tile(ox * size, oy * size, size)

        for ilayer in range(nlayers - 1):
            last_boxes = boxes
            bgfg = bgfg[::-1]
            boxes = []
            for bx, by, bsize in last_boxes:
                if rand.random() <= chance(bx, by, bsize):
                    for dx, dy in range2d(2, 2):
                        nbsize = bsize / 2
                        nbx, nby = bx + dx * nbsize, by + dy * nbsize
                        one_tile(nbx, nby, nbsize)

        if grid:
            for x, y, size in all_boxes:
                ctx.set_line_width(.5)
                ctx.rectangle(x, y, size, size)
                ctx.set_source_rgb(1, 0, 0)
                ctx.stroke()

    return ctx