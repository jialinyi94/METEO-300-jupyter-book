---
title: hydrostatic balance
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

# hydrostatic balance

## 知识点

本页取自 METEO 300 第 2 课 2.2 节。
pressure 随 geometric height 增加而减小。
hydrostatic equation 把 pressure 的垂直变化和 density 联系起来。

$$
\frac{\partial p}{\partial z} = -\rho g_0
$$

scale height $H = R_d T / g_0$ 约为 8 km。
temperature 为 250 K 时，scale height 约为 7.3 km。

## 真实 data

ERA5 在 37 个 isobaric surface 上给出 temperature 和 geopotential。
我们读取 2023-01-15 00:00 UTC 的 data。
本页用到的 isobaric surface 在 ［500, 1000］ hPa 之内。
三个 isobaric surface 是 1000 hPa、850 hPa 和 500 hPa，geopotential height 分别是 111 m、1457 m 和 5574 m。

:::{figure} ../images/example.png
:label: fig-example
:alt: 位势高度廓线

2023-01-15 00 UTC，伦敦上空的 geopotential height 廓线。data 来源：ERA5。
:::

| 中文术语 | 单位 |
|---|---|
| geopotential height | m |
| 2 m temperature | K |

```{code-cell} python
# 代码里的括号、被动句和“气温”都不检查。
import metpy.calc as mpcalc
from metpy.units import units

thickness = mpcalc.thickness_hydrostatic(
    [1000, 500] * units.hPa, [280, 250] * units.K
)
print(thickness.to("m"))  # (被检查器跳过)
```

变量 `t2m` 是 2 m temperature，单位 K。
函数 {func}`metpy.calc.potential_temperature` 计算 potential temperature。
更多内容见 [METEO 300](https://www.e-education.psu.edu/meteo300/) 和 [](#fig-example)。

% 这一行是 MyST 注释（不检查），里面的气温也不检查。

<!-- HTML 注释（不检查）：气温 -->

% ste-ignore
错误写法：“500 hPa 高度”和“气温”。

## English summary

The book uses ERA5 data on pressure levels.
The model computes the thickness of each layer.
