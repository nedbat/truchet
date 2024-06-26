
from drawing import CE, CS, CW, CN, DEG90, DEG180
from tiler import TileBase, collect, stroke


n6_tiles = []
n6_connected = []
n6_circles = []
n6_weird = []
n6_filled = []
n6_lattice = []

class Tile(TileBase):
    """Multi-scale truchet tiles of my own devising."""

    class G(TileBase.G):
        def __init__(self, wh, bgfg=None):
            super().__init__(wh, bgfg)
            # +-----+-----+-----+-----+-----+-----+
            # 0    w16   w26         w46   w56    wh
            #   w1c   w3c               w9c
            #                  w12
            self.w1c = wh / 12
            self.w3c = wh * 3 / 12
            self.w9c = wh * 9 / 12
            self.w16 = wh / 6
            self.w26 = wh * 2 / 6
            self.w46 = wh * 4 / 6
            self.w56 = wh * 5 / 6
            self.w12 = wh / 2
            self.w1cc = wh / 24

    def init_tile(self, ctx, g, base_color=None):
        ctx.arc(0, 0, g.w16, CS, CE)
        ctx.arc(g.w12, 0, g.w16, CW, CE)
        ctx.arc(g.wh, 0, g.w16, CW, CS)
        ctx.arc(g.wh, g.w12, g.w16, CN, CS)
        ctx.arc(g.wh, g.wh, g.w16, CN, CW)
        ctx.arc(g.w12, g.wh, g.w16, CE, CW)
        ctx.arc(0, g.wh, g.w16, CE, CN)
        ctx.arc(0, g.w12, g.w16, CS, CN)
        ctx.set_source_rgba(*(base_color or g.bgfg[0]))
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

    @stroke
    def four_corners(self, ctx, g, which=(0,1,2,3)):
        with ctx.save_restore():
            for i in which:
                with ctx.rotated(g.wh, i):
                    ctx.arc(g.w3c, 0, g.w1c, CW, CE)
                    ctx.arc(0, 0, g.w26, CE, CS)
                    ctx.arc(0, g.w3c, g.w1c, CS, CN)
                    ctx.arc_negative(0, 0, g.w16, CS, CE)
                    ctx.fill()
    @stroke
    def all_dots(self, ctx, g):
        for a in [g.w3c, g.w9c]:
            for b in [0, g.wh]:
                self.dot(ctx, g, a, b)
                self.dot(ctx, g, b, a)

    @stroke
    def bar(self, ctx, g):
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.arc(g.wh, g.w3c, g.w1c, CN, CS)
        ctx.fill()

    @stroke
    def bar_gapped(self, ctx, g):
        self.bar(ctx, g)
        ctx.set_source_rgba(*g.bgfg[0])
        ctx.rectangle(0, g.w16 - g.w1cc, g.wh, g.w1cc)
        ctx.fill()
        ctx.rectangle(0, g.w26, g.wh, g.w1cc)
        ctx.fill()

    @stroke
    def half_bar_gapped(self, ctx, g):
        with ctx.save_restore():
            ctx.arc(0, g.w3c, g.w1c, CS, CN)
            ctx.line_to(g.w12, g.w16)
            ctx.line_to(g.w12, g.w26)
            ctx.close_path()
            ctx.fill()
            ctx.set_source_rgba(*g.bgfg[0])
            ctx.rectangle(0, g.w16 - g.w1cc, g.w12, g.w1cc)
            ctx.fill()
            ctx.rectangle(0, g.w26, g.w12, g.w1cc)
            ctx.fill()

    @stroke
    def slash(self, ctx, g):
        with ctx.save_restore():
            ctx.arc(g.w9c, 0, g.w1c, CW, CE)
            ctx.arc(0, 0, g.w56, CE, CS)
            ctx.arc(0, g.w9c, g.w1c, CS, CN)
            ctx.arc_negative(0, 0, g.w46, CS, CE)
            ctx.fill()

    @stroke
    def slash_gapped(self, ctx, g):
        self.slash(ctx, g)
        with ctx.save_restore():
            ctx.set_source_rgba(*g.bgfg[0])
            ctx.arc(0, 0, g.w46, CE, CS)
            ctx.arc_negative(0, 0, g.w46 - g.w1cc, CS, CE)
            ctx.fill()
            ctx.arc_negative(0, 0, g.w56, CS, CE)
            ctx.arc(0, 0, g.w56 + g.w1cc, CE, CS)
            ctx.fill()

    @stroke
    def top_edge(self, ctx, g):
        with ctx.save_restore():
            ctx.arc(g.w3c, 0, g.w1c, CW, CE)
            ctx.arc_negative(g.w12, 0, g.w16, CW, CE)
            ctx.arc(g.w9c, 0, g.w1c, CW, CE)
            ctx.arc(g.w12, 0, g.w26, CE, CW)
            ctx.fill()

    @stroke
    def ell(self, ctx, g):
        with ctx.save_restore():
            ctx.arc(g.w9c, 0, g.w1c, CW, CE)
            ctx.arc(g.w12, 0, g.w26, CE, CS)
            ctx.arc(0, g.w3c, g.w1c, CS, CN)
            ctx.arc_negative(g.w12, 0, g.w16, CS, CE)
            ctx.fill()

    @stroke
    def high_frown(self, ctx, g):
        ctx.arc(g.w3c, g.wh, g.w1c, CE, CW)
        ctx.arc(g.w12, g.w9c, g.w26, CW, CE)
        ctx.arc(g.w9c, g.wh, g.w1c, CE, CW)
        ctx.arc_negative(g.w12, g.w9c, g.w16, CE, CW)
        ctx.fill()

    @stroke
    def cowboy_hat(self, ctx, g):
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.w12, 0, g.w16, CW, CE)
        ctx.arc(g.w9c, 0, g.w1c, CW, CE)
        ctx.arc(0, 0, g.w56, CE, CS)
        ctx.arc(0, g.w9c, g.w1c, CS, CN)
        ctx.arc_negative(0, g.w12, g.w16, CS, CN)
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.arc_negative(0, 0, g.w16, CS, CE)
        ctx.fill()

    @stroke
    def mid_loop(self, ctx, g):
        ctx.arc(0, g.w9c, g.w1c, CS, CN)
        ctx.arc_negative(0, g.w12, g.w16, CS, CE)
        ctx.arc(g.w12, g.w12, g.w26, CW, CE)
        ctx.arc_negative(g.wh, g.w12, g.w16, CW, CS)
        ctx.arc(g.wh, g.w9c, g.w1c, CN, CS)
        ctx.arc(g.wh, g.w12, g.w26, CS, CW)
        ctx.arc_negative(g.w12, g.w12, g.w16, CE, CW)
        ctx.arc(0, g.w12, g.w26, CE, CS)
        ctx.fill()

    def draw(self, ctx, g):
        ...


