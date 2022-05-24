import itertools
import math
import random

from drawing import cairo_context
from helpers import all_subclasses, color


# Compass points for making circle arcs
CE = 0
CS = math.pi / 2
CW = math.pi
CN = -math.pi / 2
FULL_CIRCLE = (0, 2 * math.pi)


class Tile:
    """Multi-scale truchet tiles of my own devising."""

    # +-----+-----+-----+-----+-----+
    # 0    w15   w25   w35   w45    wh
    #               w12
    #   w1a   w3a        w7a    w9a

    def __init__(self, rot=0):
        self.rot = rot

    def init_tile(self, ctx, wh, bgfg=None):
        if bgfg is None:
            bgfg = [color(1), color(0)]
        w12 = wh / 2
        w15 = wh / 5
        w1a = wh / 10
        ctx.arc(0, 0, w15, CS, CE)
        ctx.arc(w12, 0, w1a, CW, CE)
        ctx.arc(wh, 0, w15, CW, CS)
        ctx.arc(wh, w12, w1a, CN, CS)
        ctx.arc(wh, wh, w15, CN, CW)
        ctx.arc(w12, wh, w1a, CE, CW)
        ctx.arc(0, wh, w15, CE, CN)
        ctx.arc(0, w12, w1a, CS, CN)
        ctx.close_path()
        ctx.set_source_rgba(*bgfg[0])
        ctx.fill()
        ctx.set_source_rgba(*bgfg[1])
        ctx.translate(w12, w12)
        ctx.rotate(math.pi / 2 * self.rot)
        ctx.translate(-w12, -w12)

    def edge_dots(self, ctx, wh):
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        for a in [w3a, w7a]:
            for b in [0, wh]:
                ctx.arc(a, b, w1a, *FULL_CIRCLE)
                ctx.fill()
                ctx.arc(b, a, w1a, *FULL_CIRCLE)
                ctx.fill()

    def draw(self, ctx, wh: int):
        ...


class Slash21(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w15 = wh / 5
        w25 = wh * 2 / 5
        w35 = wh * 3 / 5
        w45 = wh * 4 / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc(0, 0, w25, CE, CS)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w15, CS, CE)
        ctx.fill()
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc(0, 0, w45, CE, CS)
        ctx.arc(0, w7a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w35, CS, CE)
        ctx.fill()
        ctx.arc(wh, w3a, w1a, *FULL_CIRCLE)
        ctx.fill()
        ctx.arc(w3a, wh, w1a, *FULL_CIRCLE)
        ctx.fill()
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc_negative(wh, wh, w15, CN, CW)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc(wh, wh, w25, CW, CN)
        ctx.fill()


class ThickSlash(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w12 = wh / 2
        w15 = wh / 5
        w25 = wh * 2 / 5
        w35 = wh * 3 / 5
        w45 = wh * 4 / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc_negative(w12, 0, w1a, CW, CE)
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc(0, 0, w45, CE, CS)
        ctx.arc(0, w7a, w1a, CS, CN)
        ctx.arc_negative(0, w12, w1a, CS, CN)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w15, CS, CE)
        ctx.fill()
        ctx.arc(wh, w3a, w1a, *FULL_CIRCLE)
        ctx.fill()
        ctx.arc(w3a, wh, w1a, *FULL_CIRCLE)
        ctx.fill()
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc_negative(wh, wh, w15, CN, CW)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc(wh, wh, w25, CW, CN)
        ctx.fill()


class Dark34(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w12 = wh / 2
        w15 = wh / 5
        w25 = wh * 2 / 5
        w35 = wh * 3 / 5
        w45 = wh * 4 / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc_negative(w12, 0, w1a, CW, CE)
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc_negative(wh, 0, w15, CW, CS)
        ctx.arc(wh, w3a, w1a, CN, CS)
        ctx.arc_negative(wh, wh, w35, CN, CW)
        ctx.arc(w3a, wh, w1a, CE, CW)
        ctx.arc_negative(0, wh, w15, CE, CN)
        ctx.arc(0, w7a, w1a, CS, CN)
        ctx.arc_negative(0, w12, w1a, CS, CN)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w15, CS, CE)
        ctx.fill()
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc_negative(wh, wh, w15, CN, CW)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc(wh, wh, w25, CW, CN)
        ctx.fill()


