
from drawing import CE, CS, CW, CN, DEG90, DEG180
from helpers import color


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

n6_tiles = []
n6_connected = []
n6_circles = []
n6_weird = []


class Tile:
    """Multi-scale truchet tiles of my own devising."""

    class G:
        def __init__(self, wh, bgfg=None):
            self.wh = wh
            self.bgfg = bgfg
            if self.bgfg is None:
                self.bgfg = [color(1), color(0)]
            # +-----+-----+---------+-----+-----+
            # 0    w16   w26       w46   w56    wh
            #                 w12
            #   w1c   w3c            w9c
            self.w1c = wh / 12
            self.w3c = wh * 3 / 12
            self.w9c = wh * 9 / 12
            self.w16 = wh / 6
            self.w26 = wh * 2 / 6
            self.w46 = wh * 4 / 6
            self.w56 = wh * 5 / 6
            self.w12 = wh / 2
            self.w1cc = wh / 24


    rotations = 4
    flip = False

    def __init__(self, rot=0, flipped=False):
        self.rot = rot
        self.flipped = flipped

    def init_tile(self, ctx, g):
        ctx.arc(0, 0, g.w16, CS, CE)
        ctx.arc(g.w12, 0, g.w16, CW, CE)
        ctx.arc(g.wh, 0, g.w16, CW, CS)
        ctx.arc(g.wh, g.w12, g.w16, CN, CS)
        ctx.arc(g.wh, g.wh, g.w16, CN, CW)
        ctx.arc(g.w12, g.wh, g.w16, CE, CW)
        ctx.arc(0, g.wh, g.w16, CE, CN)
        ctx.arc(0, g.w12, g.w16, CS, CN)
        ctx.set_source_rgba(*g.bgfg[0])
        ctx.fill()
        ctx.set_source_rgba(*g.bgfg[1])
        ctx.translate(g.w12, g.w12)
        ctx.rotate(DEG90 * self.rot)
        ctx.translate(-g.w12, -g.w12)
        if self.flipped:
            ctx.translate(g.wh, 0)
            ctx.scale(-1, 1)

    def dot(self, ctx, g, x, y):
        ctx.circle(x, y, g.w1c)
        ctx.fill()

    def four_corners(self, ctx, g, which=(0,1,2,3)):
        ctx.save()
        for i in range(4):
            if i in which:
                ctx.arc(g.w3c, 0, g.w1c, CW, CE)
                ctx.arc(0, 0, g.w26, CE, CS)
                ctx.arc(0, g.w3c, g.w1c, CS, CN)
                ctx.arc_negative(0, 0, g.w16, CS, CE)
                ctx.fill()
            ctx.translate(g.wh, 0)
            ctx.rotate(DEG90)
        ctx.restore()

    def slash(self, ctx, g, with_gap=False):
        ctx.save()
        ctx.arc(g.w9c, 0, g.w1c, CW, CE)
        ctx.arc(0, 0, g.w56, CE, CS)
        ctx.arc(0, g.w9c, g.w1c, CS, CN)
        ctx.arc_negative(0, 0, g.w46, CS, CE)
        ctx.fill()
        ctx.restore()

    def slash_cross(self, ctx, g):
        ctx.save()
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.wh, 0, g.w46, CW, CS)
        ctx.arc(g.wh, g.w9c, g.w1c, CN, CS)
        ctx.arc(g.wh, 0, g.w56, CS, CW)
        ctx.fill()
        ctx.set_source_rgba(*g.bgfg[0])
        ctx.arc(0, 0, g.w46, CE, CS)
        ctx.arc_negative(0, 0, g.w46 - g.w1cc, CS, CE)
        ctx.fill()
        ctx.arc_negative(0, 0, g.w56, CS, CE)
        ctx.arc(0, 0, g.w56 + g.w1cc, CE, CS)
        ctx.fill()
        ctx.restore()

    def top_edge(self, ctx, g):
        ctx.save()
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.w12, 0, g.w16, CW, CE)
        ctx.arc(g.w9c, 0, g.w1c, CW, CE)
        ctx.arc(g.w12, 0, g.w26, CE, CW)
        ctx.fill()
        ctx.restore()

    def ell(self, ctx, g):
        ctx.save()
        ctx.arc(g.w9c, 0, g.w1c, CW, CE)
        ctx.arc(g.w12, 0, g.w26, CE, CS)
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.arc_negative(g.w12, 0, g.w16, CS, CE)
        ctx.fill()
        ctx.restore()

    def high_frown(self, ctx, g):
        ctx.arc(g.w3c, g.wh, g.w1c, CE, CW)
        ctx.arc(g.w12, g.w9c, g.w26, CW, CE)
        ctx.arc(g.w9c, g.wh, g.w1c, CE, CW)
        ctx.arc_negative(g.w12, g.w9c, g.w16, CE, CW)
        ctx.fill()

    def draw(self, ctx, g):
        ...


