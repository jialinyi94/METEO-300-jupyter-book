# 写作规范

本书的正文用中文。代码、标识符、数据集名和软件包名用英文。本规范改编自 ASD-STE100 简化技术英语。

检查器 `tools/ste_check.py` 自动检查标有“自动检查”的规则。提交前，pre-commit 运行检查器。CI 也运行检查器，有违规时构建失败。

术语以 [glossary.md](glossary.md) 为准。

## 1 中文规则

### 规则 1：一词一义，一义一词

每个概念只用一个词。一个词只表示一个概念。给一种量起了名字，全书都用这个名字。术语表的“弃用词”一列列出不用的词。自动检查。

- 错误：500 hPa 高度在槽前降低，这个气压层上的气温也降低。
- 正确：500 hPa 位势高度在槽前降低，这个等压面上的温度也降低。

### 规则 2：一句只说一件事，不超过 40 字

计数方法：每个汉字、英文单词和数字各算 1 个。标点不算。行内公式和行内代码不算。自动检查。

一个句子列出 3 个或更多数字时，数字不计数。这样的句子先说每个数字是什么，再列数字。

- 错误：ERA5 是 ECMWF 制作的再分析数据集，它把观测和数值模式结合起来，给出 1940 年以来每小时 0.25° 网格上的全球大气状态。
- 正确：ERA5 是 ECMWF 制作的再分析数据集。它把观测和数值模式结合起来。它给出 1940 年以来每小时的全球大气状态。网格间距是 0.25°。
- 错误：结果是 111 m、1457 m 和 5574 m。
- 正确：1000 hPa、850 hPa 和 500 hPa 的位势高度分别是 111 m、1457 m 和 5574 m。

### 规则 3：主语清楚，用主动语态

每个句子说清楚谁做了什么。不用“被”字句。不用没有主语的“给出了”“得到了”。自动检查“被”“给出了”“得到了”。

- 错误：给出了 159 的 RMSE。
- 正确：模型给 159 m² s⁻² 的 RMSE。
- 错误：2 m 温度被模型低估了 2 K。
- 正确：模型把 2 m 温度低估了 2 K。

### 规则 4：一段只有一个主题，最多六句

一个段落只讲一件事。换主题时，换段落。自动检查句数。

- 错误：一个段落先讲静力平衡，再讲 ERA5 的下载方式，最后讲 GraphCast 的输入变量。
- 正确：三个主题写成三个段落，分别放在“知识点”“数据集”“AI 天气连接”三节。

### 规则 5：不用括号写附加说明

括号里的内容要么重要，要么不重要。重要的内容写成一个句子。不重要的内容删去。英文术语放在术语表或页面的术语表格里。自动检查。

- 错误：位温（potential temperature）在干绝热过程中守恒。
- 正确：位温在干绝热过程中守恒。
- 错误：ERA5（ECMWF 的第五代再分析）有 37 个等压面。
- 正确：ERA5 是 ECMWF 的第五代再分析。它有 37 个等压面。

## 2 英文规则

README 的英文摘要和图的替代文字使用英文。英文使用 ASD-STE100 的以下规则。

1. A descriptive sentence has 25 words or fewer. An instruction has 20 words or fewer. The checker counts words.
2. Use the active voice. The checker finds "be + past participle".
3. A paragraph has one topic and six sentences or fewer.
4. Use one word for one meaning. Use the English terms of the glossary.
5. Write an instruction in the imperative.
6. Do not use parentheses for side remarks.

例子：

- Wrong: The forecast was evaluated against ERA5 by the team, and it was found that the error grows with lead time over the whole hemisphere.
- Right: We evaluate the forecast against ERA5. The error grows with lead time.
- Wrong: The packages should be installed with uv (see below).
- Right: Install the packages with uv.

## 3 格式约定

### 3.1 区间

区间写作 ［下限, 上限］，单位写在右括号后，中间空一格。括号是全角方括号 ［ ］。两个数之间用半角逗号加一个空格。下限小于上限。自动检查。

- 错误：850–1000 hPa、850~1000 hPa、850 到 1000 hPa、[850, 1000] hPa、（850，1000）hPa
- 正确：［850, 1000］ hPa
- 错误：云量的取值是 0-1。
- 正确：云量的取值区间是 ［0, 1］。

日期 2023-01-15 和时间 06:00 不是区间。检查器跳过它们。

### 3.2 数字和单位

数字和单位之间空一格。单位用国际单位制符号，负指数写成上标。单位符号之间空一格，不用斜杠。自动检查数字和单位之间的空格。

- 错误：500hPa、10m/s、15℃、5 kg/m³、1000 mb
- 正确：500 hPa、10 m s⁻¹、15 °C、5 kg m⁻³、1000 hPa

例外：百分号和角度符号紧贴数字，例如 85%、30°N、0.25°。

风速的单位 knot 只写符号 kt，和 hPa 一样。“节”只表示文档的节，例如“第 2 课 2.2 节”。自动检查数字后面的“节”。

- 错误：平均风速 51 节、风速的单位是节
- 正确：平均风速 51 kt、风速的单位是 kt

公式里的单位写在 `\mathrm{}` 里，例如 $g_0 = 9.80665\ \mathrm{m\,s^{-2}}$。

### 3.3 代码字体

