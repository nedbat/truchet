import math
import random

from helpers import range2d, show_svg, svg_context

PI = math.pi
PI2 = math.pi / 2

eps = .5

class SmithTile:
    def __init__(self, bw: int):
        self.bg = [bw] * 3
        self.fg = [1 - bw] * 3
        
    def init_tile(self, ctx, wh):
        eps = 0
        ctx.rectangle(0 - eps, 0 - eps, wh + eps, wh + eps)
        ctx.set_source_rgb(*self.bg)
        ctx.fill()
        ctx.set_source_rgb(*self.fg)
        
    def draw(self, ctx, wh: int):
        ...
        
class SmithLeftTile(SmithTile):
    def draw(self, ctx, wh: int):
        self.init_tile(ctx, wh)
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
    def draw(self, ctx, wh: int):
        wh2 = wh / 2
        ctx.save()
        ctx.translate(wh2, wh2)
        ctx.rotate(PI2)
        ctx.translate(-wh2, -wh2)
        super().draw(ctx, wh)
        ctx.restore()
        
def smith(width=400, height=200, tilew=40, grid=False, gap=0):
    with svg_context(width, height) as ctx:
        tiles = [
            [SmithLeftTile(0), SmithRightTile(1)],
            [SmithLeftTile(1), SmithRightTile(0)],
        ]
        for ox, oy in range2d(width // tilew, height // tilew):
            ctx.save()
            ctx.translate(ox * (tilew + gap), oy * (tilew + gap))
            random.choice(tiles[(ox+oy)%2]).draw(ctx, tilew)
            if grid:
                ctx.set_line_width(.1)
                ctx.rectangle(0, 0, tilew, tilew)
                ctx.set_source_rgb(0, 0, 0)
                ctx.stroke()
            ctx.restore()
    return show_svg(ctx)
