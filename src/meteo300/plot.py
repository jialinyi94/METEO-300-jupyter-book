"""Plot helpers: Chinese labels, offline coastlines and wind vectors on maps.

``import meteo300.plot`` sets a Chinese font when one exists. CI installs ``fonts-noto-cjk``.
Without a CJK font, Matplotlib draws boxes for Chinese characters; English labels still work.

:func:`grid_vectors` corrects the direction of wind arrows and barbs on cartopy maps.
"""

from __future__ import annotations

import os
from pathlib import Path

import meteo300  # noqa: F401  - points cartopy to the bundled Natural Earth files

import matplotlib as mpl
import numpy as np
from matplotlib import font_manager

CJK_FONTS = [
    "Noto Sans CJK SC",
    "Noto Sans CJK JP",
    "Noto Sans SC",
    "Source Han Sans SC",
    "WenQuanYi Zen Hei",
]


def _register_font_files() -> None:
    """Add CJK font files that the Matplotlib font cache does not hold.

    ``METEO300_CJK_FONT`` can name a font file, for example ``NotoSansCJKsc-VF.ttf``.
    """
    paths = []
    env = os.environ.get("METEO300_CJK_FONT")
    if env:
        paths.append(Path(env).expanduser())
    for pattern in ("NotoSansCJK*", "NotoSansSC*", "SourceHanSans*"):
        paths += sorted((Path.home() / ".local" / "share" / "fonts").glob(pattern))
    for path in paths:
        if path.is_file():
            try:
                font_manager.fontManager.addfont(str(path))
            except (OSError, RuntimeError, ValueError):
                continue


def cjk_font() -> str | None:
    """Name of the first installed CJK font, or None."""
    names = {f.name for f in font_manager.fontManager.ttflist}
    found = next((n for n in CJK_FONTS if n in names), None)
    if found is None:
        _register_font_files()
        names = {f.name for f in font_manager.fontManager.ttflist}
        found = next((n for n in CJK_FONTS if n in names), None)
    return found


def setup() -> bool:
    """Use a CJK font for all text when one exists. Return True if Chinese labels will work."""
    font = cjk_font()
    if font is None:
        return False
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["font.sans-serif"] = [font, "DejaVu Sans"]
    mpl.rcParams["axes.unicode_minus"] = False  # CJK fonts lack the Unicode minus sign
    return True


def coastlines(ax, resolution: str = "110m", borders: bool = False, **kwargs):
    """Draw coastlines (and country borders) from the bundled Natural Earth files.

    ``resolution`` is ``"110m"`` or ``"50m"``. Both are in ``data/natural_earth``, so the call
    needs no network. Keyword arguments go to ``ax.add_feature``.
    """
    import cartopy.feature as cfeature

    kwargs = {"linewidth": 0.6, "edgecolor": "0.2", **kwargs}
    ax.add_feature(cfeature.COASTLINE.with_scale(resolution), facecolor="none", **kwargs)
    if borders:
        ax.add_feature(
            cfeature.BORDERS.with_scale(resolution), facecolor="none", linestyle=":", **kwargs
        )
    return ax


def grid_vectors(lat, u, v):
    """Turn east and north wind components into vectors that cartopy draws correctly.

    Use the result in place of ``u`` and ``v`` with ``transform=ccrs.PlateCarree()`` in
    ``ax.quiver``, ``ax.barbs`` or MetPy ``StationPlot.plot_barb`` on a cartopy map.

    Cartopy reads the components of a vector on ``PlateCarree`` as steps in degrees of
    longitude and latitude. A degree of longitude is shorter than a degree of latitude by the
    factor cos(latitude). Without a correction, cartopy turns each arrow toward north or south.
    The error is zero for a wind along a meridian or a parallel and largest in between. It
    grows with latitude: up to 16° at 55°N and 19° at 60°N. This function makes the eastward
    step larger by 1/cos(latitude) and keeps the length of the vector, so quiver keys and barb
    flags stay correct.

    ``lat`` is in degrees and must broadcast against ``u`` and ``v``. For a field on a
    (latitude, longitude) grid of NumPy arrays, pass a 2-D latitude, for example from
    ``np.meshgrid``. xarray DataArrays broadcast by dimension name. Use values without units.
    A calm wind stays zero and a missing value stays NaN.
    """
    ue = u / np.cos(np.deg2rad(lat))
    length = np.hypot(ue, v)
    factor = np.hypot(u, v) / np.maximum(length, np.finfo(float).tiny)
    return ue * factor, v * factor


CHINESE_LABELS = setup()
