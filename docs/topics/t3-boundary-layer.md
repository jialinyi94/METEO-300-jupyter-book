---
title: atmospheric boundary layer
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

## 知识点

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 11 课 11.1 节到 11.3 节、11.5 节、11.6 节、11.8 节、11.9 节、11.11 节和第 10 课 10.10 节。

atmospheric boundary layer 是 troposphere 最低的一层。surface 的加热、冷却和 friction 在 1 h 以内影响整层。白天的 atmospheric boundary layer 约 1 km 厚，晴朗的夜间常常只有约 100 m 厚。[](#fig-ch04-sounding) 用两次 sounding 看了 atmospheric boundary layer 的 potential temperature 廓线。[力与 geostrophic wind](ch05-dynamics-geostrophic.md) 一页看了 friction 怎样让 10 m wind 斜穿 isobar。本页用一座 213 m 的观测塔看 atmospheric boundary layer 的 diurnal cycle，再用 sonic anemometer 看 turbulence 本身。

### atmospheric boundary layer 的 diurnal cycle

白天，太阳加热 surface。surface 用 sensible heat flux 加热贴地的空气，热空气上升，形成 convection。convection 把 atmospheric boundary layer 搅匀，这一层叫 mixed layer。mixed layer 里的 potential temperature 和 wind speed 几乎不随 geometric height 变化。mixed layer 顶上是一个稳定层。上升的热空气冲进稳定层，把上面的空气卷进 mixed layer，这个过程叫 entrainment。

日落以后，surface 用 longwave radiation 冷却。贴地的空气跟着变冷，形成 temperature inversion，这一层叫 stable boundary layer。稳定层削弱 turbulence。stable boundary layer 上面留下前一天的 mixed layer 空气，这一层叫 residual layer。日出以后，mixed layer 从 surface 向上增长，先吞掉 stable boundary layer，再吞掉 residual layer。

### low-level jet

白天，turbulence 把上层的动量送到 surface，所以整个 mixed layer 的 wind 都比 geostrophic wind 慢。日落以后，stable boundary layer 把 residual layer 和 surface 隔开。residual layer 的空气突然不再受 friction，pressure gradient force 和 Coriolis force 不再和 wind 平衡。wind 绕着 geostrophic wind 做 inertial oscillation，周期是 inertial period $2\pi/f$。[](#fig-ch01-inertial) 画了只受 Coriolis force 的 inertial oscillation。

在 52°N，$f = 1.15 \times 10^{-4}\ \mathrm{s^{-1}}$，inertial period 约 15.2 h。日落时 wind 比 geostrophic wind 慢。约半个 inertial period 以后，wind 比 geostrophic wind 快。这个时刻约在日落后 7.6 h，也就是后半夜。这时离地几百米处出现一个 wind speed 的极大值，叫 low-level jet。荷兰的 Cabauw 观测塔经常测到 low-level jet。

### Reynolds averaging

turbulence 的 wind 变化得很快。sonic anemometer 每秒测 20 次 wind。把每个量写成平均值和 turbulent fluctuation 的和：

```{math}
:label: eq-t3-reynolds
u = \overline{u} + u', \qquad \overline{u'} = 0
```

$\overline{u}$ 是一段时间的平均值，本页取 30 min。$u'$ 是 turbulent fluctuation，它的平均值按定义等于零。两个量的乘积的平均值是：

```{math}
:label: eq-t3-product
\overline{u\,w} = \overline{u}\,\overline{w} + \overline{u'w'}
```

$\overline{u'w'}$ 是 $u$ 和 $w$ 的 covariance。两个 turbulent fluctuation 各自的平均值是零，它们的乘积的平均值一般不是零。这一项就是 turbulent flux。Reynolds averaging 把运动方程分成平均 wind 的方程和 turbulence 的方程，turbulence 只通过这些 covariance 影响平均 wind。

### turbulent flux

$w$ 是 vertical velocity。$\overline{w'\theta'}$ 是热量的 kinematic flux，单位是 K m s⁻¹。乘以空气的 density 和 specific heat capacity at constant pressure，就得到 sensible heat flux：

```{math}
:label: eq-t3-qh
Q_H = \rho\, c_p\, \overline{w'\theta'}
```

白天，贴地的 potential temperature 随 geometric height 降低。上升的空气比周围暖，$w' > 0$ 时 $\theta' > 0$。下沉的空气比周围冷，$w' < 0$ 时 $\theta' < 0$。两种情况的乘积都为正，所以 $\overline{w'\theta'} > 0$，热量向上输送。夜间，potential temperature 随 geometric height 升高，符号全部相反，热量向下输送。

$\overline{u'w'}$ 是 momentum flux，单位是 m² s⁻²。wind speed 随 geometric height 增大，下沉的空气带来较快的 wind，所以 $\overline{u'w'} < 0$，动量向下输送。surface 吸收这些动量，这就是 atmospheric boundary layer 的 friction。friction velocity 把 momentum flux 写成一个速度：

```{math}
:label: eq-t3-ustar
u_* = \left(\overline{u'w'}^{\,2} + \overline{v'w'}^{\,2}\right)^{1/4}
```

turbulent kinetic energy 是三个 wind speed 分量的 variance 之和的一半，$\tfrac{1}{2}\left(\overline{u'^2} + \overline{v'^2} + \overline{w'^2}\right)$。convection 和 vertical wind shear 产生 turbulent kinetic energy。大的涡旋把能量传给小的涡旋，最小的涡旋把能量变成热。

### power-law wind profile

surface 的 friction 让 wind speed 随 geometric height 增大。增大得多快取决于 static stability。风电行业常用 power-law wind profile 描述这个关系：

```{math}
:label: eq-t3-power
V(z) = V(z_r)\left(\frac{z}{z_r}\right)^{n}
```

$z_r$ 是参考 geometric height，常取 10 m。$n$ 是 power-law exponent。在 neutral stratification 的平坦陆面上，$n$ 约为 1/7。白天的 mixed layer 把动量搅匀，wind speed 随 geometric height 变化小，$n$ 小。夜间的稳定层削弱 turbulence，上层的 wind 和 surface 脱节，$n$ 大。所以同一个 10 m wind speed，在夜间对应更大的 100 m wind speed。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| atmospheric boundary layer | 边界层 | ABL |
| boundary layer height | 边界层高度 | $z_i$ |
| mixed layer | 混合层 | — |
| stable boundary layer | 稳定边界层 | SBL |
| residual layer | 残留层 | — |
| entrainment | 夹卷 | — |
| diurnal cycle | 日变化 | — |
| low-level jet | 低空急流 | — |
| inertial oscillation | 惯性振荡 | — |
| inertial period | 惯性周期 | — |
| turbulence | 湍流 | — |
| Reynolds averaging | Reynolds 平均 | — |
| turbulent fluctuation | 脉动量 | $u'$ |
| variance | 方差 | $\overline{u'^2}$ |
| covariance | 协方差 | $\overline{a'b'}$ |
| turbulent flux | 湍流通量 | — |
| kinematic flux | 运动学通量 | — |
| sensible heat flux | 感热通量 | $Q_H$ |
| momentum flux | 动量通量 | $\overline{u'w'}$ |
| friction velocity | 摩擦速度 | $u_*$ |
| turbulent kinetic energy | 湍流动能 | TKE |
| eddy covariance | 涡动协方差 | — |
| sonic anemometer | 超声风速仪 | — |
| sonic temperature | 超声温度 | $T_s$ |
| power-law wind profile | 幂律风廓线 | — |
| power-law exponent | 幂律指数 | $n$ |
| 100 m wind | 100 m 风 | $u_{100}$, $v_{100}$ |
| hub height | 轮毂高度 | $z_{\mathrm{hub}}$ |
| wind power output | 风电出力 | $P_{\mathrm{W}}$ |
| power curve | 功率曲线 | — |
| capacity factor | 容量系数 | — |
| cut-in wind speed | 切入风速 | $V_{\mathrm{in}}$ |
| rated wind speed | 额定风速 | $V_{\mathrm{rated}}$ |
| cut-out wind speed | 切出风速 | $V_{\mathrm{out}}$ |
| rated power | 额定功率 | — |
| installed capacity | 装机容量 | — |
| Richardson number | Richardson 数 | Ri |

## 真实 data

本页的个例是 2026-04-21 00 UTC 到 2026-04-23 00 UTC。这几天一个 high 停在北海上空，荷兰吹东北风。两个白天都几乎没有云，中间的夜晚也没有云。所以 48 h 里先有一个 mixed layer，再有一个 stable boundary layer 和 low-level jet，然后又是一个 mixed layer。

### Cabauw 观测塔的 48 h

KNMI 的 Cabauw 观测塔在荷兰中部的平坦草地上，高 213 m。塔上的仪器在 10、20、40、80、140 和 200 m 测 wind，在这些 geometric height 和 2 m 测 temperature。每个值是 10 min 的平均。potential temperature 用 earthkit-meteo 从 temperature 和气压计算，各层的 pressure 从 surface pressure 用 hypsometric equation 推算。计算一节核对这个 potential temperature。

```{code-cell} python
from meteo300 import data as d
from meteo300.pages import t3

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
import xarray as xr
from earthkit.meteo import thermo, wind
from earthkit.transforms import climatology
from metpy.units import units

G0, RD = 9.80665, 287.05  # m s⁻²，J kg⁻¹ K⁻¹
tower = d.page_data(t3.SAMPLE_FILES["tower"], t3.cabauw_tower)
surface = d.page_data(t3.SAMPLE_FILES["surface"], t3.cabauw_surface)
era = d.page_data(t3.SAMPLE_FILES["era5_case"], t3.era5_case)

speed = tower["F"].to_pandas()  # wind speed，m s⁻¹；列是 geometric height
temp = tower["TA"].to_pandas()  # temperature，K
z = temp.columns.to_numpy()
# hypsometric equation：从 surface pressure 向上推各层的 pressure，layer-mean temperature 取 2 m 和本层的平均
p_sfc = surface["P0"].reindex(temp.index).to_numpy()[:, None] * 100  # Pa
t_layer = (temp.to_numpy() + temp[2.0].to_numpy()[:, None]) / 2
pres = p_sfc * np.exp(-G0 * z / (RD * t_layer))
theta = pd.DataFrame(thermo.potential_temperature(temp.to_numpy(), pres), temp.index, z)

case = slice(*t3.CASE)
hourly_speed = speed.resample("1h").mean()
hourly_theta = theta.resample("1h").mean()
for label, hour in [("白天", "2026-04-21T13"), ("夜间", "2026-04-22T04")]:
    v, th = hourly_speed.loc[hour], hourly_theta.loc[hour]
    print(f"{hour} UTC {label}：10 m wind speed {v[10.0]:.1f}，200 m wind speed {v[200.0]:.1f} m s⁻¹；"
          f"200 m 和 2 m 的 potential temperature 差 {th[200.0] - th[2.0]:+.1f} K")
jet = speed.loc["2026-04-21T18":"2026-04-22T07", 200.0]
print(f"夜间 200 m wind speed 最大 {jet.max():.1f} m s⁻¹，时间 {jet.idxmax():%H:%M} UTC")
blh = era["blh"].loc[case]
print(f"ERA5 boundary layer height：［{blh.min():.0f}, {blh.max():.0f}］ m")
print(f"Cabauw sensible heat flux：［{surface['H'].loc[case].min():.0f}, {surface['H'].loc[case].max():.0f}］ W m⁻²")
```

```{code-cell} python
#| label: fig-t3-tower
#| caption: 2026-04-21 00 UTC 到 2026-04-23 00 UTC，Cabauw 观测塔的 10 min 平均值。从上到下：各 geometric height 的 wind speed；各 geometric height 的 potential temperature；surface 的 sensible heat flux，向上为正；ERA5 的 boundary layer height，虚线是塔顶的 200 m。灰色是太阳在地平线以下的时段。data 来源：KNMI Cabauw、ERA5。
spans = t3.night_spans(speed.loc[case].index)
fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)
colors = plt.cm.viridis(np.linspace(0, 0.9, 6))
for c, h in zip(colors, [10.0, 20.0, 40.0, 80.0, 140.0, 200.0], strict=True):
    axs[0].plot(speed.loc[case].index, speed.loc[case, h], color=c, lw=1, label=f"{h:.0f} m")
for c, h in zip(colors, [2.0, 10.0, 40.0, 80.0, 140.0, 200.0], strict=True):
    axs[1].plot(theta.loc[case].index, theta.loc[case, h] - 273.15, color=c, lw=1, label=f"{h:.0f} m")
axs[2].plot(surface.loc[case].index, surface.loc[case, "H"], color="tab:red", lw=1)
axs[2].axhline(0, color="k", lw=0.5)
axs[3].plot(blh.index, blh, "o-", color="tab:blue", ms=3)
axs[3].axhline(200, color="k", ls="--", lw=0.8)
axs[0].set(ylabel="wind speed (m s$^{-1}$)")
axs[1].set(ylabel="potential temperature (°C)")
axs[2].set(ylabel="sensible heat flux (W m$^{-2}$)")
axs[3].set(ylabel="ERA5 boundary layer height (m)", xlabel="time (UTC)")
axs[0].legend(ncols=6, fontsize=8, loc="upper left")
axs[1].legend(ncols=6, fontsize=8, loc="upper left")
for ax in axs:
    for start, end in spans:
        ax.axvspan(start, end, color="0.85", lw=0)
    ax.grid(alpha=0.3)
axs[3].xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18]))
axs[3].xaxis.set_major_formatter(mdates.DateFormatter("%d %H"))
fig.tight_layout()
```

读 [](#fig-t3-tower) 时看四点：

1. 白天，各层的 wind speed 挤在一起。2026-04-21 13 UTC，10 m 的 wind speed 是 4.3 m s⁻¹，200 m 的 wind speed 是 5.9 m s⁻¹。mixed layer 把动量搅匀了。
2. 白天，各层的 potential temperature 也挤在一起。2 m 的 potential temperature 比 200 m 高约 0.9 K，贴地的一层不稳定。夜间，各层的 potential temperature 分开，2 m 最冷。2026-04-22 04 UTC，200 m 的 potential temperature 比 2 m 高 7.5 K，这是 stable boundary layer。
3. 2026-04-21 18 UTC，200 m 的 wind speed 约 7 m s⁻¹。夜间，它增大到 12.5 m s⁻¹，10 m 的 wind speed 却减小到约 3 m s⁻¹。这是 low-level jet。04 UTC 以后，140 m 的 wind 比 200 m 快，jet stream 核降到塔里。日出以后，mixed layer 把 jet stream 的动量带到 surface，上层的 wind 很快减弱。
4. sensible heat flux 在白天向上，最大约 157 W m⁻²。它在日落前约 2 h 变成向下，夜间约为 −20 W m⁻²。ERA5 的 boundary layer height 在白天超过 1200 m，在夜间降到约 170 m，低于塔顶。

### 20 Hz 的 turbulence

Cabauw 只公开 10 min 的平均值。本页的 20 Hz data 来自德国 Hartheim 的森林 weather station DE-Har。sonic anemometer 装在 27 m 高的塔上，森林高约 18 m。下面是 2024-07-01 的两个 30 min 时段。12 UTC 是晴朗的中午，21 UTC 是日落后的夜间。

```{code-cell} python
day = t3.turbulence_frame(d.turbulence_20hz(t3.TURBULENCE_DAY))
night = t3.turbulence_frame(d.page_data(t3.SAMPLE_FILES["night"], t3.turbulence_night))
blocks = {"12 UTC": day, "21 UTC": night}
for name, blk in blocks.items():
    print(f"{name}：{len(blk)} 个值，w 的范围 ［{blk['w'].min():.2f}, {blk['w'].max():.2f}］ m s⁻¹，"
          f"sonic temperature 的范围 ［{blk['t_sonic'].min():.1f}, {blk['t_sonic'].max():.1f}］ °C")
```

```{code-cell} python
#| label: fig-t3-hf
#| caption: 2024-07-01，DE-Har 森林 weather station 27 m 处的 20 Hz 观测。上：vertical velocity。下：sonic temperature 减去 30 min 的平均值。左列从 12:00 UTC 开始，右列从 21:00 UTC 开始，每列 30 min。虚线是 30 min 的平均值。data 来源：DE-Har，Zenodo。
fig, axs = plt.subplots(2, 2, figsize=(11, 5.5), sharex="col", sharey="row")
for j, (name, blk) in enumerate(blocks.items()):
    minutes = (blk.index - blk.index[0]).total_seconds() / 60
    axs[0, j].plot(minutes, blk["w"], color="tab:blue", lw=0.2)
    axs[0, j].axhline(blk["w"].mean(), color="k", ls="--", lw=0.8)
    axs[1, j].plot(minutes, blk["t_sonic"] - blk["t_sonic"].mean(), color="tab:red", lw=0.2)
    axs[1, j].axhline(0, color="k", ls="--", lw=0.8)
    axs[0, j].set_title(f"start {name}")
    axs[1, j].set_xlabel("minutes")
axs[0, 0].set_ylabel("vertical velocity (m s$^{-1}$)")
axs[1, 0].set_ylabel("sonic temperature minus mean (K)")
for ax in axs.flat:
    ax.grid(alpha=0.3)
fig.tight_layout()
```

读 [](#fig-t3-hf) 时看三点：

1. 中午的 vertical velocity 在 ［−4.0, 4.1］ m s⁻¹ 之间跳动。夜间的幅度只有中午的约三分之一。
2. 中午的 sonic temperature 有很多尖峰，向上偏。暖的空 air mass 从森林里升起，经过 wind speed 仪。
3. 两个时段都有几分钟长的起伏，也有不到一秒的抖动。turbulence 同时包含很多尺度的涡旋。

## dataset

KNMI 的 Cabauw 观测塔是欧洲最常用的 atmospheric boundary layer 观测。本页用 `d.cabauw` 读取三个 dataset：`tower_meteo` 是塔上的 wind 和 temperature，`surface_flux` 是 surface 的 turbulent flux，`surface_meteo` 是 surface pressure。三个 dataset 都是 10 min 平均，经过验证并填补了缺测。它们以 CC BY 4.0 许可发布。

ERA5 是 ECMWF 制作的 reanalysis dataset，发布的 grid spacing 是 0.25°。本页从 ARCO-ERA5 读取离 Cabauw 最近的 grid point，52.0°N、5.0°E。变量是 boundary layer height `blh`、瞬时 sensible heat flux `ishf`、100 m wind `u100` 和 `v100`、10 m wind 和 2 m temperature。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

ERA5 用整体 Richardson number 诊断 boundary layer height `blh`。从 surface 向上，整体 Richardson number 第一次达到临界值 0.25 的地方就是 atmospheric boundary layer 顶。这个诊断方法见 IFS CY41R2 文档 [第 IV 部分](https://www.ecmwf.int/en/elibrary/16648-part-iv-physical-processes) 第 3.10.1 节。它沿用 Seidel 等，2012，[doi:10.1029/2012JD018143](https://doi.org/10.1029/2012JD018143)。

20 Hz 的 data 来自 DE-Har weather station 的 eddy covariance 原始 data。Zenodo 以 CC BY 4.0 许可公开 2023 年和 2024 年的 data。`d.turbulence_20hz` 读取它，每个 30 min 时段还附带 weather station 用 EddyPro 算出的通量。

AI 天气连接一节用 ECMWF 开放 data 里的 AIFS Single 和 IFS forecast，CC BY 4.0 许可。AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。

模块 `meteo300.pages.t3` 里的函数记录了样本的制作方法。在线时，`d.page_data` 运行这些函数。离线时，它读取样本。样本的来源和许可见 `data/samples/ATTRIBUTION-t3.md`。

下面是两个备选 dataset。ICOS 的通量 weather station 网有欧洲约 100 个 eddy covariance weather station。它的原始高频 data 要申请账户。很多 weather station 的 sounding 和激光雷达也能估计 boundary layer height，例如 IGRA2 的 sounding。完整的 dataset 条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

本节先在 20 Hz data 上做 Reynolds averaging，算出 momentum flux 和 sensible heat flux，再和 EddyPro 的结果核对。然后用 Cabauw 的塔拟合 power-law exponent，并说明怎样从塔上的观测得到 100 m wind。

### Reynolds averaging

sonic anemometer 的坐标轴不一定沿着 wind。先旋转坐标轴，使 $x$ 轴沿着 30 min 的平均 wind，使平均的 vertical velocity 为零。`t3.double_rotation` 做这两次旋转。然后按 [](#eq-t3-reynolds) 把每个量分成平均值和 turbulent fluctuation，再检查 [](#eq-t3-product)。

```{code-cell} python
u, v, w = t3.double_rotation(day["u"], day["v"], day["w"])
up, vp, wp = u - u.mean(), v - v.mean(), w - w.mean()
print(f"平均 wind speed {u.mean():.2f} m s⁻¹，平均 v {v.mean():.1e}，平均 w {w.mean():.1e} m s⁻¹")
print(f"turbulent fluctuation 的平均值：u' {up.mean():.1e}，w' {wp.mean():.1e} m s⁻¹")

uw_mean = np.mean(u * w)
uw_cov = np.mean(up * wp)  # 手算的 covariance
print(f"mean(u w) = {uw_mean:.4f}，mean(u) mean(w) = {u.mean() * w.mean():.1e}，"
      f"mean(u' w') = {uw_cov:.4f} m² s⁻²")
assert np.isclose(uw_mean, u.mean() * w.mean() + uw_cov)
assert np.isclose(uw_cov, np.cov(u, w, bias=True)[0, 1])  # numpy 的 covariance
```

旋转以后，平均的 $v$ 和 $w$ 都是零。turbulent fluctuation 的平均值也是零，只差计算机的舍入误差。$\overline{u\,w}$ 几乎全部来自 covariance $\overline{u'w'}$，因为 $\overline{w} = 0$。手算的 covariance 和 numpy 的 `np.cov` 相同。

### momentum flux 和 sensible heat flux

sonic temperature $T_s$ 接近 virtual temperature，它比 temperature 高约 $0.51\,q\,T$。所以 $\overline{w'T_s'}$ 包含 water vapour 的贡献。下面先用气体分析仪的 water vapour density 算出 $\overline{w'q'}$，再从 $\overline{w'T_s'}$ 减去 water vapour 的部分。在 27 m 处，potential temperature 的 turbulent fluctuation 和 temperature 的 turbulent fluctuation 几乎相同。density 用 MetPy 从 pressure 和温度计算，单位用 pint 检查。

```{code-cell} python
CP = 1005 * units("J kg^-1 K^-1")  # dry air 的 specific heat capacity at constant pressure
M_H2O = 18.015e-6  # kg mmol⁻¹


def fluxes(blk):
    """一个 30 min 时段的 momentum flux、friction velocity 和 sensible heat flux。"""
    u, v, w = t3.double_rotation(blk["u"], blk["v"], blk["w"])
    wp = w - w.mean()
    ts = blk["t_sonic"].to_numpy() + 273.15
    p = blk.attrs["pa_kpa"] * units.kPa
    t_air = (blk.attrs["eddypro_TA_EP"] * units.degC).to("K")
    rho = mpcalc.density(p, t_air, 0 * units("g/kg"))
    rho_v = blk["h2o"].to_numpy() * M_H2O  # water vapour density，kg m⁻³
    wq = np.mean(wp * (rho_v - rho_v.mean())) / rho.m_as("kg/m^3")  # w'q'
    wts = np.mean(wp * (ts - ts.mean()))  # w'Ts'
    wt = wts - 0.51 * ts.mean() * wq  # w'T'：去掉 water vapour 的贡献
    uw, vw = np.mean((u - u.mean()) * wp), np.mean((v - v.mean()) * wp)
    q_h = (rho * CP * wt * units("K m/s")).to("W/m^2")
    return {
        "u'w' (m2 s-2)": uw,
        "u* (m s-1)": (uw**2 + vw**2) ** 0.25,
        "w'Ts' (K m s-1)": wts,
        "w'T' (K m s-1)": wt,
        "Q_H (W m-2)": q_h.m,
        "EddyPro u*": blk.attrs["eddypro_USTAR"],
        "EddyPro Q_H": blk.attrs["eddypro_H"],
    }


table = pd.DataFrame({name: fluxes(blk) for name, blk in blocks.items()})
print(table.round(4).to_string())
for name in blocks:
    assert np.isclose(table.loc["u* (m s-1)", name], table.loc["EddyPro u*", name], rtol=0.03)
    assert np.isclose(table.loc["Q_H (W m-2)", name], table.loc["EddyPro Q_H", name], rtol=0.03)
```

两个时段的 friction velocity 和 sensible heat flux 都和 EddyPro 相差不到 3%。EddyPro 是 weather station 用的软件，它还做了谱修正等几项修正。

中午的 sensible heat flux 约为 242 W m⁻²，热量向上。夜间约为 −32 W m⁻²，热量向下。中午的 friction velocity 约是夜间的 3 倍。去掉 water vapour 的贡献以后，中午的 $\overline{w'T'}$ 比 $\overline{w'T_s'}$ 小约 7%。森林在中午 evaporation 大量的水，所以这一项不能省略。

下面的图把每个 20 Hz 的值画成一个点，横轴是 $w'$，纵轴是 $T_s'$。

```{code-cell} python
#| label: fig-t3-quadrant
#| caption: 2024-07-01，DE-Har 27 m 处 vertical velocity 的 turbulent fluctuation 和 sonic temperature 的 turbulent fluctuation。每个时段 36 000 个 20 Hz 的值，颜色越深，点越密。左：12:00 UTC 起的 30 min。右：21:00 UTC 起的 30 min。data 来源：DE-Har，Zenodo。
fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
for ax, (name, blk) in zip(axs, blocks.items(), strict=True):
    _, _, w_rot = t3.double_rotation(blk["u"], blk["v"], blk["w"])
    w_p = w_rot - w_rot.mean()
    t_p = blk["t_sonic"].to_numpy() - blk["t_sonic"].mean()
    ax.hexbin(w_p, t_p, gridsize=60, bins="log", cmap="Greys", extent=(-3, 3, -2, 2))
    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(0, color="k", lw=0.5)
    share = np.mean(w_p * t_p > 0)
    ax.set_title(f"start {name}: w'Ts' = {np.mean(w_p * t_p):+.3f} K m s$^{{-1}}$, "
                 f"w'Ts' > 0 for {share:.0%} of points", fontsize=9)
    ax.set(xlabel="w' (m s$^{-1}$)", xlim=(-3, 3), ylim=(-2, 2))
axs[0].set_ylabel("Ts' (K)")
fig.tight_layout()
```

中午，68% 的点落在右上和左下两个象限：上升的空气暖，下沉的空气冷。夜间，只有 38% 的点在这两个象限，多数点在左上和右下：下沉的空气暖。夜间的点也挤在原点附近，因为稳定层削弱了 turbulence。

turbulent kinetic energy 也说明这一点。下面用旋转后的三个分量计算它。

```{code-cell} python
for name, blk in blocks.items():
    comps = t3.double_rotation(blk["u"], blk["v"], blk["w"])
    tke = 0.5 * sum(np.var(c) for c in comps)
    print(f"{name}：turbulent kinetic energy {tke:.2f} m² s⁻²")
```

中午的 turbulent kinetic energy 是夜间的约 13 倍。中午的 turbulent kinetic energy 主要来自 convection。夜间只有 vertical wind shear 产生 turbulent kinetic energy，稳定层又消耗它。

### potential temperature 的核对

真实 data 一节用 earthkit-meteo 计算了 Cabauw 的 potential temperature。下面用 MetPy 计算同一个值，再用公式手算。

```{code-cell} python
t0, h0 = "2026-04-22T04:00", 200.0
p_pa = pd.DataFrame(pres, temp.index, z).loc[t0, h0]
th_mp = mpcalc.potential_temperature(p_pa * units.Pa, temp.loc[t0, h0] * units.K)
th_hand = temp.loc[t0, h0] * (1e5 / p_pa) ** (287.05 / 1005)  # Rd / cp
print(f"{t0} UTC，{h0:.0f} m：pressure {p_pa / 100:.1f} hPa；potential temperature earthkit {theta.loc[t0, h0]:.3f} K，"
      f"MetPy {th_mp.m:.3f} K，手算 {th_hand:.3f} K")
assert abs(th_mp.m - theta.loc[t0, h0]) < 0.01
assert abs(th_hand - theta.loc[t0, h0]) < 0.02
```

### power-law exponent

对 [](#eq-t3-power) 两边取对数，$\ln V = \ln V(z_r) + n \ln(z/z_r)$。所以在对数坐标里，power-law wind profile 是一条直线，斜率就是 $n$。下面用 numpy 的 `polyfit` 拟合这条直线，再用最小二乘的斜率公式手算核对：

```{math}
:label: eq-t3-slope
n = \frac{\sum_k (x_k - \overline{x})(y_k - \overline{y})}{\sum_k (x_k - \overline{x})^2}, \qquad x_k = \ln\frac{z_k}{z_r}, \quad y_k = \ln V(z_k)
```

拟合用 10 m 到 200 m 的 6 个 geometric height，每个时刻取 1 h 的平均。

```{code-cell} python
heights = np.array([10.0, 20.0, 40.0, 80.0, 140.0, 200.0])
x = np.log(heights / 10.0)


def power_law(z, v_ref, n):
    return v_ref * (z / 10.0) ** n


def exponent(profile):
    """numpy 在对数坐标里拟合直线，斜率就是 power-law exponent n。"""
    return np.polyfit(x, np.log(profile[heights].to_numpy()), 1)[0]


n_series = hourly_speed.apply(exponent, axis=1)
for hour in ["2026-04-21T13", "2026-04-22T04"]:
    y = np.log(hourly_speed.loc[hour, heights].to_numpy())
    n_hand = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)
    print(f"{hour} UTC：numpy n = {n_series.loc[hour]:.3f}，手算 n = {n_hand:.3f}")
    assert np.isclose(n_hand, n_series.loc[hour])
```

下图左边是两个时刻的廓线，右边是 15 天里每个时刻的 $n$ 的平均值。diurnal cycle 的平均值用 earthkit-transforms 的 `climatology.mean` 计算，它按一天中的小时分组。

```{code-cell} python
n_da = xr.DataArray(n_series.to_numpy(), coords={"time": n_series.index}, dims="time", name="n")
n_diurnal = climatology.mean(n_da, frequency="hour")
n_check = n_series.groupby(n_series.index.hour).mean()  # pandas 手算
assert np.allclose(n_diurnal.to_numpy(), n_check.to_numpy())
print(f"2026-04-16 到 2026-04-30，{len(n_series)} 个小时")
print(f"n 的 diurnal cycle：最小 {n_check.min():.2f}，在 {n_check.idxmin()} UTC；"
      f"最大 {n_check.max():.2f}，在 {n_check.idxmax()} UTC")
```

```{code-cell} python
#| label: fig-t3-profiles
#| caption: Cabauw 观测塔的 wind speed 廓线和 power-law exponent。左：2026-04-21 13 UTC 和 2026-04-22 04 UTC 的 1 h 平均 wind speed，线是幂律拟合，两个坐标轴都是对数坐标。中：同两个时刻的 potential temperature 廓线。右：2026-04-16 到 2026-04-30，每个小时的 power-law exponent，线是 15 天的平均值，虚线是 n = 1/7。data 来源：KNMI Cabauw。
fig, axs = plt.subplots(1, 3, figsize=(12, 4.2))
zz = np.linspace(10, 200, 50)
for hour, color in [("2026-04-21T13", "tab:orange"), ("2026-04-22T04", "tab:blue")]:
    prof = hourly_speed.loc[hour]
    n_h = n_series.loc[hour]
    v_ref = np.exp(np.polyfit(np.log(heights / 10.0), np.log(prof[heights].to_numpy()), 1)[1])
    label = f"{hour[5:10]} {hour[11:]} UTC, n = {n_h:.2f}"
    axs[0].plot(prof[heights], heights, "o", color=color, label=label)
    axs[0].plot(power_law(zz, v_ref, n_h), zz, color=color)
    axs[1].plot(hourly_theta.loc[hour] - 273.15, z, "o-", color=color, label=label)
axs[0].set(xscale="log", yscale="log", xlabel="wind speed (m s$^{-1}$)", ylabel="height (m)")
axs[0].minorticks_off()
axs[0].set_xticks([2, 3, 5, 8, 12], labels=["2", "3", "5", "8", "12"])
axs[0].set_yticks([10, 20, 40, 80, 140, 200], labels=["10", "20", "40", "80", "140", "200"])
axs[1].set(xlabel="potential temperature (°C)", ylabel="height (m)")
axs[0].legend(fontsize=8)
axs[1].legend(fontsize=8)
axs[2].plot(n_series.index.hour, n_series, ".", color="0.6", ms=3)
axs[2].plot(n_check.index, n_check, "k-", lw=2)
axs[2].axhline(1 / 7, color="k", ls="--", lw=0.8)
axs[2].set(xlabel="hour (UTC)", ylabel="power-law exponent n", xticks=range(0, 24, 3), ylim=(-0.1, 0.8))
for ax in axs:
    ax.grid(alpha=0.3, which="both")
fig.tight_layout()
```

2026-04-21 13 UTC 的 $n$ 是 0.11，2026-04-22 04 UTC 是 0.42。04 UTC 的廓线在 140 m 以上不再是直线，因为 jet stream 核就在 140 m 附近。15 天的平均值在白天的 ［08, 14］ UTC 之间约为 0.08，在夜间约为 0.4。$n = 1/7$ 只在约 07 UTC 和约 16 UTC 成立，这两个时刻的 stratification 接近 neutral。用 $n = 1/7$ 从 10 m wind 推算 100 m wind，夜间会严重低估 100 m wind。

### 100 m wind

风电和 AI weather model 都用 100 m wind。Cabauw 的塔在 100 m 没有仪器。本页用 80 m 和 140 m 的 wind speed 确定这一层的 $n$，再用 [](#eq-t3-power) 插值到 100 m：

```{math}
:label: eq-t3-v100
n_{80,140} = \frac{\ln(V_{140}/V_{80})}{\ln(140/80)}, \qquad V_{100} = V_{80}\left(\frac{100}{80}\right)^{n_{80,140}}
```

这个方法的误差可以用塔本身检查。下面假装 80 m 没有观测，用 40 m 和 140 m 插值到 80 m，再和 80 m 的观测比较。

```{code-cell} python
def interpolate(v_lo, v_hi, z_lo, z_hi, z_t):
    """在两个 geometric height 之间按 power-law wind profile 插值。"""
    n_layer = np.log(v_hi / v_lo) / np.log(z_hi / z_lo)
    return v_lo * (z_t / z_lo) ** n_layer


v80 = interpolate(speed[40.0], speed[140.0], 40, 140, 80)
v80_linear = speed[40.0] + (speed[140.0] - speed[40.0]) * (80 - 40) / (140 - 40)
for label, est in [("幂律", v80), ("线性", v80_linear)]:
    err = est - speed[80.0]
    print(f"{label}插值到 80 m：bias {err.mean():+.2f} m s⁻¹，RMSE {np.sqrt((err**2).mean()):.2f} m s⁻¹")
v100 = interpolate(speed[80.0], speed[140.0], 80, 140, 100)
print(f"15 天的平均 wind speed：80 m {speed[80.0].mean():.2f}，100 m {v100.mean():.2f}，"
      f"140 m {speed[140.0].mean():.2f} m s⁻¹")
```

幂律插值的 RMSE 是 0.35 m s⁻¹，linear interpolation 是 0.48 m s⁻¹。幂律插值的 bias 也更小。80 m 到 140 m 的间隔比 40 m 到 140 m 短，所以 100 m 的插值误差应当更小。下一节把这个 100 m wind 当作观测。

## AI 天气连接

### 100 m wind 和风电

现代陆上风电机组的 hub height 常在 ［80, 140］ m 之间，海上的更高。所以风电 forecast 最常用的变量是 100 m wind。ERA5 的变量是 `u100` 和 `v100`，长名是 `100m_u_component_of_wind` 和 `100m_v_component_of_wind`。ECMWF 开放 data 的参数名是 `100u` 和 `100v`。AIFS Single 输出这两个分量，GraphCast 和 WeatherBench 2 的标准变量里没有它们。

风电机组从 wind 中取得的功率是：

```{math}
:label: eq-t3-wind-power
P_{\mathrm{W}} = \tfrac{1}{2}\, \rho\, A\, C_p\, V^3
```

$A$ 是叶片扫过的面积，$C_p$ 是风电机组的效率，它不超过 16/27。功率和 wind speed 的三次方成正比。wind speed 的相对误差为 $\varepsilon$ 时，功率的相对误差是 $(1 + \varepsilon)^3 - 1 \approx 3\varepsilon$。例如 8 m s⁻¹ 的 wind 低估 1 m s⁻¹，功率低估约 33%。高估 1 m s⁻¹，功率高估约 42%。

真实的风电机组按 power curve 发电。wind speed 低于 cut-in wind speed 时不发电。wind speed 在 cut-in wind speed 和 rated wind speed 之间时，功率近似按三次方增大。wind speed 超过 rated wind speed 时，功率保持 rated power。wind speed 超过 cut-out wind speed 时，风电机组停机。

所以三次方的放大只出现在中等 wind speed。英国的 wind power output 很大，它决定燃气电厂要补多少电，也影响电价和天然气需求。

### AIFS 和 IFS 的 diurnal cycle bias

上一节说明，100 m wind 的 diurnal cycle 取决于稳定度。夜间的稳定层让 100 m wind 变大、2 m temperature 变低。这正是 numerical weather prediction model 和 AI weather model 难 forecast 的地方。

下面比较 2026-04-16 到 2026-04-30 的 15 天。forecast 来自每天 00 UTC 起报的 AIFS Single 和 IFS，lead time 在 ［24, 45］ h 之间。AIFS Single 每 6 h 输出一次，IFS 每 3 h 输出一次。ERA5 也一起比较，因为 AIFS 用 ERA5 预训练。这段时间运行的是 AIFS Single v1.1。它用 ［1979, 2022］ 年的 ERA5 预训练，用 ［2016, 2022］ 年的 IFS 业务 analysis 微调，见它的 [模型卡](https://huggingface.co/ecmwf/aifs-single-1.1)。

塔的 10 min 平均值的时间标签是时段的开始。forecast 是 valid time 的瞬时值。所以本页把 valid time 前后各 10 min 的两个平均值再平均，和 forecast 比较。模型的值取离 Cabauw 最近的 grid point。wind speed 用 earthkit-meteo 的 `wind.speed` 从两个分量计算。

```{code-cell} python
fc = d.page_data(t3.SAMPLE_FILES["ecmwf"], t3.ecmwf_point)
era_3h = d.page_data(t3.SAMPLE_FILES["era5_period"], t3.era5_period)

obs_v100 = interpolate(speed[80.0], speed[140.0], 80, 140, 100).rolling(2).mean()
obs_t2m = temp[2.0].rolling(2).mean()  # valid time 前后各 10 min


def errors(model_df):
    """一个模型在每个 valid time 的 100 m wind speed 和 2 m temperature，以及它们的误差。"""
    v = wind.speed(model_df["u100"].to_numpy(), model_df["v100"].to_numpy())
    assert np.allclose(v, np.hypot(model_df["u100"], model_df["v100"]))
    out = pd.DataFrame({"v100": v, "t2m": model_df["t2m"].to_numpy()}, index=model_df.index)
    out["v100_obs"] = obs_v100.reindex(out.index).to_numpy()
    out["t2m_obs"] = obs_t2m.reindex(out.index).to_numpy()
    out["v100_err"] = out["v100"] - out["v100_obs"]
    out["t2m_err"] = out["t2m"] - out["t2m_obs"]
    return out.dropna()  # 2026-04-16 00 UTC 缺少前一个 10 min 平均值


models = {
    "ERA5": errors(era_3h),
    "IFS": errors(fc[fc["model"] == "ifs"]),
    "AIFS Single": errors(fc[fc["model"] == "aifs-single"]),
}
diurnal = {}
for name, df in models.items():
    ds = xr.Dataset.from_dataframe(df)
    diurnal[name] = climatology.mean(ds, frequency="hour").to_dataframe()
    assert np.allclose(diurnal[name]["v100_err"], df["v100_err"].groupby(df.index.hour).mean())
    print(f"{name}：{len(df)} 个 valid time；100 m wind speed 的 bias {df['v100_err'].mean():+.2f} m s⁻¹，"
          f"2 m temperature 的 bias {df['t2m_err'].mean():+.2f} K")
```

```{code-cell} python
#| label: fig-t3-diurnal-bias
#| caption: 2026-04-16 到 2026-04-30，Cabauw 的 100 m wind speed 和 2 m temperature 的 diurnal cycle。左列：15 天的平均值，黑线是塔的观测。右列：模型减去观测，再按小时平均，得到 bias。AIFS Single 和 IFS 在每天 00 UTC 起报，lead time 在 ［24, 45］ h 之间。ERA5 每 3 h 取一个值。data 来源：KNMI Cabauw、ERA5、ECMWF 开放 data。
styles = {"ERA5": ("0.4", "s"), "IFS": ("tab:blue", "o"), "AIFS Single": ("tab:red", "D")}
fig, axs = plt.subplots(2, 2, figsize=(11, 7), sharex=True)
obs_diurnal = diurnal["IFS"]
axs[0, 0].plot(obs_diurnal.index, obs_diurnal["v100_obs"], "k-", lw=2, label="Cabauw tower")
axs[1, 0].plot(obs_diurnal.index, obs_diurnal["t2m_obs"] - 273.15, "k-", lw=2, label="Cabauw tower")
for name, (color, marker) in styles.items():
    one = diurnal[name]
    axs[0, 0].plot(one.index, one["v100"], marker=marker, color=color, label=name)
    axs[1, 0].plot(one.index, one["t2m"] - 273.15, marker=marker, color=color, label=name)
    axs[0, 1].plot(one.index, one["v100_err"], marker=marker, color=color, label=name)
    axs[1, 1].plot(one.index, one["t2m_err"], marker=marker, color=color, label=name)
axs[0, 0].set(ylabel="100 m wind speed (m s$^{-1}$)")
axs[1, 0].set(ylabel="2 m temperature (°C)", xlabel="hour (UTC)")
axs[0, 1].set(ylabel="bias of 100 m wind speed (m s$^{-1}$)")
axs[1, 1].set(ylabel="bias of 2 m temperature (K)", xlabel="hour (UTC)")
for ax in axs[:, 1]:
    ax.axhline(0, color="k", lw=0.8)
for ax in axs.flat:
    ax.grid(alpha=0.3)
    ax.set_xticks(range(0, 24, 3))
axs[0, 0].legend(fontsize=8)
fig.tight_layout()
```

[](#fig-t3-diurnal-bias) 说明了下面四点：

1. 三个模型在每个小时都低估 100 m wind speed。15 天的 bias 是：ERA5 −0.42 m s⁻¹，IFS −0.80 m s⁻¹，AIFS Single −0.66 m s⁻¹。
2. 低估最多的时间是 18 UTC，接近日落。这时塔的 100 m wind speed 增大得最快。ERA5、IFS 和 AIFS Single 分别低估 0.71、1.30 和 1.06 m s⁻¹。所以模型的 100 m wind 的 diurnal cycle 比观测弱。
3. 2 m temperature 的 bias 随时间变化。IFS 在 09 UTC 到 18 UTC 偏冷 ［0.56, 0.90］ K，在 21 UTC 偏暖 0.47 K。ERA5 在傍晚偏暖，21 UTC 偏暖 0.82 K。AIFS Single 的 bias 在 ［−0.46, 0.42］ K 之间，全天平均的 bias 最小。它在 18 UTC 偏暖 0.42 K，和 ERA5 相近，和 IFS 相反。
4. 样本很小。每个小时只有 15 个值，每个小时的 bias 的 standard error 在 ［0.2, 0.3］ m s⁻¹ 或 K 之间。两个模型相差不到约 0.5 m s⁻¹ 或 0.5 K 时，这 15 天的 data 不能说明哪个模型更好。

全天都有的低估可能有一部分来自 grid point 和观测点的差别。模型的值是一个格子的平均值，格子宽约 9 km 到 31 km。格子里有村庄、树木和城镇，它们的 roughness length 比 Cabauw 的草地大。所以格子平均的 wind speed 可能比塔上的 wind speed 小。

18 UTC 的额外低估和稳定层有关。numerical weather prediction model 在稳定层里常常混合得太强，使 low-level jet 太弱，夜间的降温太小。Sandu 等，2013 说明了 IFS 的这个问题，[doi:10.1002/jame.20013](https://doi.org/10.1002/jame.20013)。他们也指出，IFS 夜间的 2 m temperature 在陆地上仍然常常偏冷。AIFS 从 ERA5 和 IFS 的 analysis 学习，所以它也会学到这些 data 在稳定层里的 bias。本页只有一个观测点和 15 天，不能证明这个原因。

### 从 wind speed 的误差到 wind power output 的误差

下面用一条简化的 power curve 把 100 m wind speed 换成 wind power output。cut-in wind speed 3 m s⁻¹，rated wind speed 12 m s⁻¹，cut-out wind speed 25 m s⁻¹。在 cut-in wind speed 和 rated wind speed 之间，出力按 wind speed 的三次方增大。capacity factor 是平均出力和 rated power 之比。

```{code-cell} python
V_IN, V_RATED, V_OUT = 3.0, 12.0, 25.0  # m s⁻¹


def power_fraction(v):
    """简化的 power curve：出力和 rated power 之比。"""
    v = np.asarray(v, dtype=float)
    frac = np.clip((v**3 - V_IN**3) / (V_RATED**3 - V_IN**3), 0, 1)
    return np.where(v >= V_OUT, 0.0, frac)


def relative_error(model, obs):
    """平均值的相对误差，单位是 %。"""
    return 100 * (np.mean(model) / np.mean(obs) - 1)


rows = {}
for name, df in models.items():
    p_obs, p_mod = power_fraction(df["v100_obs"]), power_fraction(df["v100"])
    evening = df.index.hour.isin([18, 21, 0, 3])
    rows[name] = {
        "capacity factor, tower (%)": 100 * p_obs.mean(),
        "capacity factor, model (%)": 100 * p_mod.mean(),
        "all hours: wind error (%)": relative_error(df["v100"], df["v100_obs"]),
        "all hours: power error (%)": relative_error(p_mod, p_obs),
        "18 to 03 UTC: wind error (%)": relative_error(df["v100"][evening], df["v100_obs"][evening]),
        "18 to 03 UTC: power error (%)": relative_error(p_mod[evening], p_obs[evening]),
    }
print(pd.DataFrame(rows).round(1).to_string())

# 三次方关系的手算：8 m s⁻¹ 的 wind 低估 1 m s⁻¹，功率低估约 33%
assert abs((7 / 8) ** 3 - 1 + 0.33) < 0.01
```

用塔的 100 m wind 计算，capacity factor 约是 19%。三个模型的 capacity factor 都更小：ERA5 是 16.1%，AIFS Single 是 14.6%，IFS 是 12.9%。全天的 wind speed 低估 ［6.6, 12.7］%，出力低估 ［16.9, 33.3］%。出力的误差约是 wind speed 误差的 2.5 倍。它比 3 倍小，因为 power curve 在 cut-in wind speed 以下和 rated wind speed 以上不按三次方变化。18 UTC 到次日 03 UTC 的误差比全天的误差稍大。

到 2026 年第二季度末，英国的风电 installed capacity 约 34 GW，见 DESNZ 的 [Energy Trends 第 6 节](https://www.gov.uk/government/statistics/energy-trends-section-6-renewables)。假设全国的 forecast 都像 AIFS Single 在 Cabauw 这样，把 capacity factor 低估 4.7 个百分点。对 33.6 GW 来说，这是约 1.6 GW 的出力，要由燃气电厂或进口电力补上。所以英国的电网运营者和能源交易者都关心 100 m wind 的 forecast，特别是傍晚和夜间的 forecast。这些时间的稳定层最难 forecast，三次方关系又放大风速的误差。

分析师可以对任何一个 AI weather model 做同样的检查。第一，按一天中的小时分组计算 100 m wind speed 和 2 m temperature 的 bias。夜间和白天的 bias 常常符号相反，全天平均会掩盖它们。第二，用模型的 100 m wind 和 10 m wind 计算夜间的 power-law exponent，和塔的观测比较。$n$ 太小说明模型的夜间混合太强。

## 练习

:::{exercise}
:label: ex-t3-1

计算一节用 30 min 做 Reynolds averaging。把中午的时段分成 6 个 5 min 的小段，在每个小段里分别做平均、计算 $\overline{w'T_s'}$，再把 6 个结果平均。sensible heat flux 变大还是变小？为什么？
:::

:::{solution} ex-t3-1
:class: dropdown

```python
parts = [day.iloc[k * 6000 : (k + 1) * 6000] for k in range(6)]  # 6 个 5 min 的小段
wts_5min = []
for part in parts:
    _, _, w5 = t3.double_rotation(part["u"], part["v"], part["w"])
    ts5 = part["t_sonic"].to_numpy()
    wts_5min.append(np.mean((w5 - w5.mean()) * (ts5 - ts5.mean())))
print(np.mean(wts_5min), table.loc["w'Ts' (K m s-1)", "12 UTC"])
```

6 个小段的平均值是 0.211 K m s⁻¹，30 min 的值是 0.222 K m s⁻¹。sensible heat flux 变小了约 5%。5 min 的平均值跟着周期较长的涡旋一起变化。所以这些涡旋算进了平均值，没有算进 turbulent fluctuation。中午的 convection 涡旋很大，周期可以超过 5 min。所以 eddy covariance weather station 常用 30 min 的平均时段。
:::

:::{exercise}
:label: ex-t3-2

风电场常常只有 10 m wind 的观测。用 $n = 1/7$ 从 Cabauw 的 10 m wind 推算 100 m wind，再和 [](#eq-t3-v100) 的 100 m wind 比较。白天和夜间的误差各是多少？换算成 wind power output 的误差是多少？
:::

:::{solution} ex-t3-2
:class: dropdown

```python
v100_17 = speed[10.0] * (100 / 10) ** (1 / 7)
v100_tower = interpolate(speed[80.0], speed[140.0], 80, 140, 100)
hour = v100_17.index.hour
is_night = (hour >= 20) | (hour < 4)
for label, sel in [("night", is_night), ("day", ~is_night)]:
    err = v100_17[sel].mean() / v100_tower[sel].mean() - 1
    perr = power_fraction(v100_17[sel]).mean() / power_fraction(v100_tower[sel]).mean() - 1
    print(label, round(100 * err, 1), round(100 * perr, 1))
```

夜间指 20 UTC 到次日 04 UTC。用 $n = 1/7$ 推算的 100 m wind speed 平均是 3.7 m s⁻¹，塔插值的值是 6.9 m s⁻¹。wind speed 低估 45%，出力低估 83%。夜间的 $n$ 约是 0.4，比 1/7 大得多，所以 1/7 低估了夜间的 100 m wind。

白天指 04 UTC 到 20 UTC。wind speed 低估 10%，出力低估 24%。08 UTC 到 14 UTC 的 $n$ 小于 1/7，早晨和傍晚的 $n$ 大于 1/7，两部分的误差大部分相互抵消。出力的误差总是比 wind speed 的误差大很多，因为三次方关系放大了它。
:::

:::{exercise}
:label: ex-t3-3

METEO 300 的 11.8 节给出 mixed layer 的增温率 $\partial\overline{\theta}/\partial t \approx \overline{w'\theta'}_0 / h$，$h$ 是 mixed layer 的 thickness。2026-04-21 09 UTC 到 13 UTC，Cabauw 的 sensible heat flux 平均约 115 W m⁻²。同一时段，ERA5 的 boundary layer height 从约 600 m 增大到约 1130 m，11 UTC 是 790 m。估计 mixed layer 每小时增温多少，再和 [](#fig-t3-tower) 里 200 m 的 potential temperature 比较。
:::

:::{solution} ex-t3-3
:class: dropdown

运动学 sensible heat flux 是 $\overline{w'\theta'}_0 = H/(\rho c_p) \approx 115 / (1.25 \times 1005) \approx 0.092\ \mathrm{K\,m\,s^{-1}}$。取 $h = 790$ m，增温率约是 $0.092 / 790 \times 3600 \approx 0.42\ \mathrm{K\,h^{-1}}$。$h$ 取 600 m 和 1130 m 时，增温率在 ［0.29, 0.55］ K h⁻¹ 之间。

塔的 data 说明，200 m 的 potential temperature 从 09 UTC 到 13 UTC 由 280.2 K 升到 284.3 K，约 1.0 K h⁻¹。2 m 到 200 m 的各层增温得差不多。所以 mixed layer 实际的增温率是估计值的 2 倍多。

可能的原因有三个。第一，公式忽略了 mixed layer 顶的通量。mixed layer 增厚时，entrainment 把上面较暖的空气带进 mixed layer。第二，eddy covariance 观测的 sensible heat flux 常常偏小，surface energy balance 常常不闭合。第三，warm advection 也能让空气增温。本页的 data 不能区分这三个原因。
:::

:::{exercise}
:label: ex-t3-4

本页说 low-level jet 约在日落后半个 inertial period 达到最大。计算 Cabauw 的 inertial period。2026-04-21 的日落约在 18:50 UTC。jet stream 应该在什么时间最强？和 [](#fig-t3-tower) 比较。
:::

:::{solution} ex-t3-4
:class: dropdown

$f = 2\Omega\sin\varphi = 2 \times 7.292 \times 10^{-5} \times \sin 51.97° \approx 1.149 \times 10^{-4}\ \mathrm{s^{-1}}$。inertial period 是 $2\pi/f \approx 15.2$ h，半个周期约是 7.6 h。从 18:50 UTC 起算，jet stream 应该在约 02:25 UTC 最强。

塔的 data 说明，200 m 的 wind speed 在 01:00 到 01:30 UTC 最大，约 12.4 m s⁻¹。140 m 和 80 m 的 wind speed 在约 02:00 UTC 最大。观测的最大值比估计早约 1 h。

surface 的 sensible heat flux 在约 16:30 UTC 已经变负，比日落早约 2 h 20 min。从 16:30 UTC 起算，估计的时间是约 00:05 UTC。观测的时间在两个估计之间。所以起算的时间应该是 turbulence 变弱的时间，它不一定是日落的时间。
:::