class Dark34Deeper(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w12 = wh / 2
        w15 = wh / 5
        w25 = wh * 2 / 5
        w35 = wh * 3 / 5
        w45 = wh * 4 / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc_negative(w12, 0, w1a, CW, CE)
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc_negative(wh, 0, w15, CW, CS)
        ctx.arc(wh, w3a, w1a, CN, CS)
        ctx.arc_negative(w12, w12, w1a, CN, CW)
        ctx.arc(w3a, wh, w1a, CE, CW)
        ctx.arc_negative(0, wh, w15, CE, CN)
        ctx.arc(0, w7a, w1a, CS, CN)
        ctx.arc_negative(0, w12, w1a, CS, CN)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w15, CS, CE)
        ctx.fill()
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc_negative(wh, wh, w15, CN, CW)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc(wh, wh, w25, CW, CN)
        ctx.fill()


class Dark(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w12 = wh / 2
        w15 = wh / 5
        w25 = wh * 2 / 5
        w35 = wh * 3 / 5
        w45 = wh * 4 / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc_negative(w12, 0, w1a, CW, CE)
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc_negative(wh, 0, w15, CW, CS)
        ctx.arc(wh, w3a, w1a, CN, CS)
        ctx.arc_negative(wh, w12, w1a, CN, CS)
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc_negative(wh, wh, w15, CN, CW)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc_negative(w12, wh, w1a, CE, CW)
        ctx.arc(w3a, wh, w1a, CE, CW)
        ctx.arc_negative(0, wh, w15, CE, CN)
        ctx.arc(0, w7a, w1a, CS, CN)
        ctx.arc_negative(0, w12, w1a, CS, CN)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w15, CS, CE)
        ctx.fill()


class DarkSlot(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w12 = wh / 2
        w15 = wh / 5
        w25 = wh * 2 / 5
        w35 = wh * 3 / 5
        w45 = wh * 4 / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc_negative(w12, w12, w1a, CW, CE)
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc_negative(wh, 0, w15, CW, CS)
        ctx.arc(wh, w3a, w1a, CN, CS)
        ctx.arc_negative(wh, w12, w1a, CN, CS)
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc_negative(wh, wh, w15, CN, CW)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc_negative(w12, wh, w1a, CE, CW)
        ctx.arc(w3a, wh, w1a, CE, CW)
        ctx.arc_negative(0, wh, w15, CE, CN)
        ctx.arc(0, w7a, w1a, CS, CN)
        ctx.arc_negative(0, w12, w1a, CS, CN)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w15, CS, CE)
        ctx.fill()


class CornerHash(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w15 = wh / 5
        w25 = wh * 2 / 5
        w35 = wh * 3 / 5
        w45 = wh * 4 / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc(0, 0, w25, CE, CS)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w15, CS, CE)
        ctx.fill()
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc_negative(wh, 0, w15, CW, CS)
        ctx.arc(wh, w3a, w1a, CN, CS)
        ctx.arc(wh, 0, w25, CS, CW)
        ctx.fill()
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc_negative(wh, wh, w15, CN, CW)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc(wh, wh, w25, CW, CN)
        ctx.fill()
        ctx.arc(0, w7a, w1a, CS, CN)
        ctx.arc(0, wh, w25, CN, CE)
        ctx.arc(w3a, wh, w1a, CE, CW)
        ctx.arc_negative(0, wh, w15, CE, CN)
        ctx.fill()


class Bikini(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w12 = wh / 2
        w15 = wh / 5
        w25 = wh * 2 / 5
        w35 = wh * 3 / 5
        w45 = wh * 4 / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc_negative(w12, 0, w1a, CW, CE)
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc_negative(wh, 0, w15, CW, CS)
        ctx.arc(wh, w3a, w1a, CN, CS)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w15, CS, CE)
        ctx.fill()
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc_negative(wh, wh, w15, CN, CW)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc(wh, wh, w25, CW, CN)
        ctx.fill()
        ctx.arc(0, w7a, w1a, CS, CN)
        ctx.arc(0, wh, w25, CN, CE)
        ctx.arc(w3a, wh, w1a, CE, CW)
        ctx.arc_negative(0, wh, w15, CE, CN)
        ctx.fill()


class Bridge(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w12 = wh / 2
        w15 = wh / 5
        w25 = wh * 2 / 5
        w35 = wh * 3 / 5
        w45 = wh * 4 / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc_negative(w12, 0, w1a, CW, CE)
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc_negative(wh, 0, w15, CW, CS)
        ctx.arc(wh, w3a, w1a, CN, CS)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w15, CS, CE)
        ctx.fill()
        ctx.arc(wh, w7a, w1a, *FULL_CIRCLE)
        ctx.fill()
        ctx.arc(w7a, wh, w1a, *FULL_CIRCLE)
        ctx.fill()
        ctx.arc(w3a, wh, w1a, *FULL_CIRCLE)
        ctx.fill()
        ctx.arc(0, w7a, w1a, *FULL_CIRCLE)
        ctx.fill()


