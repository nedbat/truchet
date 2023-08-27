from helpers import make_bgfg
from n6 import n6_circles
from tiler import multiscale_truchet

DIR = "~/wallpaper/tru6/1680"
NIMG = 30
for i in range(NIMG):
    multiscale_truchet(
        tiles=n6_circles, width=1680, height=1050, tilew=200, nlayers=3,
        chance=.4,
        seed=i,
        **make_bgfg(i/NIMG, (.55, .45), .45),
        format="png", output=f"{DIR}/bg_{i:02d}.png",
    )

DIR = "~/wallpaper/tru6/1920"
NIMG = 15
for i in range(NIMG):
    multiscale_truchet(
        tiles=n6_circles, width=1920, height=1080, tilew=200, nlayers=3,
        chance=.4,
        seed=i,
        **make_bgfg(i/NIMG, (.55, .45), .45),
        format="png", output=f"{DIR}/bg_{i:02d}.png",
    )

DIR = "~/wallpaper/tru6/2872"
for i in range(NIMG):
    multiscale_truchet(
        tiles=n6_circles, width=2872, height=5108, tilew=300, nlayers=3,
        chance=.4, bg="#335495", fg="#243b6a", seed=i,
        format="png", output=f"{DIR}/bg_{i:02d}.png",
    )

DIR = "~/wallpaper/tru6/1360"
NIMG = 120
for i in range(NIMG):
    multiscale_truchet(
        tiles=n6_circles, width=1360, height=768, tilew=150, nlayers=3,
        chance=.4,
        seed=i*10,
        **make_bgfg(i/NIMG, (.55, .45), .45),
        format="png", output=f"{DIR}/bg_{i:03d}.png",
    )
