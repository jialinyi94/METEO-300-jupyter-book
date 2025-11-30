import numpy as np


def compute_avg_temperature(
    pressure_level_a: float,
    hight_a: float,
    pressure_level_b: float,
    hight_b: float,
    air_gas_constant: float = 287.05,
    gravity: float = 9.80665,
):
    """
    Compute the average temperature between two pressure levels using the hypsometric equation.

    Parameters
    ----------
    pressure_level_a : float
        Pressure at level a (in Pascals).
    hight_a : float
        Height at level a (in meters).
    pressure_level_b : float
        Pressure at level b (in Pascals).
    hight_b : float
        Height at level b (in meters).
    air_gas_constant : float, optional
        Specific gas constant for dry air (default is 287.05 J/(kg·K)).
    gravity : float, optional
        Acceleration due to gravity (default is 9.80665 m/s²).

    Returns
    -------
    float
        Average temperature between the two pressure levels (in Kelvin).
    """
    delta_z = hight_b - hight_a
    delta_ln_p = np.log(pressure_level_a / pressure_level_b)
    avg_temperature = ( gravity  * delta_z) / (air_gas_constant* delta_ln_p)
    return avg_temperature

# Example usage:
if __name__ == "__main__":
    p_a = 50000  # Pressure at level a in Pascals
    z_a = 5600       # Height at level a in meters
    p_b = 100000   # Pressure at level b in Pascals
    z_b = 0    # Height at level b in meters

    avg_temp = compute_avg_temperature(p_a, z_a, p_b, z_b)
    print(f"Average Temperature between the two pressure levels: {avg_temp:.2f} K")
