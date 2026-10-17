"""Plot helpers: Chinese labels and offline coastlines.

``import meteo300.plot`` sets a Chinese font when one exists. CI installs ``fonts-noto-cjk``.
Without a CJK font, Matplotlib draws boxes for Chinese characters; English labels still work.
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib as mpl
from matplotlib import font_manager

import meteo300  # noqa: F401  - points cartopy to the bundled Natural Earth files

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


CHINESE_LABELS = setup()
