from drawing import cairo_context
from helpers import range2d

import numpy as np

def downsample_by_averaging(img, window_shape):
    return np.mean(
        img.reshape((
            *img.shape[:-2],
            img.shape[-2] // window_shape[-2], window_shape[-2],
            img.shape[-1] // window_shape[-1], window_shape[-1],
        )),
        axis=(-1, -3),
    )

def show_array_as_blocks(image, width, tilew):
    imgh, imgw = image.shape
    tile_across = width // tilew
    window_w = imgw // tile_across
    simg = downsample_by_averaging(image, (window_w, window_w))
    imgh, imgw = simg.shape
    with cairo_context(width, width) as ctx:
        for x, y in range2d(imgw, imgh):
            color = simg[y, x] / 256
            dx = x * tilew
            dy = y * tilew
            ctx.set_source_rgb(color, color, color)
            ctx.rectangle(dx, dy, tilew, tilew)
            ctx.fill()
    return ctx
