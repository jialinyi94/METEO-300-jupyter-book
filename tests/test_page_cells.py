"""Static checks of the code cells in the book pages."""

import ast
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGES = sorted((ROOT / "docs").rglob("*.md"))
CELL = re.compile(r"^```\{code-cell\}[^\n]*\n(.*?)^```", re.S | re.M)

# Matplotlib and cartopy calls that return an artist or a list of artists. When such a call is
# the last line of a cell, the page shows a line like "<matplotlib.colorbar.Colorbar at 0x...>".
RETURNS_ARTIST = {
    "add_feature",
    "annotate",
    "arrow",
    "axhline",
    "axhspan",
    "axvline",
    "axvspan",
    "bar",
    "barbs",
    "barh",
    "clabel",
    "coastlines",
    "colorbar",
    "contour",
    "contourf",
    "errorbar",
    "fill_between",
    "fill_betweenx",
    "gridlines",
    "hist",
    "imshow",
    "legend",
    "pcolormesh",
    "plot",
    "plot_barbs",
    "quiver",
    "quiverkey",
    "scatter",
    "set_title",
    "set_xlabel",
    "set_ylabel",
    "step",
    "streamplot",
    "suptitle",
    "text",
}


def _last_artist_calls(path: Path, root: Path = ROOT) -> list[str]:
    text = path.read_text(encoding="utf-8")
    found = []
    for match in CELL.finditer(text):
        # Blank the ":tags:" option lines, so that line numbers stay right.
        lines = ["" if line.startswith(":") else line for line in match.group(1).splitlines()]
        try:
            body = ast.parse("\n".join(lines)).body
        except SyntaxError:
            continue  # ruff reports syntax errors
        if not body or not isinstance(body[-1], ast.Expr):
            continue
        call = body[-1].value
        if (
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Attribute)
            and call.func.attr in RETURNS_ARTIST
        ):
            line = text[: match.start(1)].count("\n") + body[-1].lineno
            found.append(f"{path.relative_to(root).as_posix()}:{line}: {call.func.attr}(...)")
    return found


@pytest.mark.parametrize("path", PAGES, ids=lambda p: p.name)
def test_no_cell_ends_with_a_call_that_returns_an_artist(path):
    # Assign the result to a variable, for example "cbar = fig.colorbar(...)".
    assert _last_artist_calls(path) == []


def test_the_check_finds_a_colorbar_call(tmp_path):
    page = tmp_path / "docs" / "page.md"
    page.parent.mkdir()
    page.write_text(
        "```{code-cell} python\n:tags: [hide-input]\nfig.colorbar(cf, ax=ax)\n```\n"
        "```{code-cell} python\ncbar = fig.colorbar(cf, ax=ax)\n```\n",
        encoding="utf-8",
    )
    found = _last_artist_calls(page, root=tmp_path)
    assert found == ["docs/page.md:3: colorbar(...)"]

