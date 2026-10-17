"""Show which data services with accounts are ready on this machine.

Usage::

    uv run python -m meteo300.check_credentials           # look for credentials only
    uv run python -m meteo300.check_credentials --verify  # also log in and test a download

The command never prints a secret. It prints where it found the credentials, or how to
register.

Valid credentials are not always enough. NASA GES DISC (``imerg``) and the EUMETSAT Data
Store (``meteosat``) answer HTTP 403 until the user accepts their terms on a website. With
``--verify``, the command opens one small file of each and reads at most 16 bytes. When the
answer is one of these 403s, it prints what the user must do (see ``data.licence_hint``).
"""

from __future__ import annotations

import argparse
import datetime as dt
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


# Files that --verify opens to test a download. GES DISC: one monthly IMERG file (V07B).
# EUMETSAT: the SEVIRI full disc of the hourly slot 2025-07-01 12:00 UTC.
GESDISC_PROBE = (
    "https://data.gesdisc.earthdata.nasa.gov/data/GPM_L3/GPM_3IMERGM.07/2020/"
    "3B-MO.MS.MRG.3IMERG.20200101-S000000-E235959.01.V07B.HDF5"
)
EUMETSAT_PROBE = ("EO:EUM:DAT:MSG:HRSEVIRI", dt.datetime(2025, 7, 1, 12, 0))


def _short(err: BaseException) -> str:
    text = str(err).splitlines()[0][:120] if str(err) else ""
    return f"failed: {type(err).__name__} {text}"


def _probe_gesdisc() -> str:
    """Open one IMERG file at GES DISC without downloading it. 'ok' or the reason."""
    import earthaccess

    session = earthaccess.get_requests_https_session()
    with session.get(GESDISC_PROBE, stream=True, timeout=d.HTTP_TIMEOUT) as resp:
        status = resp.status_code
        if not resp.ok:
            return d.licence_hint(resp.text[:2000]) or f"failed: HTTP {status}"
        if resp.raw.read(4) == b"\x89HDF":
            return "ok"
    return f"failed: HTTP {status}, but the answer is not an HDF5 file (a login page?)"


def _probe_eumetsat(token) -> str:
    """Read the first 16 bytes of one SEVIRI product. 'ok' or the reason."""
    import eumdac

    collection, when = EUMETSAT_PROBE
    found = (
        eumdac.DataStore(token)
        .get_collection(collection)
        .search(dtstart=when, dtend=when + dt.timedelta(minutes=15))
    )
    products = list(found)
    if not products:
        return f"failed: no product of {collection} at {when:%Y-%m-%d %H:%M} UTC"
    try:
        with products[0].open(chunk=(0, 16)) as fsrc:
            fsrc.read(16)
    except Exception as err:  # noqa: BLE001 - report every failure as text
        return d.licence_hint(err) or _short(err)
    return "ok"


def _verify(service: str) -> str:
    """Log in once, and test a download where terms can block it.

    Return 'ok' or a short error without secrets. For a 403 of terms not accepted yet, the
    text has several lines: what the user must do on the website.
    """
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
            if not getattr(auth, "authenticated", False):
                return "login failed"
            return f"ok; GES DISC download for imerg(): {_probe_gesdisc()}"
        if service == "eumetsat":
            import eumdac

            token = eumdac.AccessToken(d.eumetsat_credentials())
            if not str(token):
                return "login failed"
            return f"ok; Data Store download for meteosat(): {_probe_eumetsat(token)}"
        key, _own = d.knmi_key()
        url = f"{d.KNMI_API}/cesar_tower_meteo_lc1_t10/versions/v1.1/files?maxKeys=1"
        d._http_get(url, headers={"Authorization": key})
        return "ok"
    except Exception as err:  # noqa: BLE001 - report every failure as text
        return d.licence_hint(err) or _short(err)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--verify", action="store_true", help="log in to each ready service and test a download"
    )
    args = parser.parse_args(argv)
    width = max(len(s[1]) for s in SERVICES)
    ready_count = 0
    for service, title, readers, where in SERVICES:
        ready, detail = _status(service)
        ready_count += ready
        mark = "READY  " if ready else "MISSING"
        print(f"{mark} {title:<{width}}  {readers:<22} {detail}")
        if ready and args.verify:
            first, *more = _verify(service).splitlines()
            print(f"        login: {first}")
            for line in more:
                print(f"          {line}")
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
