import collections
import itertools
import math
import random

import numpy as np
from PIL import Image

from drawing import cairo_context
from helpers import color, range2d, closest

def rotations(cls, num_rots=4):
    return map(cls, range(num_rots))

def collect(tile_list, repeat=1, rotations=None, flip=None):
    def _dec(cls):
        rots = rotations
        if rots is None:
            rots = cls.rotations
        will_flip = flip
        if will_flip is None:
            will_flip = cls.flip
        flips = [False, True] if will_flip else [False]
        for _ in range(repeat):
            for rot in range(rots):
                for flipped in flips:
                    tile_list.append(cls(rot=rot, flipped=flipped))
        return cls
    return _dec


def stroke(method):
    method.is_stroke = True
    return method


class TileBase:
    class G:
        def __init__(self, wh, bgfg=None):
            self.wh = wh
            self.bgfg = bgfg
            if self.bgfg is None:
                self.bgfg = [color(1), color(0)]

    rotations = 4
    flip = False

    def __init__(self, rot=0, flipped=False):
        self.rot = rot
        self.flipped = flipped

    def draw_tile(self, ctx, wh, bgfg=None, base_color=None, meth_name="draw"):
        g = self.G(wh, bgfg)
        self.init_tile(ctx, g, base_color=base_color)
        getattr(self, meth_name)(ctx, g)



def tile_value(tile):
    pic = multiscale_truchet(tiles=[tile], width=10, height=10, tilew=10, nlayers=1, format="png")
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
        for t in tiles:
            value = tile_value(t)
            tick(value, 50)
            if inverted:
                tick(1 - value, 50)
        ctx.set_source_rgb(1, 0, 0)
        ctx.set_line_width(2)
        for i in range(11):
            tick(i / 10, 10)
    return ctx


def show_tiles(
    tiles,
    size=100,
    frac=.6,
    width=950,
    with_value=False,
    with_name=False,
    only_one=False,
    sort=True,
):
    if only_one:
        # Keep only one of each class
        classes = {tile.__class__ for tile in tiles}
        tiles = [cls() for cls in classes]
    if with_value:
        values = {t: f"{tile_value(t):.3f}" for t in tiles}
    if sort:
        tiles = sorted(tiles, key=lambda t: t.__class__.__name__)
        if with_value:
            tiles = sorted(tiles, key=values.get)
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

            tile.draw_tile(ctx, wh)

            ctx.rectangle(0, 0, wh, wh)
            ctx.set_source_rgba(0.5, 0.5, 0.5, 0.75)
            ctx.set_line_width(1)
            ctx.set_dash([5, 5], 7.5)
            ctx.stroke()
            ctx.restore()

            if with_value:
                ctx.move_to(2, 10)
                ctx.set_source_rgba(0, 0, 0, 1)
                ctx.show_text(values[tile])

            if with_name:
                ctx.move_to(2, size - 2)
                ctx.set_source_rgba(0, 0, 0, 1)
                ctx.show_text(tile.__class__.__name__)

            ctx.restore()

    return ctx


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
    tiles=None,
    tile_chooser=None,
    width=400,
    height=200,
    tilew=40,
    nlayers=2,
    chance=0.5,
    should_split=None,
    bg=1,
    fg=0,
    seed=None,
    format="svg",
    output=None,
    grid=False,
):
    all_boxes = []

    rand = random.Random(seed)

    if isinstance(tiles, (list, tuple)):
        assert tile_chooser is None
        tile_chooser = lambda ux, uy, uw, ilevel: rand.choice(tiles)

    if isinstance(chance, float):
        _chance = chance
        chance = lambda *a, **k: _chance

    if should_split is None:
        should_split = lambda x, y, size, ilayer: rand.random() <= chance(x, y, size, ilayer)

    def one_tile(x, y, size, ilayer):
        tile = tile_chooser(x / width, y / width, size / width, ilayer)
        with ctx.save_restore():
            ctx.translate(x, y)
            tile.draw_tile(ctx, size, bgfg)
        boxes.append((x, y, size))
        if grid:
            all_boxes.append((x, y, size))

    with cairo_context(width, height, format=format, output=output) as ctx:
        boxes = []
        size = tilew
        bgfg = [color(bg), color(fg)]
        for ox, oy in range2d(int(width / size), int(height / size)):
            one_tile(ox * size, oy * size, size, 0)

        for ilayer in range(nlayers - 1):
            last_boxes = boxes
            bgfg = bgfg[::-1]
            boxes = []
            for bx, by, bsize in last_boxes:
                if should_split(bx / width, by / width, bsize / width, ilayer):
                    nbsize = bsize / 2
                    for dx, dy in range2d(2, 2):
                        nbx, nby = bx + dx * nbsize, by + dy * nbsize
                        one_tile(nbx, nby, nbsize, ilayer-1)

        if grid:
            ctx.set_line_width(.5)
            ctx.set_source_rgb(1, 0, 0)
            for x, y, size in all_boxes:
                ctx.rectangle(x, y, size, size)
                ctx.stroke()

    return ctx