变量名、函数名、参数名、文件名和路径用行内代码字体。数据集名和软件包名用普通字体。物理量用公式符号。

- 错误：ERA5 的 t2m 变量用 metpy.calc.potential_temperature 计算位温 theta。
- 正确：ERA5 的 `t2m` 是 2 m 温度。函数 `metpy.calc.potential_temperature` 计算位温 $\theta$。
- 错误：用 `xarray` 打开 `ERA5`。
- 正确：用 xarray 打开 ERA5。

### 3.4 图题

每张图有一个 `label` 和一个图题。`label` 的格式是 `fig-<页面短名>-<内容>`，例如 `fig-ch03-z500`。正文用 `[](#fig-ch03-z500)` 引用图。

图题的第一句说明时间、区域、等压面和变量。第二句写数据来源。时间写作 `YYYY-MM-DD HH UTC`。

- 错误：图 1：位势高度。
- 正确：2023-01-15 00 UTC，北大西洋 500 hPa 的位势高度。数据来源：ERA5。

代码生成的图，在代码单元的开头写 `label` 和 `caption`：

````md
```{code-cell} python
#| label: fig-ch03-z500
#| caption: 2023-01-15 00 UTC，北大西洋 500 hPa 的位势高度。数据来源：ERA5。
ax = z500.plot()
```
````

静态图片用 `figure` 指令：

```md
:::{figure} images/ch03-profile.png
:label: fig-ch03-profile
:alt: Geopotential height profile over London

2023-01-15 00 UTC，伦敦上空的位势高度廓线。数据来源：ERA5。
:::
```

### 3.5 引用 METEO 300

METEO 300 是宾夕法尼亚州立大学的公开课程，作者是 William H. Brune。课程以 CC BY-NC-SA 4.0 许可发布。本书改编它的内容，所以本书的正文也以 CC BY-NC-SA 4.0 发布。

1. 每页“知识点”一节的第一句写出处，格式是：本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 N 课 N.M 节。
2. 用自己的话写知识点。不整段翻译课程原文。
3. 只重用图片来源写有 “© Penn State” 和 “CC BY-NC-SA 4.0” 的 METEO 300 图。来源是其他机构或其他作者的图不用。
4. 重用的图，图题末尾写：图片来源：W. Brune，METEO 300，Penn State，CC BY-NC-SA 4.0。
5. 只用公开许可的材料。不用付费课程或许可不明的文字、图和习题。

- 错误：本页内容参考了网上的课程。
- 正确：本页取自 METEO 300 第 2 课 2.2 节。

### 3.6 引用数据集

每页“数据集”一节写出数据集名、提供方、访问方式和许可。完整的数据集条目在数据集参考页 `docs/reference/datasets.md`。页面链接到那里，不重复全部条目。

第一次引用一个数据集时，写出它的论文或 DOI。

- 错误：数据来自网上。
- 正确：本页用 ERA5 再分析。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 Copernicus 产品许可发布。

### 3.7 标点和空格

1. 中文句子用全角标点：，。：；？！和“ ”。
2. 中文和英文单词、数字之间空一格，例如“ERA5 的 37 个等压面”。
3. 完整句子的列表项以句号结尾。
4. 标题不加句号。

- 错误：ERA5有37个等压面.
- 正确：ERA5 有 37 个等压面。

### 3.8 术语

1. 只用术语表的中文术语。新概念先加入术语表，再写进页面。
2. 每页“知识点”一节的末尾有一张术语表格，列出本页术语的中文、英文和符号。正文不在括号里写英文。
3. 一个公式符号只表示一个量。符号以术语表为准。

## 4 检查器

运行检查器：

```bash
uv run python tools/ste_check.py                 # 检查 intro.md、README.md 和 docs/
uv run python tools/ste_check.py docs/topics/ch03-pressure-hydrostatic.md
```

每条违规输出一行，格式是 `file:line: rule: text`。有违规时，退出码是 1。

| 规则 | 检查内容 |
|---|---|
| `zh-sentence-length` | 中文句子超过 40 字 |
| `en-sentence-length` | 英文句子超过 25 个单词 |
| `paragraph-length` | 段落超过 6 句 |
| `passive-voice` | 被、给出了、得到了，英文的 be + 过去分词 |
| `parentheses` | 正文里的括号 |
| `interval-format` | 区间不是 ［下限, 上限］ |
| `unit-space` | 数字和单位之间没有空格，或使用 ℃ |
| `unit-symbol` | 整数后面的“节”、“单位是节”和“以节为单位”，风速单位应写 kt |
| `rejected-term` | 术语表的弃用词 |

检查器跳过这些内容：frontmatter、代码单元、代码块、公式、行内代码、行内公式、角色、网址、注释和指令的选项行。

页面必须展示错误写法时，例如在练习里，用忽略标记：

```md
% ste-ignore
这一段不检查，直到下一个空行。

% ste-ignore-start
这里的多个段落都不检查。
% ste-ignore-end
```

GitHub 直接显示的文件，例如 README.md，用 `<!-- ste-ignore -->`、`<!-- ste-ignore-start -->` 和 `<!-- ste-ignore-end -->`。

检查器的设置在 `pyproject.toml` 的 `[tool.ste_check]` 一节。检查器的测试在 `tests/test_ste_check.py`，运行 `uv run pytest`。