@collect(n6_tiles)
@collect(n6_circles, repeat=3)
class Slash21(Tile):
    def draw(self, ctx, g):
        self.slash(ctx, g)
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, g.w3c, g.wh)
        self.four_corners(ctx, g, which=(0, 2))

@collect(n6_tiles)
@collect(n6_circles, repeat=3)
class Slash11(Tile):
    def draw(self, ctx, g):
        self.slash(ctx, g)
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, 0, g.w3c)
        self.dot(ctx, g, g.w3c, 0)
        self.four_corners(ctx, g, which=(2,))

@collect(n6_tiles)
@collect(n6_circles, repeat=3)
class Slash2(Tile):
    def draw(self, ctx, g):
        self.slash(ctx, g)
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, g.wh, g.w9c)
        self.dot(ctx, g, g.w9c, g.wh)
        self.four_corners(ctx, g, which=(0,))

@collect(n6_weird)
@collect(n6_lattice)
class SlashCross(Tile):
    def draw(self, ctx, g):
        self.slash(ctx, g)
        with ctx.flip_lr(g.wh):
            self.slash_gapped(ctx, g)
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, 0, g.w3c)
        self.dot(ctx, g, g.w9c, g.wh)

@collect(n6_tiles)
@collect(n6_circles, repeat=2)
class Cowboy(Tile):
    def draw(self, ctx, g):
        self.cowboy_hat(ctx, g)
        self.four_corners(ctx, g, which=(2,))
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, g.w3c, g.wh)

