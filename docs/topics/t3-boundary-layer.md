---
title: 边界层
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

边界层是对流层最低的一层。地面的加热、冷却和摩擦力在 1 h 以内影响整层。白天的边界层约 1 km 厚，晴朗的夜间常常只有约 100 m 厚。[](#fig-ch04-sounding) 用两次探空看了边界层的位温廓线。[力与地转风](ch05-dynamics-geostrophic.md) 一页看了摩擦力怎样让 10 m 风斜穿等压线。本页用一座 213 m 的观测塔看边界层的日变化，再用超声风速仪看湍流本身。

### 边界层的日变化

白天，太阳加热地面。地面用感热通量加热贴地的空气，热空气上升，形成对流。对流把边界层搅匀，这一层叫混合层。混合层里的位温和风速几乎不随几何高度变化。混合层顶上是一个稳定层。上升的热空气冲进稳定层，把上面的空气卷进混合层，这个过程叫夹卷。

日落以后，地面用长波辐射冷却。贴地的空气跟着变冷，形成逆温，这一层叫稳定边界层。稳定层削弱湍流。稳定边界层上面留下前一天的混合层空气，这一层叫残留层。日出以后，混合层从地面向上增长，先吞掉稳定边界层，再吞掉残留层。

### 低空急流

白天，湍流把上层的动量送到地面，所以整个混合层的风都比地转风慢。日落以后，稳定边界层把残留层和地面隔开。残留层的空气突然不再受摩擦力，气压梯度力和 Coriolis 力不再和风平衡。风绕着地转风做惯性振荡，周期是惯性周期 $2\pi/f$。[](#fig-ch01-inertial) 画了只受 Coriolis 力的惯性振荡。

在 52°N，$f = 1.15 \times 10^{-4}\ \mathrm{s^{-1}}$，惯性周期约 15.2 h。日落时风比地转风慢。约半个惯性周期以后，风比地转风快。这个时刻约在日落后 7.6 h，也就是后半夜。这时离地几百米处出现一个风速的极大值，叫低空急流。荷兰的 Cabauw 观测塔经常测到低空急流。

### Reynolds 平均

湍流的风变化得很快。超声风速仪每秒测 20 次风。把每个量写成平均值和脉动量的和：

```{math}
:label: eq-t3-reynolds
u = \overline{u} + u', \qquad \overline{u'} = 0
```

$\overline{u}$ 是一段时间的平均值，本页取 30 min。$u'$ 是脉动量，它的平均值按定义等于零。两个量的乘积的平均值是：

```{math}
:label: eq-t3-product
\overline{u\,w} = \overline{u}\,\overline{w} + \overline{u'w'}
```

$\overline{u'w'}$ 是 $u$ 和 $w$ 的协方差。两个脉动量各自的平均值是零，它们的乘积的平均值一般不是零。这一项就是湍流通量。Reynolds 平均把运动方程分成平均风的方程和湍流的方程，湍流只通过这些协方差影响平均风。

### 湍流通量

$w$ 是垂直速度。$\overline{w'\theta'}$ 是热量的运动学通量，单位是 K m s⁻¹。乘以空气的密度和定压比热容，就得到感热通量：

```{math}
:label: eq-t3-qh
Q_H = \rho\, c_p\, \overline{w'\theta'}
```

白天，贴地的位温随几何高度降低。上升的空气比周围暖，$w' > 0$ 时 $\theta' > 0$。下沉的空气比周围冷，$w' < 0$ 时 $\theta' < 0$。两种情况的乘积都为正，所以 $\overline{w'\theta'} > 0$，热量向上输送。夜间，位温随几何高度升高，符号全部相反，热量向下输送。

$\overline{u'w'}$ 是动量通量，单位是 m² s⁻²。风速随几何高度增大，下沉的空气带来较快的风，所以 $\overline{u'w'} < 0$，动量向下输送。地面吸收这些动量，这就是边界层的摩擦力。摩擦速度把动量通量写成一个速度：

```{math}
:label: eq-t3-ustar
u_* = \left(\overline{u'w'}^{\,2} + \overline{v'w'}^{\,2}\right)^{1/4}
```

湍流动能是三个风速分量的方差之和的一半，$\tfrac{1}{2}\left(\overline{u'^2} + \overline{v'^2} + \overline{w'^2}\right)$。对流和垂直风切变产生湍流动能。大的涡旋把能量传给小的涡旋，最小的涡旋把能量变成热。

### 幂律风廓线

地面的摩擦力让风速随几何高度增大。增大得多快取决于静力稳定度。风电行业常用幂律风廓线描述这个关系：

```{math}
:label: eq-t3-power
V(z) = V(z_r)\left(\frac{z}{z_r}\right)^{n}
```

$z_r$ 是参考几何高度，常取 10 m。$n$ 是幂律指数。在中性层结的平坦陆面上，$n$ 约为 1/7。白天的混合层把动量搅匀，风速随几何高度变化小，$n$ 小。夜间的稳定层削弱湍流，上层的风和地面脱节，$n$ 大。所以同一个 10 m 风速，在夜间对应更大的 100 m 风速。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 边界层 | atmospheric boundary layer | ABL |
| 边界层高度 | boundary layer height | $z_i$ |
| 混合层 | mixed layer | — |
| 稳定边界层 | stable boundary layer | SBL |
| 残留层 | residual layer | — |
| 夹卷 | entrainment | — |
| 日变化 | diurnal cycle | — |
| 低空急流 | low-level jet | — |
| 惯性振荡 | inertial oscillation | — |
| 惯性周期 | inertial period | — |
| 湍流 | turbulence | — |
| Reynolds 平均 | Reynolds averaging | — |
| 脉动量 | turbulent fluctuation | $u'$ |
| 方差 | variance | $\overline{u'^2}$ |
| 协方差 | covariance | $\overline{a'b'}$ |
| 湍流通量 | turbulent flux | — |
| 运动学通量 | kinematic flux | — |
| 感热通量 | sensible heat flux | $Q_H$ |
| 动量通量 | momentum flux | $\overline{u'w'}$ |
| 摩擦速度 | friction velocity | $u_*$ |
| 湍流动能 | turbulent kinetic energy | TKE |
| 涡动协方差 | eddy covariance | — |
| 超声风速仪 | sonic anemometer | — |
| 超声温度 | sonic temperature | $T_s$ |
| 幂律风廓线 | power-law wind profile | — |
| 幂律指数 | power-law exponent | $n$ |
| 100 m 风 | 100 m wind | $u_{100}$, $v_{100}$ |
| 轮毂高度 | hub height | $z_{\mathrm{hub}}$ |
| 风电出力 | wind power output | $P_{\mathrm{W}}$ |
| 功率曲线 | power curve | — |
| 容量系数 | capacity factor | — |
| 切入风速 | cut-in wind speed | $V_{\mathrm{in}}$ |
| 额定风速 | rated wind speed | $V_{\mathrm{rated}}$ |
| 切出风速 | cut-out wind speed | $V_{\mathrm{out}}$ |
| 额定功率 | rated power | — |
| 装机容量 | installed capacity | — |
| Richardson 数 | Richardson number | Ri |

## 真实数据

本页的个例是 2026-04-21 00 UTC 到 2026-04-23 00 UTC。这几天一个高压停在北海上空，荷兰吹东北风。两个白天都几乎没有云，中间的夜晚也没有云。所以 48 h 里先有一个混合层，再有一个稳定边界层和低空急流，然后又是一个混合层。

### Cabauw 观测塔的 48 h

KNMI 的 Cabauw 观测塔在荷兰中部的平坦草地上，高 213 m。塔上的仪器在 10、20、40、80、140 和 200 m 测风，在这些几何高度和 2 m 测温度。每个值是 10 min 的平均。位温用 earthkit-meteo 从温度和气压计算，各层的气压从地面气压用压高公式推算。计算一节核对这个位温。

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

speed = tower["F"].to_pandas()  # 风速，m s⁻¹；列是几何高度
temp = tower["TA"].to_pandas()  # 温度，K
z = temp.columns.to_numpy()
# 压高公式：从地面气压向上推各层的气压，层平均温度取 2 m 和本层的平均
p_sfc = surface["P0"].reindex(temp.index).to_numpy()[:, None] * 100  # Pa
t_layer = (temp.to_numpy() + temp[2.0].to_numpy()[:, None]) / 2
pres = p_sfc * np.exp(-G0 * z / (RD * t_layer))
theta = pd.DataFrame(thermo.potential_temperature(temp.to_numpy(), pres), temp.index, z)

case = slice(*t3.CASE)
hourly_speed = speed.resample("1h").mean()
hourly_theta = theta.resample("1h").mean()
for label, hour in [("白天", "2026-04-21T13"), ("夜间", "2026-04-22T04")]:
    v, th = hourly_speed.loc[hour], hourly_theta.loc[hour]
    print(f"{hour} UTC {label}：10 m 风速 {v[10.0]:.1f}，200 m 风速 {v[200.0]:.1f} m s⁻¹；"
          f"200 m 和 2 m 的位温差 {th[200.0] - th[2.0]:+.1f} K")
jet = speed.loc["2026-04-21T18":"2026-04-22T07", 200.0]
print(f"夜间 200 m 风速最大 {jet.max():.1f} m s⁻¹，时间 {jet.idxmax():%H:%M} UTC")
blh = era["blh"].loc[case]
print(f"ERA5 边界层高度：［{blh.min():.0f}, {blh.max():.0f}］ m")
print(f"Cabauw 感热通量：［{surface['H'].loc[case].min():.0f}, {surface['H'].loc[case].max():.0f}］ W m⁻²")
```

```{code-cell} python
#| label: fig-t3-tower
#| caption: 2026-04-21 00 UTC 到 2026-04-23 00 UTC，Cabauw 观测塔的 10 min 平均值。从上到下：各几何高度的风速；各几何高度的位温；地面的感热通量，向上为正；ERA5 的边界层高度，虚线是塔顶的 200 m。灰色是太阳在地平线以下的时段。数据来源：KNMI Cabauw、ERA5。
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

1. 白天，各层的风速挤在一起。2026-04-21 13 UTC，10 m 的风速是 4.3 m s⁻¹，200 m 的风速是 5.9 m s⁻¹。混合层把动量搅匀了。
2. 白天，各层的位温也挤在一起。2 m 的位温比 200 m 高约 0.9 K，贴地的一层不稳定。夜间，各层的位温分开，2 m 最冷。2026-04-22 04 UTC，200 m 的位温比 2 m 高 7.5 K，这是稳定边界层。
3. 2026-04-21 18 UTC，200 m 的风速约 7 m s⁻¹。夜间，它增大到 12.5 m s⁻¹，10 m 的风速却减小到约 3 m s⁻¹。这是低空急流。04 UTC 以后，140 m 的风比 200 m 快，急流核降到塔里。日出以后，混合层把急流的动量带到地面，上层的风很快减弱。
4. 感热通量在白天向上，最大约 157 W m⁻²。它在日落前约 2 h 变成向下，夜间约为 −20 W m⁻²。ERA5 的边界层高度在白天超过 1200 m，在夜间降到约 170 m，低于塔顶。

### 20 Hz 的湍流

Cabauw 只公开 10 min 的平均值。本页的 20 Hz 数据来自德国 Hartheim 的森林观测站 DE-Har。超声风速仪装在 27 m 高的塔上，森林高约 18 m。下面是 2024-07-01 的两个 30 min 时段。12 UTC 是晴朗的中午，21 UTC 是日落后的夜间。

```{code-cell} python
day = t3.turbulence_frame(d.turbulence_20hz(t3.TURBULENCE_DAY))
night = t3.turbulence_frame(d.page_data(t3.SAMPLE_FILES["night"], t3.turbulence_night))
blocks = {"12 UTC": day, "21 UTC": night}
for name, blk in blocks.items():
    print(f"{name}：{len(blk)} 个值，w 的范围 ［{blk['w'].min():.2f}, {blk['w'].max():.2f}］ m s⁻¹，"
          f"超声温度的范围 ［{blk['t_sonic'].min():.1f}, {blk['t_sonic'].max():.1f}］ °C")
```

```{code-cell} python
#| label: fig-t3-hf
#| caption: 2024-07-01，DE-Har 森林观测站 27 m 处的 20 Hz 观测。上：垂直速度。下：超声温度减去 30 min 的平均值。左列从 12:00 UTC 开始，右列从 21:00 UTC 开始，每列 30 min。虚线是 30 min 的平均值。数据来源：DE-Har，Zenodo。
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

1. 中午的垂直速度在 ［−4.0, 4.1］ m s⁻¹ 之间跳动。夜间的幅度只有中午的约三分之一。
2. 中午的超声温度有很多尖峰，向上偏。暖的空气团从森林里升起，经过风速仪。
3. 两个时段都有几分钟长的起伏，也有不到一秒的抖动。湍流同时包含很多尺度的涡旋。

## 数据集

KNMI 的 Cabauw 观测塔是欧洲最常用的边界层观测。本页用 `d.cabauw` 读取三个数据集：`tower_meteo` 是塔上的风和温度，`surface_flux` 是地面的湍流通量，`surface_meteo` 是地面气压。三个数据集都是 10 min 平均，经过验证并填补了缺测。它们以 CC BY 4.0 许可发布。

ERA5 是 ECMWF 制作的再分析数据集，网格间距是 0.25°。本页从 ARCO-ERA5 读取离 Cabauw 最近的格点，52.0°N、5.0°E。变量是边界层高度 `blh`、瞬时感热通量 `ishf`、100 m 风 `u100` 和 `v100`、10 m 风和 2 m 温度。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

20 Hz 的数据来自 DE-Har 观测站的涡动协方差原始数据。Zenodo 以 CC BY 4.0 许可公开 2023 年和 2024 年的数据。`d.turbulence_20hz` 读取它，每个 30 min 时段还附带观测站用 EddyPro 算出的通量。

AI 天气连接一节用 ECMWF 开放数据里的 AIFS Single 和 IFS 预报，CC BY 4.0 许可。AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。

模块 `meteo300.pages.t3` 里的函数记录了样本的制作方法。在线时，`d.page_data` 运行这些函数。离线时，它读取样本。样本的来源和许可见 `data/samples/ATTRIBUTION-t3.md`。

下面是两个备选数据集。ICOS 的通量观测站网有欧洲约 100 个涡动协方差观测站。它的原始高频数据要申请账户。很多观测站的探空和激光雷达也能估计边界层高度，例如 IGRA2 的探空。完整的数据集条目见 [数据集参考页](../reference/datasets.md)。

## 计算

本节先在 20 Hz 数据上做 Reynolds 平均，算出动量通量和感热通量，再和 EddyPro 的结果核对。然后用 Cabauw 的塔拟合幂律指数，并说明怎样从塔上的观测得到 100 m 风。

### Reynolds 平均

超声风速仪的坐标轴不一定沿着风。先旋转坐标轴，使 $x$ 轴沿着 30 min 的平均风，使平均的垂直速度为零。`t3.double_rotation` 做这两次旋转。然后按 [](#eq-t3-reynolds) 把每个量分成平均值和脉动量，再检查 [](#eq-t3-product)。

```{code-cell} python
u, v, w = t3.double_rotation(day["u"], day["v"], day["w"])
up, vp, wp = u - u.mean(), v - v.mean(), w - w.mean()
print(f"平均风速 {u.mean():.2f} m s⁻¹，平均 v {v.mean():.1e}，平均 w {w.mean():.1e} m s⁻¹")
print(f"脉动量的平均值：u' {up.mean():.1e}，w' {wp.mean():.1e} m s⁻¹")

uw_mean = np.mean(u * w)
uw_cov = np.mean(up * wp)  # 手算的协方差
print(f"mean(u w) = {uw_mean:.4f}，mean(u) mean(w) = {u.mean() * w.mean():.1e}，"
      f"mean(u' w') = {uw_cov:.4f} m² s⁻²")
assert np.isclose(uw_mean, u.mean() * w.mean() + uw_cov)
assert np.isclose(uw_cov, np.cov(u, w, bias=True)[0, 1])  # numpy 的协方差
```

旋转以后，平均的 $v$ 和 $w$ 都是零。脉动量的平均值也是零，只差计算机的舍入误差。$\overline{u\,w}$ 几乎全部来自协方差 $\overline{u'w'}$，因为 $\overline{w} = 0$。手算的协方差和 numpy 的 `np.cov` 相同。

### 动量通量和感热通量

超声温度 $T_s$ 接近虚温，它比温度高约 $0.51\,q\,T$。所以 $\overline{w'T_s'}$ 包含水汽的贡献。下面先用气体分析仪的水汽密度算出 $\overline{w'q'}$，再从 $\overline{w'T_s'}$ 减去水汽的部分。在 27 m 处，位温的脉动量和温度的脉动量几乎相同。密度用 MetPy 从气压和温度计算，单位用 pint 检查。

```{code-cell} python
CP = 1005 * units("J kg^-1 K^-1")  # 干空气的定压比热容
M_H2O = 18.015e-6  # kg mmol⁻¹


def fluxes(blk):
    """一个 30 min 时段的动量通量、摩擦速度和感热通量。"""
    u, v, w = t3.double_rotation(blk["u"], blk["v"], blk["w"])
    wp = w - w.mean()
    ts = blk["t_sonic"].to_numpy() + 273.15
    p = blk.attrs["pa_kpa"] * units.kPa
    t_air = (blk.attrs["eddypro_TA_EP"] * units.degC).to("K")
    rho = mpcalc.density(p, t_air, 0 * units("g/kg"))
    rho_v = blk["h2o"].to_numpy() * M_H2O  # 水汽密度，kg m⁻³
    wq = np.mean(wp * (rho_v - rho_v.mean())) / rho.m_as("kg/m^3")  # w'q'
    wts = np.mean(wp * (ts - ts.mean()))  # w'Ts'
    wt = wts - 0.51 * ts.mean() * wq  # w'T'：去掉水汽的贡献
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

两个时段的摩擦速度和感热通量都和 EddyPro 相差不到 3%。EddyPro 是观测站用的软件，它还做了谱修正等几项修正。

中午的感热通量约为 242 W m⁻²，热量向上。夜间约为 −32 W m⁻²，热量向下。中午的摩擦速度约是夜间的 3 倍。去掉水汽的贡献以后，中午的 $\overline{w'T'}$ 比 $\overline{w'T_s'}$ 小约 7%。森林在中午蒸发大量的水，所以这一项不能省略。

下面的图把每个 20 Hz 的值画成一个点，横轴是 $w'$，纵轴是 $T_s'$。

```{code-cell} python
#| label: fig-t3-quadrant
#| caption: 2024-07-01，DE-Har 27 m 处垂直速度的脉动量和超声温度的脉动量。每个时段 36 000 个 20 Hz 的值，颜色越深，点越密。左：12:00 UTC 起的 30 min。右：21:00 UTC 起的 30 min。数据来源：DE-Har，Zenodo。
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

中午，68% 的点落在右上和左下两个象限：上升的空气暖，下沉的空气冷。夜间，只有 38% 的点在这两个象限，多数点在左上和右下：下沉的空气暖。夜间的点也挤在原点附近，因为稳定层削弱了湍流。

湍流动能也说明这一点。下面用旋转后的三个分量计算它。

```{code-cell} python
for name, blk in blocks.items():
    comps = t3.double_rotation(blk["u"], blk["v"], blk["w"])
    tke = 0.5 * sum(np.var(c) for c in comps)
    print(f"{name}：湍流动能 {tke:.2f} m² s⁻²")
```

中午的湍流动能是夜间的约 13 倍。中午的湍流动能主要来自对流。夜间只有垂直风切变产生湍流动能，稳定层又消耗它。

### 位温的核对

真实数据一节用 earthkit-meteo 计算了 Cabauw 的位温。下面用 MetPy 计算同一个值，再用公式手算。

```{code-cell} python
t0, h0 = "2026-04-22T04:00", 200.0
p_pa = pd.DataFrame(pres, temp.index, z).loc[t0, h0]
th_mp = mpcalc.potential_temperature(p_pa * units.Pa, temp.loc[t0, h0] * units.K)
th_hand = temp.loc[t0, h0] * (1e5 / p_pa) ** (287.05 / 1005)  # Rd / cp
print(f"{t0} UTC，{h0:.0f} m：气压 {p_pa / 100:.1f} hPa；位温 earthkit {theta.loc[t0, h0]:.3f} K，"
      f"MetPy {th_mp.m:.3f} K，手算 {th_hand:.3f} K")
assert abs(th_mp.m - theta.loc[t0, h0]) < 0.01
assert abs(th_hand - theta.loc[t0, h0]) < 0.02
```

### 幂律指数

对 [](#eq-t3-power) 两边取对数，$\ln V = \ln V(z_r) + n \ln(z/z_r)$。所以在对数坐标里，幂律风廓线是一条直线，斜率就是 $n$。下面用 numpy 的 `polyfit` 拟合这条直线，再用最小二乘的斜率公式手算核对：

```{math}
:label: eq-t3-slope
n = \frac{\sum_k (x_k - \overline{x})(y_k - \overline{y})}{\sum_k (x_k - \overline{x})^2}, \qquad x_k = \ln\frac{z_k}{z_r}, \quad y_k = \ln V(z_k)
```

拟合用 10 m 到 200 m 的 6 个几何高度，每个时刻取 1 h 的平均。

```{code-cell} python
heights = np.array([10.0, 20.0, 40.0, 80.0, 140.0, 200.0])
x = np.log(heights / 10.0)


def power_law(z, v_ref, n):
    return v_ref * (z / 10.0) ** n


def exponent(profile):
    """numpy 在对数坐标里拟合直线，斜率就是幂律指数 n。"""
    return np.polyfit(x, np.log(profile[heights].to_numpy()), 1)[0]


n_series = hourly_speed.apply(exponent, axis=1)
for hour in ["2026-04-21T13", "2026-04-22T04"]:
    y = np.log(hourly_speed.loc[hour, heights].to_numpy())
    n_hand = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)
    print(f"{hour} UTC：numpy n = {n_series.loc[hour]:.3f}，手算 n = {n_hand:.3f}")
    assert np.isclose(n_hand, n_series.loc[hour])
```

下图左边是两个时刻的廓线，右边是 15 天里每个时刻的 $n$ 的平均值。日变化的平均值用 earthkit-transforms 的 `climatology.mean` 计算，它按一天中的小时分组。

```{code-cell} python
n_da = xr.DataArray(n_series.to_numpy(), coords={"time": n_series.index}, dims="time", name="n")
n_diurnal = climatology.mean(n_da, frequency="hour")
n_check = n_series.groupby(n_series.index.hour).mean()  # pandas 手算
assert np.allclose(n_diurnal.to_numpy(), n_check.to_numpy())
print(f"2026-04-16 到 2026-04-30，{len(n_series)} 个小时")
print(f"n 的日变化：最小 {n_check.min():.2f}，在 {n_check.idxmin()} UTC；"
      f"最大 {n_check.max():.2f}，在 {n_check.idxmax()} UTC")
```

```{code-cell} python
#| label: fig-t3-profiles
#| caption: Cabauw 观测塔的风速廓线和幂律指数。左：2026-04-21 13 UTC 和 2026-04-22 04 UTC 的 1 h 平均风速，线是幂律拟合，两个坐标轴都是对数坐标。中：同两个时刻的位温廓线。右：2026-04-16 到 2026-04-30，每个小时的幂律指数，线是 15 天的平均值，虚线是 n = 1/7。数据来源：KNMI Cabauw。
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

2026-04-21 13 UTC 的 $n$ 是 0.11，2026-04-22 04 UTC 是 0.42。04 UTC 的廓线在 140 m 以上不再是直线，因为急流核就在 140 m 附近。15 天的平均值在白天的 ［08, 14］ UTC 之间约为 0.08，在夜间约为 0.4。$n = 1/7$ 只在约 07 UTC 和约 16 UTC 成立，这两个时刻的层结接近中性。用 $n = 1/7$ 从 10 m 风推算 100 m 风，夜间会严重低估 100 m 风。

### 100 m 风

风电和 AI 天气模型都用 100 m 风。Cabauw 的塔在 100 m 没有仪器。本页用 80 m 和 140 m 的风速确定这一层的 $n$，再用 [](#eq-t3-power) 插值到 100 m：

```{math}
:label: eq-t3-v100
n_{80,140} = \frac{\ln(V_{140}/V_{80})}{\ln(140/80)}, \qquad V_{100} = V_{80}\left(\frac{100}{80}\right)^{n_{80,140}}
```

这个方法的误差可以用塔本身检查。下面假装 80 m 没有观测，用 40 m 和 140 m 插值到 80 m，再和 80 m 的观测比较。

```{code-cell} python
def interpolate(v_lo, v_hi, z_lo, z_hi, z_t):
    """在两个几何高度之间按幂律风廓线插值。"""
    n_layer = np.log(v_hi / v_lo) / np.log(z_hi / z_lo)
    return v_lo * (z_t / z_lo) ** n_layer


v80 = interpolate(speed[40.0], speed[140.0], 40, 140, 80)
v80_linear = speed[40.0] + (speed[140.0] - speed[40.0]) * (80 - 40) / (140 - 40)
for label, est in [("幂律", v80), ("线性", v80_linear)]:
    err = est - speed[80.0]
    print(f"{label}插值到 80 m：偏差 {err.mean():+.2f} m s⁻¹，均方根误差 {np.sqrt((err**2).mean()):.2f} m s⁻¹")
v100 = interpolate(speed[80.0], speed[140.0], 80, 140, 100)
print(f"15 天的平均风速：80 m {speed[80.0].mean():.2f}，100 m {v100.mean():.2f}，"
      f"140 m {speed[140.0].mean():.2f} m s⁻¹")
```

幂律插值的均方根误差是 0.35 m s⁻¹，线性插值是 0.48 m s⁻¹。幂律插值的偏差也更小。80 m 到 140 m 的间隔比 40 m 到 140 m 短，所以 100 m 的插值误差应当更小。下一节把这个 100 m 风当作观测。

## AI 天气连接

### 100 m 风和风电

现代陆上风电机组的轮毂高度常在 ［80, 140］ m 之间，海上的更高。所以风电预报最常用的变量是 100 m 风。ERA5 的变量是 `u100` 和 `v100`，长名是 `100m_u_component_of_wind` 和 `100m_v_component_of_wind`。ECMWF 开放数据的参数名是 `100u` 和 `100v`。AIFS Single 输出这两个分量，GraphCast 和 WeatherBench 2 的标准变量里没有它们。

风电机组从风中取得的功率是：

```{math}
:label: eq-t3-wind-power
P_{\mathrm{W}} = \tfrac{1}{2}\, \rho\, A\, C_p\, V^3
```

$A$ 是叶片扫过的面积，$C_p$ 是风电机组的效率，它不超过 16/27。功率和风速的三次方成正比。风速的相对误差为 $\varepsilon$ 时，功率的相对误差是 $(1 + \varepsilon)^3 - 1 \approx 3\varepsilon$。例如 8 m s⁻¹ 的风低估 1 m s⁻¹，功率低估约 33%。高估 1 m s⁻¹，功率高估约 42%。

真实的风电机组按功率曲线发电。风速低于切入风速时不发电。风速在切入风速和额定风速之间时，功率近似按三次方增大。风速超过额定风速时，功率保持额定功率。风速超过切出风速时，风电机组停机。

所以三次方的放大只出现在中等风速。英国的风电出力很大，它决定燃气电厂要补多少电，也影响电价和天然气需求。

### AIFS 和 IFS 的日变化偏差

上一节说明，100 m 风的日变化取决于稳定度。夜间的稳定层让 100 m 风变大、2 m 温度变低。这正是数值模式和 AI 天气模型难预报的地方。

下面比较 2026-04-16 到 2026-04-30 的 15 天。预报来自每天 00 UTC 起报的 AIFS Single 和 IFS，预报时效在 ［24, 45］ h 之间。AIFS Single 每 6 h 输出一次，IFS 每 3 h 输出一次。ERA5 也一起比较，因为 AIFS 用 ERA5 训练。

塔的 10 min 平均值的时间标签是时段的开始。预报是有效时间的瞬时值。所以本页把有效时间前后各 10 min 的两个平均值再平均，和预报比较。模型的值取离 Cabauw 最近的格点。风速用 earthkit-meteo 的 `wind.speed` 从两个分量计算。

```{code-cell} python
fc = d.page_data(t3.SAMPLE_FILES["ecmwf"], t3.ecmwf_point)
era_3h = d.page_data(t3.SAMPLE_FILES["era5_period"], t3.era5_period)

obs_v100 = interpolate(speed[80.0], speed[140.0], 80, 140, 100).rolling(2).mean()
obs_t2m = temp[2.0].rolling(2).mean()  # 有效时间前后各 10 min


def errors(model_df):
    """一个模型在每个有效时间的 100 m 风速和 2 m 温度，以及它们的误差。"""
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
    print(f"{name}：{len(df)} 个有效时间；100 m 风速的偏差 {df['v100_err'].mean():+.2f} m s⁻¹，"
          f"2 m 温度的偏差 {df['t2m_err'].mean():+.2f} K")
```

```{code-cell} python
#| label: fig-t3-diurnal-bias
#| caption: 2026-04-16 到 2026-04-30，Cabauw 的 100 m 风速和 2 m 温度的日变化。左列：15 天的平均值，黑线是塔的观测。右列：模型减去观测的偏差。AIFS Single 和 IFS 在每天 00 UTC 起报，预报时效在 ［24, 45］ h 之间。ERA5 每 3 h 取一个值。数据来源：KNMI Cabauw、ERA5、ECMWF 开放数据。
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

1. 三个模型在每个小时都低估 100 m 风速。15 天的平均偏差是：ERA5 −0.42 m s⁻¹，IFS −0.80 m s⁻¹，AIFS Single −0.66 m s⁻¹。
2. 低估最多的时间是 18 UTC，接近日落。这时塔的 100 m 风速增大得最快。ERA5、IFS 和 AIFS Single 分别低估 0.71、1.30 和 1.06 m s⁻¹。所以模型的 100 m 风的日变化比观测弱。
3. 2 m 温度的偏差随时间变化。IFS 在 09 UTC 到 18 UTC 偏冷 ［0.56, 0.90］ K，在 21 UTC 偏暖 0.47 K。ERA5 在傍晚偏暖，21 UTC 偏暖 0.82 K。AIFS Single 的偏差在 ［−0.46, 0.42］ K 之间，平均偏差最小。它在 18 UTC 偏暖 0.42 K，和 ERA5 相近，和 IFS 相反。
4. 样本很小。每个小时只有 15 个值，每个小时的平均偏差的标准误差在 ［0.2, 0.3］ m s⁻¹ 或 K 之间。两个模型相差不到约 0.5 m s⁻¹ 或 0.5 K 时，这 15 天的数据不能说明哪个模型更好。

全天都有的低估可能有一部分来自格点和观测点的差别。模型的值是一个格子的平均值，格子宽约 9 km 到 31 km。格子里有村庄、树木和城镇，它们的粗糙度长度比 Cabauw 的草地大。所以格子平均的风速可能比塔上的风速小。

18 UTC 的额外低估和稳定层有关。数值模式在稳定层里常常混合得太强，所以低空急流太弱，地面太暖。Sandu 等，2013 说明了 IFS 的这个问题，[doi:10.1002/jame.20013](https://doi.org/10.1002/jame.20013)。AIFS 从 ERA5 和 IFS 的分析场学习，所以它也会学到这些数据在稳定层里的偏差。本页只有一个观测点和 15 天，不能证明这个原因。

### 从风速的误差到风电出力的误差

下面用一条简化的功率曲线把 100 m 风速换成风电出力。切入风速 3 m s⁻¹，额定风速 12 m s⁻¹，切出风速 25 m s⁻¹。在切入风速和额定风速之间，出力按风速的三次方增大。容量系数是平均出力和额定功率之比。

```{code-cell} python
V_IN, V_RATED, V_OUT = 3.0, 12.0, 25.0  # m s⁻¹


def power_fraction(v):
    """简化的功率曲线：出力和额定功率之比。"""
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

# 三次方关系的手算：8 m s⁻¹ 的风低估 1 m s⁻¹，功率低估约 33%
assert abs((7 / 8) ** 3 - 1 + 0.33) < 0.01
```

用塔的 100 m 风计算，容量系数约是 19%。三个模型的容量系数都更小：ERA5 是 16.1%，AIFS Single 是 14.6%，IFS 是 12.9%。全天的风速低估 ［6.6, 12.7］%，出力低估 ［16.9, 33.3］%。出力的误差约是风速误差的 2.5 倍。它比 3 倍小，因为功率曲线在切入风速以下和额定风速以上不按三次方变化。18 UTC 到次日 03 UTC 的误差比全天的误差稍大。

英国的风电装机容量约 30 GW。假设全国的预报都像 AIFS Single 在 Cabauw 这样，把容量系数低估 4.7 个百分点。对 30 GW 来说，这是约 1.4 GW 的出力，要由燃气电厂或进口电力补上。所以英国的电网运营者和能源交易者都关心 100 m 风的预报，特别是傍晚和夜间的预报。这些时间的稳定层最难预报，三次方关系又放大风速的误差。

分析师可以对任何一个 AI 天气模型做同样的检查。第一，按一天中的小时分组计算 100 m 风速和 2 m 温度的偏差。夜间和白天的偏差常常符号相反，全天平均会掩盖它们。第二，用模型的 100 m 风和 10 m 风计算夜间的幂律指数，和塔的观测比较。$n$ 太小说明模型的夜间混合太强。

## 练习

:::{exercise}
:label: ex-t3-1

计算一节用 30 min 做 Reynolds 平均。把中午的时段分成 6 个 5 min 的小段，在每个小段里分别做平均、计算 $\overline{w'T_s'}$，再把 6 个结果平均。感热通量变大还是变小？为什么？
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

6 个小段的平均值是 0.211 K m s⁻¹，30 min 的值是 0.222 K m s⁻¹。感热通量变小了约 5%。5 min 的平均值跟着周期较长的涡旋一起变化。所以这些涡旋算进了平均值，没有算进脉动量。中午的对流涡旋很大，周期可以超过 5 min。所以涡动协方差观测站常用 30 min 的平均时段。
:::

:::{exercise}
:label: ex-t3-2

风电场常常只有 10 m 风的观测。用 $n = 1/7$ 从 Cabauw 的 10 m 风推算 100 m 风，再和 [](#eq-t3-v100) 的 100 m 风比较。白天和夜间的误差各是多少？换算成风电出力的误差是多少？
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

夜间指 20 UTC 到次日 04 UTC。用 $n = 1/7$ 推算的 100 m 风速平均是 3.7 m s⁻¹，塔插值的值是 6.9 m s⁻¹。风速低估 45%，出力低估 83%。夜间的 $n$ 约是 0.4，比 1/7 大得多，所以 1/7 低估了夜间的 100 m 风。

白天指 04 UTC 到 20 UTC。风速低估 10%，出力低估 24%。08 UTC 到 14 UTC 的 $n$ 小于 1/7，早晨和傍晚的 $n$ 大于 1/7，两部分的误差大部分相互抵消。出力的误差总是比风速的误差大很多，因为三次方关系放大了它。
:::

:::{exercise}
:label: ex-t3-3

METEO 300 的 11.8 节给出混合层的增温率 $\partial\overline{\theta}/\partial t \approx \overline{w'\theta'}_0 / h$，$h$ 是混合层的厚度。2026-04-21 09 UTC 到 13 UTC，Cabauw 的感热通量平均约 115 W m⁻²。同一时段，ERA5 的边界层高度从约 600 m 增大到约 1130 m，11 UTC 是 790 m。估计混合层每小时增温多少，再和 [](#fig-t3-tower) 里 200 m 的位温比较。
:::

:::{solution} ex-t3-3
:class: dropdown

运动学感热通量是 $\overline{w'\theta'}_0 = H/(\rho c_p) \approx 115 / (1.25 \times 1005) \approx 0.092\ \mathrm{K\,m\,s^{-1}}$。取 $h = 790$ m，增温率约是 $0.092 / 790 \times 3600 \approx 0.42\ \mathrm{K\,h^{-1}}$。$h$ 取 600 m 和 1130 m 时，增温率在 ［0.29, 0.55］ K h⁻¹ 之间。

塔的数据说明，200 m 的位温从 09 UTC 到 13 UTC 由 280.2 K 升到 284.3 K，约 1.0 K h⁻¹。2 m 到 200 m 的各层增温得差不多。所以混合层实际的增温率是估计值的 2 倍多。

可能的原因有三个。第一，公式忽略了混合层顶的通量。混合层增厚时，夹卷把上面较暖的空气带进混合层。第二，涡动协方差观测的感热通量常常偏小，地面能量平衡常常不闭合。第三，暖平流也能让空气增温。本页的数据不能区分这三个原因。
:::

:::{exercise}
:label: ex-t3-4

本页说低空急流约在日落后半个惯性周期达到最大。计算 Cabauw 的惯性周期。2026-04-21 的日落约在 18:50 UTC。急流应该在什么时间最强？和 [](#fig-t3-tower) 比较。
:::

:::{solution} ex-t3-4
:class: dropdown

$f = 2\Omega\sin\varphi = 2 \times 7.292 \times 10^{-5} \times \sin 51.97° \approx 1.149 \times 10^{-4}\ \mathrm{s^{-1}}$。惯性周期是 $2\pi/f \approx 15.2$ h，半个周期约是 7.6 h。从 18:50 UTC 起算，急流应该在约 02:25 UTC 最强。

塔的数据说明，200 m 的风速在 01:00 到 01:30 UTC 最大，约 12.4 m s⁻¹。140 m 和 80 m 的风速在约 02:00 UTC 最大。观测的最大值比估计早约 1 h。

地面的感热通量在约 16:30 UTC 已经变负，比日落早约 2 h 20 min。从 16:30 UTC 起算，估计的时间是约 00:05 UTC。观测的时间在两个估计之间。所以起算的时间应该是湍流变弱的时间，它不一定是日落的时间。
:::
