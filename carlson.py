import math
import random

from helpers import cairo_context, color, range2d


# Compass points for making circle arcs
CE = 0
CS = math.pi / 2
CW = math.pi
CN = -math.pi / 2
FULL_CIRCLE = (0, 2 * math.pi)


class CarlsonTile:
    """https://christophercarlson.com/portfolio/multi-scale-truchet-patterns/"""

    def __init__(self, rot=0):
        self.rot = rot

    def init_tile(self, ctx, wh, bgfg=None):
        if bgfg is None:
            bgfg = [color(1), color(0)]
        wh1 = wh / 3
        wh2 = wh / 2
        ctx.arc(0, 0, wh1, CS, CE)
        ctx.arc(wh, 0, wh1, CW, CS)
        ctx.arc(wh, wh, wh1, CN, CW)
        ctx.arc(0, wh, wh1, CE, CN)
        ctx.close_path()
        ctx.set_source_rgba(*bgfg[0])
        ctx.fill()
        ctx.set_source_rgba(*bgfg[1])
        ctx.translate(wh2, wh2)
        ctx.rotate(math.pi / 2 * self.rot)
        ctx.translate(-wh2, -wh2)

    def draw(self, ctx, wh: int):
        ...


class CarlsonSlash(CarlsonTile):
    def draw(self, ctx, wh, bgfg=None):
        wh1 = wh / 3
        wh2 = wh / 2
        wh3 = wh - wh1
        wh6 = wh / 6
        self.init_tile(ctx, wh, bgfg)
        ctx.arc(wh2, 0, wh6, CW, CE)
        ctx.arc_negative(wh, 0, wh1, CW, CS)
        ctx.arc(wh, wh2, wh6, CN, CS)
        ctx.arc(wh, 0, wh3, CS, CW)
        ctx.fill()
        ctx.arc(0, wh2, wh6, CS, CN)
        ctx.arc(0, wh, wh3, CN, CE)
        ctx.arc(wh2, wh, wh6, CE, CW)
        ctx.arc_negative(0, wh, wh1, CE, CN)
        ctx.fill()


class CarlsonMinus(CarlsonTile):
    def draw(self, ctx, wh, bgfg=None):
        wh1 = wh / 3
        wh2 = wh / 2
        wh3 = wh - wh1
        wh6 = wh / 6
        self.init_tile(ctx, wh, bgfg)
        ctx.arc(wh2, 0, wh6, *FULL_CIRCLE)
        ctx.fill()
        ctx.arc(wh, wh2, wh6, CN, CS)
        ctx.arc(0, wh2, wh6, CS, CN)
        ctx.close_path()
        ctx.fill()
        ctx.arc(wh2, wh, wh6, *FULL_CIRCLE)
        ctx.fill()


class CarlsonFour(CarlsonTile):
    def draw(self, ctx, wh, bgfg=None):
        wh2 = wh / 2
        wh6 = wh / 6
        self.init_tile(ctx, wh, bgfg)
        for x, y in [(wh2, 0), (wh, wh2), (wh2, wh), (0, wh2)]:
            ctx.arc(x, y, wh6, *FULL_CIRCLE)
            ctx.fill()


class CarlsonX(CarlsonTile):
    def draw(self, ctx, wh, bgfg=None):
        wh1 = wh / 3
        wh2 = wh / 2
        wh6 = wh / 6
        self.init_tile(ctx, wh, bgfg)
        ctx.arc(wh2, 0, wh6, CW, CE)
        ctx.arc_negative(wh, 0, wh1, CW, CS)
        ctx.arc(wh, wh2, wh6, CN, CS)
        ctx.arc_negative(wh, wh, wh1, CN, CW)
        ctx.arc(wh2, wh, wh6, CE, CW)
        ctx.arc_negative(0, wh, wh1, CE, CN)
        ctx.arc(0, wh2, wh6, CS, CN)
        ctx.arc_negative(0, 0, wh1, CS, CE)
        ctx.fill()


class CarlsonPlus(CarlsonTile):
    def draw(self, ctx, wh, bgfg=None):
        wh2 = wh / 2
        wh6 = wh / 6
        self.init_tile(ctx, wh, bgfg)
        ctx.arc(wh, wh2, wh6, CN, CS)
        ctx.arc(0, wh2, wh6, CS, CN)
        ctx.close_path()
        ctx.fill()
        ctx.arc(wh2, 0, wh6, CW, CE)
        ctx.arc(wh2, wh, wh6, CE, CW)
        ctx.close_path()
        ctx.fill()


