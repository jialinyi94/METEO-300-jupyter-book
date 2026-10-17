"""Tests of the 403 answers for terms that the user has not accepted yet.

NASA GES DISC and the EUMETSAT Data Store answer HTTP 403 until the user accepts their terms
on a website. The tests use fake responses with the bodies that the services sent on
2026-10-17. No test sends a request.
"""

from __future__ import annotations

import datetime as dt
import json
import socket

from meteo300 import check_credentials
from meteo300 import data as d

import pytest
import requests

GESDISC_BODY = json.dumps(
    {
        "status_code": 403,
        "error_description": "EULA Acceptance Failure",
        "resolution_url": "https://urs.earthdata.nasa.gov/approve_app?client_id=TEST-ID_1",
    }
)
EUMETSAT_BODY = json.dumps(
    {
        "type": "ExceptionReport",
        "exceptions": [
            {
                "type": "Exception",
                "exceptionCode": "http://www.opengis.net/ows/2.0#NoApplicableCode",
                "exceptionText": "GeneralLicense required to access this collection",
            }
        ],
    }
)


def _response(status: int, body: str, url: str) -> requests.Response:
    resp = requests.Response()
    resp.status_code = status
    resp._content = body.encode()
    resp.encoding = "utf-8"
    resp.url = url
    return resp


def _eumdac_error():
    """The error that eumdac raises for the 403 of the Data Store."""
    from eumdac.errors import eumdac_raise_for_status
    from eumdac.product import ProductError

    url = "https://api.eumetsat.int/data/download/1.0.0/collections/C/products/P"
    try:
        eumdac_raise_for_status(
            "Could not download Product P", _response(403, EUMETSAT_BODY, url), ProductError
        )
    except ProductError as err:
        return err
    raise AssertionError("eumdac did not raise")


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Fail any test of this file that opens a connection."""

    def refuse(*args, **kwargs):
        raise AssertionError("a test tried to open a network connection")

    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)


@pytest.fixture
def accounts(monkeypatch, tmp_path):
    """Fake credentials of NASA Earthdata and EUMETSAT, and an empty cache."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("METEO300_CACHE", str(tmp_path / "cache"))
    monkeypatch.delenv("METEO300_OFFLINE", raising=False)
    monkeypatch.setenv("EARTHDATA_TOKEN", "SECRET-NASA")
    monkeypatch.setenv("EUMETSAT_CONSUMER_KEY", "KEY123")
    monkeypatch.setenv("EUMETSAT_CONSUMER_SECRET", "SECRET-EUM")


def test_licence_hint_gesdisc():
    hint = d.licence_hint(GESDISC_BODY)
    assert "NASA GESDISC DATA ARCHIVE" in hint and "Approve More Applications" in hint
    assert "client_id=TEST-ID_1" in hint
    # earthaccess hides the body; the hint then gives the known approval page.
    from earthaccess.exceptions import EulaNotAccepted

    err = EulaNotAccepted("Eula Acceptance Failure for https://data.gesdisc.earthdata.nasa.gov/x")
    assert d.GESDISC_APPROVE_URL in d.licence_hint(err)


def test_licence_hint_eumetsat():
    err = _eumdac_error()
    assert "GeneralLicense" not in str(err)  # the text is only in err.extra_info
    hint = d.licence_hint(err)
    assert "https://user.eumetsat.int/profile?activeTab=data-licenses" in hint
    assert "Meteosat > 1 hr latency & Metop" in hint
    # The hint also works through a chain of exceptions.
    try:
        raise RuntimeError("download failed") from err
    except RuntimeError as outer:
        assert d.licence_hint(outer) == hint


def test_licence_hint_other_errors():
    url = "https://data.gesdisc.earthdata.nasa.gov/x"
    other_403 = requests.HTTPError(response=_response(403, '{"error": "forbidden"}', url))
    assert d.licence_hint(other_403) is None
    assert d.licence_hint(ConnectionError("timed out")) is None
    assert d.licence_hint("HTTP 404 Not Found") is None


