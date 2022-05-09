import math
import random

from helpers import range2d, show_svg, svg_context

PI = math.pi
PI2 = math.pi / 2


class CarlsonTile:
    """https://christophercarlson.com/portfolio/multi-scale-truchet-patterns/"""

    def __init__(self, rot, bw=1):
        self.bg = [bw] * 3
        self.fg = [1 - bw] * 3
        self.rot = rot

    def init_tile(self, ctx, wh):
        wh1 = wh / 3
        wh2 = wh / 2
        ctx.arc(0, 0, wh1, PI2, 0)
        ctx.arc(wh, 0, wh1, PI, PI2)
        ctx.arc(wh, wh, wh1, -PI2, PI)
        ctx.arc(0, wh, wh1, 0, -PI2)
        ctx.close_path()
        ctx.set_source_rgb(*self.bg)
        ctx.fill()
        ctx.set_source_rgb(*self.fg)
        ctx.translate(wh2, wh2)
        ctx.rotate(PI2 * self.rot)
        ctx.translate(-wh2, -wh2)

    def draw(self, ctx, wh: int):
        ...


class CarlsonSlash(CarlsonTile):
    def draw(self, ctx, wh: int):
        wh1 = wh / 3
        wh2 = wh / 2
        wh3 = wh - wh1
        wh6 = wh / 6
        self.init_tile(ctx, wh)
        ctx.arc(wh2, 0, wh6, PI, 0)
        ctx.arc_negative(wh, 0, wh1, PI, PI2)
        ctx.arc(wh, wh2, wh6, -PI2, PI2)
        ctx.arc(wh, 0, wh3, PI2, PI)
        ctx.fill()
        ctx.arc(0, wh2, wh6, PI2, -PI2)
        ctx.arc(0, wh, wh3, -PI2, 0)
        ctx.arc(wh2, wh, wh6, 0, PI)
        ctx.arc_negative(0, wh, wh1, 0, -PI2)
        ctx.fill()


class CarlsonMinus(CarlsonTile):
    def draw(self, ctx, wh: int):
        wh1 = wh / 3
        wh2 = wh / 2
        wh3 = wh - wh1
        wh6 = wh / 6
        self.init_tile(ctx, wh)
        ctx.arc(wh2, 0, wh6, 0, 2 * PI)
        ctx.fill()
        ctx.arc(wh, wh2, wh6, -PI2, PI2)
        ctx.arc(0, wh2, wh6, PI2, -PI2)
        ctx.close_path()
        ctx.fill()
        ctx.arc(wh2, wh, wh6, 0, 2 * PI)
        ctx.fill()


class CarlsonFour(CarlsonTile):
    def draw(self, ctx, wh: int):
        wh2 = wh / 2
        wh6 = wh / 6
        self.init_tile(ctx, wh)
        for x, y in [(wh2, 0), (wh, wh2), (wh2, wh), (0, wh2)]:
            ctx.arc(x, y, wh6, 0, 2 * PI)
            ctx.fill()


class CarlsonX(CarlsonTile):
    def draw(self, ctx, wh: int):
        wh1 = wh / 3
        wh2 = wh / 2
        wh6 = wh / 6
        self.init_tile(ctx, wh)
        ctx.arc(wh2, 0, wh6, PI, 0)
        ctx.arc_negative(wh, 0, wh1, PI, PI2)
        ctx.arc(wh, wh2, wh6, -PI2, PI2)
        ctx.arc_negative(wh, wh, wh1, -PI2, PI)
        ctx.arc(wh2, wh, wh6, 0, PI)
        ctx.arc_negative(0, wh, wh1, 0, -PI2)
        ctx.arc(0, wh2, wh6, PI2, -PI2)
        ctx.arc_negative(0, 0, wh1, PI2, 0)
        ctx.fill()