@collect(n6_tiles)
class CowboyMinus(Tile):
    def draw(self, ctx, g):
        self.cowboy_hat(ctx, g)
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, g.wh, g.w9c)
        self.dot(ctx, g, g.w9c, g.wh)

@collect(n6_tiles)
class Empty(Tile):
    rotations = 1
    def draw(self, ctx, g):
        self.all_dots(ctx, g)

@collect(n6_tiles)
class Empty1(Tile):
    def draw(self, ctx, g):
        self.all_dots(ctx, g)
        self.dot(ctx, g, g.w12, g.w3c)

@collect(n6_tiles)
class Dotted(Tile):
    rotations = 1
    def draw(self, ctx, g):
        self.all_dots(ctx, g)
        self.dot(ctx, g, g.w12, g.w3c)
        self.dot(ctx, g, g.w3c, g.w12)
        self.dot(ctx, g, g.w9c, g.w12)
        self.dot(ctx, g, g.w12, g.w9c)

@collect(n6_tiles)
@collect(n6_filled)
@collect(n6_connected)
class Filled(Tile):
    rotations = 1
    def draw(self, ctx, g):
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.w12, 0, g.w16, CW, CE)
        ctx.arc(g.w9c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.wh, 0, g.w16, CW, CS)
        ctx.arc(g.wh, g.w3c, g.w1c, CN, CS)
        ctx.arc_negative(g.wh, g.w12, g.w16, CN, CS)
        ctx.arc(g.wh, g.w9c, g.w1c, CN, CS)
        ctx.arc_negative(g.wh, g.wh, g.w16, CN, CW)
        ctx.arc(g.w9c, g.wh, g.w1c, CE, CW)
        ctx.arc_negative(g.w12, g.wh, g.w16, CE, CW)
        ctx.arc(g.w3c, g.wh, g.w1c, CE, CW)
        ctx.arc_negative(0, g.wh, g.w16, CE, CN)
        ctx.arc(0, g.w9c, g.w1c, CS, CN)
        ctx.arc_negative(0, g.w12, g.w16, CS, CN)
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.arc_negative(0, 0, g.w16, CS, CE)
        ctx.fill()


@collect(n6_tiles)
@collect(n6_circles)
@collect(n6_filled)
@collect(n6_connected)
class FilledHollow(Filled):
    rotations = 1
    def draw(self, ctx, g):
        super().draw(ctx, g)
        ctx.set_source_rgba(*g.bgfg[0])
        ctx.circle(g.w12, g.w12, g.w16)
        ctx.fill()


@collect(n6_tiles)
@collect(n6_circles)
@collect(n6_filled)
class Filled12(Tile):
    rotations = 2
    def draw(self, ctx, g):
        ctx.arc(g.wh, g.w3c, g.w1c, CN, CS)
        ctx.arc_negative(g.wh, g.w12, g.w16, CN, CS)
        ctx.arc(g.wh, g.w9c, g.w1c, CN, CS)
        ctx.arc(0, g.w9c, g.w1c, CS, CN)
        ctx.arc_negative(0, g.w12, g.w16, CS, CN)
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.fill()
        for x in [g.w3c, g.w9c]:
            for y in [0, g.wh]:
                self.dot(ctx, g, x, y)


@collect(n6_tiles)
@collect(n6_circles)
@collect(n6_filled)
class Filled12Hollow(Filled12):
    rotations = 2
    def draw(self, ctx, g):
        super().draw(ctx, g)
        ctx.set_source_rgba(*g.bgfg[0])
        ctx.circle(g.w12, g.w12, g.w16)
        ctx.fill()


@collect(n6_tiles)
@collect(n6_circles)
@collect(n6_filled)
class Filled13(Tile):
    def draw(self, ctx, g):
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.w12, 0, g.w16, CW, CE)
        ctx.arc(g.w9c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.wh, 0, g.w16, CW, CS)
        ctx.arc(g.wh, g.w3c, g.w1c, CN, CS)
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.arc_negative(0, 0, g.w16, CS, CE)
        ctx.fill()
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, g.w9c, g.wh)
        self.dot(ctx, g, 0, g.w9c)
        self.dot(ctx, g, g.wh, g.w9c)


