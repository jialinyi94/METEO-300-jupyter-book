"""Tests for tools/ste_check.py: good samples pass, bad samples fail with the right rule."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import ste_check  # noqa: E402

GLOSSARY = ste_check.load_glossary(ROOT / "glossary.md", [])


def rules(text: str) -> list[str]:
    return [v.rule for v in ste_check.check_text(text, "x.md", GLOSSARY)]


def test_good_sample_has_no_violation():
    text = (ROOT / "tests" / "ste_samples" / "good.md").read_text(encoding="utf-8")
    violations = ste_check.check_text(text, "good.md", GLOSSARY)
    assert violations == [], "\n".join(map(str, violations))


@pytest.mark.parametrize(
    "text",
    [
        "气压随几何高度增加而减小。",
        "模型给 159。",
        "取值区间为 ［850, 1000］ hPa。",
        "取值区间为 ［-1, 1］。",
        "日期是 2023-01-15，时间是 06:00 UTC。",
        "位势高度和几何高度不同。",
        "等压面上的温度平流决定冷暖。",
        "地面能量平衡包括感热通量和潜热通量。",
        "风速是 10 m s⁻¹。",
        "相对湿度是 85%，纬度是 30°N。",
        "被动遥感测量辐照度。",
        "Use `(a, b)` and $[a, b]$ in code and math.",
        "温度露点差越小，空气越接近饱和。",
        "数值天气预报和数值模式都用物理方程。",
        "降水气候态来自 30 年的数据。",
        "标准大气中六个等压面的位势高度分别是 111 m、1457 m、3012 m、5574 m、9164 m 和 11784 m。",
        "The air is saturated at this level.",
        "1990s 的数据更少。",
    ],
)
def test_good_snippets(text):
    assert rules(text) == []


@pytest.mark.parametrize(
    ("text", "rule"),
    [
        (
            "气压随几何高度增加而减小，这个规律在对流层和平流层都成立，"
            "并且在全球每一个地方都可以用静力方程解释清楚。",
            "zh-sentence-length",
        ),
        ("温度被模型低估。", "passive-voice"),
        ("模型给出了 159。", "passive-voice"),
        ("我们得到了位温。", "passive-voice"),
        ("ERA5（再分析）有 37 个等压面。", "parentheses"),
        ("ERA5 (a reanalysis) is useful.", "parentheses"),
        ("取值在 850–1000 hPa 之间。", "interval-format"),
        ("取值在 850~1000 hPa 之间。", "interval-format"),
        ("取值在 850 到 1000 hPa 之间。", "interval-format"),
        ("取值在 [850, 1000] hPa 之间。", "interval-format"),
        ("取值在 ［850，1000］ hPa 之间。", "interval-format"),
        ("取值在 ［1000, 850］ hPa 之间。", "interval-format"),
        ("等压面是 500hPa。", "unit-space"),
        ("温度是 15℃。", "unit-space"),
        ("2 m 气温升高。", "rejected-term"),
        ("500 hPa 高度升高。", "rejected-term"),
        ("ERA5 的气压层有 37 层。", "rejected-term"),
        ("热力平流使空气变暖。", "rejected-term"),
        ("地转偏向力使风偏转。", "rejected-term"),
        ("u 风是纬向风。", "rejected-term"),
        ("模型预测 Z500。", "rejected-term"),
        ("压力梯度力推动空气。", "rejected-term"),
        ("锋面气旋向东移动。", "rejected-term"),
        (
            "The model output was compared with the analysis by the team at the centre, "
            "and the result shows a clear and large error over the whole of the northern "
            "hemisphere in winter.",
            "en-sentence-length",
        ),
        ("The forecast was evaluated against ERA5.", "passive-voice"),
        ("第一句。第二句。第三句。第四句。第五句。第六句。第七句。", "paragraph-length"),
    ],
)
def test_bad_snippets(text, rule):
    assert rule in rules(text)


def test_output_format_and_line_numbers():
    text = "第一段。\n\n第二段有气温。\n"
    (v,) = ste_check.check_text(text, "docs/x.md", GLOSSARY)
    assert str(v) == "docs/x.md:3: rejected-term: 气温 → 温度"


def test_code_cells_frontmatter_and_math_are_skipped():
    text = (
        "---\ntitle: 气温（标题）\n---\n\n"
        "```{code-cell} python\nx = (1, 2)  # 被\n```\n\n"
        "$$\n(a + b)\n$$\n\n"
        "```\n气温\n```\n"
    )
    assert rules(text) == []


def test_prose_directive_is_checked_but_options_are_not():
    text = ":::{note}\n:label: note-1\n:class: (dropdown)\n气温升高。\n:::\n"
    assert rules(text) == ["rejected-term"]


def test_ignore_block():
    text = "% ste-ignore-start\n气温（错误）。\n\n气温。\n% ste-ignore-end\n\n温度。\n"
    assert rules(text) == []


def test_main_exit_code(tmp_path, capsys):
    bad = tmp_path / "bad.md"
    bad.write_text("气温升高。\n", encoding="utf-8")
    good = tmp_path / "good.md"
    good.write_text("温度升高。\n", encoding="utf-8")
    assert ste_check.main([str(good)]) == 0
    assert ste_check.main([str(bad)]) == 1
    assert "rejected-term" in capsys.readouterr().out
