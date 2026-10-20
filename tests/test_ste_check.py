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
        "pressure 随 geometric height 增加而减小。",
        "模型给 159。",
        "取值区间为 ［850, 1000］ hPa。",
        "取值区间为 ［-1, 1］。",
        "日期是 2023-01-15，时间是 06:00 UTC。",
        "geopotential height 和 geometric height 不同。",
        "isobaric surface 上的 temperature advection 决定冷暖。",
        "surface energy balance 包括 sensible heat flux 和 latent heat flux。",
        "wind speed 是 10 m s⁻¹。",
        "relative humidity 是 85%，latitude 是 30°N。",
        "被动遥感测量 irradiance。",
        "Use `(a, b)` and $[a, b]$ in code and math.",
        "dewpoint depression 越小，空气越接近 saturation。",
        "numerical weather prediction 和 numerical weather prediction model 都用物理方程。",
        "precipitation climatology 来自 30 年的 data。",
        "standard atmosphere 中六个 isobaric surface 的 geopotential height 分别是 "
        "111 m、1457 m、3012 m、5574 m、9164 m 和 11784 m。",
        "The air is saturated at this level.",
        "1990s 的 data 更少。",
        "本页取自第 1 课 1.2 节和第 8 课 8.2 节。",
        "第 3 节和本节都讲 wind。每页有六节。",
        "平均 wind speed 是 51 kt，wind gust 是 74 kt。",
        "Coriolis force 使北半球的 wind 向右偏。Hadley cell 在 30°N 附近下沉。",
        "Clausius–Clapeyron equation 描述 saturation vapour pressure 随 temperature 的变化。",
        "Stefan–Boltzmann law 和 Wien's displacement law 都描述 blackbody。",
        "Köhler curve 结合 Kelvin effect 和 solute effect。",
    ],
)
def test_good_snippets(text):
    assert rules(text) == []