@collect(n6_tiles)
@collect(n6_circles)
@collect(n6_filled)
class Filled13Bar(Tile):
    def draw(self, ctx, g):
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.w12, 0, g.w16, CW, CE)
        ctx.arc(g.w9c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.wh, 0, g.w16, CW, CS)
        ctx.arc(g.wh, g.w3c, g.w1c, CN, CS)
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.arc_negative(0, 0, g.w16, CS, CE)
        ctx.fill()
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, g.w9c, g.wh)
        with ctx.rotated(g.wh, 2):
            self.bar(ctx, g)


@collect(n6_tiles)
@collect(n6_circles)
@collect(n6_filled)
class Filled34(Tile):
    def draw(self, ctx, g):
        ctx.arc(g.w3c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.w12, 0, g.w16, CW, CE)
        ctx.arc(g.w9c, 0, g.w1c, CW, CE)
        ctx.arc_negative(g.wh, 0, g.w16, CW, CS)
        ctx.arc(g.wh, g.w3c, g.w1c, CN, CS)
        ctx.arc_negative(g.wh, g.w12, g.w16, CN, CS)
        ctx.arc(g.wh, g.w9c, g.w1c, CN, CS)
        ctx.arc(0, g.w9c, g.w1c, CS, CN)
        ctx.arc_negative(0, g.w12, g.w16, CS, CN)
        ctx.arc(0, g.w3c, g.w1c, CS, CN)
        ctx.arc_negative(0, 0, g.w16, CS, CE)
        ctx.fill()
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, g.w9c, g.wh)


@collect(n6_tiles)
@collect(n6_circles)
@collect(n6_filled)
class Filled34Hollow(Filled34):
    def draw(self, ctx, g):
        super().draw(ctx, g)
        ctx.set_source_rgba(*g.bgfg[0])
        ctx.circle(g.w12, g.w12, g.w16)
        ctx.fill()


@collect(n6_tiles)
@collect(n6_connected)
class EdgeHash(Tile):
    rotations = 1
    def draw(self, ctx, g):
        for i in range(4):
            with ctx.rotated(g.wh, i):
                self.top_edge(ctx, g)


@collect(n6_tiles)
@collect(n6_connected)
class MidLoop(Tile):
    rotations = 4
    def draw(self, ctx, g):
        with ctx.rotated(g.wh, 2):
            self.top_edge(ctx, g)
        self.four_corners(ctx, g, which=(0, 1))
        self.mid_loop(ctx, g)


@collect(n6_tiles)
class MidLoopHalfSparse(Tile):
    rotations = 4
    flip = True
    def draw(self, ctx, g):
        with ctx.rotated(g.wh, 2):
            self.top_edge(ctx, g)
        self.four_corners(ctx, g, which=(0,))
        self.dot(ctx, g, g.w9c, 0)
        self.dot(ctx, g, g.wh, g.w3c)
        self.mid_loop(ctx, g)

@collect(n6_tiles)
class MidLoopTopSparse(Tile):
    rotations = 4
    def draw(self, ctx, g):
        with ctx.rotated(g.wh, 2):
            self.top_edge(ctx, g)
        self.dot(ctx, g, g.w3c, 0)
        self.dot(ctx, g, 0, g.w3c)
        self.dot(ctx, g, g.w9c, 0)
        self.dot(ctx, g, g.wh, g.w3c)
        self.mid_loop(ctx, g)

@collect(n6_tiles)
class MidLoopAllSparse(Tile):
    rotations = 4
    def draw(self, ctx, g):
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, g.w9c, g.wh)
        self.dot(ctx, g, g.w3c, 0)
        self.dot(ctx, g, 0, g.w3c)
        self.dot(ctx, g, g.w9c, 0)
        self.dot(ctx, g, g.wh, g.w3c)
        self.mid_loop(ctx, g)

@collect(n6_tiles)
@collect(n6_connected)
class EdgeHashBar(Tile):
    rotations = 4
    def draw(self, ctx, g):
        for i in range(4):
            with ctx.rotated(g.wh, i):
                self.top_edge(ctx, g)
        self.bar(ctx, g)