@collect(n6_tiles)
@collect(n6_circles, repeat=3)
class Slash21(Tile):
    def draw(self, ctx, g):
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc(0, 0, g.w26, CE, CS)
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.arc_negative(0, 0, g.w16, CS, CE)
        ctx.fill()
        self.slash(ctx, g)
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, g.w3c, g.wh)
        ctx.arc(g.wh, g.w9c, g.w1c, CN, CS)
        ctx.arc_negative(g.wh, g.wh, g.w16, CN, CW)
        ctx.arc(g.w9c, g.wh, g.w1c, CE, CW)
        ctx.arc(g.wh, g.wh, g.w26, CW, CN)
        ctx.fill()

@collect(n6_tiles)
@collect(n6_weird)
class SlashCross(Tile):
    def draw(self, ctx, g):
        self.slash(ctx, g)
        self.slash_cross(ctx, g)
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, 0, g.w3c)
        self.dot(ctx, g, g.w9c, g.wh)

@collect(n6_tiles)
@collect(n6_circles, repeat=2)
class Cowboy(Tile):
    def draw(self, ctx, g):
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.w12, 0, g.w16, CW, CE)
        ctx.arc(g.w9c, 0, g.w1c, CW, CE)
        ctx.arc(0, 0, g.w56, CE, CS)
        ctx.arc(0, g.w9c, g.w1c, CS, CN)
        ctx.arc_negative(0, g.w12, g.w16, CS, CN)
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.arc_negative(0, 0, g.w16, CS, CE)
        ctx.fill()
        self.four_corners(ctx, g, which=(2,))
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, g.w3c, g.wh)


@collect(n6_tiles)
@collect(n6_connected)
#@collect(n6_circles)
class EdgeHash(Tile):
    rotations = 1
    def draw(self, ctx, g):
        for _ in range(4):
            self.top_edge(ctx, g)
            ctx.translate(g.wh, 0)
            ctx.rotate(DEG90)

@collect(n6_tiles)
@collect(n6_circles)
class Edge34(Tile):
    def draw(self, ctx, g):
        ctx.save()
        for _ in range(3):
            self.top_edge(ctx, g)
            ctx.translate(g.wh, 0)
            ctx.rotate(DEG90)
        ctx.restore()
        self.dot(ctx, g, 0, g.w3c)
        self.dot(ctx, g, 0, g.w9c)

@collect(n6_tiles)
@collect(n6_circles)
class HourGlass(Tile):
    rotations = 2
    def draw(self, ctx, g):
        ctx.save()
        for _ in range(2):
            self.top_edge(ctx, g)
            ctx.translate(g.wh, g.wh)
            ctx.rotate(DEG180)
        ctx.restore()
        for x in [0, g.wh]:
            for y in [g.w3c, g.w9c]:
                self.dot(ctx, g, x, y)

