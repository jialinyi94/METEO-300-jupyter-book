---
title: 页面标题
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

% 页面模板。主题页的文件已经在 docs/topics/ 里，按本模板填写。
% 每页回答四个问题：
%   1. 真实数据长什么样？
%   2. 最常用的数据集是哪一个？
%   3. 哪些软件包处理和计算这些数据？
%   4. 这些数据和 AI 天气模型有什么联系？
% 六节的顺序固定：知识点、真实数据、数据集、计算、AI 天气连接、练习。不加其他二级标题。
% 正文遵守 STYLE.md，术语只用 glossary.md 的中文术语。
% 提交前运行：uv run python tools/ste_check.py docs/topics/<文件名>.md
% 只用 METEO 300 和公开许可的数据。不用付费课程或许可不明的文字、图和习题。
% 图、表、式和练习的 label 以页面短名开头，例如 fig-ch03-z500、ex-ch03-1。
% 读取数据用 src/meteo300/data.py 的函数。CI 没有网络，函数读取 data/samples/ 的样本。
% 用法见 docs/reference/data-access-demo.md。
% 导入规则：第一个代码单元先导入 meteo300，再导入其他非标准库的软件包。
% meteo300 在 eccodes 之前加载 pyproj。顺序反了，内核可能在退出时崩溃。tests/test_page_cells.py 检查这条规则。
% 以 % 开头的行是注释，网站不显示。填写完成后，删去本模板的注释。

## 知识点

% 第一句写 METEO 300 的出处。然后用自己的话写本页的物理知识。
% 先写结论，再写公式。每个公式后写一句话，说明它的含义。

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 2 课 2.5 节。

位温是气块干绝热地移到 1000 hPa 时的温度。

$$
\theta = T \left( \frac{p_0}{p} \right)^{R_d / c_p}
$$

在干绝热过程中，气块的位温不变。

% 本节的最后一部分是本页术语表格。列出本页用到的术语。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 位温 | potential temperature | $\theta$ |
| 干绝热直减率 | dry adiabatic lapse rate | $\Gamma_d$ |

## 真实数据

% 先让读者看真实数据：一张图或一个表。
% 图题写时间、区域、等压面和变量，再写数据来源。
% 图下面用两三句话说明读者应该看到什么。

## 数据集

% 写出最常用的数据集：名字、提供方、分辨率、时间范围、访问方式和许可。
% 完整条目在数据集参考页。这里只链接过去，不重复全部条目。

% 链接路径相对于 docs/topics/。

本页用 ERA5 再分析。数据集的完整说明见 [数据集参考页](../reference/datasets.md)。

## 计算

% 用软件包算出至少一个值，再用手算核对它。用 assert 核对，核对失败时构建失败。
% 手算用公式和常数，常数写出来源。

MetPy 计算 850 hPa、288.15 K 的气块的位温。手算用 $R_d / c_p = 0.2857$。

```{code-cell} python
import meteo300

import metpy.calc as mpcalc
from metpy.units import units

theta = mpcalc.potential_temperature(850 * units.hPa, 288.15 * units.K)

# 手算：theta = T * (p0 / p) ** (Rd / cp)
theta_hand = 288.15 * (1000 / 850) ** 0.2857
assert abs(theta.m_as("K") - theta_hand) < 0.05, (theta, theta_hand)
print(f"MetPy: {theta.m_as('K'):.2f} K, 手算: {theta_hand:.2f} K")
```

两个结果都是 301.85 K。

## AI 天气连接

% 回答这些问题：
%   这个量在 AI 天气模型里是哪个变量？它是输入、输出还是诊断量？
%   模型在哪些等压面上预报它？
%   评估这个量用哪个指标？WeatherBench 2 怎样报告它？
%   这个量在 AI 天气模型里有哪些常见问题？

GraphCast 不直接输出位温。位温可以从模型输出的温度和气压算出。

## 练习

% 两到四道练习。每道练习用真实数据或本页的代码。答案放在可以折叠的 solution 里。

:::{exercise}
:label: ex-template-1

计算 500 hPa、250 K 的气块的位温。
:::

:::{solution} ex-template-1
:class: dropdown

位温约为 304.7 K。
:::