def nearest(levels, data):
    """Find the values in a closest to the values in b"""
    data_shape = data.shape
    linear = data.reshape((math.prod(data_shape),))
    adjusted = levels[np.argmin(np.abs(levels[:, np.newaxis] - linear[np.newaxis, :]), axis=0)]
    return adjusted.reshape(data_shape)


def image_truchet(
    tiles,
    image,
    width=400,
    height=400,
    tilew=40,
    nlayers=1,
    format="svg",
    output=None,
    grid=False,
    seed=None,
    scale=0,
    jitter=0,
    split_thresh=50,
    split_test=2,
):
    rand = random.Random(seed)

    if isinstance(image, str):
        image = np.array(Image.open(image).convert("L"))

    tile_valuess = []
    levelss = []
    all_levels = []
    for half in [0, 1]:
        tile_values = collections.defaultdict(list)
        for tile in tiles:
            value = int(tile_value(tile) * 255)
            if half == 1:
                value = 256 - value
            tile_values[value].append(tile)
        levels = np.array(sorted(tile_values.keys()))
        tile_valuess.append(tile_values)
        levelss.append(levels)
        all_levels.extend(levels)

    lmin, lmax = min(all_levels), max(all_levels)
    imin, imax = np.min(image), np.max(image)
    scale = float(scale)
    lmin *= scale
    lmax = 1 - scale * (1 - lmax)
    imin *= scale
    imax = 1 - scale * (1 - imax)
    image = image - imin    # make a copy of the image
    image /= (imax - imin)
    image *= (lmax - lmin)
    image += lmin

    def tile_chooser(ux, uy, us, ilayer):
        ix = int(ux * image.shape[0])
        iy = int(uy * image.shape[1])
        isize = int(us * image.shape[0])
        color = np.mean(image[iy:iy+isize, ix:ix+isize])
        if jitter:
            color += rand.random() * jitter * 2 - jitter
        close_color = closest(color, levelss[ilayer % 2])
        tiles = tile_valuess[ilayer % 2][close_color]
        return rand.choice(tiles)

    def should_split(ux, uy, us, _):
        nsplit = 2 ** split_test
        ix = int(ux * image.shape[0])
        iy = int(uy * image.shape[1])
        isize = int(us * image.shape[0] / nsplit)
        colors = []
        for dx, dy in range2d(nsplit, nsplit):
            x = ix + dx * isize
            y = iy + dy * isize
            colors.append(np.mean(image[y:y+isize, x:x+isize]))
        lo = min(colors)
        hi = max(colors)
        return (hi - lo) > split_thresh

    return multiscale_truchet(
        tile_chooser=tile_chooser,
        should_split=should_split,
        width=width,
        height=height,
        tilew=tilew,
        nlayers=nlayers,
        bg=1,
        fg=0,
        format=format,
        output=output,
        grid=grid,
        chance=.8,
    )
