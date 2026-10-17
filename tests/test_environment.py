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
