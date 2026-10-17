---
title: 静力平衡
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

# 静力平衡

## 知识点

本页取自 METEO 300 第 2 课 2.2 节。
气压随几何高度增加而减小。
静力方程把气压的垂直变化和密度联系起来。

$$
\frac{\partial p}{\partial z} = -\rho g_0
$$

标高 $H = R_d T / g_0$ 约为 8 km。
温度为 250 K 时，标高约为 7.3 km。

## 真实数据

ERA5 在 37 个等压面上给出温度和位势。
我们读取 2023-01-15 00:00 UTC 的数据。
本页用到的等压面在 ［500, 1000］ hPa 之内。
三个等压面是 1000 hPa、850 hPa 和 500 hPa，位势高度分别是 111 m、1457 m 和 5574 m。

:::{figure} ../images/example.png
:label: fig-example
:alt: 位势高度廓线

2023-01-15 00 UTC，伦敦上空的位势高度廓线。数据来源：ERA5。
:::

| 中文术语 | 单位 |
|---|---|
| 位势高度 | m |
| 2 m 温度 | K |

```{code-cell} python
# 代码里的括号、被动句和“气温”都不检查。
import metpy.calc as mpcalc
from metpy.units import units

thickness = mpcalc.thickness_hydrostatic(
    [1000, 500] * units.hPa, [280, 250] * units.K
)
print(thickness.to("m"))  # (被检查器跳过)
```

变量 `t2m` 是 2 m 温度，单位 K。
函数 {func}`metpy.calc.potential_temperature` 计算位温。
更多内容见 [METEO 300](https://www.e-education.psu.edu/meteo300/) 和 [](#fig-example)。

% 这一行是 MyST 注释（不检查），里面的气温也不检查。

<!-- HTML 注释（不检查）：气温 -->

% ste-ignore
错误写法：“500 hPa 高度”和“气温”。

## English summary

The book uses ERA5 data on pressure levels.
The model computes the thickness of each layer.
