---
title: general circulation
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

本页取自 [METEO 300](https://www.e-education.psu.edu/meteo300/) 第 12 课 12.1 节、第 1 课 1.2 节、第 7 课 7.3 节和第 10 课 10.11 节。

太阳加热低纬度多，加热高纬度少。低纬度吸收的 shortwave radiation 多于 outgoing longwave radiation，高纬度正好相反。METEO 300 第 7 课 7.3 节说，两者大约在 latitude 30° 附近相等。[辐射](t2-radiation.md) 一页用 CERES 的观测算出约 37°。大气和海洋把多余的热量从低纬度运到高纬度。general circulation 是完成这项输送的大尺度运动的平均形态。

赤道附近的空气受热上升，形成 intertropical convergence zone。上升的空气在 troposphere 上部流向两极。它在 latitude 30° 附近下沉，形成 subtropical high。下沉的空气在低层流回赤道。这个闭合的 meridional overturning circulation 叫 Hadley cell。

Coriolis force 使运动的空气在北半球向右偏，在南半球向左偏。[](#fig-ch01-inertial) 用一个只受 Coriolis force 的 air parcel 说明这一点。

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch01-inertial
#| caption: f-plane 上只受 Coriolis force 的 air parcel 的 trajectory。air parcel 从原点出发，初速度 10 m s⁻¹，方向向东。左图在 50°N，右图在 50°S。蓝色箭头是每隔四分之一个 inertial period 的速度，红色箭头是出发时的 Coriolis force。data 来源：本页的数值积分。

from meteo300 import data as d
from meteo300 import plot as mplot
from meteo300.pages import ch01

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

U0, LAT = 10.0, 50.0  # initial speed towards the east (m s-1), latitude (degrees)
f = 2 * ch01.OMEGA * np.sin(np.deg2rad(LAT))  # Coriolis parameter, s-1
period = 2 * np.pi / f / 3600  # inertial period, h
radius = U0 / f / 1000  # radius of the inertial circle, km
print(f"50°N: f = {f:.3e} s-1，inertial period {period:.1f} h，inertial circle 半径 {radius:.1f} km")

fig, axes = plt.subplots(1, 2, figsize=(8, 4.4))
for ax, lat in zip(axes, [LAT, -LAT], strict=True):
    path = ch01.inertial_trajectory(lat, U0, hours=period)
    side = np.sign(lat)  # +1: the circle lies south of the start, -1: north of it
    # After one period the parcel is back at the start, on a circle of radius U0 / |f|.
    assert np.hypot(path.x[-1], path.y[-1]) < 0.01 * radius
    assert np.allclose(np.hypot(path.x, path.y + side * radius), radius, rtol=1e-4)

    ax.plot(path.x, path.y, color="#2a78d6", lw=2)
    quarter = path.sel(time=[k * period / 4 for k in range(4)], method="nearest")
    ax.quiver(quarter.x, quarter.y, quarter.u, quarter.v, color="#2a78d6",
              scale=40, width=0.012, zorder=3)
    for t, x, y in zip(quarter.time.values, quarter.x.values, quarter.y.values, strict=True):
        ax.annotate(f"{t:.1f} h", (x, y), xytext=(8, 6), textcoords="offset points")
    ax.annotate("", xy=(0, -side * 45), xytext=(0, 0), arrowprops=dict(color="#d6402a", width=2.5))
    ax.text(6, -side * 30, "Coriolis force", color="#d6402a", va="center")
    ax.plot(0, 0, "ko", ms=5)
    hemi = "北半球 50°N：向右偏，顺时针转" if lat > 0 else "南半球 50°S：向左偏，逆时针转"
    ax.set_title(hemi, fontsize=11)
    ax.text(0.5, 0.5, f"inertial period {period:.1f} h\n半径 {radius:.1f} km",
            transform=ax.transAxes, ha="center", va="center", color="0.3")
    ax.set(aspect="equal", xlim=(-130, 130), xlabel="向东的距离 / km")
    ax.set_ylim(sorted([-side * 200, side * 40]))
    ax.grid(color="0.92")
axes[0].set_ylabel("向北的距离 / km")
fig.tight_layout()
plt.show()
```

[](#fig-ch01-inertial) 里的 air parcel 只受 Coriolis force。Coriolis force 总是垂直于速度，所以它只改变 wind direction，不改变 wind speed。北半球的 air parcel 不断向右偏，沿顺时针转圈。南半球的 air parcel 不断向左偏，沿逆时针转圈。这种运动叫 inertial oscillation，air parcel 画出的圆叫 inertial circle。

在 50°N，Coriolis parameter $f = 2\Omega\sin\varphi \approx 1.12 \times 10^{-4}\ \mathrm{s^{-1}}$。式中 $\Omega$ 是 Earth's angular velocity，$\varphi$ 是 latitude。air parcel 转一圈的时间是 inertial period $2\pi/|f|$，约 15.6 h。inertial circle 的半径等于初速度除以 $|f|$，约 89.5 km。圆的直径只跨约 1.6° latitude，所以本图把 $f$ 当作常数，这个近似叫 f-plane。真实大气里还有 pressure gradient force，它常常和 Coriolis force 接近平衡，这就是 geostrophic balance。

在两个半球，Hadley cell 高空流向极地的空气都偏向东。Hadley cell 的极地一侧因此有很强的西风，这就是 subtropical jet。低层流回赤道的空气都偏向西，形成东北 trade winds 和东南 trade winds。

subtropical jet 和北大西洋的 westerlies 不是同一支 wind。zonal mean 的 subtropical jet 只在 troposphere 上部，中心在 30°N 和 200 hPa，zonal wind 约 42 m s⁻¹。它的正下方是 subtropical high，1000 hPa 上 zonal mean 的 zonal wind 只有约 1 m s⁻¹。westerlies 从 surface 一直伸到 tropopause，大约位于 latitude 35° 和 65° 之间。extratropical cyclone 把西风动量输送到中纬度，并把它向下传到 surface。Coriolis force 还使中纬度低层流向极地的空气偏向东，这也维持低层的西风。

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch01-natl-u
#| caption: 1990 年至 2019 年 12 月至 2 月，北大西洋扇区 60°W 至 0° 平均的 zonal wind。黑线是 0 m s⁻¹ 的等值线。data 来源：ERA5，WeatherBench 2 climatology。

uv_djf = d.page_data(ch01.FILES["clim_uv"], ch01.clim_uv).sel(season="DJF")
u_djf = uv_djf["u_component_of_wind"]  # m s-1, dims (level, latitude, longitude)
u_natl = u_djf.sel(longitude=slice(-60, 0)).mean("longitude").sel(latitude=slice(0, 81))
u_zm_djf = u_djf.mean("longitude")

# Latitude of the maximum, by Eq. (1) of the TropD paper with n = 30 (see below).
upper = u_natl.sel(level=200, latitude=slice(0, 33))  # subtropical jet
low = u_natl.sel(level=850, latitude=slice(30, 70))  # eddy-driven jet
lat_stj = ch01.tropd_max_latitude(upper, upper.latitude, n=30)
lat_edj = ch01.tropd_max_latitude(low, low.latitude, n=30)
print(f"北大西洋扇区，200 hPa 的 subtropical jet：{lat_stj:.0f}°N，{float(upper.max()):.1f} m/s")
print(f"北大西洋扇区，850 hPa 的 eddy-driven jet：{lat_edj:.0f}°N，{float(low.max()):.1f} m/s")
print(f"zonal mean，30°N 的 zonal wind：200 hPa {float(u_zm_djf.sel(level=200, latitude=30, method='nearest')):.1f} m/s，"
      f"1000 hPa {float(u_zm_djf.sel(level=1000, latitude=30, method='nearest')):.1f} m/s")

fig, ax = plt.subplots(figsize=(7, 3.8))
cf = ax.contourf(u_natl.latitude, u_natl.level, u_natl, levels=np.arange(-10, 32.5, 2.5),
                 cmap="RdBu_r", extend="both")
ax.contour(u_natl.latitude, u_natl.level, u_natl, levels=[0], colors="k", linewidths=1)
ax.annotate("subtropical jet", (lat_stj, 200), xytext=(25, 420), arrowprops=dict(arrowstyle="-"))
ax.annotate("eddy-driven jet", (lat_edj, 850), xytext=(56, 520), arrowprops=dict(arrowstyle="-"))
ax.set(ylim=(1000, 100), xlim=(0, 80), xticks=range(0, 81, 10), xlabel="latitude / °N", ylabel="pressure / hPa")
cbar = fig.colorbar(cf, ax=ax)
# DejaVu Sans draws the superscript minus, which some CJK fonts lack.
cbar.set_label("zonal wind / m s⁻¹", fontfamily=[plt.rcParams["font.sans-serif"][0], "DejaVu Sans"])
plt.show()
```

[](#fig-ch01-natl-u) 只在北大西洋扇区里求 longitude 平均。troposphere 上部有两个 wind speed 中心。偏南的中心在 18°N 和 200 hPa 附近，这是 subtropical jet。偏北的中心在 45°N 附近，它从 tropopause 一直伸到 surface，这是 eddy-driven jet。extratropical cyclone 维持 eddy-driven jet。它的低层部分就是北大西洋的 westerlies，850 hPa 的 zonal wind 在 47°N 附近最强。

北大西洋低层的 westerlies 位于 Azores High 和 Icelandic Low 之间。它是这两个 pressure 中心之间的 pressure gradient 对应的 geostrophic wind。英国在这条 westerlies 里，所以冬季常有西风和 extratropical cyclone。zonal mean 把不同 longitude 的 jet stream 平均在一起。所以 [](#fig-ch01-section) 的北半球只有一个高空 wind speed 中心，它在 30°N 附近。

中纬度的 temperature 向极地降低。METEO 300 第 10 课 10.11 节用 thermal wind 说明，这个 temperature gradient 使西风随 geometric height 增大。所以 westerlies 的 wind 在 tropopause 附近最强。中纬度的热量主要由 extratropical cyclone 和 anticyclone 输送。zonal mean 以后，这些天气系统的作用表现为 Ferrel cell。Ferrel cell 的转向和 Hadley cell 相反。

surface 上，这些 circulation 对应几条 pressure 带。赤道附近是 equatorial low-pressure belt，latitude 30° 附近是 subtropical high-pressure belt，latitude 60° 附近是 subpolar low-pressure belt。[](#fig-ch01-belts) 是 12 月至 2 月 zonal mean 的 mean sea level pressure。

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch01-belts
#| caption: 1990 年至 2019 年 12 月至 2 月，zonal mean 的 mean sea level pressure。红色虚线是 PSL 指标，蓝色点线是 PSI 指标，两种指标都用 TropD 的方法算出。黄色区域是两个 Hadley cell。data 来源：ERA5，WeatherBench 2 climatology。

msl_all = d.page_data(ch01.FILES["clim_msl"], ch01.clim_msl)["mean_sea_level_pressure"]
msl_zm = msl_all.sel(season="DJF").mean("longitude") / 100  # hPa
psi_djf = ch01.mass_streamfunction(uv_djf["v_component_of_wind"].mean("longitude"))  # kg s-1
psl = ch01.tropd_psl(msl_zm)  # subtropical maximum of msl
edge = ch01.tropd_psi(psi_djf)  # poleward edge of each Hadley cell
print(f"PSL 指标：{psl['N']:.1f}°N，{-psl['S']:.1f}°S")
print(f"PSI 指标：{edge['N']:.1f}°N，{-edge['S']:.1f}°S")

fig, ax = plt.subplots(figsize=(8, 3.9))
ax.axvspan(edge["S"], edge["N"], color="#f6e7b4", label="Hadley cell")
ax.axvspan(-90, -70, color="0.88", label="南极大陆，外推值")
ax.plot(msl_zm.latitude, msl_zm, color="k", lw=2)
for h in "NS":
    ax.axvline(psl[h], color="#d6402a", ls="--", label="PSL 指标" if h == "N" else None)
    ax.axvline(edge[h], color="#2a78d6", ls=":", lw=2, label="PSI 指标" if h == "N" else None)

belts = [  # name, latitude band (degrees), "min" or "max", text offset in points
    ("equatorial low-pressure belt", (-15, 15), "min", (0, -28)),
    ("subtropical high-pressure belt", (15, 50), "max", (48, 8)),
    ("subtropical high-pressure belt", (-50, -15), "max", (-48, 8)),
    ("subpolar low-pressure belt", (45, 80), "min", (10, -26)),
    ("subpolar low-pressure belt", (-80, -45), "min", (40, 0)),
]
for name, (lo, hi), kind, offset in belts:
    band = msl_zm.sel(latitude=slice(lo, hi))
    i = int(np.argmin(band.values) if kind == "min" else np.argmax(band.values))
    lat_i, p_i = float(band.latitude[i]), float(band[i])
    ax.plot(lat_i, p_i, "o", color="k", ms=4)
    ax.annotate(f"{name}\n{p_i:.0f} hPa", (lat_i, p_i), xytext=offset, textcoords="offset points",
                ha="center", va="center", fontsize=9)
ax.set_xticks(range(-90, 91, 30), ["90°S", "60°S", "30°S", "0°", "30°N", "60°N", "90°N"])
ax.set(xlim=(-90, 90), ylim=(980, 1028), xlabel="latitude", ylabel="mean sea level pressure / hPa")
ax.legend(loc="lower right", fontsize=8, ncols=2, framealpha=0.9)
plt.show()
```

[](#fig-ch01-belts) 里，equatorial low-pressure belt 很宽，约 1010 hPa。北半球的 subtropical high-pressure belt 在 30°N 附近，约 1020 hPa。南半球的 subtropical high-pressure belt 在 36°S 附近，约 1017 hPa。南半球的 subpolar low-pressure belt 在 64.5°S 附近，约 986 hPa，它环绕南极大陆。北半球的 subpolar low-pressure belt 在 60°N 附近，只有约 1012 hPa。zonal mean 把 Icelandic Low、Aleutian Low 和大陆上的 high 平均在一起，所以这条 low 带很浅。

图中的竖线用 TropD 的方法算出。TropD 是一套计算热带宽度的方法，见 Adam 等，2018，[`doi:10.5194/gmd-11-4339-2018`](https://doi.org/10.5194/gmd-11-4339-2018)。PSL 指标是 latitude 15° 和 60° 之间 mean sea level pressure 最大的 latitude。PSI 指标是 Hadley cell 的边界，也就是 500 hPa 的 $\psi$ 从热带的极值向极地第一次变号的 latitude。本节后面定义 $\psi$。函数 `ch01.tropd_psl` 和 `ch01.tropd_psi` 按论文的定义计算这两种指标。

12 月至 2 月，PSL 指标是 31.4°N 和 34.8°S，PSI 指标是 28.9°N 和 35.1°S。两种指标在南半球只差 0.3°，在北半球差 2.5°。subtropical high-pressure belt 在 Hadley cell 的下沉支附近，所以两种指标接近。南极大陆和青藏高原上的 mean sea level pressure 是外推值。灰色区域里的曲线不可信。

海陆分布把北半球的 pressure 带分成几个中心。冬季的北大西洋北部有 Icelandic Low，南部有 Azores High。两个中心之间是强西风和 storm track，英国正好在这里。这两个中心的强弱每个月都在变，而且常常反向变化。[](#fig-ch01-nao) 用 empirical orthogonal function 找出这种变化。

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch01-nao
#| caption: 1990 年至 2019 年 12 月、1 月和 2 月，北大西洋 mean sea level pressure 月平均 anomaly 的第一 mode。上图的色块是 principal component 增加一个 standard deviation 时的 anomaly，黑线是这 90 个月的平均 mean sea level pressure。下图是标准化的 principal component。data 来源：ERA5，WeatherBench 2。

import warnings

from xeofs.single import EOF

nao_msl = d.page_data(ch01.FILES["nao_msl"], ch01.nao_msl)["mean_sea_level_pressure"] / 100  # hPa
nao_anom = nao_msl.groupby("time.month") - nao_msl.groupby("time.month").mean("time")

model = EOF(n_modes=3, use_coslat=True)  # weights sqrt(cos(latitude)), as for equal areas
with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)  # xeofs 3.0.4 and pandas MultiIndex
    model.fit(nao_anom, dim="time")
frac = float(model.explained_variance_ratio().sel(mode=1))
pc = model.scores().sel(mode=1)
pc = (pc - pc.mean()) / pc.std()  # standardised principal component
pattern = (nao_anom * pc).mean("time")  # hPa per standard deviation of the principal component

ICELAND, AZORES = (64.1, -21.9), (37.7, -25.7)  # Reykjavik and Ponta Delgada
def at(da, point):
    return da.sel(latitude=point[0], longitude=point[1], method="nearest")

sign = -np.sign(float(at(pattern, ICELAND)))  # positive phase: low pressure near Iceland
pattern, pc = sign * pattern, sign * pc

# Check xeofs with numpy: the same weights and a singular value decomposition.
w = np.sqrt(np.cos(np.deg2rad(nao_anom.latitude)))
s = np.linalg.svd((nao_anom * w).values.reshape(nao_anom.sizes["time"], -1), compute_uv=False)
assert abs(s[0] ** 2 / (s**2).sum() - frac) < 1e-3

opposite = int((np.sign(at(nao_anom, ICELAND)) != np.sign(at(nao_anom, AZORES))).sum())
print(f"第一 mode 的 explained variance fraction：{frac:.1%}")
print(f"冰岛 {float(at(pattern, ICELAND)):+.1f} hPa，亚速尔 {float(at(pattern, AZORES)):+.1f} hPa，"
      f"两地 anomaly 符号相反的月数：{opposite} / {nao_anom.sizes['time']}")

# Geostrophic zonal wind at sea level, mean of 60°W to 0°: u_g = -(dp/dy) / (rho f).
def westerly_centre(p_hpa, rho=1.25):
    p = p_hpa.sel(longitude=slice(-60, 0)).mean("longitude").sel(latitude=slice(30, 75)) * 100
    f_lat = 2 * ch01.OMEGA * np.sin(np.deg2rad(p.latitude))
    u_g = -p.differentiate("latitude") * 180 / np.pi / 6.371e6 / (rho * f_lat)
    return ch01.tropd_max_latitude(u_g, u_g.latitude, n=6), float(u_g.max())

for k in (1, -1):
    lat_c, u_max = westerly_centre(nao_msl.mean("time") + k * pattern)
    print(f"principal component 为 {k:+d} 时，地转西风的中心在 {lat_c:.1f}°N，最大 {u_max:.1f} m/s")

fig = plt.figure(figsize=(8, 5.6))
grid = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.12)
proj = ccrs.LambertConformal(central_longitude=-25, central_latitude=50)
ax = fig.add_subplot(grid[0], projection=proj)
pc_kw = dict(transform=ccrs.PlateCarree())
cf = ax.contourf(pattern.longitude, pattern.latitude, pattern, levels=np.arange(-8, 8.5, 1),
                 cmap="RdBu_r", extend="both", **pc_kw)
cs = ax.contour(nao_msl.longitude, nao_msl.latitude, nao_msl.mean("time"),
                levels=np.arange(980, 1040, 8), colors="k", linewidths=0.6, **pc_kw)
ax.clabel(cs, fmt="%d", fontsize=7)
mplot.coastlines(ax, "110m", linewidth=0.5)
for name, (lat, lon) in [("冰岛", ICELAND), ("亚速尔群岛", AZORES)]:
    ax.plot(lon, lat, "k^", ms=7, **pc_kw)
    ax.text(lon + 2, lat - 3, name, fontsize=10, **pc_kw)
ax.set_extent([-90, 39, 22.5, 79.5], crs=ccrs.PlateCarree())
ax.set_title(f"第一 mode：North Atlantic Oscillation，explained variance fraction {frac:.1%}", fontsize=11)
fig.colorbar(cf, ax=ax, shrink=0.85, label="anomaly / hPa")

ax2 = fig.add_subplot(grid[1])
x = np.arange(pc.sizes["time"])
ax2.bar(x, pc, color=np.where(pc > 0, "#d6402a", "#2a78d6"), width=0.8)
years = pc.time.dt.year.values
first = [i for i in x if pc.time.dt.month.values[i] == 1 and years[i] % 5 == 0]
ax2.set_xticks(first, [str(years[i]) for i in first])
ax2.set(xlim=(-1, x[-1] + 1), ylabel="principal component")
ax2.axhline(0, color="k", lw=0.6)
plt.show()
```

empirical orthogonal function 分析把很多个月的 anomaly 场分解成几个固定的空间型，每个空间型叫一个 mode。每个 mode 有一条时间序列，叫 principal component。mode 的 explained variance fraction 是它解释的 anomaly variance 占总 variance 的比例。北大西洋第一 mode 的 explained variance fraction 是 38.6%。它有两个符号相反的中心，一个在冰岛附近，一个在亚速尔附近。这个 mode 就是 North Atlantic Oscillation。

principal component 为正时，Icelandic Low 加深，Azores High 加强。两者之间的 pressure gradient 变大，所以 westerlies 变强，西风的中心也偏北。principal component 为负时，变化正好相反。按 geostrophic wind 估算，principal component 为 +1 和 −1 时，60°W 和 0° 之间平均的西风中心分别在 51.9°N 和 43.7°N。90 个月里，冰岛和亚速尔的 anomaly 有 66 个月符号相反，所以 North Atlantic Oscillation 像一个跷跷板。2009 年 12 月至 2010 年 2 月，三个月的 principal component 都低于 −1.9，那个冬季英国很冷。

本页用两种平均。climatology 是很多年里同一季节的时间平均。zonal mean 是沿同一 latitude 一整圈的平均：

$$
[A](\varphi, p) = \frac{1}{2\pi} \int_0^{2\pi} A(\lambda, \varphi, p)\, \mathrm{d}\lambda
$$

式中 $\lambda$ 是 longitude，$\varphi$ 是 latitude，$p$ 是 pressure。zonal mean 把三维的场变成 latitude 和 pressure 的二维剖面。

meridional mass streamfunction 描述 zonal mean 的 meridional overturning circulation：

$$
\psi(\varphi, p) = \frac{2\pi R_\mathrm{E} \cos\varphi}{g_0} \int_0^{p} [v]\, \mathrm{d}p'
$$

式中 $R_\mathrm{E}$ 是 Earth radius，$g_0$ 是 standard gravity，$[v]$ 是 zonal mean 的 meridional wind。$\psi$ 等于 pressure $p$ 以上的整层空气穿过 latitude $\varphi$ 向北的质量通量，单位是 kg s⁻¹。$\psi$ 的等值线是 meridional overturning circulation 的 streamline。两条等值线的差值等于它们之间流过的质量通量。

在 latitude 向右增大、pressure 向上减小的剖面图上，$\psi > 0$ 表示顺时针的 circulation。北半球的 Hadley cell 是顺时针的，所以它的 $\psi$ 为正。南半球的 Hadley cell 是逆时针的，它的 $\psi$ 为负。

本页术语：

| 术语 | 中文 | 符号 |
|---|---|---|
| general circulation | 大气环流 | — |
| meridional overturning circulation | 经圈环流 | — |
| Hadley cell | Hadley 环流 | — |
| Ferrel cell | Ferrel 环流 | — |
| intertropical convergence zone | 热带辐合带 | ITCZ |
| subtropical high | 副热带高压 | — |
| equatorial low-pressure belt | 赤道低压带 | — |
| subtropical high-pressure belt | 副热带高压带 | — |
| subpolar low-pressure belt | 副极地低压带 | — |
| Icelandic Low | 冰岛低压 | — |
| Azores High | 亚速尔高压 | — |
| Aleutian Low | 阿留申低压 | — |
| North Atlantic Oscillation | 北大西洋涛动 | NAO |
| trade winds | 信风 | — |
| westerlies | 西风带 | — |
| jet stream | 急流 | — |
| subtropical jet | 副热带急流 | — |
| eddy-driven jet | 涡驱动急流 | — |
| storm track | 风暴路径 | — |
| thermal wind | 热成风 | $\mathbf{v}_T$ |
| Coriolis force | Coriolis 力 | — |
| Coriolis parameter | Coriolis 参数 | $f$ |
| Earth's angular velocity | 地球自转角速度 | $\Omega$ |
| f-plane | f 平面 | — |
| inertial oscillation | 惯性振荡 | — |
| inertial circle | 惯性圆 | — |
| inertial period | 惯性周期 | — |
| pressure gradient force | 气压梯度力 | PGF |
| geostrophic balance | 地转平衡 | — |
| geostrophic wind | 地转风 | $\mathbf{v}_g$ |
| climatology | 气候态 | — |
| anomaly | 距平 | — |
| empirical orthogonal function | 经验正交函数 | EOF |
| mode | 模态 | — |
| principal component | 主成分 | PC |
| explained variance fraction | 方差贡献 | — |
| zonal mean | 纬向平均 | $[A]$ |
| zonal wind | 纬向风 | $u$ |
| meridional wind | 经向风 | $v$ |
| meridional mass streamfunction | 经向质量流函数 | $\psi$ |
| Earth radius | 地球半径 | $R_\mathrm{E}$ |
| standard gravity | 标准重力加速度 | $g_0$ |
| mean sea level pressure | 海平面气压 | $p_{\mathrm{msl}}$ |
| brightness temperature | 亮温 | $T_b$ |
| full disk image | 全圆盘图像 | — |
| latitude weighting | 纬度加权 | — |
| root mean squared error | 均方根误差 | RMSE |

## 真实 data

本页的案例是 2025-01-24 00 UTC。这时 extratropical cyclone Éowyn 正在接近爱尔兰。ERA5 的 mean sea level pressure 在它的中心是 941.7 hPa。英国气象局在 2025-01-23 发布了 1 月 24 日的红色大风预警。预警区包括北爱尔兰和苏格兰中部地带，见英国气象局的 [报告](https://www.metoffice.gov.uk/api/assets/file/2025_02_storm_eowynpdf)。下面先看这一时刻的卫星图像，再看 30 年的 climatology。

GOES-16 是美国的静止气象卫星，位于西经 75° 的赤道上空。它的 ABI 仪器每 10 min 拍一张 full disk image。第 13 spectral band 的中心 wavelength 是 10.3 µm，这是一个红外窗区 spectral band。这个 spectral band 测到的是 brightness temperature。云顶越冷，brightness temperature 越低。

```{code-cell} python
goes = d.page_data(ch01.FILES["goes_image"], ch01.goes_image)
tb = goes["brightness_temperature"]  # K, dims (y, x) in m
print(goes.attrs["platform"], goes.attrs["start_time"])
print(dict(tb.sizes), f"brightness temperature: {float(tb.min()):.0f} K 到 {float(tb.max()):.0f} K")
```

```{code-cell} python
#| label: fig-ch01-goes
#| caption: 2025-01-24 00 UTC，GOES-16 full disk image，ABI 第 13 spectral band 的 brightness temperature。红色十字是 Éowyn 的中心。data 来源：NOAA GOES-R 系列，AWS 开放 data。

crs = ch01.goes_crs(goes)
fig = plt.figure(figsize=(6.5, 6.5))
ax = fig.add_subplot(projection=crs)
im = ax.pcolormesh(tb.x, tb.y, tb, cmap="Greys", vmin=200, vmax=300, transform=crs)
mplot.coastlines(ax, "50m", edgecolor="gold", linewidth=0.5)
ax.gridlines(xlocs=range(-180, 181, 30), ylocs=range(-60, 61, 30), color="cyan", linewidth=0.4)
ax.plot(ch01.CASE_LOW_LON, ch01.CASE_LOW_LAT, "r+", ms=14, mew=2, transform=ccrs.PlateCarree())
fig.colorbar(im, ax=ax, shrink=0.7, label="brightness temperature / K")
plt.show()
```

[](#fig-ch01-goes) 里，冷的云顶发白，暖的海面发黑。grid 线每隔 30° 一条。读图时注意下面四点：

- 东太平洋和大西洋的 5°N 附近，各有一条沿 zonal 伸展的窄云带。这就是 intertropical convergence zone。
- 南美洲中部有大片白色的深 convection 云。1 月是南半球的夏季，这里的空气强烈上升。
- 两个半球的副热带海面大多发黑，也就是 clear sky。这里是 Hadley cell 的下沉区。
- 中纬度有长长的斜云带，它们属于 extratropical cyclone。右上角边缘的红色十字就是 Éowyn。

北美洲的陆地在 1 月很冷，所以那里的 brightness temperature 也低。那片灰白色是冷的 surface，不是云。

一天的图像里有很多天气系统。把很多年的 data 平均以后，general circulation 的形态才清楚。[](#fig-ch01-msl) 是 12 月至 2 月的 mean sea level pressure climatology。

```{code-cell} python
#| label: fig-ch01-msl
#| caption: 1990 年至 2019 年 12 月至 2 月，全球 mean sea level pressure 的 climatology，isobar 间隔 4 hPa。黑色十字是 2025-01-24 00 UTC Éowyn 的中心。data 来源：ERA5，WeatherBench 2 climatology。

msl = d.page_data(ch01.FILES["clim_msl"], ch01.clim_msl)["mean_sea_level_pressure"] / 100  # hPa
msl_djf = ch01.cyclic(msl.sel(season="DJF"))
levels = np.arange(984, 1041, 4)
fig = plt.figure(figsize=(9, 4.6))
ax = fig.add_subplot(projection=ccrs.Robinson())
kw = dict(levels=levels, transform=ccrs.PlateCarree())
cf = ax.contourf(msl_djf.longitude, msl_djf.latitude, msl_djf, cmap="RdBu_r", extend="both", **kw)
ax.contour(msl_djf.longitude, msl_djf.latitude, msl_djf, colors="k", linewidths=0.3, **kw)
ax.plot(ch01.CASE_LOW_LON, ch01.CASE_LOW_LAT, "kx", ms=9, mew=2, transform=ccrs.PlateCarree())
mplot.coastlines(ax, "50m", linewidth=0.4)
ax.set_global()
fig.colorbar(cf, ax=ax, shrink=0.8, label="mean sea level pressure / hPa")
plt.show()
```

[](#fig-ch01-msl) 里，subtropical high 是 30°N 和 30°S 附近的红色中心。南半球的 subtropical high 在海洋上排成一条带。南极大陆周围是一圈很深的 low 带。北半球冬季有两个深 low：北大西洋的 Icelandic Low 和北太平洋的 Aleutian Low。西伯利亚的冷陆地上有一个强 high。

Éowyn 的中心在 Icelandic Low 和 Azores High 之间。这两个中心之间的 pressure gradient 维持着北大西洋的 westerlies。青藏高原和南极高原上的 mean sea level pressure 是外推得到的，读图时不要相信这些值。

## dataset

本页的大气 data 来自 ERA5 reanalysis。ERA5 是 ECMWF 制作的第五代全球 reanalysis。它给出 1940 年以来每小时的大气状态，grid spacing 是 0.25°。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

本页用 WeatherBench 2 提供的 ERA5 climatology。这个 climatology 是 1990 年至 2019 年的平均。它对一年里的每一天和每个 6 h 时刻分别求平均，再用 61 天的滑动窗口平滑。grid spacing 是 1.5°，有 13 个 isobaric surface。WeatherBench 2 的论文是 Rasp 等，2024，[doi:10.1029/2023MS004019](https://doi.org/10.1029/2023MS004019)。data 存放在 Google Cloud Storage 上，不需要账户。

本页的季节平均只用这个 climatology 的 19 天。从季节的第一天起，每 5 天取一天。再对这 19 天和 00、06、12、18 UTC 四个时刻求平均。climatology 已经平滑过，所以这 19 天可以代表整个季节。

案例时刻的 mean sea level pressure 来自 ARCO-ERA5。ARCO-ERA5 是 Google 把 ERA5 转成的 Zarr dataset，也不需要账户。

[](#fig-ch01-nao) 的月平均来自 WeatherBench 2 的 ERA5 data。这份 data 每 6 h 一个时刻，grid spacing 是 1.5°。`d.era5_monthly` 对每个月的全部时刻求平均。

卫星图像来自 GOES-16 的 ABI L2 产品。2025-04-07 起，GOES-East 是 GOES-19。本页的案例在这之前，所以用 GOES-16。NOAA 把 GOES data 放在 AWS 的开放 data 桶 `noaa-goes16` 里，不需要账户。ABI 的论文是 Schmit 等，2017，[`doi:10.1175/BAMS-D-15-00230.1`](https://doi.org/10.1175/BAMS-D-15-00230.1)。

本页从这些 data 做了五个小样本，放在 `data/samples/` 里：

| 文件 | 内容 | 大小 |
|---|---|---|
| `ch01-era5-clim-uv-djf-jja.nc` | $u$ 和 $v$ 的两个季节的 climatology，13 个 isobaric surface，3° grid | 1.0 MB |
| `ch01-era5-clim-msl-djf-jja.nc` | mean sea level pressure 的两个季节的 climatology，1.5° grid | 0.1 MB |
| `ch01-era5-msl-20250124t00.nc` | 案例时刻的 mean sea level pressure 和同一日、同一时刻的 climatology，1.5° grid | 0.1 MB |
| `ch01-goes16-c13-20250124t0000.nc` | 案例时刻第 13 spectral band 的 brightness temperature，8 × 8 像元平均 | 0.7 MB |
| `ch01-era5-msl-monthly-djf-natl.nc` | 北大西洋 mean sea level pressure 的月平均，1990 年至 2019 年的 12 月、1 月和 2 月，3° grid | 0.1 MB |

模块 `meteo300.pages.ch01` 里的函数记录了样本的制作方法。在线时，`d.page_data` 运行这些函数。离线时，它读取样本。样本的来源和许可见 `data/samples/ATTRIBUTION-ch01.md`。

其他可选的 dataset：

- NCEP/NCAR reanalysis 1：NOAA PSL 提供它的多年平均场，grid spacing 2.5°，可以直接下载。
- JRA-3Q：日本气象厅的 reanalysis，可以和 ERA5 对比 climatology。
- Meteosat：EUMETSAT 的 geostationary satellite，覆盖欧洲和非洲，下载 data 需要账户。

完整的条目见 [dataset 参考页](../reference/datasets.md)。

## 计算

先选一个季节，再求 zonal mean。climatology 样本里有 12 月至 2 月和 6 月至 8 月两个季节。`.sel(season=SEASON)` 选出一个季节，`xarray.Dataset.mean("longitude")` 求 zonal mean。

```{code-cell} python
SEASON = "DJF"

uv = d.page_data(ch01.FILES["clim_uv"], ch01.clim_uv)
zonal = uv.sel(season=SEASON).mean("longitude")
u_zm = zonal["u_component_of_wind"]  # m s-1, dims (level, latitude)
v_zm = zonal["v_component_of_wind"]  # m s-1
print(dict(u_zm.sizes))
```

然后从 $[v]$ 求 $\psi$。函数 `ch01.mass_streamfunction` 用 `xarray.DataArray.cumulative_integrate` 按梯形公式从 50 hPa 向下积分。这里假设 50 hPa 以上的 meridional 质量通量可以忽略。Earth radius 和 standard gravity 取自 `metpy.constants`。[](#fig-ch01-belts) 的 PSI 指标也用这个函数。

```{code-cell} python
from metpy.constants import earth_avg_radius, g
from metpy.units import units

psi = ch01.mass_streamfunction(v_zm)  # kg s-1, dims (level, latitude)

north = psi.sel(latitude=slice(0, 35)).max()  # Hadley cell of the northern hemisphere
south = psi.sel(latitude=slice(-35, 0)).min()  # Hadley cell of the southern hemisphere
print(f"{SEASON} 北半球 Hadley cell: psi 最大 {float(north):.2e} kg/s")
print(f"{SEASON} 南半球 Hadley cell: psi 最小 {float(south):.2e} kg/s")
```

```{code-cell} python
#| label: fig-ch01-section
#| caption: 1990 年至 2019 年 12 月至 2 月，zonal mean 的 zonal wind 和 meridional mass streamfunction。色块是 zonal wind。黑线是 ψ，单位 10¹⁰ kg s⁻¹，虚线为负。data 来源：ERA5，WeatherBench 2 climatology。

fig, ax = plt.subplots(figsize=(8.5, 4.5))
cf = ax.contourf(u_zm.latitude, u_zm.level, u_zm, levels=np.arange(-40, 45, 5),
                 cmap="RdBu_r", extend="both")
cs = ax.contour(psi.latitude, psi.level, psi / 1e10, colors="k", linewidths=0.8,
                levels=[-20, -15, -10, -5, -2, 2, 5, 10, 15, 20])
ax.clabel(cs, fmt="%d", fontsize=8)
ax.set(ylim=(1000, 50), xlim=(-90, 90), xticks=range(-90, 91, 30),
       xlabel="latitude / °", ylabel="pressure / hPa")
fig.colorbar(cf, ax=ax, label="zonal mean 的 zonal wind / m s$^{-1}$")
plt.show()
```

[](#fig-ch01-section) 是本页最重要的图。10°S 和 30°N 之间有一个顺时针的强 circulation，这是北半球冬季的 Hadley cell。它的上升支在赤道附近和赤道以南，也就是夏半球一侧。南半球的 Hadley cell 很弱。两个半球的 latitude 30° 到 60° 之间，各有一个转向相反的弱 circulation，这就是 Ferrel cell。

zonal wind 的最大值在 200 hPa 附近。北半球冬季的 jet stream 在 30°N，比南半球的 jet stream 更强。热带的低层是东风，也就是 trade winds。中纬度的低层是西风。

下面用手算核对 $\psi$。取 9°N 和 700 hPa 这一点，用梯形公式从 50 hPa 积分到 700 hPa。pint 跟踪单位，最后把结果换成 kg s⁻¹。

```{code-cell} python
lat0, p0 = 9.0, 700
col = v_zm.sel(latitude=lat0, level=slice(50, p0))
v = col.values * units("m/s")
p = col.level.values * units.hPa
layer_sum = (0.5 * (v[1:] + v[:-1]) * np.diff(p)).sum()  # sum of [v] dp over the layers
psi_hand = (2 * np.pi * earth_avg_radius * np.cos(np.deg2rad(lat0)) / g * layer_sum).to("kg/s")
psi_pkg = float(psi.sel(latitude=lat0, level=p0))
assert abs(psi_hand.m - psi_pkg) < 1e-6 * abs(psi_pkg), (psi_hand, psi_pkg)
print(f"xarray: {psi_pkg:.4e} kg/s, 手算: {psi_hand:.4e~P}")
```

两个结果相同，约为 2.1×10¹¹ kg s⁻¹。再粗算一次量级。上层分支的 $[v]$ 约为 2 m s⁻¹，厚约 250 hPa。代入公式得 $2\pi R_\mathrm{E} \cos 9° / g_0 \times 2 \times 25000 \approx 2 \times 10^{11}$ kg s⁻¹。粗算和积分是同一个量级。

最后检查质量守恒和 wind speed。整层的 $[v]$ 积分应接近零，所以 1000 hPa 的 $\psi$ 应接近零。METEO 300 第 1 课 1.2 节说，250 hPa 的 wind speed 约为 50 m s⁻¹。zonal mean 会削弱单个 jet stream 核，所以 zonal mean 的最大风速应该略小。

```{code-cell} python
bottom = float(abs(psi.sel(level=1000)).sel(latitude=slice(-30, 30)).max())
jet = u_zm.sel(level=slice(100, 400))
jet_max = float(jet.max())
where = jet.where(jet == jet.max(), drop=True)
print(f"热带 1000 hPa 的 |psi| 最大 {bottom:.1e} kg/s，是最大值的 {bottom / float(north):.0%}")
print(f"jet stream: {jet_max:.1f} m/s，{float(where.latitude[0]):.0f}°，{int(where.level[0])} hPa")
assert 30 < jet_max < 60
```

1000 hPa 的 $\psi$ 不是零，热带的残差约是最大值的 6%。残差来自三个近似。样本只有 13 个 isobaric surface。积分止于 1000 hPa，不是 surface。高原上的 1000 hPa 在 surface 以下，那里的 wind 是外推值。

## AI 天气连接

mean sea level pressure 和 isobaric surface 上的 wind 都是 AI weather model 的核心变量。GraphCast 和 AIFS 都把它们既当作输入，也当作输出。下表列出本页的量在 dataset 和模型里的名字。

| 量 | ERA5 短名 | WeatherBench 2 名 | GraphCast | AIFS Single v1.0 |
|---|---|---|---|---|
| mean sea level pressure | `msl` | `mean_sea_level_pressure` | 输入和输出 | 输入和输出 |
| zonal wind | `u` | `u_component_of_wind` | 输入和输出，37 个 isobaric surface | 输入和输出，13 个 isobaric surface |
| meridional wind | `v` | `v_component_of_wind` | 输入和输出，37 个 isobaric surface | 输入和输出，13 个 isobaric surface |
| TOA incident solar radiation | `tisr` | `toa_incident_solar_radiation` | 只作输入 | 不用，改用 solar zenith angle 的余弦 `insolation` |
| meridional mass streamfunction | — | — | 不输出，用 $v$ 算 | 不输出，用 $v$ 算 |

GraphCast 的论文是 Lam 等，2023，[doi:10.1126/science.adi2336](https://doi.org/10.1126/science.adi2336)。它的 grid spacing 是 0.25°，时间步长是 6 h。它读入两个时刻的大气状态，forecast 6 h 后的状态。

AIFS 是 ECMWF 的 AI weather model，见 Lang 等，2024，[arXiv:2406.01465](https://arxiv.org/abs/2406.01465)。AIFS Single v1.0 的 grid spacing 约为 31 km，用 13 个 isobaric surface。2026-05-12 起，ECMWF 业务运行 AIFS Single v2。它增加了 10 hPa，共 14 个 isobaric surface。本页样本的 13 个 isobaric surface 和 AIFS Single v1.0 的完全相同。

GraphCast 把 TOA incident solar radiation 当作输入。AIFS 改用 solar zenith angle 的余弦 `insolation`，见 [anemoi 的文档](https://anemoi.readthedocs.io/projects/datasets/en/latest/building/sources/forcings.html)。两者都随 latitude 和季节变化，这个分布驱动 general circulation。模型从训练 data 里学到 Hadley cell 和 jet stream，不需要显式的 circulation 方程。

WeatherBench 2 是评估 AI weather model 的公共框架。它用 ERA5 当作真值，用本页的同一个 climatology 当作基线 forecast。climatology forecast 每天都给出这一天的多年平均值。一个模型的误差小于 climatology 的误差，这个模型才有技巧。WeatherBench 2 的 RMSE 用 latitude weighting，权重正比于每行 grid point 的面积。

下面算一次 climatology forecast 的误差。真值是 ERA5 在 2025-01-24 00 UTC 的 mean sea level pressure。anomaly 等于真值减去 climatology。

```{code-cell} python
case = d.page_data(ch01.FILES["case_msl"], ch01.case_msl)
anom = (case["mean_sea_level_pressure"] - case["mean_sea_level_pressure_climatology"]) / 100
w = ch01.wb2_latitude_weights(anom.latitude)
rmse = float(np.sqrt((anom**2 * w).mean()))

# 手算核对：latitude weighting 近似于 cos(latitude) 加权
cos_w = np.cos(np.deg2rad(anom.latitude))
rmse_cos = float(np.sqrt((anom**2).weighted(cos_w).mean()))
assert abs(rmse - rmse_cos) < 0.05, (rmse, rmse_cos)
print(f"climatology forecast 的 mean sea level pressure RMSE: {rmse:.1f} hPa，cos 加权: {rmse_cos:.1f} hPa")
print(f"最低 anomaly: {float(anom.min()):.0f} hPa")
```

```{code-cell} python
#| label: fig-ch01-anom
#| caption: 2025-01-24 00 UTC，全球 mean sea level pressure 的 anomaly。anomaly 等于 ERA5 减去 1990 年至 2019 年同一日、同一时刻的 climatology。data 来源：ERA5，ARCO-ERA5 和 WeatherBench 2 climatology。

anom_c = ch01.cyclic(anom)
fig = plt.figure(figsize=(9, 4.6))
ax = fig.add_subplot(projection=ccrs.Robinson())
cf = ax.contourf(anom_c.longitude, anom_c.latitude, anom_c, levels=np.arange(-60, 61, 10),
                 cmap="RdBu_r", extend="both", transform=ccrs.PlateCarree())
mplot.coastlines(ax, "50m", linewidth=0.4)
ax.set_global()
fig.colorbar(cf, ax=ax, shrink=0.8, label="mean sea level pressure anomaly / hPa")
plt.show()
```

这一时刻，climatology forecast 的全球 RMSE 约为 7.9 hPa。[](#fig-ch01-anom) 里最深的蓝色中心就是 Éowyn，anomaly 约为 −67 hPa。热带的 anomaly 很小，误差主要来自中纬度的天气系统。AI weather model 的工作就是 forecast 这些 anomaly。

分析师可以用本页的计算检查 AI weather model 的长时效 forecast。取同一个 forecast 的第 1 天和第 10 天，对 $v$ 和 $u$ 做 zonal mean，再算 $\psi$。比较 Hadley cell 的最大值、jet stream 的 latitude 和强度。两天的值相差很大时，模型的大尺度 circulation 可能在漂移。

## 练习

:::{exercise}
:label: ex-ch01-1

把 [](#fig-ch01-section) 上方代码里的 `SEASON = "DJF"` 改成 `SEASON = "JJA"`，然后重新运行本节的代码。哪个半球的 Hadley cell 更强？两个半球的 jet stream 在哪个 latitude，wind speed 是多少？
:::

:::{solution} ex-ch01-1
:class: dropdown

6 月至 8 月，南半球的 Hadley cell 更强。它的 $\psi$ 最小值约为 −2.4×10¹¹ kg s⁻¹，位置在 3°S 附近。南半球的 jet stream 在 30°S、200 hPa，wind speed 约 42 m s⁻¹。北半球的 jet stream 移到 42°N，wind speed 只有约 22 m s⁻¹。规律是：强的 Hadley cell 在冬半球，它的上升支在夏半球。
:::

:::{exercise}
:label: ex-ch01-2

粗算 Hadley cell 翻转一次热带大气需要多长时间。取 surface pressure 1000 hPa，$g_0 = 9.81$ m s⁻²，$R_\mathrm{E} = 6.371 \times 10^6$ m。30°S 和 30°N 之间的面积是 $2\pi R_\mathrm{E}^2$。用 $\psi$ 的最大值 2×10¹¹ kg s⁻¹ 作质量通量。
:::

:::{solution} ex-ch01-2
:class: dropdown

单位面积的空气质量是 $p_s / g_0 = 10^5 / 9.81 \approx 1.0 \times 10^4$ kg m⁻²。热带的面积是 $2\pi R_\mathrm{E}^2 \approx 2.6 \times 10^{14}$ m²。热带大气的质量约为 $2.6 \times 10^{18}$ kg。翻转时间约为 $2.6 \times 10^{18} / (2 \times 10^{11}) \approx 1.3 \times 10^{7}$ s，也就是约 150 天。METEO 300 第 12 课 12.1 节说，大气用几个月把空气从赤道运到极地。这个粗算和它的量级一致。
:::

:::{exercise}
:label: ex-ch01-3

改写计算 `rmse` 的代码，只算北大西洋的 climatology forecast 误差。用 `anom.sel(latitude=slice(30, 70), longitude=slice(-60, 0))` 取出这个区域。权重要用这个区域的 latitude 重新算。再用 `slice(-20, 20)` 只算热带。比较三个 RMSE。
:::

:::{solution} ex-ch01-3
:class: dropdown

```python
box = anom.sel(latitude=slice(30, 70), longitude=slice(-60, 0))
w_box = ch01.wb2_latitude_weights(box.latitude)
print(float(np.sqrt((box**2 * w_box).mean())))
```

北大西洋、热带和全球的 RMSE 分别约为 17.2 hPa、1.7 hPa 和 7.9 hPa。热带的 mean sea level pressure 每天变化很小，climatology 已经接近真值。中纬度的 extratropical cyclone 使 pressure 偏离 climatology 几十 hPa。所以 AI weather model 在中纬度的 mean sea level pressure 误差最大，也最值得检查。
:::
