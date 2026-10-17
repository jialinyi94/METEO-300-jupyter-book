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
