from drawing import CE, CS, CW, CN, DEG90
from tiler import TileBase, rotations


class CarlsonTile(TileBase):
    """https://christophercarlson.com/portfolio/multi-scale-truchet-patterns/"""

    class G(TileBase.G):
        def __init__(self, wh, bgfg=None):
            super().__init__(wh, bgfg)
            # +--+--+--+--+-----+
            # 0    wh1   wh3   wh
            #   wh6   wh2
            self.wh1 = wh / 3
            self.wh2 = wh / 2
            self.wh3 = wh * 2 / 3
            self.wh6 = wh / 6

    def init_tile(self, ctx, g, base_color=None):
        ctx.arc(0, 0, g.wh1, CS, CE)
        ctx.arc(g.wh, 0, g.wh1, CW, CS)
        ctx.arc(g.wh, g.wh, g.wh1, CN, CW)
        ctx.arc(0, g.wh, g.wh1, CE, CN)
        ctx.close_path()
        ctx.set_source_rgba(*g.bgfg[0])
        ctx.fill()
        ctx.set_source_rgba(*g.bgfg[1])
        ctx.translate(g.wh2, g.wh2)
        ctx.rotate(DEG90 * self.rot)
        ctx.translate(-g.wh2, -g.wh2)

    def draw(self, ctx, wh: int):
        ...


class CarlsonSlash(CarlsonTile):
    def draw(self, ctx, g):
        ctx.arc(g.wh2, 0, g.wh6, CW, CE)
        ctx.arc_negative(g.wh, 0, g.wh1, CW, CS)
        ctx.arc(g.wh, g.wh2, g.wh6, CN, CS)
        ctx.arc(g.wh, 0, g.wh3, CS, CW)
        ctx.fill()
        ctx.arc(0, g.wh2, g.wh6, CS, CN)
        ctx.arc(0, g.wh, g.wh3, CN, CE)
        ctx.arc(g.wh2, g.wh, g.wh6, CE, CW)
        ctx.arc_negative(0, g.wh, g.wh1, CE, CN)
        ctx.fill()


class CarlsonMinus(CarlsonTile):
    def draw(self, ctx, g):
        ctx.circle(g.wh2, 0, g.wh6)
        ctx.fill()
        ctx.arc(g.wh, g.wh2, g.wh6, CN, CS)
        ctx.arc(0, g.wh2, g.wh6, CS, CN)
        ctx.close_path()
        ctx.fill()
        ctx.circle(g.wh2, g.wh, g.wh6)
        ctx.fill()


class CarlsonHalfMinus(CarlsonTile):
    def draw(self, ctx, g):
        ctx.circle(g.wh2, 0, g.wh6)
        ctx.fill()
        ctx.arc(g.wh, g.wh2, g.wh6, CN, CS)
        ctx.arc(g.wh2, g.wh2, g.wh6, CS, CN)
        ctx.close_path()
        ctx.fill()
        ctx.circle(g.wh2, g.wh, g.wh6)
        ctx.fill()
        ctx.circle(0, g.wh2, g.wh6)
        ctx.fill()


class CarlsonFour(CarlsonTile):
    def draw(self, ctx, g):
        for x, y in [(g.wh2, 0), (g.wh, g.wh2), (g.wh2, g.wh), (0, g.wh2)]:
            ctx.circle(x, y, g.wh6)
            ctx.fill()


class CarlsonX(CarlsonTile):
    def draw(self, ctx, g):
        ctx.arc(g.wh2, 0, g.wh6, CW, CE)
        ctx.arc_negative(g.wh, 0, g.wh1, CW, CS)
        ctx.arc(g.wh, g.wh2, g.wh6, CN, CS)
        ctx.arc_negative(g.wh, g.wh, g.wh1, CN, CW)
        ctx.arc(g.wh2, g.wh, g.wh6, CE, CW)
        ctx.arc_negative(0, g.wh, g.wh1, CE, CN)
        ctx.arc(0, g.wh2, g.wh6, CS, CN)
        ctx.arc_negative(0, 0, g.wh1, CS, CE)
        ctx.fill()


class CarlsonPlus(CarlsonTile):
    def draw(self, ctx, g):
        ctx.arc(g.wh, g.wh2, g.wh6, CN, CS)
        ctx.arc(0, g.wh2, g.wh6, CS, CN)
        ctx.close_path()
        ctx.fill()
        ctx.arc(g.wh2, 0, g.wh6, CW, CE)
        ctx.arc(g.wh2, g.wh, g.wh6, CE, CW)
        ctx.close_path()
        ctx.fill()


class CarlsonFrown(CarlsonTile):
    def draw(self, ctx, g):
        ctx.arc(g.wh2, 0, g.wh6, CW, CE)
        ctx.arc_negative(g.wh, 0, g.wh1, CW, CS)
        ctx.arc(g.wh, g.wh2, g.wh6, CN, CS)
        ctx.arc(g.wh, 0, g.wh3, CS, CW)
        ctx.fill()
        ctx.circle(g.wh2, g.wh, g.wh6)
        ctx.fill()
        ctx.circle(0, g.wh2, g.wh6)
        ctx.fill()


class CarlsonT(CarlsonTile):
    def draw(self, ctx, g):
        ctx.arc(g.wh2, 0, g.wh6, CW, CE)
        ctx.arc_negative(g.wh, 0, g.wh1, CW, CS)
        ctx.arc(g.wh, g.wh2, g.wh6, CN, CS)
        ctx.arc(0, g.wh2, g.wh6, CS, CN)
        ctx.arc_negative(0, 0, g.wh1, CS, CE)
        ctx.fill()
        ctx.circle(g.wh2, g.wh, g.wh6)
        ctx.fill()


carlson_demo = (
    CarlsonSlash(),
    CarlsonMinus(),
    #CarlsonHalfMinus(),
    CarlsonFour(),
    CarlsonX(),
    CarlsonPlus(),
    CarlsonFrown(),
    CarlsonT(),
)


carlson_tiles = (
    *rotations(CarlsonSlash, 2),
    *rotations(CarlsonMinus, 2),
    CarlsonFour(),
    CarlsonX(),
    CarlsonPlus(),
    *rotations(CarlsonFrown, 4),
    *rotations(CarlsonT, 4),
)

carlson_extra = (
    *carlson_tiles,
    *rotations(CarlsonHalfMinus, 4),
)
