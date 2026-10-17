---
title: 气压与静力平衡
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 2 课 2.1 节和 2.2 节。

某一点的气压等于这一点上方空气柱的重量除以空气柱的底面积。向上走，上方的空气变少，所以气压降低。地面气压约 1000 hPa。这表示每平方米地面的上方约有 10 t 空气。

空气近似是理想气体。干空气的理想气体定律把气压、密度和温度联系起来：

```{math}
:label: eq-ch03-ideal-gas
p = \rho R_d T
```

式中 $R_d = 287\ \mathrm{J\,kg^{-1}\,K^{-1}}$ 是干空气气体常数。气压的单位是 Pa，温度的单位是 K。同一气压下，温度越高，密度越小。

湿空气含有水汽。水分子比干空气分子轻，所以同温同压下湿空气比干空气轻。虚温 $T_v$ 把这个差别折算成温度：

```{math}
:label: eq-ch03-virtual-temperature
T_v = T\,(1 + 0.61\,q)
```

式中 $q$ 是比湿，单位 kg kg⁻¹。湿空气满足 $p = \rho R_d T_v$。温度为 290 K、比湿为 10 g kg⁻¹ 时，虚温比温度高 1.8 K。

一块空气受三个垂直方向的力。下方的气压向上推它，上方的气压向下推它，重力向下拉它。三个力平衡时，空气处于静力平衡。静力方程是：

```{math}
:label: eq-ch03-hydrostatic
\frac{dp}{dz} = -\rho g
```

气压随几何高度降低，降低的速率等于密度乘重力加速度。地面附近的密度约 1.2 kg m⁻³，所以向上 8.5 m，气压降低 1 hPa。

大尺度的大气很接近静力平衡。在这些运动里，垂直加速度比重力加速度小几个数量级。强对流里的垂直加速度大，静力平衡只近似成立。

把理想气体定律代入静力方程，消去密度：

$$
\frac{dp}{p} = -\frac{g}{R_d T_v}\, dz
$$

气象数据用位势高度 $Z$ 代替几何高度 $z$。两者的关系是 $g_0\,dZ = g\,dz$。式中 $g_0 = 9.80665\ \mathrm{m\,s^{-2}}$ 是标准重力加速度。在对流层里，位势高度和几何高度相差约 0.1%。从等压面 $p_1$ 积分到等压面 $p_2$，结果是压高公式：

```{math}
:label: eq-ch03-hypsometric
Z_2 - Z_1 = \frac{R_d \overline{T_v}}{g_0} \ln\frac{p_1}{p_2}
```

式中 $\overline{T_v}$ 是这一层对 $\ln p$ 平均的虚温。两个等压面之间的厚度正比于层内的平均虚温。暖的空气柱厚，冷的空气柱薄。

如果虚温不随位势高度变化，压高公式就成为指数函数：

```{math}
:label: eq-ch03-scale-height
p = p_0\, e^{-Z/H}, \qquad H = \frac{R_d \overline{T_v}}{g_0}
```

式中 $H$ 是标高。平均虚温为 250 K 时，标高是 7.3 km。每向上一个标高，气压降为原来的 37%。所以 $\ln p$ 和 $Z$ 近似成直线关系。气压随位势高度单调降低，所以气压可以代替位势高度做垂直坐标。

地面气压是地面上的气压。它主要取决于地形高度：地形越高，地面气压越低。海平面气压是从地面气压换算到海平面的气压。换算时，算法在地面以下假设一段空气柱，再用压高公式。所以海平面气压图去掉了地形，只留下天气系统。