class CarlsonFrown(CarlsonTile):
    def draw(self, ctx, wh, bgfg=None):
        wh1 = wh / 3
        wh2 = wh / 2
        wh3 = wh - wh1
        wh6 = wh / 6
        self.init_tile(ctx, wh, bgfg)
        ctx.arc(wh2, 0, wh6, CW, CE)
        ctx.arc_negative(wh, 0, wh1, CW, CS)
        ctx.arc(wh, wh2, wh6, CN, CS)
        ctx.arc(wh, 0, wh3, CS, CW)
        ctx.fill()
        ctx.arc(wh2, wh, wh6, *FULL_CIRCLE)
        ctx.fill()
        ctx.arc(0, wh2, wh6, *FULL_CIRCLE)
        ctx.fill()


class CarlsonT(CarlsonTile):
    def draw(self, ctx, wh, bgfg=None):
        wh1 = wh / 3
        wh2 = wh / 2
        wh6 = wh / 6
        self.init_tile(ctx, wh, bgfg)
        ctx.arc(wh2, 0, wh6, CW, CE)
        ctx.arc_negative(wh, 0, wh1, CW, CS)
        ctx.arc(wh, wh2, wh6, CN, CS)
        ctx.arc(0, wh2, wh6, CS, CN)
        ctx.arc_negative(0, 0, wh1, CS, CE)
        ctx.fill()
        ctx.arc(wh2, wh, wh6, *FULL_CIRCLE)
        ctx.fill()


def show_tiles(tiles, per_row=5):
    W = 100
    wh = 50
    gap = 10
    nrows = len(tiles) // per_row + (1 if len(tiles) % per_row else 0)
    ncols = per_row if nrows > 1 else len(tiles)
    totalW = (W + gap) * ncols - gap
    totalH = (W + gap) * nrows - gap
    with cairo_context(totalW, totalH) as ctx:
        for i, tile in enumerate(tiles):
            r, c = divmod(i, per_row)
            ctx.save()
            ctx.translate((W + gap) * c, (W + gap) * r)
            ctx.rectangle(0, 0, W, W)
            ctx.set_source_rgb(0.85, 0.85, 0.85)
            ctx.fill()

            ctx.translate((W - wh) / 2, (W - wh) / 2)
            tile.draw(ctx, wh)

            ctx.rectangle(0, 0, wh, wh)
            ctx.set_source_rgba(0.5, 0.5, 0.5, 0.75)
            ctx.set_line_width(1)
            ctx.set_dash([5, 5], 7.5)
            ctx.stroke()

            ctx.restore()

    return ctx


def rotations(cls, num_rots):
    return map(cls, range(num_rots))


carlson_tiles = [
    *rotations(CarlsonSlash, 2),
    *rotations(CarlsonMinus, 2),
    CarlsonFour(),
    CarlsonX(),
    CarlsonPlus(),
    *rotations(CarlsonFrown, 4),
    *rotations(CarlsonT, 4),
]


def carlson(
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
):
    rand = random.Random(seed)
    with cairo_context(width, height, format=format, output=output) as ctx:
        boxes = set()
        size = tilew
        bgfg = [color(bg), color(fg)]
        for ox, oy in range2d(int(width / size), int(height / size)):
            ctx.save()
            ctx.translate(ox * size, oy * size)
            rand.choice(carlson_tiles).draw(ctx, size, bgfg)
            ctx.restore()
            boxes.add((ox * size, oy * size, size))

        for ilayer in range(nlayers - 1):
            last_boxes = boxes
            bgfg = bgfg[::-1]
            boxes = set()
            for bx, by, bsize in last_boxes:
                if rand.random() <= chance:
                    for dx, dy in range2d(2, 2):
                        nbsize = bsize / 2
                        nbx, nby = bx + dx * nbsize, by + dy * nbsize
                        ctx.save()
                        ctx.translate(nbx, nby)
                        rand.choice(carlson_tiles).draw(ctx, nbsize, bgfg)
                        ctx.restore()
                        boxes.add((nbx, nby, nbsize))

    return ctx
