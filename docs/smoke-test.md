---
title: 构建自检
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

本页检查 CI 能否执行 notebook。

```{code-cell} python
import metpy.calc as mpcalc
from metpy.units import units

theta = mpcalc.potential_temperature(850 * units.hPa, 288.15 * units.K)
print(f"theta = {theta.to('K').m:.2f} K")
```