@collect(n6_tiles)
@collect(n6_circles)
class ThatWay(Tile):
    flip = True
    def draw(self, ctx, g):
        self.top_edge(ctx, g)
        self.dot(ctx, g, 0, g.w3c)
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, 0, g.w9c)
        self.dot(ctx, g, g.w9c, g.wh)
        ctx.save()
        ctx.translate(g.wh, g.wh)
        ctx.rotate(DEG180)
        self.ell(ctx, g)
        ctx.restore()

@collect(n6_tiles)
@collect(n6_circles)
class ThoseWays(Tile):
    rotations = 2
    flip = True
    def draw(self, ctx, g):
        self.dot(ctx, g, g.w3c, 0)
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, 0, g.w9c)
        self.dot(ctx, g, g.w9c, g.wh)
        self.ell(ctx, g)
        ctx.save()
        ctx.translate(g.wh, g.wh)
        ctx.rotate(DEG180)
        self.ell(ctx, g)
        ctx.restore()

@collect(n6_tiles)
@collect(n6_circles)
class ThoseWaysX(Tile):
    flip = True
    def draw(self, ctx, g):
        self.top_edge(ctx, g)
        self.dot(ctx, g, g.w3c, 0)
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, 0, g.w9c)
        self.dot(ctx, g, g.w9c, g.wh)
        self.ell(ctx, g)
        ctx.save()
        ctx.translate(g.wh, g.wh)
        ctx.rotate(DEG180)
        self.ell(ctx, g)
        ctx.restore()

@collect(n6_tiles)
@collect(n6_connected)
@collect(n6_weird)
class Kanji(Tile):
    def draw(self, ctx, g):
        self.ell(ctx, g)
        ctx.save()
        ctx.translate(0, g.wh)
        ctx.scale(1, -1)
        self.ell(ctx, g)
        ctx.restore()
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc(g.w3c, g.wh, g.w1c, CE, CW)
        ctx.fill()
        ctx.save()
        ctx.translate(g.w12, g.w12)
        ctx.rotate(DEG90)
        ctx.translate(-g.w12, -g.w12)
        self.top_edge(ctx, g)
        ctx.restore()


@collect(n6_tiles)
@collect(n6_connected)
#@collect(n6_circles)
class CornerHash(Tile):
    rotations = 1
    def draw(self, ctx, g):
        self.four_corners(ctx, g)

@collect(n6_tiles)
@collect(n6_circles)
class Corner34(Tile):
    def draw(self, ctx, g):
        self.four_corners(ctx, g, which=(0,1,2))
        self.dot(ctx, g, 0, g.w9c)
        self.dot(ctx, g, g.w3c, g.wh)

@collect(n6_tiles)
@collect(n6_connected)
@collect(n6_circles)
class SwimSuit(Tile):
    def draw(self, ctx, g):
        self.four_corners(ctx, g)
        self.top_edge(ctx, g)

@collect(n6_tiles)
@collect(n6_connected)
@collect(n6_circles)
class SwimSuit2(Tile):
    def draw(self, ctx, g):
        self.four_corners(ctx, g)
        self.high_frown(ctx, g)

@collect(n6_tiles)
@collect(n6_circles)
class SadFace(Tile):
    def draw(self, ctx, g):
        ctx.save()
        for _ in range(2):
            ctx.arc(g.w3c, 0, g.w1c, CW, CE)
            ctx.arc(0, 0, g.w26, CE, CS)
            ctx.arc(0, g.w3c, g.w1c, CS, CN)
            ctx.arc_negative(0, 0, g.w16, CS, CE)
            ctx.fill()
            ctx.translate(g.wh, 0)
            ctx.rotate(DEG90)
        ctx.restore()
        self.dot(ctx, g, 0, g.w9c)
        self.dot(ctx, g, g.wh, g.w9c)
        ctx.arc(g.w3c, g.wh, g.w1c, CE, CW)
        ctx.arc(g.w12, g.wh, g.w26, CW, CE)
        ctx.arc(g.w9c, g.wh, g.w1c, CE, CW)
        ctx.arc_negative(g.w12, g.wh, g.w16, CE, CW)
        ctx.fill()

