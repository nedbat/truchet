import math

from helpers import all_subclasses, color


# Compass points for making circle arcs
CE = 0
CS = math.pi / 2
CW = math.pi
CN = -math.pi / 2
FULL_CIRCLE = (0, 2 * math.pi)


def rotations(cls, num_rots=4):
    return map(cls, range(num_rots))

def collect(tile_list, repeat=1, rotations=None):
    def _dec(cls):
        rots = rotations or cls.rotations
        for _ in range(repeat):
            tile_list.extend(map(cls, range(rots)))
        return cls
    return _dec

n6_tiles = []
n6_connected = []

class Tile:
    """Multi-scale truchet tiles of my own devising."""

    # +-----+-----+---------+-----+-----+
    # 0    w16   w26       w46   w56    wh
    #                 w12
    #   w1c   w3c            w9c    wbc

    rotations = 4

    def __init__(self, rot=0):
        self.rot = rot

    def init_tile(self, ctx, wh, bgfg=None):
        if bgfg is None:
            bgfg = [color(1), color(0)]
        w16 = wh / 6
        w12 = wh / 2
        ctx.arc(0, 0, w16, CS, CE)
        ctx.arc(w12, 0, w16, CW, CE)
        ctx.arc(wh, 0, w16, CW, CS)
        ctx.arc(wh, w12, w16, CN, CS)
        ctx.arc(wh, wh, w16, CN, CW)
        ctx.arc(w12, wh, w16, CE, CW)
        ctx.arc(0, wh, w16, CE, CN)
        ctx.arc(0, w12, w16, CS, CN)
        ctx.close_path()
        ctx.set_source_rgba(*bgfg[0])
        ctx.fill()
        ctx.set_source_rgba(*bgfg[1])
        ctx.translate(w12, w12)
        ctx.rotate(math.pi / 2 * self.rot)
        ctx.translate(-w12, -w12)

    def dot(self, ctx, wh, x, y):
        w1c = wh / 12
        ctx.arc(x, y, w1c, *FULL_CIRCLE)
        ctx.fill()

    def edge_dots(self, ctx, wh):
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        for a in [w3c, w9c]:
            for b in [0, wh]:
                self.dot(ctx, wh, a, b)
                self.dot(ctx, wh, b, a)

    def four_corners(self, ctx, wh):
        w1c = wh / 12
        w3c = wh * 3 / 12
        w16 = wh / 6
        w26 = wh * 2 / 6
        ctx.save()
        for _ in range(4):
            ctx.arc(w3c, 0, w1c, CW, CE)
            ctx.arc(0, 0, w26, CE, CS)
            ctx.arc(0, w3c, w1c, CS, CN)
            ctx.arc_negative(0, 0, w16, CS, CE)
            ctx.fill()
            ctx.translate(wh, 0)
            ctx.rotate(math.pi / 2)
        ctx.restore()

    def slash(self, ctx, wh):
        w1c = wh / 12
        w9c = wh * 9 / 12
        w46 = wh * 4 / 6
        w56 = wh * 5 / 6
        ctx.save()
        ctx.arc(w9c, 0, w1c, CW, CE)
        ctx.arc(0, 0, w56, CE, CS)
        ctx.arc(0, w9c, w1c, CS, CN)
        ctx.arc_negative(0, 0, w46, CS, CE)
        ctx.fill()
        ctx.restore()

    def slash_cross(self, ctx, wh, bgfg):
        w1c = wh / 12
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        w46 = wh * 4 / 6
        w56 = wh * 5 / 6
        ctx.save()
        ctx.arc(w3c, 0, w1c, CW, CE)
        ctx.arc_negative(wh, 0, w46, CW, CS)
        ctx.arc(wh, w9c, w1c, CN, CS)
        ctx.arc(wh, 0, w56, CS, CW)
        ctx.fill()
        ctx.set_source_rgba(*(bgfg or [color(1)])[0])
        ctx.arc(0, 0, w46, CE, CS)
        ctx.arc_negative(0, 0, w46 - wh / 24, CS, CE)
        ctx.fill()
        ctx.arc_negative(0, 0, w56, CS, CE)
        ctx.arc(0, 0, w56 + wh / 24, CE, CS)
        ctx.fill()
        ctx.restore()

    def top_edge(self, ctx, wh):
        w1c = wh / 12
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        w12 = wh / 2
        w16 = wh / 6
        w26 = wh * 2 / 6
        ctx.save()
        ctx.arc(w3c, 0, w1c, CW, CE)
        ctx.arc_negative(w12, 0, w16, CW, CE)
        ctx.arc(w9c, 0, w1c, CW, CE)
        ctx.arc(w12, 0, w26, CE, CW)
        ctx.fill()
        ctx.restore()

    def ell(self, ctx, wh):
        w1c = wh / 12
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        w16 = wh / 6
        w26 = wh * 2 / 6
        w12 = wh / 2
        ctx.save()
        ctx.arc(w9c, 0, w1c, CW, CE)
        ctx.arc(w12, 0, w26, CE, CS)
        ctx.arc(0, w3c, w1c, CS, CN)
        ctx.arc_negative(w12, 0, w16, CS, CE)
        ctx.fill()
        ctx.restore()

    def draw(self, ctx, wh: int):
        ...


