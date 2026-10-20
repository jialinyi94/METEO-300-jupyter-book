---
title: weather station 与 surface observation
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 1 课 1.2 节和 1.3 节，以及第 8 课 8.2 节、8.3 节和 8.4 节。

weather station 在一个固定地点测量 surface 的大气状态。机场的 weather station 每小时或每 30 分钟发一条 METAR report，英国的机场每 30 分钟发一条。一条 METAR report 有 wind direction、wind speed、visibility、云、temperature、dewpoint temperature 和 QNH。wind gust 比平均 wind speed 大 10 kt 以上时，报文还有 wind gust。这些规则见 WMO 的 [METAR 用户手册](https://wmo.int/media/news/aviation-news-2025-08-28-wmo-publishes-update-wmo-no-782-aerodrome-reports-and-forecasts-users) WMO-No. 782。

本页用一个机场一天的报文和一个时刻的许多 weather station，练习三件事：换算单位、读懂 wind direction、估计量级。

### 单位和量级

英国和爱尔兰的机场用 kt 报 wind speed，用 °C 报 temperature，用 hPa 报 QNH。有的国家用 m s⁻¹ 报 wind speed。美国的机场和美军基地用英寸汞柱报 QNH，这个报文组以 A 开头。物理计算用国际单位制：wind speed 用 m s⁻¹，temperature 用 K，pressure 用 Pa。1 kt 是每小时 1 海里，1 海里正好是 1852 m。

$$
1\ \mathrm{kt} = \frac{1852\ \mathrm{m}}{3600\ \mathrm{s}} \approx 0.514\ \mathrm{m\,s^{-1}},
\qquad
1\ \mathrm{mph} = \frac{1609.344\ \mathrm{m}}{3600\ \mathrm{s}} \approx 0.447\ \mathrm{m\,s^{-1}}
$$

kt 和英里每小时是两个不同的单位。把一个以 kt 为单位的数当成英里每小时来换算，结果会小 13%。METEO 300 第 1 课 1.2 节给出 kt 和英里的这两个定义。

量级估计用一条简单的规则：以 m s⁻¹ 为单位的 wind speed 约等于以 kt 为单位的 wind speed 的一半。10 m wind 的典型 wind speed 约为 5 m s⁻¹，也就是 10 kt。500 hPa 和 250 hPa 的典型 wind speed 分别约为 25 m s⁻¹ 和 50 m s⁻¹。这三个典型 wind speed 取自 METEO 300 第 1 课 1.2 节。一个 wind speed 结果比这些量级大 10 倍或小 10 倍，计算多半有错。

significant figures 跟着观测的精度走。METAR 的 wind speed 精确到 1 kt，wind direction 精确到 10°。所以 51 kt 换算后写成 26 m s⁻¹，不写 26.2367 m s⁻¹。

### wind 矢量和三种角

wind 是向量。local Cartesian coordinate system 的 $x$ 轴指向东，$y$ 轴指向北，$z$ 轴指向上。horizontal wind 有两个分量：zonal wind $u$ 和 meridional wind $v$。$u > 0$ 表示 wind 吹向东，$v > 0$ 表示 wind 吹向北。wind speed 是这个向量的长度：

$$
V = \sqrt{u^2 + v^2}
$$

描述 wind 的方向有三种角，读者必须分清：

| 角 | 符号 | 零度方向 | 旋转方向 | 角指向哪里 |
|---|---|---|---|---|
| wind direction | $\chi$ | 北 | 顺时针 | wind 的来向 |
| bearing of travel | — | 北 | 顺时针 | wind 的去向 |
| math angle | $\gamma$ | 东 | 逆时针 | wind 的去向 |

气象上说“wind direction 240°”，意思是 wind 从 240° 吹来。METAR、station plot 和天气 forecast 都用 wind direction。numerical weather prediction model 和 AI weather model 存储 $u$ 和 $v$，它们描述 wind 的去向。wind direction 和两个分量的关系是：

$$
u = -V \sin\chi, \qquad v = -V \cos\chi
$$

式中的负号来自“来向”。wind 从西边吹来，wind direction 是 270°，wind 吹向东，所以 $u > 0$。math angle 和 wind direction 的关系是：

$$
\gamma = 270^\circ - \chi
$$

$\gamma$ 小于 0° 时，加 360°。bearing of travel 等于 wind direction 加 180°，超过 360° 时减 360°。METAR 用 360° 表示北风。wind speed 小于 1 kt 时，METAR 报静风 00000KT。MetPy 也把北风的 wind direction 算成 360°，把静风的 wind direction 算成 0°。

METEO 300 把 wind direction 写作 $\delta$，把 math angle 写作 $\alpha$。本书的 $\delta$ 表示 divergence，$\alpha$ 表示 albedo，所以本页改用 $\chi$ 和 $\gamma$。

### 球面上的距离

latitude 差 1° 对应约 111 km 的距离。longitude 差 1° 对应的距离是 $111\ \mathrm{km} \times \cos\varphi$，$\varphi$ 是 latitude。格拉斯哥在 55.9°N，那里的 longitude 差 1° 只对应约 62 km。两个 weather station 之间的 great-circle distance 用球面余弦定理计算：

$$
\xi = \arccos\left(\sin\varphi_1 \sin\varphi_2 + \cos\varphi_1 \cos\varphi_2 \cos\Delta\lambda\right),
\qquad d = R_\mathrm{E}\,\xi
$$

$\lambda$ 是 longitude，$\xi$ 是两点的 central angle，单位是弧度。central angle 是两点与地心的两条连线之间的夹角。Earth radius $R_\mathrm{E}$ 取 6371 km。

### 时间序列的导数

第 1 课 1.3 节复习导数。weather station 的 pressure 时间序列给导数一个真实的例子。英国的 METAR 每 30 分钟报一次 QNH，所以 pressure tendency 可以用差分估计：

$$
\frac{\partial p}{\partial t} \approx \frac{\Delta p}{\Delta t}
$$

单位要写清楚。$-3\ \mathrm{hPa\,h^{-1}}$ 等于 $-300\ \mathrm{Pa} / 3600\ \mathrm{s} \approx -0.083\ \mathrm{Pa\,s^{-1}}$。

### station plot

station plot 把一个 weather station 的多个量画在一个小圆圈周围。圆圈里的填充表示 cloud cover，单位是 okta，1 okta 是天空的八分之一。wind barb 的杆从圆圈伸向 wind 的来向。短羽表示 5 kt，长羽表示 10 kt，三角旗表示 50 kt。圆圈左上方是 temperature，左下方是 dewpoint temperature，右上方是 mean sea level pressure 的三位码。这套画法见 NOAA WPC 的 [station plot 说明](https://www.wpc.ncep.noaa.gov/html/stationplot.shtml)。

三位码取 mean sea level pressure 的十分之一 hPa 的最后三位。963.3 hPa 写成 633，1004.1 hPa 写成 041。解码时先除以 10。结果大于或等于 50 时加 900 hPa，小于 50 时加 1000 hPa。这条规则假定 mean sea level pressure 在 ［950, 1050］ hPa 之内。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| weather station | 观测站 | — |
| surface observation | 地面观测 | — |
| METAR report | METAR 报文 | — |
| QNH | 修正海平面气压 | — |
| mean sea level pressure | 海平面气压 | $p_{\mathrm{msl}}$ |
| low centre | 低压中心 | — |
| visibility | 能见度 | — |
| knot | 海里每小时 | kt |
| wind speed | 风速 | $V$ |
| wind direction | 风向 | $\chi$ |
| bearing of travel | 去向方位角 | — |
| math angle | 数学角 | $\gamma$ |
| zonal wind | 纬向风 | $u$ |
| meridional wind | 经向风 | $v$ |
| 10 m wind | 10 m 风 | $u_{10}$, $v_{10}$ |
| wind gust | 阵风 | — |
| cloud cover | 云量 | — |
| wind barb | 风羽 | — |
| station plot | 观测站填图 | — |
| local Cartesian coordinate system | 局地直角坐标系 | $x$, $y$, $z$ |
| Lambert conformal conic projection | Lambert 投影 | — |
| great-circle distance | 大圆距离 | $d$ |
| central angle | 地心夹角 | $\xi$ |
| pressure tendency | 气压倾向 | $\partial p / \partial t$ |
| significant figures | 有效数字 | — |

## 真实 data

2025-01-24，风暴 Éowyn 经过爱尔兰和英国。英国气象局发布了 wind 的红色预警。预警区是北爱尔兰、苏格兰中部地带和苏格兰西南部的大部分。格拉斯哥在苏格兰中部地带，所以在预警区之内。这些事实来自英国气象局的 [风暴报告](https://www.metoffice.gov.uk/api/assets/file/2025_02_storm_eowynpdf)。本页看两份真实 data：格拉斯哥机场这一天的 48 条 METAR report，以及 06 UTC 英国和爱尔兰的全部 METAR report。

```{code-cell} python
from meteo300.pages.ch02 import (
    clean_metar,
    direction_error,
    fix_metpy_station_text,
    graphcastgfs_10m_wind,
    metar_day,
    metar_snapshot,
    nearest_reports,
    parse_metars,
    pressure_code,
)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["figure.dpi"] = 120

day = metar_day("EGPF", "2025-01-24")

print(len(day), "条报文")
for line in day["metar"].iloc[[0, 1, 25]]:
    print(line)
```

第三条是 12:50 UTC 的报文。这一天格拉斯哥的平均 wind speed 在这个时刻最大。下表逐组解读它：

| 报文组 | 含义 |
|---|---|
| `EGPF` | weather station 代码：格拉斯哥机场 |
| `241250Z` | 24 日 12:50 UTC |
| `AUTO` | 全自动观测，没有人工干预 |
| `24051G74KT` | wind direction 240°，平均 wind speed 51 kt，wind gust 74 kt |
| `2700` | visibility 2700 m |
| `-RA` | 小雨 |
| `BKN025///` | cloud cover 为 ［5, 7］ okta，cloud base height 2500 ft，约 760 m，云的类型没有测到 |
| `OVC040///` | cloud cover 为 8 okta，cloud base height 4000 ft，约 1220 m，云的类型没有测到 |
| `//////TCU` | 测到浓积云，cloud cover 和 cloud base height 没有测到 |
| `06/06` | temperature 6 °C，dewpoint temperature 6 °C |
| `Q0963` | QNH 963 hPa |

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch02-egpf-day
#| caption: 2025-01-24，格拉斯哥机场 EGPF 的 wind speed、wind gust、wind direction 和 QNH，每 30 分钟一条 METAR report。data 来源：Iowa Environmental Mesonet。

obs = parse_metars(day["metar"], year=2025, month=1)
t = obs["date_time"]

fig, axes = plt.subplots(3, 1, figsize=(7, 7), sharex=True)
ax = axes[0]
ax.plot(t, obs["wind_speed"], color="#2a78d6", lw=2, label="mean wind")
ax.plot(t, obs["wind_gust"], "o", color="#eb6834", ms=4, label="gust")
ax.set_ylabel("speed (kt)")
sec = ax.secondary_yaxis("right", functions=(lambda kt: kt * 0.514444, lambda ms: ms / 0.514444))
sec.set_ylabel("speed (m s$^{-1}$)")
ax.legend(loc="upper left", frameon=False)

ax = axes[1]
ax.plot(t, obs["wind_direction"], "o", color="#2a78d6", ms=4)
ax.set_ylim(0, 360)
ax.set_yticks([0, 90, 180, 270, 360], ["N 0°", "E 90°", "S 180°", "W 270°", "N 360°"])
ax.set_ylabel("direction\n(blowing from)")

ax = axes[2]
ax.plot(t, obs["altimeter"] * 33.8639, color="#2a78d6", lw=2)  # 1 inHg = 33.8639 hPa
ax.set_ylabel("QNH (hPa)")
ax.set_xlabel("time on 2025-01-24 (UTC)")
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%H:%M"))
for ax in axes:
    ax.grid(color="0.9")
    ax.spines[["top"]].set_visible(False)
fig.align_ylabels(axes)
plt.show()
```

[](#fig-ch02-egpf-day) 有三个要点。QNH 从 986 hPa 降到 956 hPa，最低值出现在 08:50 到 09:50 UTC。wind direction 从东风经南风转为西南偏西风，wind 的来向沿顺时针转了约 150°。最大的平均 wind speed 51 kt 出现在 12:50 UTC，这时 pressure 已经在回升。

下一张图是 06 UTC 的 station plot。英国的报文时刻是 05:50 UTC，爱尔兰是 06:00 UTC。为了让符号不重叠，代码去掉了相距不到 60 km 的部分 weather station。代码用函数 `grid_vectors` 校正 wind 的两个分量，否则地图上的 wind barb 最多偏转 18°。MetPy 用 QNH、temperature 和机场的 geometric height 估计 mean sea level pressure。在这张图的 weather station 上，两者相差不到 1 hPa。

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch02-station-plot
#| caption: 2025-01-24 06 UTC，英国和爱尔兰的 station plot。wind barb 的单位是 kt。红色数字是 temperature，绿色数字是 dewpoint temperature，单位是 °C。右上方是 mean sea level pressure 的三位码。蓝圈是格拉斯哥机场。data 来源：Iowa Environmental Mesonet。

from meteo300.plot import grid_vectors

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.calc as mpcalc
from metpy.plots import StationPlot, sky_cover
from metpy.units import units

PLOT_TIME = pd.Timestamp("2025-01-24 06:00")
KEY_STATIONS = ["EGPF", "EGPO", "EGPE", "EGPU"]

fix_metpy_station_text()  # MetPy 1.7 和 Matplotlib 3.11 的兼容补丁
snapshot = metar_snapshot(PLOT_TIME, networks=["GB__ASOS", "IE__ASOS"])
all_obs = parse_metars(snapshot["metar"], year=2025, month=1)
snap = nearest_reports(all_obs, PLOT_TIME).dropna(subset=["wind_speed"])

proj = ccrs.LambertConformal(central_longitude=-4, central_latitude=54)
xy = proj.transform_points(ccrs.PlateCarree(), snap["longitude"].values, snap["latitude"].values)
priority = np.where(snap["station_id"].isin(KEY_STATIONS), 10, 1)
keep = mpcalc.reduce_point_density(xy[:, :2], 60_000, priority=priority)
s = snap[keep]

u_kt, v_kt = mpcalc.wind_components(
    s["wind_speed"].values * units.knots, s["wind_direction"].values * units.deg
)

fig = plt.figure(figsize=(7, 8.5))
ax = fig.add_subplot(1, 1, 1, projection=proj)
ax.set_extent([-10.8, 2.2, 49.0, 60.9], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor="0.95")
ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.5, edgecolor="0.5")

sp = StationPlot(ax, s["longitude"].values, s["latitude"].values,
                 transform=ccrs.PlateCarree(), fontsize=8, clip_on=True)
sp.plot_parameter("NW", s["air_temperature"].values, color="#e34948")
sp.plot_parameter("SW", s["dew_point_temperature"].values, color="#008300")
sp.plot_parameter("NE", s["air_pressure_at_sea_level"].values, formatter=pressure_code)
sp.plot_symbol("C", s["cloud_coverage"].values, sky_cover)
# cartopy 把 PlateCarree 上的 wind 分量当作经纬度的步长，grid_vectors 校正 wind barb 的方向
sp.plot_barb(*grid_vectors(s["latitude"].values, u_kt.m, v_kt.m), length=6)
egpf = s[s["station_id"] == "EGPF"]
ax.scatter(egpf["longitude"], egpf["latitude"], s=260, facecolor="none", edgecolor="#2a78d6",
           lw=2, transform=ccrs.PlateCarree(), zorder=5)
plt.show()
print(len(snap), "个 weather station 有报文，图上画出", len(s), "个。")
```

[](#fig-ch02-station-plot) 显示一个逆时针旋转的 cyclone circulation。苏格兰北部吹东风和东南风，英格兰吹南风和西南风，爱尔兰西部吹西南偏西风。在这些 weather station 里，蒂里岛的 mean sea level pressure 最低，三位码是 513，即 951.3 hPa。ERA5 reanalysis 把这一时刻的 low centre 放在 55.5°N、9.25°W，central pressure 是 940.7 hPa。中心在爱尔兰西北方的海上，那里没有 weather station。英国气象局的风暴报告说，蒂里岛的 pressure 在 09 UTC 降到最低，是 941.9 hPa。

北半球有一条检查规则：背对 wind 站立，low 在左手边略偏前方。[AMS 气象词汇表](https://glossary.ametsoc.org/wiki/buys-ballot-s-law/) 的版本只说 low 在左手边。“偏前方”来自 surface 摩擦，它让 wind 斜穿 isobar 吹向 low。格拉斯哥 05:50 UTC 的 wind 从 150° 吹来。背对 wind 站立时，人面向 330°，左手指向 240°。蒂里岛在格拉斯哥的 295° 方向，正好在左前方。

## dataset

本页的 METAR report 来自 Iowa Environmental Mesonet，简称 IEM。IEM 由爱荷华州立大学运行，它归档全球机场的 METAR report。网页接口 `asos.py` 按 weather station 或观测网返回 CSV 文件，英国的观测网代码是 `GB__ASOS`。IEM 的 [免责声明](https://mesonet.agron.iastate.edu/disclaimer.php) 说，网站上的材料属于公有领域。它希望使用者注明来源。完整条目见 [dataset 参考页](../reference/datasets.md)。

另外两个常用的 surface observation dataset：

- NOAA 的综合 surface data 库 ISD 收集全球 weather station 的逐时观测，由 NCEI 发布。它的论文是 Smith 等，2011，[doi:10.1175/2011BAMS3015.1](https://doi.org/10.1175/2011BAMS3015.1)。2025-08-24 以后，ISD 不再更新。NCEI 建议改用后继产品 GHCNh，见 [NOAA 的通知](https://www.nesdis.noaa.gov/news/service-location-change-integrated-surface-data-global-hourly)。
- 英国气象局的 [MIDAS Open](https://catalogue.ceda.ac.uk/uuid/dbd451271eb04662beade68da43546e1) 收集英国陆地 weather station 的逐时观测，在 CEDA 发布，使用开放政府许可。下载需要一个免费的 CEDA 账户。

“AI 天气连接”一节用 GraphCastGFS 的 forecast。NOAA 用 GDAS 的 analysis 作为 initial condition，实时运行 GraphCast，产品名是 GraphCastGFS。本页的 forecast 来自 2.0 版，它只运行 13 个 isobaric surface 的模型。NOAA 微调了这个模型的权重，输入是 GDAS analysis，真值是 ERA5。

GraphCast 的论文是 Lam 等，2023，[doi:10.1126/science.adi2336](https://doi.org/10.1126/science.adi2336)。GraphCastGFS 的 forecast 存放在 AWS 开放 data 的 `noaa-nws-graphcastgfs-pds` 存储桶，以 CC0 许可发布。这些事实见 [AWS 开放 data 的说明页](https://registry.opendata.aws/noaa-nws-graphcastgfs-pds/)。

本页用模块 `meteo300.pages.ch02` 读取这三种 data。设 `METEO300_OFFLINE=1` 后，函数读 `data/samples/` 里的样本文件，不访问网络。在线读取 GraphCastGFS 还需要 `cfgrib`。

## 计算

### 解析报文，先查缺测

函数 `metpy.io.parse_metar_file` 一次解析许多条报文。英国的自动观测报文有 `//////TCU` 这样的云组。MetPy 1.7 解析不了这种组，就把它后面的 temperature、dewpoint temperature 和 QNH 当成备注。解析器不报错，所以解析后必须数一数缺测。

```{code-cell} python
raw = parse_metars(day["metar"], year=2025, month=1, clean=False)
fixed = parse_metars(day["metar"], year=2025, month=1)
columns = ["wind_speed", "wind_direction", "air_temperature", "altimeter"]
print("不清理，缺测条数：", raw[columns].isna().sum().to_dict())
print("清理后，缺测条数：", fixed[columns].isna().sum().to_dict())
assert fixed[columns].notna().all().all()
```

48 条报文里有 38 条丢了 temperature 和 pressure，wind 没有受影响。函数 `clean_metar` 删去这些云组后，所有报文都完整。

### 一条报文：从 kt 到 m s⁻¹

函数 `metpy.io.parse_metar_to_dataframe` 解析一条报文。它返回 wind speed 和 wind gust，单位是 kt。下面的代码用 pint 把它们换算成 m s⁻¹，然后用手算核对。

```{code-cell} python
from metpy.io import parse_metar_to_dataframe

one = parse_metar_to_dataframe(clean_metar(day["metar"].iloc[25]), year=2025, month=1)
speed = one["wind_speed"].iloc[0] * units(one.units["wind_speed"])
gust = one["wind_gust"].iloc[0] * units(one.units["wind_gust"])
direction = one["wind_direction"].iloc[0] * units.deg

speed_ms = speed.to("m/s")
# 手算：1 kt = 1852 m / 3600 s
assert abs(speed_ms.m - 51 * 1852 / 3600) < 1e-9
# 量级估计：m/s 约等于 kt 的一半
assert abs(speed_ms.m - 51 / 2) / speed_ms.m < 0.05
# 常见错误：把 kt 当成英里每小时
wrong = (speed.m * units.mph).to("m/s")
print(f"平均 wind speed {speed:~P} = {speed_ms:.0f~P}，wind gust {gust:~P} = {gust.to('m/s'):.0f~P}")
print(f"把 kt 当成英里每小时：{wrong:.1f~P}，偏小 {100 * (1 - wrong / speed_ms).m:.0f}%")
```

平均 wind speed 26 m s⁻¹ 正好是 500 hPa 的典型 wind speed。这说明它是一次很强的 10 m wind。

### wind direction、分量和三种角

函数 `metpy.calc.wind_components` 把 wind speed 和 wind direction 换算成 $u$ 和 $v$。函数 `metpy.calc.wind_direction` 做反向换算。代码用 [](#fig-ch02-angles) 的公式核对它们。

```{code-cell} python
u, v = mpcalc.wind_components(speed_ms, direction)

# 手算：u = -V sin(chi)，v = -V cos(chi)
chi = np.deg2rad(240)
assert abs(u.m - (-speed_ms.m * np.sin(chi))) < 1e-9
assert abs(v.m - (-speed_ms.m * np.cos(chi))) < 1e-9
assert u.m > 0 and v.m > 0  # 西南风吹向东北，两个分量都为正

back = mpcalc.wind_direction(u, v)                      # wind direction，来向
travel = mpcalc.wind_direction(u, v, convention="to")   # bearing of travel
gamma = np.rad2deg(np.arctan2(v.m, u.m))                # math angle
assert abs(back.m - 240) < 1e-9
assert abs(gamma - (270 - 240)) < 1e-9
print(f"u = {u:.1f~P}，v = {v:.1f~P}")
print(f"wind direction {back.m:.0f}°，bearing of travel {travel.m:.0f}°，math angle {gamma:.0f}°")
```

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch02-angles
#| caption: 2025-01-24 12:50 UTC，格拉斯哥机场 10 m wind 的三种角。wind direction 240° 是来向，bearing of travel 是 060°，math angle 是 30°。data 来源：Iowa Environmental Mesonet。

from matplotlib.patches import Arc

BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "0.45"
fig, ax = plt.subplots(figsize=(5.6, 5.2))
g = np.deg2rad(30)            # math angle
tip = np.array([np.cos(g), np.sin(g)])
src = np.deg2rad(90 - 240)    # wind 的来向在图上的角
for end in [(1.3, 0), (0, 1.25)]:
    ax.annotate("", xy=end, xytext=(-end[0], -end[1]), arrowprops=dict(arrowstyle="->", color=GREY))
ax.text(1.32, -0.03, "x: east", fontsize=9, va="center")
ax.text(0.04, 1.22, "y: north", fontsize=9)
# 来向和 wind 矢量
ax.plot([0, np.cos(src)], [0, np.sin(src)], ls="--", color=ORANGE, lw=2)
ax.text(
    np.cos(src), np.sin(src) - 0.12, "air comes from here", color=ORANGE, fontsize=9, ha="center"
)
ax.annotate("", xy=tip, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.5))
ax.text(tip[0] + 0.04, tip[1] + 0.04, "wind vector:\nair goes to 060°", color=BLUE, fontsize=9)
# 分量
ax.plot([0, tip[0]], [0, 0], color=BLUE, lw=5, alpha=0.3, solid_capstyle="butt")
ax.plot([0, 0], [0, tip[1]], color=BLUE, lw=5, alpha=0.3, solid_capstyle="butt")
ax.plot([tip[0], tip[0], 0], [0, tip[1], tip[1]], ":", color=BLUE)
ax.text(tip[0] / 2, -0.1, "u = +22.7 m/s", fontsize=9, ha="center", va="top")
ax.text(-0.04, tip[1] + 0.06, "v = +13.1 m/s", fontsize=9, ha="right")
# wind direction chi：从北顺时针量到来向
ax.add_patch(Arc((0, 0), 0.6, 0.6, theta1=90 - 240, theta2=90, color=ORANGE, lw=1.5))
ax.text(0.28, -0.42, "χ = 240°\nclockwise from north", color=ORANGE, fontsize=9)
# math angle gamma：从东逆时针量到去向
ax.add_patch(Arc((0, 0), 1.2, 1.2, theta1=0, theta2=30, color=BLUE, lw=1.5))
ax.text(0.63, 0.13, "γ = 30°", color=BLUE, fontsize=9)
ax.set_xlim(-1.3, 1.75)
ax.set_ylim(-1.15, 1.35)
ax.set_aspect("equal")
ax.axis("off")
plt.show()
```

wind direction 四舍五入到 10°，所以真实的 wind direction 可能偏 5°。在 26 m s⁻¹ 的 wind 里，5° 的方向误差对应 $26 \times \sin 5^\circ \approx 2.3\ \mathrm{m\,s^{-1}}$ 的横向分量。所以比较模式和观测时，小于 5° 的 wind direction 误差没有意义。

### 一天的分量

同一组函数可以一次处理整天的报文。下面的表格列出四个时刻。wind direction 越过 180° 时，$u$ 由负变正。

```{code-cell} python
obs_u, obs_v = mpcalc.wind_components(
    obs["wind_speed"].values * units.knots, obs["wind_direction"].values * units.deg
)
table = pd.DataFrame({
    "time": obs["date_time"].dt.strftime("%H:%M"),
    "direction (deg)": obs["wind_direction"],
    "speed (m/s)": (obs["wind_speed"].values * units.knots).to("m/s").m.round(1),
    "u (m/s)": obs_u.to("m/s").m.round(1),
    "v (m/s)": obs_v.to("m/s").m.round(1),
})
table.iloc[[0, 11, 12, 25]]
```

### pressure tendency

MetPy 把报文里的 `Q0986` 换算成英寸汞柱，存在 `altimeter` 列。下面的代码先从报文里直接读出 Q 组，再和 MetPy 的值比较。然后它用 `numpy.argmin` 找出 3 h 内 pressure 下降最快的时段，并换算成 Pa s⁻¹。

```{code-cell} python
qnh = day["metar"].str.extract(r" Q(\d{4})")[0].astype(float).values * units.hPa
p_metpy = (obs["altimeter"].values * units.inHg).to("hPa")
print(f"MetPy 存 {obs['altimeter'][0]} inHg，换回 {p_metpy[0]:.2f~P}；报文是 {qnh[0]:~P}")
# 0.01 inHg 约等于 0.34 hPa，所以两者最多差半个舍入单位
assert np.all(abs(p_metpy - qnh) < 0.18 * units.hPa)

dp_3h = qnh[6:] - qnh[:-6]  # 6 条报文相隔 3 h
i = int(np.argmin(dp_3h.m))
rate = (dp_3h[i] / (3 * units.hour)).to("Pa/s")
# 手算：-14 hPa / 3 h = -1400 Pa / 10800 s
assert dp_3h[i].m == -14
assert abs(rate.m - (-1400 / 10800)) < 1e-9
t0, t3 = obs["date_time"][i], obs["date_time"][i + 6]
print(f"{t0:%H:%M} 到 {t3:%H:%M} UTC：{dp_3h[i]:~P}，即 {rate:.2f~P}")
```

英国气象局把 3 h 的 pressure 变化分成几档，最高一档是变化超过 6.0 hPa。这些档见它的 [海岸与海洋术语表](https://weather.metoffice.gov.uk/guides/coast-and-sea/glossary)。格拉斯哥的 -14 hPa 是这个阈值的两倍多。这一天格拉斯哥的 pressure 先降 30 hPa，然后在 14 h 里回升 32 hPa。

### 两个机场之间的距离

类 `pyproj.Geod` 在 WGS84 椭球面上计算两点之间的最短距离。在球面上，这个最短距离就是 great-circle distance。下面的代码计算格拉斯哥机场到伦敦希思罗机场的距离，再用球面余弦定理和平面近似核对。

```{code-cell} python
from pyproj import Geod

lat1, lon1 = 55.8719, -4.4331   # EGPF，格拉斯哥
lat2, lon2 = 51.4785, -0.4614   # EGLL，伦敦希思罗
_, _, d_geod = Geod(ellps="WGS84").inv(lon1, lat1, lon2, lat2)

# 手算 1：球面余弦定理，Earth radius 6371 km
p1, p2, dl = np.deg2rad([lat1, lat2, lon2 - lon1])
d_sphere = 6371e3 * np.arccos(np.sin(p1) * np.sin(p2) + np.cos(p1) * np.cos(p2) * np.cos(dl))
# 手算 2：平面近似，latitude 1° = 111.2 km，longitude 1° = 111.2 km × cos(平均 latitude)
dy = 111.2e3 * (lat2 - lat1)
dx = 111.2e3 * np.cos(np.deg2rad((lat1 + lat2) / 2)) * (lon2 - lon1)
d_flat = np.hypot(dx, dy)

assert abs(d_sphere - d_geod) / d_geod < 0.005
assert abs(d_flat - d_geod) / d_geod < 0.01
print(f"Geod {d_geod / 1e3:.0f} km，球面 {d_sphere / 1e3:.0f} km，平面 {d_flat / 1e3:.0f} km")
```

三个结果相差不到 1%。在几百公里的尺度上，local Cartesian coordinate system 够用。尺度到几千公里时，必须用球面公式。

## AI 天气连接

AI weather model 不输出 wind direction。它们输出 10 m wind 的两个分量。ERA5 的变量名是 `u10` 和 `v10`，WeatherBench 2 的变量名是 `10m_u_component_of_wind` 和 `10m_v_component_of_wind`。ECMWF 开放 data 的参数名是 `10u` 和 `10v`。GraphCast 和 AIFS 每 6 h 输出一次这两个分量。ERA5 还有 100 m wind `u100` 和 `v100`，这个 geometric height 更接近风机的轮毂。

交易员和风电预报员需要 wind speed 和 wind direction，不看 $u$ 和 $v$。风机功率在 rated wind speed 以下大致和 wind speed 的三次方成正比。所以 wind speed 偏高 10%，功率约偏高 33%。分析员把 $u$、$v$ 换成 wind speed 和 wind direction 时，最常见的错误有四个：

1. 用 `np.arctan2(v, u)` 得到的是 math angle，不是 wind direction。wind direction 要用 `metpy.calc.wind_direction`。
2. 用 `np.arctan2(u, v)` 得到的是 bearing of travel，和 wind direction 差 180°。
3. 直接平均 wind direction。350° 和 10° 的算术平均是 180°，正确的平均 wind direction 是 360°。要先平均 $u$ 和 $v$，再换算 wind direction。
4. 有的 grid 不沿东和北。旋转极 grid 或 Lambert conformal conic projection grid 上的 $u$ 和 $v$ 常常沿 grid 方向。读文件前要查清楚。规则经纬度 grid 没有这个问题。

weather station 是检验 AI forecast 的一个基准。下面的代码把 GraphCastGFS 的 forecast 和格拉斯哥机场的 METAR report 对比。forecast 的 initialization time 是 2025-01-23 00 UTC，lead time 是 ［24, 48］ h。代码把 grid point 值 bilinear interpolation 到机场，再取离 valid time 最近的报文。

```{code-cell} python
fc = graphcastgfs_10m_wind("2025-01-23 00:00", steps=[24, 30, 36, 42, 48])
point = fc.interp(latitude=55.8719, longitude=-4.4331)
fc_u = point["u10"].values * units("m/s")
fc_v = point["v10"].values * units("m/s")
fc_speed = mpcalc.wind_speed(fc_u, fc_v)
fc_dir = mpcalc.wind_direction(fc_u, fc_v)

valid = pd.to_datetime(point["valid_time"].values)
match = obs.loc[[(obs["date_time"] - vt).abs().idxmin() for vt in valid]]
ob_speed = (match["wind_speed"].values * units.knots).to("m/s")
ob_dir = match["wind_direction"].values

# wind direction 误差按圆周计算：10° 减 350° 是 +20°，不是 -340°
assert direction_error(10, 350) == 20
speed_error = (fc_speed - ob_speed).m
assert abs(speed_error[2] - (-4.8)) < 0.1 and abs(speed_error[3] - (-6.7)) < 0.1
verify = pd.DataFrame({
    "valid time": valid.strftime("%d %H UTC"),
    "lead (h)": point["step"].values,
    "METAR time": match["date_time"].dt.strftime("%H:%M").values,
    "METAR speed (m/s)": ob_speed.m.round(1),
    "GraphCastGFS speed (m/s)": fc_speed.m.round(1),
    "METAR dir (deg)": ob_dir,
    "GraphCastGFS dir (deg)": fc_dir.m.round(0),
    "speed error (m/s)": speed_error.round(1),
    "dir error (deg)": direction_error(fc_dir.m, ob_dir).round(0),
})
verify.set_index("valid time")
```

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch02-ai-vs-metar
#| caption: 2025-01-24，格拉斯哥机场的 10 m wind speed 和 wind direction。线和小圆点是 METAR report，大圆点是 GraphCastGFS 在 2025-01-23 00 UTC 起报的 forecast。data 来源：Iowa Environmental Mesonet 和 NOAA GraphCastGFS。

fig, axes = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
ax = axes[0]
obs_speed = (obs["wind_speed"].values * units.knots).to("m/s").m
ax.plot(t, obs_speed, color="#2a78d6", lw=2, label="METAR")
ax.plot(valid, fc_speed.m, "o", color="#eb6834", ms=9, label="GraphCastGFS")
ax.set_ylabel("speed (m s$^{-1}$)")
ax.legend(loc="upper left", frameon=False)
ax = axes[1]
ax.plot(t, obs["wind_direction"], "o", color="#2a78d6", ms=4)
ax.plot(valid, fc_dir.m, "o", color="#eb6834", ms=9)
ax.set_ylim(0, 360)
ax.set_yticks([0, 90, 180, 270, 360], ["N 0°", "E 90°", "S 180°", "W 270°", "N 360°"])
ax.set_ylabel("direction\n(blowing from)")
ax.set_xlabel("time (UTC), 2025-01-24 to 2025-01-25")
ax.xaxis.set_major_locator(plt.matplotlib.dates.HourLocator(byhour=range(0, 24, 3)))
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%H:%M"))
for ax in axes:
    ax.grid(color="0.9")
    ax.spines[["top", "right"]].set_visible(False)
fig.align_ylabels(axes)
plt.show()
```

[](#fig-ch02-ai-vs-metar) 和上表有三个要点。06 UTC 以后，wind direction 误差不超过 22°，GraphCastGFS 抓住了 wind direction 的顺时针转动。00 UTC 的 wind 只有 5 m s⁻¹，wind direction 误差是 56°。弱 wind 的 wind direction 本来就不稳定，所以这个误差的影响小。最大的问题是 wind speed：GraphCastGFS 在 12 UTC 低估了 4.8 m s⁻¹，在 18 UTC 低估了 6.7 m s⁻¹。

这个对比有代表性问题。METAR 的 wind speed 是一个点上 10 分钟的平均。GraphCastGFS 的 grid point 值代表一个约 28 km 宽的 grid。相隔 30 分钟的两条报文也会差很多：11:50 UTC 是 17 m s⁻¹，12:20 UTC 是 23 m s⁻¹。所以一个 weather station 和一个 grid point 的差，不全是 forecast 误差。

分析员可以对任何 AI forecast 做同样的检查。先选几个机场，把 $u_{10}$ 和 $v_{10}$ 换成 wind speed 和 wind direction。然后按圆周计算 wind direction 误差，并把 wind speed 误差换算成功率误差。

## 练习

:::{exercise}
:label: ex-ch02-1

格拉斯哥机场 12:50 UTC 的报文是 `24051G74KT`。一个同事的脚本报告这一刻的 wind speed 是 99 m s⁻¹。

1. 用“kt 的一半”估计正确的 wind speed。脚本错在哪里？
2. 有人把 51 kt 当成 51 mph。他得到的 wind speed 是多少 m s⁻¹？
3. Met Éireann 报告，爱尔兰 Mace Head 测到 183 km h⁻¹ 的 wind gust。把它换算成 m s⁻¹ 和 kt。它比格拉斯哥的 wind gust 大多少？
:::

:::{solution} ex-ch02-1
:class: dropdown

1. 51 kt 的一半约是 26 m s⁻¹。99 m s⁻¹ 大了约 4 倍，量级不对。脚本把 51 乘以 1.944，而 1.944 是从 m s⁻¹ 换算到 kt 的系数。正确的做法是乘以 0.514。
2. 51 mph 是 $51 \times 0.447 = 22.8\ \mathrm{m\,s^{-1}}$，比正确值 26.2 m s⁻¹ 小 13%。
3. $183\ \mathrm{km\,h^{-1}} = 183\,000\ \mathrm{m} / 3600\ \mathrm{s} = 50.8\ \mathrm{m\,s^{-1}}$，也就是 98.8 kt。格拉斯哥的 wind gust 74 kt 是 38 m s⁻¹。Mace Head 的 wind gust 大约大 13 m s⁻¹。这次 wind gust 是爱尔兰的临时纪录，见英国气象局的 [回顾文章](https://www.metoffice.gov.uk/blog/2025/a-look-back-on-storm-eowyn)。

用 pint 核对：

```python
from metpy.units import units
print((183 * units("km/h")).to("m/s"), (183 * units("km/h")).to("knots"))
```
:::

:::{exercise}
:label: ex-ch02-2

ERA5 在某个 grid point 给 $u_{10} = -6.0\ \mathrm{m\,s^{-1}}$ 和 $v_{10} = +8.0\ \mathrm{m\,s^{-1}}$。

1. wind 吹向哪个象限？wind 从哪个象限吹来？
2. 计算 wind speed $V$、wind direction $\chi$、bearing of travel 和 math angle $\gamma$。
3. 三个候选值 143°、323° 和 127° 里，哪一个应该写进 METAR report？
:::

:::{solution} ex-ch02-2
:class: dropdown

1. $u < 0$ 表示 wind 吹向西，$v > 0$ 表示 wind 吹向北。wind 吹向西北，所以 wind 从东南吹来。
2. $V = \sqrt{6^2 + 8^2} = 10\ \mathrm{m\,s^{-1}}$。math angle $\gamma = \arctan2(8, -6) = 126.9^\circ$。wind direction $\chi = 270^\circ - 126.9^\circ = 143.1^\circ$。bearing of travel $= 143.1^\circ + 180^\circ = 323.1^\circ$。
3. METAR 报 wind direction，即来向，所以写 140°，这是 143° 四舍五入到 10° 的结果。323° 是 bearing of travel，127° 是 math angle。

用 MetPy 核对：

```python
import metpy.calc as mpcalc
from metpy.units import units
u, v = -6.0 * units("m/s"), 8.0 * units("m/s")
print(mpcalc.wind_speed(u, v), mpcalc.wind_direction(u, v))
print(mpcalc.wind_direction(u, v, convention="to"))
```
:::

:::{exercise}
:label: ex-ch02-3

把 [](#fig-ch02-station-plot) 的代码里的 `PLOT_TIME` 改成 `pd.Timestamp("2025-01-24 12:00")`，重新运行。

1. 哪个 weather station 报静风 `00000KT`？它的 wind barb 怎样画？为什么那里没有 wind？
2. 因弗内斯机场 EGPE 的三位码是多少？用解码规则解码，结果合理吗？
:::

:::{solution} ex-ch02-3
:class: dropdown

1. 斯托诺韦机场 EGPO 报静风，QNH 是 949 hPa。MetPy 把静风画成一个空圆圈，没有杆。ERA5 把 12 UTC 的 low centre 放在 57.5°N、4.5°W，在苏格兰北部。中心附近的 pressure gradient 很小，所以 wind 很弱。周围 weather station 的 wind 绕着中心逆时针转。
2. EGPE 的 mean sea level pressure 约是 947.3 hPa，三位码是 473。解码规则给 1047.3 hPa。这个结果错了 100 hPa。周围的 weather station 都在 ［945, 965］ hPa 之内，1047 hPa 在风暴里不可能出现。三位码只在 ［950, 1050］ hPa 之内不含歧义，深 low 附近要用量级检查。
:::

:::{exercise}
:label: ex-ch02-4

一个风电场有两座测 wind 塔。它们同一时刻报告 wind direction 355° 和 15°，wind speed 都是 10 m s⁻¹。一个脚本报告平均 wind direction 185°。

1. 这个结果错在哪里？正确的平均 wind direction 是多少？
2. 用 `metpy.calc.wind_components` 和 `metpy.calc.wind_direction` 写出正确的计算。
:::

:::{solution} ex-ch02-4
:class: dropdown

1. 脚本做了算术平均：$(355 + 15) / 2 = 185$。wind direction 是圆周上的量，355° 和 15° 只差 20°。两个 wind 都是偏北风，正确的平均 wind direction 是 5°。
2. 先平均分量，再换算 wind direction：

```python
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units
u, v = mpcalc.wind_components(np.array([10, 10]) * units("m/s"), np.array([355, 15]) * units.deg)
print(mpcalc.wind_direction(u.mean(), v.mean()))  # 约 5°
```
:::