1976 年美国标准大气是一条约定的平均廓线。它的海平面气压是 1013.25 hPa，海平面温度是 15 °C。在对流层里，它的温度每升高 1 km 降低 6.5 K。位势高度在 ［11, 20］ km 时，它的温度保持 216.65 K。一次探空和标准大气在同一等压面上的位势高度差，来自两部分。一部分来自地面气压的差，另一部分来自空气柱温度的差。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 气压 | pressure | $p$ |
| 地面气压 | surface pressure | $p_s$ |
| 海平面气压 | mean sea level pressure | $p_{\mathrm{msl}}$ |
| 低压中心 | low centre | — |
| 密度 | density | $\rho$ |
| 理想气体定律 | ideal gas law | — |
| 干空气气体常数 | gas constant for dry air | $R_d$ |
| 虚温 | virtual temperature | $T_v$ |
| 比湿 | specific humidity | $q$ |
| 混合比 | mixing ratio | $r$ |
| 温度露点差 | dewpoint depression | $T - T_d$ |
| 静力平衡 | hydrostatic balance | — |
| 静力方程 | hydrostatic equation | — |
| 几何高度 | geometric height | $z$ |
| 位势 | geopotential | $\Phi$ |
| 位势高度 | geopotential height | $Z$ |
| 标准重力加速度 | standard gravity | $g_0$ |
| 厚度 | thickness | $\Delta Z$ |
| 压高公式 | hypsometric equation | — |
| 标高 | scale height | $H$ |
| 标准大气 | standard atmosphere | — |
| 等压面 | isobaric surface; pressure level | — |
| 标准等压面 | mandatory pressure level | — |
| 探空 | sounding | — |
| 探空仪 | radiosonde | — |
| 对流层顶 | tropopause | — |

## 真实数据

本页的个例是风暴 Éowyn。2025-01-24，这个温带气旋袭击了爱尔兰和英国。ERA5 里，它的中心海平面气压在 18 h 内降低了 39 hPa。这样快的加深叫爆发性气旋。2025-01-24 00 UTC，它的中心在爱尔兰以西，中心海平面气压是 941.7 hPa。

Camborne 观测站在英格兰西南端的康沃尔。它在低压中心的东南偏东方向，相距约 700 km。观测站每天施放两次探空仪。下面是 2025-01-24 00 UTC 的探空。探空仪的升空时间是 2025-01-23 23:17 UTC。

下面的代码读取本页的全部数据。联网时，函数从 IGRA2、ERA5 和 ECMWF 开放数据下载数据。离线时，`d.page_data` 读取 `data/samples/` 里的样本。

```{code-cell} python
from meteo300 import data as d
from meteo300.pages import ch03

snd = d.page_data(ch03.SAMPLES["sounding"], ch03.camborne_sounding)
sfc = d.page_data(ch03.SAMPLES["era5_surface"], ch03.era5_surface)
era5pl = d.page_data(ch03.SAMPLES["era5_levels"], ch03.era5_levels)
aifs = d.page_data(ch03.SAMPLES["aifs_levels"], ch03.aifs_levels)

# 最低一层是地面。IGRA2 不报告它的位势高度，所以用观测站的几何高度 87 m。
snd.loc[0, "height"] = ch03.CAMBORNE["elevation_m"]
levels = snd.dropna(subset=["height"])  # 地面和标准等压面
snd.head()
```

```{code-cell} python
#| label: fig-ch03-sounding
#| caption: 2025-01-24 00 UTC，Camborne 观测站的探空。左图是标准等压面上的气压和位势高度，灰线是 1976 年美国标准大气。右图是温度廓线。数据来源：IGRA2。
fig = ch03.plot_sounding(snd.dropna(subset=["temperature"]), levels)
```

左图显示气压随位势高度迅速降低。位势高度 20.2 km 处的气压是 50 hPa，只有地面气压的 5%。探空的点几乎落在标准大气的曲线上，但是每一点都比曲线低。右图显示温度从地面向上降低，到 200 hPa 停止降低。200 hPa 是这次探空的对流层顶，它的位势高度是 11.6 km。

探空的位势高度只在标准等压面上有值。其他层只有温度和温度露点差。计算一节用压高公式算出这些层的位势高度。