@collect(n6_tiles)
class Slash21(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w1c = wh / 12
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        w16 = wh / 6
        w26 = wh * 2 / 6
        ctx.arc(w3c, 0, w1c, CW, CE)
        ctx.arc(0, 0, w26, CE, CS)
        ctx.arc(0, w3c, w1c, CS, CN)
        ctx.arc_negative(0, 0, w16, CS, CE)
        ctx.fill()
        self.slash(ctx, wh)
        self.dot(ctx, wh, wh, w3c)
        self.dot(ctx, wh, w3c, wh)
        ctx.arc(wh, w9c, w1c, CN, CS)
        ctx.arc_negative(wh, wh, w16, CN, CW)
        ctx.arc(w9c, wh, w1c, CE, CW)
        ctx.arc(wh, wh, w26, CW, CN)
        ctx.fill()

@collect(n6_tiles)
class SlashCross(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        self.slash(ctx, wh)
        self.slash_cross(ctx, wh, bgfg)
        self.dot(ctx, wh, wh, w3c)
        self.dot(ctx, wh, w3c, wh)
        self.dot(ctx, wh, 0, w3c)
        self.dot(ctx, wh, w9c, wh)


@collect(n6_tiles)
@collect(n6_connected)
class EdgeHash(Tile):
    rotations = 1
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        for _ in range(4):
            self.top_edge(ctx, wh)
            ctx.translate(wh, 0)
            ctx.rotate(math.pi / 2)

@collect(n6_tiles)
class HourGlass(Tile):
    rotations = 2
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        ctx.save()
        for _ in range(2):
            self.top_edge(ctx, wh)
            ctx.translate(wh, wh)
            ctx.rotate(math.pi)
        ctx.restore()
        for x in [0, wh]:
            for y in [w3c, w9c]:
                self.dot(ctx, wh, x, y)

@collect(n6_tiles)
class ThatWay(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        self.top_edge(ctx, wh)
        self.dot(ctx, wh, 0, w3c)
        self.dot(ctx, wh, wh, w3c)
        self.dot(ctx, wh, 0, w9c)
        self.dot(ctx, wh, w9c, wh)
        ctx.save()
        ctx.translate(wh, wh)
        ctx.rotate(math.pi)
        self.ell(ctx, wh)
        ctx.restore()

@collect(n6_tiles)
class ThoseWays(Tile):
    rotations = 2
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        self.dot(ctx, wh, w3c, 0)
        self.dot(ctx, wh, wh, w3c)
        self.dot(ctx, wh, 0, w9c)
        self.dot(ctx, wh, w9c, wh)
        self.ell(ctx, wh)
        ctx.save()
        ctx.translate(wh, wh)
        ctx.rotate(math.pi)
        self.ell(ctx, wh)
        ctx.restore()

@collect(n6_tiles)
class ThoseWaysX(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        self.top_edge(ctx, wh)
        self.dot(ctx, wh, w3c, 0)
        self.dot(ctx, wh, wh, w3c)
        self.dot(ctx, wh, 0, w9c)
        self.dot(ctx, wh, w9c, wh)
        self.ell(ctx, wh)
        ctx.save()
        ctx.translate(wh, wh)
        ctx.rotate(math.pi)
        self.ell(ctx, wh)
        ctx.restore()

@collect(n6_tiles)
@collect(n6_connected)
class CornerHash(Tile):
    rotations = 1
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        self.four_corners(ctx, wh)

@collect(n6_tiles)
class SadFace(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w1c = wh / 12
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        w16 = wh / 6
        w26 = wh * 2 / 6
        w12 = wh / 2
        ctx.save()
        for _ in range(2):
            ctx.arc(w3c, 0, w1c, CW, CE)
            ctx.arc(0, 0, w26, CE, CS)
            ctx.arc(0, w3c, w1c, CS, CN)
            ctx.arc_negative(0, 0, w16, CS, CE)
            ctx.fill()
            ctx.translate(wh, 0)
            ctx.rotate(math.pi / 2)
        ctx.restore()
        self.dot(ctx, wh, 0, w9c)
        self.dot(ctx, wh, wh, w9c)
        ctx.arc(w3c, wh, w1c, CE, CW)
        ctx.arc(w12, wh, w26, CW, CE)
        ctx.arc(w9c, wh, w1c, CE, CW)
        ctx.arc_negative(w12, wh, w16, CE, CW)
        ctx.fill()

@collect(n6_tiles)
class SadFaceHigh(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w1c = wh / 12
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        w16 = wh / 6
        w26 = wh * 2 / 6
        w12 = wh / 2
        ctx.save()
        for _ in range(2):
            ctx.arc(w3c, 0, w1c, CW, CE)
            ctx.arc(0, 0, w26, CE, CS)
            ctx.arc(0, w3c, w1c, CS, CN)
            ctx.arc_negative(0, 0, w16, CS, CE)
            ctx.fill()
            ctx.translate(wh, 0)
            ctx.rotate(math.pi / 2)
        ctx.restore()
        self.dot(ctx, wh, 0, w9c)
        self.dot(ctx, wh, wh, w9c)
        ctx.arc(w3c, wh, w1c, CE, CW)
        ctx.arc(w12, w9c, w26, CW, CE)
        ctx.arc(w9c, wh, w1c, CE, CW)
        ctx.arc_negative(w12, w9c, w16, CE, CW)
        ctx.fill()

@collect(n6_tiles)
class Frog(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w1c = wh / 12
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        w16 = wh / 6
        w26 = wh * 2 / 6
        ctx.save()
        for _ in range(2):
            ctx.arc(w3c, 0, w1c, CW, CE)
            ctx.arc(0, 0, w26, CE, CS)
            ctx.arc(0, w3c, w1c, CS, CN)
            ctx.arc_negative(0, 0, w16, CS, CE)
            ctx.fill()
            ctx.translate(wh, 0)
            ctx.rotate(math.pi / 2)
        ctx.restore()
        ctx.arc(0, w9c, w1c, CS, CN)
        ctx.arc(wh, w9c, w1c, CN, CS)
        ctx.fill()
        self.dot(ctx, wh, w3c, wh)
        self.dot(ctx, wh, w9c, wh)


@collect(n6_tiles)
class CrossCross(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        w1c = wh / 12
        w3c = wh * 3 / 12
        w9c = wh * 9 / 12
        w16 = wh / 6
        w26 = wh * 2 / 6
        w46 = wh * 4 / 6
        w56 = wh * 5 / 6
        ctx.arc(w3c, 0, w1c, CW, CE)
        ctx.arc(0, 0, w26, CE, CS)
        ctx.arc(0, w3c, w1c, CS, CN)
        ctx.arc_negative(0, 0, w16, CS, CE)
        ctx.fill()

        ctx.arc(0, w9c, w1c, CS, CN)
        ctx.arc(wh, w9c, w1c, CN, CS)
        ctx.fill()
        self.dot(ctx, wh, w3c, wh)

        ctx.arc(w9c, 0, w1c, CW, CE)
        ctx.line_to(w56, w46 - wh / 24)
        ctx.line_to(w46, w46 - wh / 24)
        ctx.fill()

        ctx.arc(w9c, wh, w1c, CE, CW)
        ctx.line_to(w46, w56 + wh / 24)
        ctx.line_to(w56, w56 + wh / 24)
        ctx.fill()

        self.dot(ctx, wh, wh, w3c)

@collect(n6_tiles)
@collect(n6_connected)
class CornerSlash(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        self.four_corners(ctx, wh)
        self.slash(ctx, wh)

@collect(n6_tiles)
@collect(n6_connected)
class CornerSlashCross(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        self.slash(ctx, wh)
        self.slash_cross(ctx, wh, bgfg)
        self.four_corners(ctx, wh)

@collect(n6_tiles)
@collect(n6_connected)
class CornerSlashCrossUnder(Tile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        self.four_corners(ctx, wh)
        self.slash(ctx, wh)
        self.slash_cross(ctx, wh, bgfg)


n6_demo = [c() for c in all_subclasses(Tile)]
