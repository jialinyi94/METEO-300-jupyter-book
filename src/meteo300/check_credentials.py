"""Show which data services with accounts are ready on this machine.

Usage::

    uv run python -m meteo300.check_credentials           # look for credentials only
    uv run python -m meteo300.check_credentials --verify  # also log in to each service

The command never prints a secret. It prints where it found the credentials, or how to
register.
"""

from __future__ import annotations

import argparse
import sys

from meteo300 import data as d

SERVICES = [
    ("ads", "Copernicus ADS", "cams()", "~/.cdsapirc or ~/.adsapirc with the ADS url"),
    (
        "earthdata",
        "NASA Earthdata",
        "imerg(), ceres_ebaf()",
        "~/.netrc, ~/.config/earthdata/token or EARTHDATA_*",
    ),
    ("eumetsat", "EUMETSAT Data Store", "meteosat()", "~/.eumdac/credentials"),
    ("knmi", "KNMI Data Platform", "cabauw()", "KNMI_API_KEY or ~/.config/knmi/api_key"),
]


def _status(service: str) -> tuple[bool, str]:
    if service == "ads":
        creds = d.ads_credentials()
        return (creds is not None, f"url {creds[0]}" if creds else "no ADS key found")
    if service == "earthdata":
        strategy = d.earthdata_credentials()
        return (strategy is not None, f"login strategy '{strategy}'" if strategy else "none")
    if service == "eumetsat":
        creds = d.eumetsat_credentials()
        return (creds is not None, "consumer key and secret found" if creds else "none")
    key, own = d.knmi_key()
    return (True, "own key" if own else "public anonymous key (shared, rate-limited)")


def _verify(service: str) -> str:
    """Log in once. Return 'ok' or a short error without secrets."""
    try:
        if service == "ads":
            import cdsapi

            url, key = d.ads_credentials()
            client = cdsapi.Client(url=url, key=key, quiet=True, progress=False)
            inner = getattr(client, "client", None)
            if inner is not None and hasattr(inner, "check_authentication"):
                inner.check_authentication()
                return "ok"
            return "found; cdsapi has no login test, a first download will test it"
        if service == "earthdata":
            import earthaccess

            auth = earthaccess.login(strategy=d.earthdata_credentials())
            return "ok" if getattr(auth, "authenticated", False) else "login failed"
        if service == "eumetsat":
            import eumdac

            token = eumdac.AccessToken(d.eumetsat_credentials())
            return "ok" if str(token) else "login failed"
        key, _own = d.knmi_key()
        url = f"{d.KNMI_API}/cesar_tower_meteo_lc1_t10/versions/v1.1/files?maxKeys=1"
        d._http_get(url, headers={"Authorization": key})
        return "ok"
    except Exception as err:  # noqa: BLE001 - report every failure as text
        text = str(err).splitlines()[0][:120] if str(err) else ""
        return f"failed: {type(err).__name__} {text}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verify", action="store_true", help="log in to each ready service")
    args = parser.parse_args(argv)
    width = max(len(s[1]) for s in SERVICES)
    ready_count = 0
    for service, title, readers, where in SERVICES:
        ready, detail = _status(service)
        ready_count += ready
        mark = "READY  " if ready else "MISSING"
        print(f"{mark} {title:<{width}}  {readers:<22} {detail}")
        if ready and args.verify:
            print(f"        login: {_verify(service)}")
        if not ready:
            print(f"        place: {where}")
            for line in d.HOW_TO_REGISTER[service].splitlines():
                print(f"        {line}")
    print("Public readers need no account: era5, era5_monthly, era5_daily_mean,")
    print("era5_climatology, sounding, metar, ecmwf_forecast, weatherbench2, wb2_scores, co2,")
    print("goes_abi, meteosat_image, aeronet_aod, gpcp, turbulence_20hz.")
    print(f"{ready_count} of {len(SERVICES)} services ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