同一时刻，ERA5 有地面气压和海平面气压两个场。[](#fig-ch03-sp-msl) 用同一个色标画出两个场。

```{code-cell} python
#| label: fig-ch03-sp-msl
#| caption: 2025-01-24 00 UTC，北大西洋东部和欧洲的地面气压与海平面气压。左图是地面气压，右图是海平面气压，白线是间隔 8 hPa 的等压线，星号是 Camborne。数据来源：ERA5。
fig = ch03.plot_sp_msl(sfc)
```

左图的地面气压主要显示地形。阿尔卑斯山上的地面气压低到 753 hPa，冰岛和挪威的山地也低于 830 hPa。右图的海平面气压去掉了地形，只留下风暴。等压线围绕爱尔兰以西的低压中心。在海上，两张图几乎相同，因为海面的地形高度是 0 m。

## 数据集

探空用 IGRA2。IGRA2 是 NOAA NCEI 的全球探空数据集。它收集 2800 多个观测站的探空，最早的记录始于 1905 年。每个观测站有一个文本文件，软件包 siphon 可以读取它。

IGRA2 的论文是 Durre 等，2018，[`doi:10.1175/JTECH-D-17-0223.1`](https://doi.org/10.1175/JTECH-D-17-0223.1)。数据集的 DOI 是 [`10.7289/V5X63K0Q`](https://doi.org/10.7289/V5X63K0Q)。IGRA2 是美国政府的数据，使用没有限制。

地图用 ERA5 再分析。ERA5 是 ECMWF 制作的再分析数据集。它给出 1940 年以来每小时的全球大气状态，网格间距是 0.25°。本页读取 ARCO-ERA5 的 `surface_pressure` 和 `mean_sea_level_pressure`，它们的 ERA5 短名是 `sp` 和 `msl`。

AI 天气连接一节还读取 37 个等压面上的 `z`、`t` 和 `q`。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。从 2025-07-02 起，ERA5 以 CC BY 4.0 许可发布。

AI 预报用 ECMWF 开放数据里的 AIFS。AIFS 是 ECMWF 的 AI 天气模型，网格间距是 0.25°。本页读取 2025-01-22 00 UTC 起报的预报，预报时效是 48 h。这次预报早于 2025-02-25，那时 AIFS 还是试验版本。AIFS 的论文是 Lang 等，2024，[`arXiv:2406.01465`](https://arxiv.org/abs/2406.01465)。ECMWF 开放数据以 CC BY 4.0 许可发布。

标准大气用 1976 年美国标准大气。它由 NOAA、NASA 和美国空军在 1976 年发布。MetPy 的函数 `pressure_to_height_std` 和 `add_height_to_pressure` 用它的对流层部分。

两个备选数据集：怀俄明大学的探空网站提供同样的探空，siphon 也能读取。ERA5 的等压面数据提供每个格点的廓线，可以代替探空。完整的数据集条目见 [数据集参考页](../reference/datasets.md)。

## 计算

### 地面的密度

MetPy 的函数 `density` 用气压、温度和混合比算出密度。露点温度下的饱和水汽压等于实际的水汽压，所以混合比可以从露点温度算出。探空最低一层的气压是 983 hPa，温度是 10.8 °C，温度露点差是 0.8 K。手算用式 [](#eq-ch03-virtual-temperature) 和 $R_d = 287\ \mathrm{J\,kg^{-1}\,K^{-1}}$。

```{code-cell} python
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
from metpy.constants import Rd
from metpy.constants import g as g0
from metpy.units import units

low = snd.iloc[0]
p_sfc = low["pressure"] * units.hPa
t_sfc = low["temperature"] * units.degC
td_sfc = low["dewpoint"] * units.degC

r_sfc = mpcalc.mixing_ratio(mpcalc.saturation_vapor_pressure(td_sfc), p_sfc)
rho_sfc = mpcalc.density(p_sfc, t_sfc, r_sfc)

# 手算：q = r / (1 + r)，T_v = T (1 + 0.61 q)，rho = p / (R_d T_v)
q = r_sfc.m_as("kg/kg") / (1 + r_sfc.m_as("kg/kg"))
tv_hand = (low["temperature"] + 273.15) * (1 + 0.61 * q)
rho_hand = low["pressure"] * 100 / (287 * tv_hand)
assert abs(rho_sfc.m_as("kg/m^3") - rho_hand) < 0.002, (rho_sfc, rho_hand)
print(f"混合比 {r_sfc.m_as('g/kg'):.2f} g/kg，虚温 {tv_hand:.2f} K")
print(f"MetPy: {rho_sfc.m_as('kg/m^3'):.3f} kg/m3，手算: {rho_hand:.3f} kg/m3")
```

两个结果都是 1.200 kg m⁻³。虚温比温度高 1.4 K，所以湿空气的密度比同温同压的干空气小 0.5%。

### 用压高公式积分出位势高度

探空只在标准等压面上报告位势高度。下面的代码从观测站的几何高度 87 m 出发，逐层使用式 [](#eq-ch03-hypsometric)。每一层的平均虚温取上下两层虚温的平均值。代码同时用温度代替虚温再积分一次，看看水汽的作用。

```{code-cell} python
prof = snd.dropna(subset=["temperature", "dewpoint"]).reset_index(drop=True)
p = prof["pressure"].to_numpy() * units.hPa
t = prof["temperature"].to_numpy() * units.degC
r = mpcalc.mixing_ratio(mpcalc.saturation_vapor_pressure(prof["dewpoint"].to_numpy() * units.degC), p)
prof["Tv"] = mpcalc.virtual_temperature(t, r).m_as("K")

z_station = 87.0 * units.m
lnp = np.log(p.m_as("hPa"))


def integrate(tv):
    """Integrate the hypsometric equation upward from the station."""
    dz = (Rd / g0 * 0.5 * (tv[1:] + tv[:-1]) * (lnp[:-1] - lnp[1:])).to("m")
    return z_station.m + np.concatenate([[0.0], np.cumsum(dz.m)])


prof["Z_calc"] = integrate(prof["Tv"].to_numpy() * units.K)
prof["Z_dry"] = integrate(t.to("K"))
```

```{code-cell} python
mand = prof.dropna(subset=["height"]).iloc[1:]  # 标准等压面，不含最低一层
check = pd.DataFrame({
    "p (hPa)": mand["pressure"],
    "Z_obs (m)": mand["height"],
    "Z_calc - Z_obs (m)": (mand["Z_calc"] - mand["height"]).round(1),
    "Z_dry - Z_obs (m)": (mand["Z_dry"] - mand["height"]).round(1),
}).set_index("p (hPa)")
assert check["Z_calc - Z_obs (m)"].abs().max() < 10
check
```

积分的位势高度和探空报告的位势高度相差不到 6 m。只用温度时，误差增大到 21 m，而且都是负值。干空气比湿空气重，所以只用温度算出的厚度偏小。

MetPy 的函数 `thickness_hydrostatic` 做同样的积分。下面用它算出 ［500, 850］ hPa 层的厚度，再和探空比较。

```{code-cell} python
dz_metpy = mpcalc.thickness_hydrostatic(p, t, mixing_ratio=r,
                                        bottom=850 * units.hPa, depth=350 * units.hPa)
z_obs = mand.set_index("pressure")["height"]
dz_obs = z_obs[500] - z_obs[850]
assert abs(dz_metpy.m_as("m") - dz_obs) < 5
print(f"MetPy: {dz_metpy.m_as('m'):.1f} m，探空: {dz_obs:.0f} m")
```

### 和标准大气比较

MetPy 的函数 `pressure_to_height_std` 把气压换算成标准大气中的位势高度。它只用对流层的公式，海平面温度取 288 K。所以它在 11 km 以上偏离 1976 年美国标准大气。本页的函数 `ch03.std_atmosphere_height` 包含 ［0, 32］ km 的三层。手算核对 500 hPa：对流层公式是 $Z = \frac{T_0}{\Gamma}\left[1 - (p/p_0)^{R_d \Gamma / g_0}\right]$。

```{code-cell} python
p_m = mand["pressure"].to_numpy()
std = pd.DataFrame({
    "p (hPa)": p_m,
    "Z_obs (m)": mand["height"].to_numpy(),
    "Z_std (m)": ch03.std_atmosphere_height(p_m).round(0),
    "MetPy (m)": mpcalc.pressure_to_height_std(p_m * units.hPa).m_as("m").round(0),
}).set_index("p (hPa)")
std["Z_obs - Z_std (m)"] = std["Z_obs (m)"] - std["Z_std (m)"]

# 手算：T0 = 288.15 K，Gamma = 0.0065 K/m，p0 = 1013.25 hPa，R = 287.053 J/(kg K)
z500_hand = 288.15 / 0.0065 * (1 - (500 / 1013.25) ** (287.053 * 0.0065 / 9.80665))
assert abs(std.loc[500, "Z_std (m)"] - z500_hand) < 1
std
```

探空的位势高度在每个标准等压面上都比标准大气低。在 925 hPa 和 850 hPa，差约 170 m。原因是这天的地面气压低。换算到海平面，地面气压比 1013.25 hPa 低约 20 hPa，相当于约 170 m。从 700 hPa 到 300 hPa，差从 175 m 缩小到 114 m，所以这一层的空气柱比标准大气暖。300 hPa 以上，差又增大，因为这里的空气比标准大气冷。

在 100 hPa，MetPy 的结果比 1976 年美国标准大气低 391 m。所以 11 km 以上要用三层的公式。

### 把地面气压换算到海平面

MetPy 的函数 `add_height_to_pressure` 在标准大气中把一个气压移动一段位势高度。把 983 hPa 向下移动 87 m，结果是海平面气压的估计值。手算用静力方程 $\Delta p = \rho g_0 \Delta z$ 和上面算出的地面密度。

```{code-cell} python
p_sea = mpcalc.add_height_to_pressure(p_sfc, -z_station)
dp_hand = (rho_sfc * g0 * z_station).to("hPa")
assert abs((p_sea - p_sfc).m_as("hPa") - dp_hand.m) < 0.2
print(f"MetPy: {p_sea.m_as('hPa'):.1f} hPa，手算: {(p_sfc + dp_hand).m_as('hPa'):.1f} hPa")

# ERA5 在 Camborne 最近格点上的海平面气压，线性插值到探空仪升空的 23:17 UTC
msl_point = sfc["msl_point"].to_series()
msl_launch = np.interp(17 / 60, [0, 1], msl_point.loc["2025-01-23 23:00":"2025-01-24 00:00"])
print(f"ERA5: {msl_launch:.1f} hPa")
```

两个结果都是 993.2 hPa。ERA5 在 23 UTC 和 00 UTC 的海平面气压是 994.2 hPa 和 991.7 hPa。这时风暴正在接近，气压每小时降低约 2.5 hPa。插值到 23:17 UTC，ERA5 的海平面气压是 993.5 hPa，和换算的结果只差 0.3 hPa。

### 拟合标高

式 [](#eq-ch03-scale-height) 说明，$\ln p$ 和 $Z$ 成直线关系，斜率是 $-1/H$。下面的代码用标准等压面上报告的位势高度分别拟合对流层和平流层。对流层取 ［200, 983］ hPa，平流层取 ［50, 200］ hPa。手算用层内对 $\ln p$ 平均的虚温和 $H = R_d \overline{T_v} / g_0$。

```{code-cell} python
fits = {}
for name, p_bottom, p_top in [("对流层", 983, 200), ("平流层", 200, 50)]:
    sel = levels[levels["pressure"].between(p_top, p_bottom)]
    slope, intercept = np.polyfit(sel["height"], np.log(sel["pressure"]), 1)
    h_fit = -1 / slope
    layer = prof[prof["pressure"].between(p_top, p_bottom)]
    tv_mean = ch03.mean_tv_over_lnp(layer["pressure"], layer["Tv"]) * units.K
    h_hand = (Rd * tv_mean / g0).m_as("m")
    assert abs(h_fit / h_hand - 1) < 0.02, (name, h_fit, h_hand)
    fits[name] = (p_bottom, p_top, h_fit, np.exp(intercept))
    print(f"{name}：拟合 H = {h_fit / 1000:.2f} km，"
          f"平均虚温 {tv_mean.m:.1f} K 给 H = {h_hand / 1000:.2f} km")
```

```{code-cell} python
#| label: fig-ch03-scale-height
#| caption: 2025-01-24 00 UTC，Camborne 探空的气压和位势高度。蓝点是报告的位势高度，灰点是积分的位势高度，两条直线是对流层和平流层的拟合。数据来源：IGRA2。
fig = ch03.plot_scale_height(prof, levels, fits)
```

对流层的标高是 7.33 km，平流层的标高是 6.21 km。平流层的空气更冷，所以标高更小。拟合的标高和平均虚温算出的标高很接近。对流层相差约 1%，平流层相差不到 0.5%。对流层里虚温随位势高度降低，所以 $\ln p$ 和 $Z$ 的关系略有弯曲，直线只能近似它。

## AI 天气连接

AI 天气模型在等压面上预报。Pangu-Weather、FuXi 和 AIFS 都用同样的 13 个等压面。GraphCast 有 37 层和 13 层两个版本。WeatherBench 2 也在这 13 个等压面上评估模型。13 个等压面的气压分别是 50、100、150、200、250、300、400、500、600、700、850、925 和 1000 hPa。

每个等压面上，模型输出位势 `z`、温度 `t` 和比湿 `q`。WeatherBench 2 把它们叫作 `geopotential`、`temperature` 和 `specific_humidity`。`z` 是位势，单位 m² s⁻²。位势除以 $g_0$ 才是位势高度。

数值模式从温度积分出位势，所以它的输出满足压高公式。AI 天气模型把每个等压面上的 `z` 和 `t` 当作独立的输出通道。网络里没有约束让它们满足压高公式。所以分析师可以用压高公式检查 AI 预报的物理一致性。

检查的方法是这样的。对相邻的两个等压面，用 `t` 和 `q` 算出平均虚温，再用压高公式算出厚度。模型 `z` 给的厚度减去这个厚度，结果是静力残差。函数 `ch03.hydrostatic_residual` 对每个格点和每一层做这个计算。

下面比较三组数据的静力残差。第一组是 13 个等压面上的 ERA5。第二组是 AIFS 的预报，起报时间是 2025-01-22 00 UTC，预报时效是 48 h。第三组是 37 个等压面上的 ERA5，它的细层残差合并到同样的 13 层里。三组数据的有效时间都是 2025-01-24 00 UTC，网格间距都是 1°。

```{code-cell} python
resid = {
    "ERA5，13 层": ch03.hydrostatic_residual(era5pl.sel(level=list(ch03.LEVELS_13))),
    "AIFS 预报，13 层": ch03.hydrostatic_residual(aifs),
    "ERA5，37 层": ch03.regroup_residual(ch03.hydrostatic_residual(era5pl)),
}
table = ch03.residual_table(resid, era5pl["sp"])  # 去掉在地面以下的层
table
```

```{code-cell} python
#| label: fig-ch03-residual
#| caption: 2025-01-24 00 UTC，北大西洋东部和欧洲各层静力残差的均方根。AIFS 的起报时间是 2025-01-22 00 UTC。数据来源：ERA5，ECMWF 开放数据。
fig = ch03.plot_residual(table)
```

ERA5 来自数值模式，所以它的 `z` 和 `t` 满足静力平衡。它在 13 个等压面上的残差来自离散化：层内的虚温不是 $\ln p$ 的线性函数。37 个等压面的层更薄。在 300 hPa 以下，37 层的残差只有 13 层的 ［9, 25］ %。所以 13 层 ERA5 的残差是这个检查的基线。

AIFS 的静力残差和 13 层 ERA5 的残差一样小。所以这次 AIFS 预报的 `z` 和 `t` 互相一致，不一致的程度在离散化误差以内。下面的代码说明，同一个预报在 500 hPa 的位势高度和 ERA5 相差约 18 m。一个预报可以有预报误差，同时保持静力平衡。

```{code-cell} python
err_z500 = np.sqrt(((aifs["z"] - era5pl["z"]).sel(level=500) ** 2).mean()) / g0.m
assert 5 < float(err_z500) < 50
print(f"AIFS 和 ERA5 的 500 hPa 位势高度之差，均方根 {float(err_z500):.1f} m")
```

分析师可以对每次 AI 预报做这个检查。先算出 ERA5 的残差，作为基线。某一层的残差远大于基线时，这一层的 `z` 和 `t` 至少有一个不可信。WeatherBench 2 的指标比较预报和 ERA5。这些指标不检查同一个预报里的 `z` 和 `t` 是否一致。

## 练习

:::{exercise}
:label: ex-ch03-1

在地面附近，密度约 1.2 kg m⁻³。在 500 hPa，温度约 253 K。在这两个地方，气压降低 1 hPa 各要向上多少米？
:::

:::{solution} ex-ch03-1
:class: dropdown

用静力方程，$\Delta z = \Delta p / (\rho g)$。地面附近，$\Delta z = 100 / (1.2 \times 9.81) = 8.5\ \mathrm{m}$。500 hPa 的密度是 $50000 / (287 \times 253) = 0.69\ \mathrm{kg\,m^{-3}}$，所以 $\Delta z = 14.8\ \mathrm{m}$。空气越稀薄，气压随位势高度降低得越慢。
:::

:::{exercise}
:label: ex-ch03-2

改动拟合标高的代码，增加一层 ［500, 983］ hPa。这一层的标高比整个对流层的标高大还是小？为什么？
:::

:::{solution} ex-ch03-2
:class: dropdown

在 `for` 循环的列表里加上 `("对流层低层", 983, 500)`。这一层的标高约 7.90 km，平均虚温约 270 K。整个对流层的标高是 7.33 km。低层的空气更暖，所以标高更大。
:::

:::{exercise}
:label: ex-ch03-3

改动 AI 天气连接一节的代码，把 AIFS 预报的温度在每个等压面上都加 1 K，再算静力残差。哪一层的残差增大最多？用压高公式解释。
:::

:::{solution} ex-ch03-3
:class: dropdown

在计算残差以前加一行 `aifs_warm = aifs.assign(t=aifs["t"] + 1)`，再用 `aifs_warm` 算残差。压高公式给的厚度增大 $R_d / g_0 \times 1\ \mathrm{K} \times \ln(p_1 / p_2)$。这个值和 $\ln(p_1 / p_2)$ 成正比，所以 ［50, 100］ hPa 层增大最多。这一层的 $\ln 2 = 0.69$，厚度增大 20.3 m，残差的均方根从约 12 m 增大到约 26 m。［925, 1000］ hPa 层只增大 2.3 m。
:::

:::{exercise}
:label: ex-ch03-4

一个 AI 天气模型预报的 500 hPa 位势高度正确。但是它把 ［500, 1000］ hPa 这一层的平均虚温高估了 2 K。这一层的厚度和这个温度不一致。不一致的程度是多少米？用 ERA5 的基线判断，分析师能不能发现它？
:::

:::{solution} ex-ch03-4
:class: dropdown

用式 [](#eq-ch03-hypsometric)，厚度的变化是 $R_d / g_0 \times 2\ \mathrm{K} \times \ln 2 = 29.3 \times 2 \times 0.693 = 40.6\ \mathrm{m}$。所以静力残差约为 41 m。13 层 ERA5 在 ［500, 1000］ hPa 的五层里，每层残差的均方根不到 4 m。所以分析师能发现它。
:::
