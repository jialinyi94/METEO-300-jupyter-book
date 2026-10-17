"""Static checks of the code cells in the book pages."""

import ast
import re
import sys
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


def _cells(text: str):
    """Code cells of a MyST page: (match, parsed module or None)."""
    for match in CELL.finditer(text):
        # Blank the ":tags:" option lines, so that line numbers stay right.
        lines = ["" if line.startswith(":") else line for line in match.group(1).splitlines()]
        try:
            yield match, ast.parse("\n".join(lines))
        except SyntaxError:
            yield match, None  # ruff reports syntax errors


def _last_artist_calls(path: Path, root: Path = ROOT) -> list[str]:
    text = path.read_text(encoding="utf-8")
    found = []
    for match, tree in _cells(text):
        if tree is None:
            continue
        body = tree.body
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


# ---------------------------------------------------------------------------------------------
# Import rule: the first code cell imports meteo300 before any package outside the standard
# library. meteo300 loads pyproj before eccodes; the other order can crash the kernel at exit.
# ---------------------------------------------------------------------------------------------


def _first_cell_import_error(text: str) -> str | None:
    """Why the first code cell breaks the import rule, or None."""
    first = next(_cells(text), None)
    if first is None:
        return None  # a page without code
    _, tree = first
    if tree is None:
        return "the first code cell does not parse"
    imports = sorted(
        (n for n in ast.walk(tree) if isinstance(n, ast.Import | ast.ImportFrom)),
        key=lambda n: (n.lineno, n.col_offset),
    )
    for node in imports:
        names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module]
        top = (names[0] or "").split(".")[0]
        if top == "meteo300":
            return None
        if top not in sys.stdlib_module_names:
            return f"line {node.lineno} imports {top} before meteo300"
    return "the first code cell does not import meteo300"


@pytest.mark.parametrize("path", PAGES, ids=lambda p: p.name)
def test_first_cell_imports_meteo300_before_other_packages(path):
    assert _first_cell_import_error(path.read_text(encoding="utf-8")) is None


@pytest.mark.parametrize(
    ("cell", "error"),
    [
        ("import os\nfrom meteo300 import data\nimport numpy\n", None),
        ("import meteo300\nimport eccodes\n", None),
        ("import numpy as np\n\nfrom meteo300 import data\n", "imports numpy before"),
        ("import cfgrib\n", "imports cfgrib before"),
        ("x = 1\n", "does not import meteo300"),
    ],
)
def test_the_import_rule_check(cell, error):
    text = "Text.\n\n```{code-cell} python\n:tags: [hide-input]\n" + cell + "```\n"
    found = _first_cell_import_error(text)
    if error is None:
        assert found is None
    else:
        assert found is not None and error in found