def test_imerg_turns_the_403_into_steps(accounts, monkeypatch):
    import earthaccess
    from earthaccess.exceptions import EulaNotAccepted

    def download(granules, local_path):
        raise EulaNotAccepted(
            "Eula Acceptance Failure for https://data.gesdisc.earthdata.nasa.gov/x"
        )

    monkeypatch.setattr(earthaccess, "login", lambda strategy: None)
    monkeypatch.setattr(earthaccess, "search_data", lambda **kw: ["granule"])
    monkeypatch.setattr(earthaccess, "download", download)
    with pytest.raises(d.CredentialsError, match="NASA GESDISC DATA ARCHIVE") as info:
        d.imerg("2020-01-01T00:00")
    assert isinstance(info.value.__cause__, EulaNotAccepted)


class _FakeProduct:
    sensing_start = dt.datetime(2025, 7, 1, 12, 0, 9)
    entries = ["MSG3-SEVI-MSG15-0100-NA-20250701121243.nat"]

    def __str__(self):
        return "MSG3-SEVI-MSG15-0100-NA-20250701121243.207000000Z-NA"

    def open(self, entry=None, chunk=None):
        raise _eumdac_error()


class _FakeStore:
    def __init__(self, token):
        pass

    def get_collection(self, collection):
        return self

    def search(self, dtstart, dtend):
        return iter([_FakeProduct()])


def test_meteosat_turns_the_403_into_steps(accounts, monkeypatch):
    import eumdac

    monkeypatch.setattr(eumdac, "AccessToken", lambda creds: "token")
    monkeypatch.setattr(eumdac, "DataStore", _FakeStore)
    with pytest.raises(d.CredentialsError, match="Meteosat > 1 hr latency & Metop"):
        d.meteosat("2025-07-01T12:00")


class _FakeHttpResponse:
    def __init__(self, status, body):
        self.status_code, self.text, self.ok = status, body, status < 400
        self.raw = self

    def read(self, n):
        return self.text.encode("latin-1")[:n]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _FakeSession:
    def __init__(self, status, body):
        self.answer = _FakeHttpResponse(status, body)

    def get(self, url, **kw):
        assert url == check_credentials.GESDISC_PROBE and kw["stream"]
        return self.answer


class _FakeAuth:
    authenticated = True


def test_verify_prints_the_steps(accounts, monkeypatch, capsys):
    import earthaccess
    import eumdac

    monkeypatch.setattr(earthaccess, "login", lambda strategy: _FakeAuth())
    session = _FakeSession(403, GESDISC_BODY)
    monkeypatch.setattr(earthaccess, "get_requests_https_session", lambda: session)
    text = check_credentials._verify("earthdata")
    assert text.startswith("ok; GES DISC download for imerg(): NASA GES DISC answered HTTP 403")
    assert "client_id=TEST-ID_1" in text

    session.answer = _FakeHttpResponse(200, "\x89HDF\r\n\x1a\n")
    assert check_credentials._verify("earthdata").endswith("imerg(): ok")
    session.answer = _FakeHttpResponse(200, "<html>Earthdata Login</html>")
    assert "not an HDF5 file" in check_credentials._verify("earthdata")

    class Token:
        def __str__(self):
            return "token"

    monkeypatch.setattr(eumdac, "AccessToken", lambda creds: Token())
    monkeypatch.setattr(eumdac, "DataStore", _FakeStore)
    text = check_credentials._verify("eumetsat")
    assert "meteosat(): EUMETSAT Data Store answered HTTP 403" in text
    assert "Meteosat > 1 hr latency & Metop" in text

    # main prints every line of the steps, and never a secret.
    monkeypatch.setattr(check_credentials, "_verify", lambda service: f"ok; {service}\nstep 1")
    check_credentials.main(["--verify"])
    out = capsys.readouterr().out
    assert "        login: ok; eumetsat\n          step 1\n" in out
    assert "SECRET" not in out and "KEY123" not in out
