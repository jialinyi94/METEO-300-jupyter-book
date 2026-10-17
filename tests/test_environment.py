"""Checks that the packages the pages use import and work together."""

import numpy as np
import pytest


def test_earthkit_meteo_and_transforms_import():
    import earthkit.meteo.thermo as thermo
    import earthkit.transforms  # needs geopandas, which the package does not require

    assert earthkit.transforms.temporal is not None
    # Potential temperature of 280 K at 850 hPa: 280 * (1000 / 850) ** 0.2857 = 293.3 K.
    theta = thermo.potential_temperature(np.array([280.0]), np.array([85000.0]))
    assert theta[0] == pytest.approx(293.3, abs=0.1)


def test_importing_metpy_first_in_a_kernel_prints_no_warning():
    # "import metpy.calc" imports pooch, which imports tqdm.auto. Without ipywidgets, tqdm warns
    # "IProgress not found" in every notebook that imports MetPy.
    from jupyter_client.manager import start_new_kernel

    km, kc = start_new_kernel(kernel_name="python3")
    stderr = []

    def hook(msg):
        if msg["msg_type"] == "stream" and msg["content"]["name"] == "stderr":
            stderr.append(msg["content"]["text"])

    try:
        reply = kc.execute_interactive("import metpy.calc", output_hook=hook, timeout=120)
    finally:
        kc.stop_channels()
        km.shutdown_kernel(now=True)
    assert reply["content"]["status"] == "ok"
    assert "".join(stderr) == ""


# ---------------------------------------------------------------------------------------------
# Import rule: meteo300 loads pyproj before eccodes. eccodes >= 2.43 and earthkit-geo bring a
# second copy of the PROJ library. When that copy loads first, the process crashes at exit.
# Each check runs in a new Python process, because the crash happens only at exit.
# ---------------------------------------------------------------------------------------------

RIGHT_ORDER = """
import os
import tempfile

import meteo300
import eccodes
import earthkit.data
import earthkit.geo
import earthkit.plots

import cartopy.crs as ccrs
import numpy as np
import pyproj
import xarray as xr

with tempfile.TemporaryDirectory() as tmp:
    # Write the GRIB 2 sample of eccodes to a file, then read the file in three ways.
    path = os.path.join(tmp, "sample.grib2")
    gid = eccodes.codes_grib_new_from_samples("regular_ll_sfc_grib2")
    with open(path, "wb") as f:
        eccodes.codes_write(gid, f)
    eccodes.codes_release(gid)
    with open(path, "rb") as f:
        gid = eccodes.codes_grib_new_from_file(f)
        n = eccodes.codes_get(gid, "numberOfValues")
        values = eccodes.codes_get_values(gid)
        eccodes.codes_release(gid)
    assert n > 0 and values.size == n
    fields = earthkit.data.from_source("file", path).to_fieldlist()
    assert len(fields) == 1 and fields[0].to_numpy().size == n
    ds = xr.open_dataset(path, engine="cfgrib", backend_kwargs={"indexpath": ""})
    assert ds[list(ds.data_vars)[0]].size == n
    ds.close()

x, y = pyproj.Transformer.from_crs(4326, 27700, always_xy=True).transform(-0.46, 51.47)
assert 500_000 < x < 520_000 and 170_000 < y < 180_000  # Heathrow on the British grid
p = ccrs.LambertConformal().transform_points(ccrs.PlateCarree(), np.array([-5.0]), np.array([52.0]))
assert np.isfinite(p).all()
print("ok")
"""


def _python(code: str):
    import os
    import subprocess
    import sys

    env = os.environ | {"MPLBACKEND": "Agg"}
    return subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, timeout=300, env=env
    )


@pytest.mark.parametrize("run", [1, 2, 3])
def test_meteo300_first_then_eccodes_and_earthkit_exits_cleanly(run):
    result = _python(RIGHT_ORDER)
    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip().endswith("ok")
    assert "import meteo300 before eccodes" not in result.stderr


@pytest.mark.parametrize(
    ("first", "warns"),
    [
        ("import eccodes", True),
        ("import cfgrib", True),
        ("import earthkit.geo", True),
        ("import earthkit.plots", False),  # earthkit.plots does not load eccodes
        ("import pyproj\nimport eccodes", False),
    ],
)
def test_meteo300_warns_when_eccodes_came_first(first, warns):
    # os._exit skips the clean-up at exit, where the wrong order crashes.
    code = f"import os\nimport sys\n{first}\nimport meteo300\nsys.stderr.flush()\nos._exit(0)\n"
    result = _python(code)
    assert result.returncode == 0, result.stderr[-2000:]
    assert ("import meteo300 before eccodes" in result.stderr) == warns
    if warns:
        # The warning points to the line of the user's code that imports meteo300.
        assert "<string>:" in result.stderr and "RuntimeWarning" in result.stderr