class EdgeHash(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w12 = wh / 2
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc_negative(w12, 0, w1a, CW, CE)
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc(w12, 0, w3a, CE, CW)
        ctx.fill()
        ctx.arc(wh, w3a, w1a, CN, CS)
        ctx.arc_negative(wh, w12, w1a, CN, CS)
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc(wh, w12, w3a, CS, CN)
        ctx.fill()
        ctx.arc(w3a, wh, w1a, CE, CW)
        ctx.arc(w12, wh, w3a, CW, CE)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc_negative(w12, wh, w1a, CE, CW)
        ctx.fill()
        ctx.arc(0, w7a, w1a, CS, CN)
        ctx.arc_negative(0, w12, w1a, CS, CN)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc(0, w12, w3a, CN, CS)
        ctx.fill()


class EdgeHash34(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w12 = wh / 2
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc_negative(w12, 0, w1a, CW, CE)
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc(w12, 0, w3a, CE, CW)
        ctx.fill()
        ctx.arc(wh, w3a, w1a, CN, CS)
        ctx.arc_negative(wh, w12, w1a, CN, CS)
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc(wh, w12, w3a, CS, CN)
        ctx.fill()
        ctx.arc(w3a, wh, w1a, CE, CW)
        ctx.arc(w12, wh, w3a, CW, CE)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc_negative(w12, wh, w1a, CE, CW)
        ctx.fill()
        ctx.arc(0, w7a, w1a, *FULL_CIRCLE)
        ctx.fill()
        ctx.arc(0, w3a, w1a, *FULL_CIRCLE)
        ctx.fill()


class CornerHash34(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w15 = wh / 5
        w25 = wh * 2 / 5
        w35 = wh * 3 / 5
        w45 = wh * 4 / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc(0, 0, w25, CE, CS)
        ctx.arc(0, w3a, w1a, CS, CN)
        ctx.arc_negative(0, 0, w15, CS, CE)
        ctx.fill()
        ctx.arc(w7a, 0, w1a, CW, CE)
        ctx.arc_negative(wh, 0, w15, CW, CS)
        ctx.arc(wh, w3a, w1a, CN, CS)
        ctx.arc(wh, 0, w25, CS, CW)
        ctx.fill()
        ctx.arc(wh, w7a, w1a, CN, CS)
        ctx.arc_negative(wh, wh, w15, CN, CW)
        ctx.arc(w7a, wh, w1a, CE, CW)
        ctx.arc(wh, wh, w25, CW, CN)
        ctx.fill()
        ctx.arc(0, w7a, w1a, *FULL_CIRCLE)
        ctx.arc(w3a, wh, w1a, *FULL_CIRCLE)
        ctx.fill()


class Hash(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w1a = wh / 10
        w3a = wh * 3 / 10
        w7a = wh * 7 / 10
        for a in [w3a, w7a]:
            ctx.arc(a, 0, w1a, CW, CE)
            ctx.arc(a, wh, w1a, CE, CW)
            ctx.fill()
            ctx.arc(0, a, w1a, CS, CN)
            ctx.arc(wh, a, w1a, CN, CS)
            ctx.fill()


class CornerHashDot(CornerHash):
    def draw(self, ctx, wh, bgfg=None):
        super().draw(ctx, wh, bgfg)
        ctx.arc(wh / 2, wh / 2, wh / 10, *FULL_CIRCLE)
        ctx.fill()


class Empty(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        self.edge_dots(ctx, wh)


class DarkMoon(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        self.edge_dots(ctx, wh)
        ctx.arc(wh / 2, wh / 2, wh * 3 / 10, *FULL_CIRCLE)
        ctx.fill()


class CulDeSac(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        self.edge_dots(ctx, wh)
        w12 = wh / 2
        w15 = wh / 5
        w1a = wh / 10
        w3a = wh * 3 / 10
        ctx.arc(w3a, 0, w1a, CW, CE)
        ctx.arc_negative(w12, w1a, w1a, CW, CS)
        ctx.arc(wh / 2, wh / 2, wh * 3 / 10, CN, CW)
        ctx.fill()


class Donut(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        self.edge_dots(ctx, wh)
        w12 = wh / 2
        ctx.arc(w12, w12, wh * 3 / 10, CN - 1, CS + 1)
        ctx.arc_negative(w12, w12, wh / 10, CS, CN)
        ctx.fill()
        ctx.arc(w12, w12, wh * 3 / 10, CS, CN)
        ctx.arc_negative(w12, w12, wh / 10, CN, CS)
        ctx.fill()


def rotations(cls, num_rots):
    return map(cls, range(num_rots))


n5_classes = all_subclasses(Tile)

n5_demo = [c() for c in n5_classes]

n5_tiles = list(itertools.chain.from_iterable(rotations(c, 4) for c in n5_classes))
