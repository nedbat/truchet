import math
import random

from helpers import range2d, CairoSvg

PI = math.pi
PI2 = math.pi / 2

eps = 0.5


class SmithTile:
    def init_tile(self, ctx, wh, bgfg=None):
        if bgfg is None:
            bgfg = [[1, 1, 1, 1], [0, 0, 0, 1]]
        eps = 0
        ctx.rectangle(0 - eps, 0 - eps, wh + eps, wh + eps)
        ctx.set_source_rgba(*bgfg[0])
        ctx.fill()
        ctx.set_source_rgba(*bgfg[1])

    def draw(self, ctx, wh):
        ...


class SmithLeftTile(SmithTile):
    def draw(self, ctx, wh, bgfg=None):
        self.init_tile(ctx, wh, bgfg)
        wh2 = wh // 2
        ctx.move_to(0 - eps, wh2)
        ctx.arc(0 - eps, wh + eps, wh2 + eps, -PI2, 0)
        ctx.line_to(0 - eps, wh + eps)
        ctx.close_path()
        ctx.fill()

        ctx.move_to(wh + eps, wh2)
        ctx.arc(wh + eps, 0 - eps, wh2 + eps, PI2, PI)
        ctx.line_to(wh + eps, 0 - eps)
        ctx.close_path()
        ctx.fill()


class SmithRightTile(SmithLeftTile):
    def draw(self, ctx, wh, bgfg):
        wh2 = wh / 2
        ctx.save()
        ctx.translate(wh2, wh2)
        ctx.rotate(PI2)
        ctx.translate(-wh2, -wh2)
        super().draw(ctx, wh, bgfg)
        ctx.restore()


def smith(width=400, height=200, tilew=40, grid=False, gap=0):
    with CairoSvg(width, height) as ctx:
        tiles = [SmithLeftTile(), SmithRightTile()]
        bgfgs = [
            [[1, 1, 1, 1], [0, 0, 0, 1]],
            [[0, 0, 0, 1], [1, 1, 1, 1]],
        ]
        for ox, oy in range2d(width // tilew, height // tilew):
            ctx.save()
            ctx.translate(ox * (tilew + gap), oy * (tilew + gap))
            coin = random.choice([0, 1])
            tiles[coin].draw(ctx, tilew, bgfgs[(ox + oy + coin) % 2])
            if grid:
                ctx.set_line_width(0.1)
                ctx.rectangle(0, 0, tilew, tilew)
                ctx.set_source_rgb(0, 0, 0)
                ctx.stroke()
            ctx.restore()
    return ctx