@pytest.mark.parametrize(
    ("text", "rule"),
    [
        (
            "pressure 随 geometric height 增加而减小，"
            "这个规律在 troposphere 和 stratosphere 都成立，"
            "并且在全球每一个地方、每一个季节和每一个时刻都可以用 hydrostatic equation 解释清楚。",
            "zh-sentence-length",
        ),
        ("temperature 被模型低估。", "passive-voice"),
        ("模型给出了 159。", "passive-voice"),
        ("我们得到了 potential temperature。", "passive-voice"),
        ("ERA5（reanalysis）有 37 个 isobaric surface。", "parentheses"),
        ("ERA5 (a reanalysis) is useful.", "parentheses"),
        ("取值在 850–1000 hPa 之间。", "interval-format"),
        ("取值在 850~1000 hPa 之间。", "interval-format"),
        ("取值在 850 到 1000 hPa 之间。", "interval-format"),
        ("取值在 [850, 1000] hPa 之间。", "interval-format"),
        ("取值在 ［850，1000］ hPa 之间。", "interval-format"),
        ("取值在 ［1000, 850］ hPa 之间。", "interval-format"),
        ("isobaric surface 是 500hPa。", "unit-space"),
        ("temperature 是 15℃。", "unit-space"),
        ("平均 wind speed 是 51 节。", "unit-symbol"),
        ("1节约等于 0.514 m s⁻¹。", "unit-symbol"),
        ("METAR wind speed 的单位是节。", "unit-symbol"),
        ("以节为单位的 wind speed 约是 m s⁻¹ 的两倍。", "unit-symbol"),
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


# Terms named after a person are written in English. The old transliterations are
# rejected terms. User decisions, 2026-10-17 and 2026-10-20.
EPONYMS = {
    "科里奥利力": "Coriolis force",
    "科里奥利参数": "Coriolis parameter",
    "罗斯贝数": "Rossby number",
    "哈得来环流": "Hadley cell",
    "费雷尔环流": "Ferrel cell",
    "埃克曼螺线": "Ekman spiral",
    "开尔文效应": "Kelvin effect",
    "科勒曲线": "Köhler curve",
    "贝吉龙过程": "Wegener–Bergeron–Findeisen process",
    "克劳修斯-克拉珀龙方程": "Clausius–Clapeyron equation",
    "斯特藩-玻尔兹曼定律": "Stefan–Boltzmann law",
    "维恩位移定律": "Wien's displacement law",
    "基尔霍夫定律": "Kirchhoff's law",
    "比尔-朗伯定律": "Beer–Lambert law",
    "普朗克函数": "Planck function",
    "瑞利散射": "Rayleigh scattering",
    "米散射": "Mie scattering",
    "理查森数": "Richardson number",
    "雷诺平均": "Reynolds averaging",
    "莫宁-奥布霍夫长度": "Obukhov length",
    "欧拉视角": "Eulerian view",
    "拉格朗日视角": "Lagrangian view",
    "拉普拉斯算子": "Laplacian",
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
        "MSE 最小的 forecast 最平滑。ACC 衡量两个 anomaly 场的形状有多像。",
        "AIFS 的 14 个 forecast 里有 13 个 hit，IFS 有 7 个 miss。",
        "hit rate 和 false alarm 要一起报告。",
        "WeatherBench 2 用 SEEPS 和 CRPS 评估 precipitation。",
        "sounding 报告的 geopotential height 和积分的 geopotential height 相差不到 6 m。",
        "standard error 是 standard deviation 除以样本数的平方根。",
    ],
)
def test_english_metric_names_pass(text):
    assert rules(text) == []


def test_words_that_contain_a_metric_name():
    # "标准偏差" is the standard deviation, not the bias.
    (v,) = ste_check.check_text("标准偏差。", "x.md", GLOSSARY)
    assert str(v) == "x.md:1: rejected-term: 标准偏差 → standard deviation"
    # The allow list of pyproject.toml keeps the other correlation coefficients.
    cfg = ste_check.load_config(ROOT)
    glossary = ste_check.load_glossary(ROOT / cfg["glossary"], list(cfg["allow"]))
    for text in ["自相关系数衡量一个序列的记忆。", "偏相关系数去掉第三个变量的影响。"]:
        assert ste_check.check_text(text, "x.md", glossary, cfg) == []


# The six dynamics terms were the first terms written in English. User decision, 2026-10-20.
DYNAMICS_TERMS = {
    "地转风速": "geostrophic wind speed",
    "次地转风": "subgeostrophic wind",
    "超地转风": "supergeostrophic wind",
    "梯度风平衡": "gradient wind balance",
    "向心加速度": "centripetal acceleration",
    "曲率半径": "radius of curvature",
}


@pytest.mark.parametrize(("old", "new"), DYNAMICS_TERMS.items())
def test_chinese_dynamics_term_is_rejected(old, new):
    (v,) = ste_check.check_text(f"本页讲{old}。", "x.md", GLOSSARY)
    assert str(v) == f"x.md:1: rejected-term: {old} → {new}"
    assert rules(f"本页讲 {new}。") == []


@pytest.mark.parametrize(
    "text",
    [
        "low 周围的 wind 是 subgeostrophic wind，high 周围的 wind 是 supergeostrophic wind。",
        "这一点的 geostrophic wind speed 是 33.0 m s⁻¹，wind 比 geostrophic wind 慢 3%。",
        "这种三个力的平衡叫 gradient wind balance，满足它的 wind 叫 gradient wind。",
        "$R$ 是路径的 radius of curvature，$V^2/R$ 叫 centripetal acceleration。",
        "整个区域还有许多细小的斑点，ageostrophic wind speed 约 ［3, 6］ m s⁻¹。",
    ],
)
def test_english_dynamics_terms_pass(text):
    assert rules(text) == []


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
    assert str(v) == "docs/x.md:3: rejected-term: 气温 → temperature"


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
    text = "% ste-ignore-start\n气温（错误）。\n\n气温。\n% ste-ignore-end\n\ntemperature。\n"
    assert rules(text) == []


def test_main_exit_code(tmp_path, capsys):
    bad = tmp_path / "bad.md"
    bad.write_text("气温升高。\n", encoding="utf-8")
    good = tmp_path / "good.md"
    good.write_text("temperature 升高。\n", encoding="utf-8")
    assert ste_check.main([str(good)]) == 0
    assert ste_check.main([str(bad)]) == 1
    assert "rejected-term" in capsys.readouterr().out


# All terms are written in English. The Chinese name in the column 中文 of glossary.md
# is a rejected term. User decision, 2026-10-20.
@pytest.mark.parametrize(
    ("old", "new"),
    [("气压", "pressure"), ("地转风", "geostrophic wind"), ("Coriolis 力", "Coriolis force")],
)
def test_chinese_name_is_rejected(old, new):
    (v,) = ste_check.check_text(f"本页讲{old}。", "x.md", GLOSSARY)
    assert str(v) == f"x.md:1: rejected-term: {old} → {new}"
    assert rules(f"本页讲 {new}。") == []


def test_chinese_column_of_a_term_table_is_not_checked():
    text = "| 术语 | 中文 | 符号 |\n|---|---|---|\n| pressure | 气压 | $p$ |\n\n气压。\n"
    assert rules(text) == ["rejected-term"]


def test_common_words_that_contain_a_term_are_allowed():
    cfg = ste_check.load_config(ROOT)
    glossary = ste_check.load_glossary(ROOT / cfg["glossary"], list(cfg["allow"]))
    text = "中纬度的西风里有风暴，预报员看 wind speed。"
    assert ste_check.check_text(text, "x.md", glossary, cfg) == []
