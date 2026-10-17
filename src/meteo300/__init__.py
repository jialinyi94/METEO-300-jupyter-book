"""meteo300: data access and plotting helpers of the data book."""

from pathlib import Path

_NATURAL_EARTH = Path(__file__).resolve().parents[2] / "data" / "natural_earth"


def _use_bundled_natural_earth() -> None:
    """Let cartopy find the bundled Natural Earth files, so maps work without network.

    cartopy looks for ``<pre_existing_data_dir>/shapefiles/natural_earth/...`` first and
    downloads a file only when it is not there. The default directory is ``"."``.
    """
    try:
        import cartopy
    except ImportError:
        return
    current = Path(cartopy.config.get("pre_existing_data_dir") or ".")
    if _NATURAL_EARTH.is_dir() and not (current / "shapefiles" / "natural_earth").is_dir():
        cartopy.config["pre_existing_data_dir"] = str(_NATURAL_EARTH)


_use_bundled_natural_earth()