@collect(n6_tiles)
@collect(n6_circles)
class SadFaceHigh(Tile):
    def draw(self, ctx, g):
        ctx.save()
        for _ in range(2):
            ctx.arc(g.w3c, 0, g.w1c, CW, CE)
            ctx.arc(0, 0, g.w26, CE, CS)
            ctx.arc(0, g.w3c, g.w1c, CS, CN)
            ctx.arc_negative(0, 0, g.w16, CS, CE)
            ctx.fill()
            ctx.translate(g.wh, 0)
            ctx.rotate(DEG90)
        ctx.restore()
        self.dot(ctx, g, 0, g.w9c)
        self.dot(ctx, g, g.wh, g.w9c)
        self.high_frown(ctx, g)

@collect(n6_tiles)
@collect(n6_circles)
class Frog(Tile):
    def draw(self, ctx, g):
        ctx.save()
        for _ in range(2):
            ctx.arc(g.w3c, 0, g.w1c, CW, CE)
            ctx.arc(0, 0, g.w26, CE, CS)
            ctx.arc(0, g.w3c, g.w1c, CS, CN)
            ctx.arc_negative(0, 0, g.w16, CS, CE)
            ctx.fill()
            ctx.translate(g.wh, 0)
            ctx.rotate(DEG90)
        ctx.restore()
        ctx.arc(0, g.w9c, g.w1c, CS, CN)
        ctx.arc(g.wh, g.w9c, g.w1c, CN, CS)
        ctx.fill()
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, g.w9c, g.wh)


@collect(n6_tiles)
class CrossCross(Tile):
    def draw(self, ctx, g):
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc(0, 0, g.w26, CE, CS)
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.arc_negative(0, 0, g.w16, CS, CE)
        ctx.fill()

        ctx.arc(0, g.w9c, g.w1c, CS, CN)
        ctx.arc(g.wh, g.w9c, g.w1c, CN, CS)
        ctx.fill()
        self.dot(ctx, g, g.w3c, g.wh)

        ctx.arc(g.w9c, 0, g.w1c, CW, CE)
        ctx.line_to(g.w56, g.w46 - g.w1cc)
        ctx.line_to(g.w46, g.w46 - g.w1cc)
        ctx.fill()

        ctx.arc(g.w9c, g.wh, g.w1c, CE, CW)
        ctx.line_to(g.w46, g.w56 + g.w1cc)
        ctx.line_to(g.w56, g.w56 + g.w1cc)
        ctx.fill()

        self.dot(ctx, g, g.wh, g.w3c)

@collect(n6_tiles)
@collect(n6_connected)
@collect(n6_circles, repeat=3)
class CornerSlash(Tile):
    def draw(self, ctx, g):
        self.four_corners(ctx, g)
        self.slash(ctx, g)

@collect(n6_tiles)
@collect(n6_circles, repeat=3)
class CornerSlashMinus(Tile):
    def draw(self, ctx, g):
        self.four_corners(ctx, g, which=(0,2,3))
        self.slash(ctx, g)
        self.dot(ctx, g, g.wh, g.w3c)

@collect(n6_tiles)
@collect(n6_connected)
@collect(n6_weird)
class CornerSlashCross(Tile):
    def draw(self, ctx, g):
        self.slash(ctx, g)
        self.slash_cross(ctx, g)
        self.four_corners(ctx, g)

@collect(n6_weird)
class CornerSlashCrossUnder(Tile):
    def draw(self, ctx, g):
        self.four_corners(ctx, g)
        self.slash(ctx, g)
        self.slash_cross(ctx, g)

@collect(n6_tiles)
@collect(n6_weird)
class Sprout(Tile):
    def draw(self, ctx, g):
        self.slash(ctx, g)
        self.ell(ctx, g)
        self.four_corners(ctx, g, which=(1,2,3))
        self.dot(ctx, g, g.w3c, 0)