@collect(n6_tiles)
@collect(n6_circles)
class Edge34(Tile):
    def draw(self, ctx, g):
        with ctx.save_restore():
            for _ in range(3):
                self.top_edge(ctx, g)
                ctx.translate(g.wh, 0)
                ctx.rotate(DEG90)
        self.dot(ctx, g, 0, g.w3c)
        self.dot(ctx, g, 0, g.w9c)

@collect(n6_tiles)
@collect(n6_circles)
class Edge34Bar(Tile):
    def draw(self, ctx, g):
        with ctx.save_restore():
            for _ in range(3):
                self.top_edge(ctx, g)
                ctx.translate(g.wh, 0)
                ctx.rotate(DEG90)
        self.dot(ctx, g, 0, g.w3c)
        self.dot(ctx, g, 0, g.w9c)
        with ctx.rotated(g.wh, 1):
            self.bar(ctx, g)

@collect(n6_tiles)
@collect(n6_circles)
class HourGlass(Tile):
    rotations = 2
    def draw(self, ctx, g):
        with ctx.save_restore():
            for _ in range(2):
                self.top_edge(ctx, g)
                ctx.translate(g.wh, g.wh)
                ctx.rotate(DEG180)
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
        with ctx.save_restore():
            ctx.translate(g.wh, g.wh)
            ctx.rotate(DEG180)
            self.ell(ctx, g)

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
        with ctx.rotated(g.wh, 2):
            self.ell(ctx, g)

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
        with ctx.rotated(g.wh, 2):
            self.ell(ctx, g)

@collect(n6_connected)
@collect(n6_weird)
class Kanji(Tile):
    def draw(self, ctx, g):
        self.ell(ctx, g)
        with ctx.flip_tb(g.wh):
            self.ell(ctx, g)
        with ctx.rotated(g.wh, 3):
            self.bar(ctx, g)
        with ctx.rotated(g.wh, 1):
            self.top_edge(ctx, g)

@collect(n6_connected)
@collect(n6_weird)
@collect(n6_lattice)
class KanjiGapped(Kanji):
    def draw(self, ctx, g):
        super().draw(ctx, g)
        self.half_bar_gapped(ctx, g)
        with ctx.rotated(g.wh, 3):
            self.half_bar_gapped(ctx, g)

@collect(n6_tiles)
@collect(n6_connected)
@collect(n6_circles)
class CornerHash(Tile):
    rotations = 1
    def draw(self, ctx, g):
        self.four_corners(ctx, g)

@collect(n6_weird)
class Octagon(Tile):
    rotations = 1
    def draw(self, ctx, g):
        self.four_corners(ctx, g)
        for i in range(4):
            with ctx.rotated(g.wh, i):
                self.top_edge(ctx, g)


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
@collect(n6_connected)
@collect(n6_circles)
class SwimSuit2Plus(Tile):
    def draw(self, ctx, g):
        self.four_corners(ctx, g)
        self.high_frown(ctx, g)
        self.dot(ctx, g, g.w12, g.w9c)

@collect(n6_tiles)
@collect(n6_circles)
class SadFace(Tile):
    def draw(self, ctx, g):
        with ctx.save_restore():
            for _ in range(2):
                ctx.arc(g.w3c, 0, g.w1c, CW, CE)
                ctx.arc(0, 0, g.w26, CE, CS)
                ctx.arc(0, g.w3c, g.w1c, CS, CN)
                ctx.arc_negative(0, 0, g.w16, CS, CE)
                ctx.fill()
                ctx.translate(g.wh, 0)
                ctx.rotate(DEG90)
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
        with ctx.save_restore():
            for _ in range(2):
                ctx.arc(g.w3c, 0, g.w1c, CW, CE)
                ctx.arc(0, 0, g.w26, CE, CS)
                ctx.arc(0, g.w3c, g.w1c, CS, CN)
                ctx.arc_negative(0, 0, g.w16, CS, CE)
                ctx.fill()
                ctx.translate(g.wh, 0)
                ctx.rotate(DEG90)
        self.dot(ctx, g, 0, g.w9c)
        self.dot(ctx, g, g.wh, g.w9c)
        self.high_frown(ctx, g)

