"""Tests for tools/ste_check.py: good samples pass, bad samples fail with the right rule."""

import re
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
        "本页取自第 1 课 1.2 节和第 8 课 8.2 节。",
        "第 3 节和本节都讲风。每页有六节。",
        "平均风速是 51 kt，阵风是 74 kt。",
        "Coriolis 力使北半球的风向右偏。Hadley 环流在 30°N 附近下沉。",
        "Clausius–Clapeyron 方程描述饱和水汽压随温度的变化。",
        "Stefan–Boltzmann 定律和 Wien 位移定律都描述黑体。",
        "Köhler 曲线结合 Kelvin 效应和溶质效应。",
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
        ("平均风速是 51 节。", "unit-symbol"),
        ("1节约等于 0.514 m s⁻¹。", "unit-symbol"),
        ("METAR 风速的单位是节。", "unit-symbol"),
        ("以节为单位的风速约是 m s⁻¹ 的两倍。", "unit-symbol"),
        ("2 m 气温升高。", "rejected-term"),
        ("500 hPa 高度升高。", "rejected-term"),
        ("ERA5 的气压层有 37 层。", "rejected-term"),
        ("热力平流使空气变暖。", "rejected-term"),
        ("地转偏向力使风偏转。", "rejected-term"),
        ("u 风是纬向风。", "rejected-term"),
        ("模型预测 Z500。", "rejected-term"),
        ("压力梯度力推动空气。", "rejected-term"),
        ("锋面气旋向东移动。", "rejected-term"),
        ("科里奥利力使风偏转。", "rejected-term"),
        ("哈得来环流在 30°N 附近下沉。", "rejected-term"),
        ("克劳修斯-克拉珀龙方程描述饱和水汽压。", "rejected-term"),
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


# Terms named after a person are written as the English name plus a Chinese word.
# The old transliterations are rejected terms. User decision, 2026-10-17.
EPONYMS = {
    "科里奥利力": "Coriolis 力",
    "科里奥利参数": "Coriolis 参数",
    "罗斯贝数": "Rossby 数",
    "哈得来环流": "Hadley 环流",
    "费雷尔环流": "Ferrel 环流",
    "埃克曼螺线": "Ekman 螺线",
    "开尔文效应": "Kelvin 效应",
    "科勒曲线": "Köhler 曲线",
    "贝吉龙过程": "Bergeron 过程",
    "克劳修斯-克拉珀龙方程": "Clausius–Clapeyron 方程",
    "斯特藩-玻尔兹曼定律": "Stefan–Boltzmann 定律",
    "维恩位移定律": "Wien 位移定律",
    "基尔霍夫定律": "Kirchhoff 定律",
    "比尔-朗伯定律": "Beer–Lambert 定律",
    "普朗克函数": "Planck 函数",
    "瑞利散射": "Rayleigh 散射",
    "米散射": "Mie 散射",
    "理查森数": "Richardson 数",
    "雷诺平均": "Reynolds 平均",
    "莫宁-奥布霍夫长度": "Monin–Obukhov 长度",
    "欧拉视角": "Euler 视角",
    "拉格朗日视角": "Lagrange 视角",
    "拉普拉斯算子": "Laplace 算子",
}


@pytest.mark.parametrize(("old", "new"), EPONYMS.items())
def test_old_eponym_transliteration_is_rejected(old, new):
    (v,) = ste_check.check_text(f"本页讲{old}。", "x.md", GLOSSARY)
    assert str(v) == f"x.md:1: rejected-term: {old} → {new}"
    assert rules(f"本页讲 {new}。") == []


# Metric names are written in English. The Chinese names are rejected terms.
# User decision, 2026-10-17.
METRICS = {
    "均方根误差": "RMSE",
    "均方误差": "MSE",
    "平均绝对误差": "MAE",
    "均方根": "RMS",
    "偏差": "bias",
    "距平相关系数": "ACC",
    "相关系数": "correlation",
    "命中": "hit",
    "漏报": "miss",
    "空报": "false alarm",
    "连续分级概率评分": "CRPS",
    "SEEPS 评分": "SEEPS",
    "技巧评分": "skill score",
    "集合离散度": "spread",
}


@pytest.mark.parametrize(("old", "new"), METRICS.items())
def test_chinese_metric_name_is_rejected(old, new):
    (v,) = ste_check.check_text(f"本页讲{old}。", "x.md", GLOSSARY)
    assert str(v) == f"x.md:1: rejected-term: {old} → {new}"
    assert rules(f"本页讲 {new}。") == []


@pytest.mark.parametrize(
    "text",
    [
        "AIFS 的 RMSE 是 2.1 K，bias 是 −0.3 K，correlation 是 0.9。",
        "MSE 最小的预报最平滑。ACC 衡量两个距平场的形状有多像。",
        "AIFS 的 14 个预报里有 13 个 hit，IFS 有 7 个 miss。",
        "hit rate 和 false alarm 要一起报告。",
        "WeatherBench 2 用 SEEPS 和 CRPS 评估降水。",
        "探空报告的位势高度和积分的位势高度相差不到 6 m。",
        "标准误差是标准差除以样本数的平方根。",
    ],
)
def test_english_metric_names_pass(text):
    assert rules(text) == []


def test_words_that_contain_a_metric_name():
    # "标准偏差" is the standard deviation, not the bias.
    (v,) = ste_check.check_text("标准偏差。", "x.md", GLOSSARY)
    assert str(v) == "x.md:1: rejected-term: 标准偏差 → 标准差"
    # The allow list of pyproject.toml keeps the other correlation coefficients.
    cfg = ste_check.load_config(ROOT)
    glossary = ste_check.load_glossary(ROOT / cfg["glossary"], list(cfg["allow"]))
    for text in ["自相关系数衡量一个序列的记忆。", "偏相关系数去掉第三个变量的影响。"]:
        assert ste_check.check_text(text, "x.md", glossary, cfg) == []


def test_every_rejected_word_is_found():
    missed = [w for w in GLOSSARY.rejected if "rejected-term" not in rules(f"{w}。")]
    assert missed == []


def test_glossary_terms_space_latin_and_han():
    """STYLE.md 3.8: one half-width space between an English name and the Chinese word."""
    han = f"[{ste_check.HAN}]"
    latin = r"[A-Za-z0-9À-ÿ]"
    lines = (ROOT / "glossary.md").read_text(encoding="utf-8").splitlines()
    terms = [line.split("|")[1].strip() for line in lines if line.startswith("| ")]
    bad = [
        t
        for t in terms
        if re.search(f"{latin}{han}|{han}{latin}|{latin}  +{han}|{han}  +{latin}", t)
    ]
    assert bad == []


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