class CarlsonPlus(CarlsonTile):
    def draw(self, ctx, wh: int):
        wh2 = wh / 2
        wh6 = wh / 6
        self.init_tile(ctx, wh)
        ctx.arc(wh, wh2, wh6, -PI2, PI2)
        ctx.arc(0, wh2, wh6, PI2, -PI2)
        ctx.close_path()
        ctx.fill()
        ctx.arc(wh2, 0, wh6, PI, 0)
        ctx.arc(wh2, wh, wh6, 0, PI)
        ctx.close_path()
        ctx.fill()


class CarlsonFrown(CarlsonTile):
    def draw(self, ctx, wh: int):
        wh1 = wh / 3
        wh2 = wh / 2
        wh3 = wh - wh1
        wh6 = wh / 6
        self.init_tile(ctx, wh)
        ctx.arc(wh2, 0, wh6, PI, 0)
        ctx.arc_negative(wh, 0, wh1, PI, PI2)
        ctx.arc(wh, wh2, wh6, -PI2, PI2)
        ctx.arc(wh, 0, wh3, PI2, PI)
        ctx.fill()
        ctx.arc(wh2, wh, wh6, 0, 2 * PI)
        ctx.fill()
        ctx.arc(0, wh2, wh6, 0, 2 * PI)
        ctx.fill()


class CarlsonT(CarlsonTile):
    def draw(self, ctx, wh: int):
        wh1 = wh / 3
        wh2 = wh / 2
        wh6 = wh / 6
        self.init_tile(ctx, wh)
        ctx.arc(wh2, 0, wh6, PI, 0)
        ctx.arc_negative(wh, 0, wh1, PI, PI2)
        ctx.arc(wh, wh2, wh6, -PI2, PI2)
        ctx.arc(0, wh2, wh6, PI2, -PI2)
        ctx.arc_negative(0, 0, wh1, PI2, 0)
        ctx.fill()
        ctx.arc(wh2, wh, wh6, 0, 2 * PI)
        ctx.fill()


def show_tiles(tiles, per_row=5):
    W = 100
    wh = 50
    gap = 10
    nrows = len(tiles) // per_row + (1 if len(tiles) % per_row else 0)
    ncols = per_row if nrows > 1 else len(tiles)
    totalW = (W + gap) * ncols - gap
    totalH = (W + gap) * nrows - gap
    with svg_context(totalW, totalH) as ctx:
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

    return show_svg(ctx)


carlson_classes = [
    (CarlsonSlash, 0),
    (CarlsonSlash, 1),
    (CarlsonMinus, 0),
    (CarlsonMinus, 1),
    (CarlsonFour, 0),
    (CarlsonX, 0),
    (CarlsonPlus, 0),
    (CarlsonFrown, 0),
    (CarlsonFrown, 2),
    (CarlsonFrown, 3),
    (CarlsonFrown, 1),
    (CarlsonT, 0),
    (CarlsonT, 2),
    (CarlsonT, 1),
    (CarlsonT, 3),
]

carlson_tiles = [[cls(rot, bw=bw) for cls, rot in carlson_classes] for bw in [1, 0]]


def carlson(width=400, height=200, tilew=40, nlayers=2, chance=0.5):
    with svg_context(width, height) as ctx:
        boxes = set()
        size = tilew
        for ox, oy in range2d(int(width / size), int(height / size)):
            ctx.save()
            ctx.translate(ox * size, oy * size)
            random.choice(carlson_tiles[0]).draw(ctx, size)
            ctx.restore()
            boxes.add((ox * size, oy * size, size))

        for ilayer in range(nlayers - 1):
            last_boxes = boxes
            boxes = set()
            for bx, by, bsize in last_boxes:
                if random.random() <= chance:
                    for dx, dy in range2d(2, 2):
                        nbsize = bsize / 2
                        nbx, nby = bx + dx * nbsize, by + dy * nbsize
                        ctx.save()
                        ctx.translate(nbx, nby)
                        random.choice(carlson_tiles[(ilayer + 1) % 2]).draw(ctx, nbsize)
                        ctx.restore()
                        boxes.add((nbx, nby, nbsize))
    return show_svg(ctx)