@collect(n6_tiles)
@collect(n6_circles)
class Frog(Tile):
    def draw(self, ctx, g):
        with ctx.save_restore():
            for _ in range(2):
                ctx.arc(g.w3c, 0, g.w1c, CW, CE)
                ctx.arc(0, 0, g.w26, CE, CS)
                ctx.arc(0, g.w3c, g.w1c, CS, CN)
                ctx.arc_negative(0, 0, g.w16, CS, CE)
                ctx.fill()
                ctx.translate(g.wh, 0)
                ctx.rotate(DEG90)
        with ctx.rotated(g.wh, 2):
            self.bar(ctx, g)
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

        with ctx.rotated(g.wh, 1):
            self.bar(ctx, g)
        with ctx.rotated(g.wh, 2):
            self.bar_gapped(ctx, g)

        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, g.wh, g.w3c)

@collect(n6_lattice)
class CrossCrossSlash(CrossCross):
    def draw(self, ctx, g):
        super().draw(ctx, g)
        with ctx.rotated(g.wh, 2):
            self.slash_gapped(ctx, g)
        with ctx.rotated(g.wh, 1):
            self.half_bar_gapped(ctx, g)

@collect(n6_lattice)
class Hash(Tile):
    def draw(self, ctx, g):
        for _ in range(4):
            self.bar(ctx, g)
            ctx.translate(g.wh, 0)
            ctx.rotate(DEG90)
        for _ in range(4):
            self.half_bar_gapped(ctx, g)
            ctx.translate(g.wh, 0)
            ctx.rotate(DEG90)


@collect(n6_tiles)
@collect(n6_connected)
@collect(n6_circles, repeat=3)
class CornerSlash(Tile):
    def draw(self, ctx, g):
        self.four_corners(ctx, g)
        self.slash(ctx, g)

@collect(n6_tiles)
class CornerSlashMinus(Tile):
    def draw(self, ctx, g):
        self.four_corners(ctx, g, which=(0,2,3))
        self.slash(ctx, g)
        self.dot(ctx, g, g.wh, g.w3c)

@collect(n6_connected)
@collect(n6_weird)
class CornerSlashCross(Tile):
    def draw(self, ctx, g):
        self.slash(ctx, g)
        with ctx.flip_lr(g.wh):
            self.slash_gapped(ctx, g)
        self.four_corners(ctx, g)

@collect(n6_weird)
@collect(n6_lattice)
class CornerSlashCrossUnder(Tile):
    def draw(self, ctx, g):
        self.four_corners(ctx, g)
        self.slash(ctx, g)
        with ctx.flip_lr(g.wh):
            self.slash_gapped(ctx, g)

@collect(n6_weird)
class Sprout(Tile):
    def draw(self, ctx, g):
        self.slash(ctx, g)
        self.ell(ctx, g)
        self.four_corners(ctx, g, which=(1,2,3))
        self.dot(ctx, g, g.w3c, 0)

@collect(n6_tiles)
@collect(n6_circles)
class DoubleEll(Tile):
    def draw(self, ctx, g):
        self.ell(ctx, g)
        with ctx.flip_lr(g.wh):
            with ctx.rotated(g.wh, 1):
                self.ell(ctx, g)
        self.four_corners(ctx, g, which=(2,))
        self.dot(ctx, g, g.wh, g.w3c)
        self.dot(ctx, g, g.w3c, g.wh)

@collect(n6_circles)
class TopEdge(Tile):
    def draw(self, ctx, g):
        self.bar(ctx, g)
        self.top_edge(ctx, g)
        self.all_dots(ctx, g)


@collect(n6_lattice)
class SlashTriangle(Tile):
    def draw(self, ctx, g):
        self.bar(ctx, g)
        self.slash_gapped(ctx, g)
        with ctx.flip_lr(g.wh):
            self.slash_gapped(ctx, g)
        self.half_bar_gapped(ctx, g)
        self.dot(ctx, g, g.w3c, g.wh)
        self.dot(ctx, g, g.w9c, g.wh)


n6_strokes = []
for meth_name in dir(Tile):
    meth = getattr(Tile, meth_name, None)
    if getattr(meth, "is_stroke", False):
        class _OneStroke(Tile):
            def draw_tile(self, ctx, wh, meth_name=meth_name):
                super().draw_tile(ctx, wh, base_color=(1, .65, .65), meth_name=meth_name)
        cls = type(meth_name, (_OneStroke,), {})
        n6_strokes.append(cls())
