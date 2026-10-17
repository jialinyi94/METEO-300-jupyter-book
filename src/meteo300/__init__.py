"""meteo300: data access and plotting helpers of the data book.

Import rule: import meteo300 before eccodes, cfgrib and earthkit.

eccodes >= 2.43, cfgrib and earthkit-geo load eckitlib, which brings its own copy of the PROJ
and SQLite libraries. pyproj brings another copy. When the eckitlib copy loads first, the
process crashes at exit with "double free" or a segmentation fault. The results before the
exit are correct. When pyproj loads first, nothing crashes. So this package imports pyproj
before any other third-party package, and warns when eccodes was imported before it.
"""

import sys
import warnings
from pathlib import Path

# Python modules that load the eckitlib copy of PROJ: eccodes and cfgrib load gribapi and
# eckitlib, earthkit-geo loads eckitlib.
_ECKIT_MODULES = ("eccodes", "gribapi", "eckitlib")


def _eckit_loaded_before_pyproj() -> bool:
    """True when an eckit module is in sys.modules and pyproj is not, or came later."""
    order = list(sys.modules)  # sys.modules keeps the order of the imports
    first_eckit = min((order.index(m) for m in _ECKIT_MODULES if m in sys.modules), default=None)
    if first_eckit is None:
        return False
    return "pyproj" not in sys.modules or order.index("pyproj") > first_eckit


if _eckit_loaded_before_pyproj():
    warnings.warn(
        "eccodes, cfgrib or earthkit.geo was imported before meteo300. Their copy of the PROJ "
        "library loaded before the copy of pyproj, so this process may crash at exit (double "
        "free or segmentation fault). Restart the kernel or the program, and import meteo300 "
        "before eccodes, cfgrib or earthkit.",
        RuntimeWarning,
        skip_file_prefixes=("<frozen importlib", str(Path(__file__).parent)),
    )

import pyproj  # noqa: E402, F401  - must load before eccodes: see the module docstring

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
