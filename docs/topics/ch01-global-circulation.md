---
title: 大气环流
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

太阳加热低纬度多，加热高纬度少。低纬度吸收的短波辐射多于射出长波辐射，高纬度正好相反。两者大约在纬度 35° 附近相等。大气和海洋把多余的热量从低纬度运到高纬度。大气环流是完成这项输送的大尺度运动的平均形态。

赤道附近的空气受热上升，形成热带辐合带。上升的空气在对流层上部流向两极。它在纬度 30° 附近下沉，形成副热带高压。下沉的空气在低层流回赤道。这个闭合的经圈环流叫 Hadley 环流。

Coriolis 力使运动的空气在北半球向右偏，在南半球向左偏。[](#fig-ch01-inertial) 用一个只受 Coriolis 力的气块说明这一点。

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch01-inertial
#| caption: f 平面上只受 Coriolis 力的气块的轨迹。气块从原点出发，初速度 10 m s⁻¹，方向向东。左图在 50°N，右图在 50°S。蓝色箭头是每隔四分之一个惯性周期的速度，红色箭头是出发时的 Coriolis 力。数据来源：本页的数值积分。

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

from meteo300 import data as d
from meteo300 import plot as mplot
from meteo300.pages import ch01

U0, LAT = 10.0, 50.0  # initial speed towards the east (m s-1), latitude (degrees)
f = 2 * ch01.OMEGA * np.sin(np.deg2rad(LAT))  # Coriolis parameter, s-1
period = 2 * np.pi / f / 3600  # inertial period, h
radius = U0 / f / 1000  # radius of the inertial circle, km
print(f"50°N: f = {f:.3e} s-1，惯性周期 {period:.1f} h，惯性圆半径 {radius:.1f} km")

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
    ax.text(6, -side * 30, "Coriolis 力", color="#d6402a", va="center")
    ax.plot(0, 0, "ko", ms=5)
    hemi = "北半球 50°N：向右偏，顺时针转" if lat > 0 else "南半球 50°S：向左偏，逆时针转"
    ax.set_title(hemi, fontsize=11)
    ax.text(0.5, 0.5, f"惯性周期 {period:.1f} h\n半径 {radius:.1f} km",
            transform=ax.transAxes, ha="center", va="center", color="0.3")
    ax.set(aspect="equal", xlim=(-130, 130), xlabel="向东的距离 / km")
    ax.set_ylim(sorted([-side * 200, side * 40]))
    ax.grid(color="0.92")
axes[0].set_ylabel("向北的距离 / km")
fig.tight_layout()
plt.show()
```

[](#fig-ch01-inertial) 里的气块只受 Coriolis 力。Coriolis 力总是垂直于速度，所以它只改变风向，不改变风速。北半球的气块不断向右偏，沿顺时针转圈。南半球的气块不断向左偏，沿逆时针转圈。这种运动叫惯性振荡，气块画出的圆叫惯性圆。

在 50°N，Coriolis 参数 $f = 2\Omega\sin\varphi \approx 1.12 \times 10^{-4}\ \mathrm{s^{-1}}$。式中 $\Omega$ 是地球自转角速度，$\varphi$ 是纬度。气块转一圈的时间是惯性周期 $2\pi/|f|$，约 15.6 h。惯性圆的半径等于初速度除以 $|f|$，约 89.5 km。圆的直径只跨约 1.6° 纬度，所以本图把 $f$ 当作常数，这个近似叫 f 平面。真实大气里还有气压梯度力，它常常和 Coriolis 力接近平衡，这就是地转平衡。

在两个半球，Hadley 环流高空流向极地的空气都偏向东。Hadley 环流的极地一侧因此有很强的西风，这就是副热带急流。低层流回赤道的空气都偏向西，形成东北信风和东南信风。

副热带急流和北大西洋的西风带不是同一支风。纬向平均的副热带急流只在对流层上部，中心在 30°N 和 200 hPa，纬向风约 42 m s⁻¹。它的正下方是副热带高压，1000 hPa 上纬向平均的纬向风只有约 1 m s⁻¹。西风带从地面一直伸到对流层顶，大约位于纬度 35° 和 65° 之间。温带气旋把西风动量输送到中纬度，并把它向下传到地面。Coriolis 力还使中纬度低层流向极地的空气偏向东，这也维持低层的西风。

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch01-natl-u
#| caption: 1990 年至 2019 年 12 月至 2 月，北大西洋扇区 60°W 至 0° 平均的纬向风。黑线是 0 m s⁻¹ 的等值线。数据来源：ERA5，WeatherBench 2 气候态。

uv_djf = d.page_data(ch01.FILES["clim_uv"], ch01.clim_uv).sel(season="DJF")
u_djf = uv_djf["u_component_of_wind"]  # m s-1, dims (level, latitude, longitude)
u_natl = u_djf.sel(longitude=slice(-60, 0)).mean("longitude").sel(latitude=slice(0, 81))
u_zm_djf = u_djf.mean("longitude")

# Latitude of the maximum, by Eq. (1) of the TropD paper with n = 30 (see below).
upper = u_natl.sel(level=200, latitude=slice(0, 33))  # subtropical jet
low = u_natl.sel(level=850, latitude=slice(30, 70))  # eddy-driven jet
lat_stj = ch01.tropd_max_latitude(upper, upper.latitude, n=30)
lat_edj = ch01.tropd_max_latitude(low, low.latitude, n=30)
print(f"北大西洋扇区，200 hPa 的副热带急流：{lat_stj:.0f}°N，{float(upper.max()):.1f} m/s")
print(f"北大西洋扇区，850 hPa 的涡驱动急流：{lat_edj:.0f}°N，{float(low.max()):.1f} m/s")
print(f"纬向平均，30°N 的纬向风：200 hPa {float(u_zm_djf.sel(level=200, latitude=30, method='nearest')):.1f} m/s，"
      f"1000 hPa {float(u_zm_djf.sel(level=1000, latitude=30, method='nearest')):.1f} m/s")

fig, ax = plt.subplots(figsize=(7, 3.8))
cf = ax.contourf(u_natl.latitude, u_natl.level, u_natl, levels=np.arange(-10, 32.5, 2.5),
                 cmap="RdBu_r", extend="both")
ax.contour(u_natl.latitude, u_natl.level, u_natl, levels=[0], colors="k", linewidths=1)
ax.annotate("副热带急流", (lat_stj, 200), xytext=(25, 420), arrowprops=dict(arrowstyle="-"))
ax.annotate("涡驱动急流", (lat_edj, 850), xytext=(56, 520), arrowprops=dict(arrowstyle="-"))
ax.set(ylim=(1000, 100), xlim=(0, 80), xticks=range(0, 81, 10), xlabel="纬度 / °N", ylabel="气压 / hPa")
cbar = fig.colorbar(cf, ax=ax)
# DejaVu Sans draws the superscript minus, which some CJK fonts lack.
cbar.set_label("纬向风 / m s⁻¹", fontfamily=[plt.rcParams["font.sans-serif"][0], "DejaVu Sans"])
plt.show()
```

[](#fig-ch01-natl-u) 只在北大西洋扇区里求经度平均。对流层上部有两个风速中心。偏南的中心在 18°N 和 200 hPa 附近，这是副热带急流。偏北的中心在 45°N 附近，它从对流层顶一直伸到地面，这是涡驱动急流。温带气旋维持涡驱动急流。它的低层部分就是北大西洋的西风带，850 hPa 的纬向风在 47°N 附近最强。

北大西洋低层的西风带位于亚速尔高压和冰岛低压之间。它是这两个气压中心之间的气压梯度对应的地转风。英国在这条西风带里，所以冬季常有西风和温带气旋。纬向平均把不同经度的急流平均在一起。所以 [](#fig-ch01-section) 的北半球只有一个高空风速中心，它在 30°N 附近。

中纬度的温度向极地降低。METEO 300 第 10 课 10.11 节用热成风说明，这个温度梯度使西风随几何高度增大。所以西风带的风在对流层顶附近最强。中纬度的热量主要由温带气旋和反气旋输送。纬向平均以后，这些天气系统的作用表现为 Ferrel 环流。Ferrel 环流的转向和 Hadley 环流相反。

地面上，这些环流对应几条气压带。赤道附近是赤道低压带，纬度 30° 附近是副热带高压带，纬度 60° 附近是副极地低压带。[](#fig-ch01-belts) 是 12 月至 2 月纬向平均的海平面气压。

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch01-belts
#| caption: 1990 年至 2019 年 12 月至 2 月，纬向平均的海平面气压。红色虚线是 PSL 指标，蓝色点线是 PSI 指标，两种指标都用 TropD 的方法算出。黄色区域是两个 Hadley 环流。数据来源：ERA5，WeatherBench 2 气候态。

msl_all = d.page_data(ch01.FILES["clim_msl"], ch01.clim_msl)["mean_sea_level_pressure"]
msl_zm = msl_all.sel(season="DJF").mean("longitude") / 100  # hPa
psi_djf = ch01.mass_streamfunction(uv_djf["v_component_of_wind"].mean("longitude"))  # kg s-1
psl = ch01.tropd_psl(msl_zm)  # subtropical maximum of msl
edge = ch01.tropd_psi(psi_djf)  # poleward edge of each Hadley cell
print(f"PSL 指标：{psl['N']:.1f}°N，{-psl['S']:.1f}°S")
print(f"PSI 指标：{edge['N']:.1f}°N，{-edge['S']:.1f}°S")

fig, ax = plt.subplots(figsize=(8, 3.9))
ax.axvspan(edge["S"], edge["N"], color="#f6e7b4", label="Hadley 环流")
ax.axvspan(-90, -70, color="0.88", label="南极大陆，外推值")
ax.plot(msl_zm.latitude, msl_zm, color="k", lw=2)
for h in "NS":
    ax.axvline(psl[h], color="#d6402a", ls="--", label="PSL 指标" if h == "N" else None)
    ax.axvline(edge[h], color="#2a78d6", ls=":", lw=2, label="PSI 指标" if h == "N" else None)

belts = [  # name, latitude band (degrees), "min" or "max", text offset in points
    ("赤道低压带", (-15, 15), "min", (0, -28)),
    ("副热带高压带", (15, 50), "max", (48, 8)),
    ("副热带高压带", (-50, -15), "max", (-48, 8)),
    ("副极地低压带", (45, 80), "min", (10, -26)),
    ("副极地低压带", (-80, -45), "min", (40, 0)),
]
for name, (lo, hi), kind, offset in belts:
    band = msl_zm.sel(latitude=slice(lo, hi))
    i = int(np.argmin(band.values) if kind == "min" else np.argmax(band.values))
    lat_i, p_i = float(band.latitude[i]), float(band[i])
    ax.plot(lat_i, p_i, "o", color="k", ms=4)
    ax.annotate(f"{name}\n{p_i:.0f} hPa", (lat_i, p_i), xytext=offset, textcoords="offset points",
                ha="center", va="center", fontsize=9)
ax.set_xticks(range(-90, 91, 30), ["90°S", "60°S", "30°S", "0°", "30°N", "60°N", "90°N"])
ax.set(xlim=(-90, 90), ylim=(980, 1028), xlabel="纬度", ylabel="海平面气压 / hPa")
ax.legend(loc="lower right", fontsize=8, ncols=2, framealpha=0.9)
plt.show()
```

[](#fig-ch01-belts) 里，赤道低压带很宽，约 1010 hPa。北半球的副热带高压带在 30°N 附近，约 1020 hPa。南半球的副热带高压带在 36°S 附近，约 1017 hPa。南半球的副极地低压带在 64.5°S 附近，约 986 hPa，它环绕南极大陆。北半球的副极地低压带在 60°N 附近，只有约 1012 hPa。纬向平均把冰岛低压、阿留申低压和大陆上的高压平均在一起，所以这条低压带很浅。

图中的竖线用 TropD 的方法算出。TropD 是 Adam 等在 2018 年发表的一套计算热带宽度的方法，论文见 <https://doi.org/10.5194/gmd-11-4339-2018>。PSL 指标是纬度 15° 和 60° 之间海平面气压最大的纬度。PSI 指标是 Hadley 环流的边界，也就是 500 hPa 的 $\psi$ 从热带的极值向极地第一次变号的纬度。本节后面定义 $\psi$。函数 `ch01.tropd_psl` 和 `ch01.tropd_psi` 按论文的定义计算这两种指标。

12 月至 2 月，PSL 指标是 31.4°N 和 34.8°S，PSI 指标是 28.9°N 和 35.1°S。两种指标在南半球只差 0.3°，在北半球差 2.5°。副热带高压带在 Hadley 环流的下沉支附近，所以两种指标接近。南极大陆和青藏高原上的海平面气压是外推值。灰色区域里的曲线不可信。

海陆分布把北半球的气压带分成几个中心。冬季的北大西洋北部有冰岛低压，南部有亚速尔高压。两个中心之间是强西风和风暴路径，英国正好在这里。这两个中心的强弱每个月都在变，而且常常反向变化。[](#fig-ch01-nao) 用经验正交函数找出这种变化。

```{code-cell} python
:tags: [hide-input]
#| label: fig-ch01-nao
#| caption: 1990 年至 2019 年 12 月、1 月和 2 月，北大西洋海平面气压月平均距平的第一模态。上图的色块是主成分增加一个标准差时的距平，黑线是这 90 个月的平均海平面气压。下图是标准化的主成分。数据来源：ERA5，WeatherBench 2。

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
print(f"第一模态的方差贡献：{frac:.1%}")
print(f"冰岛 {float(at(pattern, ICELAND)):+.1f} hPa，亚速尔 {float(at(pattern, AZORES)):+.1f} hPa，"
      f"两地距平符号相反的月数：{opposite} / {nao_anom.sizes['time']}")

# Geostrophic zonal wind at sea level, mean of 60°W to 0°: u_g = -(dp/dy) / (rho f).
def westerly_centre(p_hpa, rho=1.25):
    p = p_hpa.sel(longitude=slice(-60, 0)).mean("longitude").sel(latitude=slice(30, 75)) * 100
    f_lat = 2 * ch01.OMEGA * np.sin(np.deg2rad(p.latitude))
    u_g = -p.differentiate("latitude") * 180 / np.pi / 6.371e6 / (rho * f_lat)
    return ch01.tropd_max_latitude(u_g, u_g.latitude, n=6), float(u_g.max())

for k in (1, -1):
    lat_c, u_max = westerly_centre(nao_msl.mean("time") + k * pattern)
    print(f"主成分为 {k:+d} 时，地转西风的中心在 {lat_c:.1f}°N，最大 {u_max:.1f} m/s")

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
ax.set_title(f"第一模态：北大西洋涛动，方差贡献 {frac:.1%}", fontsize=11)
fig.colorbar(cf, ax=ax, shrink=0.85, label="距平 / hPa")

ax2 = fig.add_subplot(grid[1])
x = np.arange(pc.sizes["time"])
ax2.bar(x, pc, color=np.where(pc > 0, "#d6402a", "#2a78d6"), width=0.8)
years = pc.time.dt.year.values
first = [i for i in x if pc.time.dt.month.values[i] == 1 and years[i] % 5 == 0]
ax2.set_xticks(first, [str(years[i]) for i in first])
ax2.set(xlim=(-1, x[-1] + 1), ylabel="主成分")
ax2.axhline(0, color="k", lw=0.6)
plt.show()
```

经验正交函数分析把很多个月的距平场分解成几个固定的空间型，每个空间型叫一个模态。每个模态有一条时间序列，叫主成分。模态的方差贡献是它解释的距平方差占总方差的比例。北大西洋第一模态的方差贡献是 38.6%。它有两个符号相反的中心，一个在冰岛附近，一个在亚速尔附近。这个模态就是北大西洋涛动。

主成分为正时，冰岛低压加深，亚速尔高压加强。两者之间的气压梯度变大，所以西风带变强，西风的中心也偏北。主成分为负时，变化正好相反。按地转风估算，主成分为 +1 和 −1 时，60°W 和 0° 之间平均的西风中心分别在 51.9°N 和 43.7°N。90 个月里，冰岛和亚速尔的距平有 66 个月符号相反，所以北大西洋涛动像一个跷跷板。2009 年 12 月至 2010 年 2 月，三个月的主成分都低于 −1.9，那个冬季英国很冷。

本页用两种平均。气候态是很多年里同一季节的时间平均。纬向平均是沿同一纬度一整圈的平均：

$$
[A](\varphi, p) = \frac{1}{2\pi} \int_0^{2\pi} A(\lambda, \varphi, p)\, \mathrm{d}\lambda
$$

式中 $\lambda$ 是经度，$\varphi$ 是纬度，$p$ 是气压。纬向平均把三维的场变成纬度和气压的二维剖面。

经向质量流函数描述纬向平均的经圈环流：

$$
\psi(\varphi, p) = \frac{2\pi R_\mathrm{E} \cos\varphi}{g_0} \int_0^{p} [v]\, \mathrm{d}p'
$$

式中 $R_\mathrm{E}$ 是地球半径，$g_0$ 是标准重力加速度，$[v]$ 是纬向平均的经向风。$\psi$ 等于气压 $p$ 以上的整层空气穿过纬度 $\varphi$ 向北的质量通量，单位是 kg s⁻¹。$\psi$ 的等值线是经圈环流的流线。两条等值线的差值等于它们之间流过的质量通量。

在纬度向右增大、气压向上减小的剖面图上，$\psi > 0$ 表示顺时针的环流。北半球的 Hadley 环流是顺时针的，所以它的 $\psi$ 为正。南半球的 Hadley 环流是逆时针的，它的 $\psi$ 为负。

本页术语：

| 中文术语 | English term | 符号 |
|---|---|---|
| 大气环流 | general circulation | — |
| 经圈环流 | meridional overturning circulation | — |
| Hadley 环流 | Hadley cell | — |
| Ferrel 环流 | Ferrel cell | — |
| 热带辐合带 | intertropical convergence zone | ITCZ |
| 副热带高压 | subtropical high | — |
| 赤道低压带 | equatorial low-pressure belt | — |
| 副热带高压带 | subtropical high-pressure belt | — |
| 副极地低压带 | subpolar low-pressure belt | — |
| 冰岛低压 | Icelandic Low | — |
| 亚速尔高压 | Azores High | — |
| 阿留申低压 | Aleutian Low | — |
| 北大西洋涛动 | North Atlantic Oscillation | NAO |
| 信风 | trade winds | — |
| 西风带 | westerlies | — |
| 急流 | jet stream | — |
| 副热带急流 | subtropical jet | — |
| 涡驱动急流 | eddy-driven jet | — |
| 风暴路径 | storm track | — |
| 热成风 | thermal wind | $\mathbf{v}_T$ |
| Coriolis 力 | Coriolis force | — |
| Coriolis 参数 | Coriolis parameter | $f$ |
| 地球自转角速度 | Earth's angular velocity | $\Omega$ |
| f 平面 | f-plane | — |
| 惯性振荡 | inertial oscillation | — |
| 惯性圆 | inertial circle | — |
| 惯性周期 | inertial period | — |
| 气压梯度力 | pressure gradient force | PGF |
| 地转平衡 | geostrophic balance | — |
| 地转风 | geostrophic wind | $\mathbf{v}_g$ |
| 气候态 | climatology | — |
| 距平 | anomaly | — |
| 经验正交函数 | empirical orthogonal function | EOF |
| 模态 | mode | — |
| 主成分 | principal component | PC |
| 方差贡献 | explained variance fraction | — |
| 纬向平均 | zonal mean | $[A]$ |
| 纬向风 | zonal wind | $u$ |
| 经向风 | meridional wind | $v$ |
| 经向质量流函数 | meridional mass streamfunction | $\psi$ |
| 地球半径 | Earth radius | $R_\mathrm{E}$ |
| 标准重力加速度 | standard gravity | $g_0$ |
| 海平面气压 | mean sea level pressure | $p_{\mathrm{msl}}$ |
| 亮温 | brightness temperature | $T_b$ |
| 全圆盘图像 | full disk image | — |
| 纬度加权 | latitude weighting | — |
| 均方根误差 | root mean squared error | RMSE |

## 真实数据

本页的案例是 2025-01-24 00 UTC。这时温带气旋 Éowyn 正在接近爱尔兰。ERA5 的海平面气压在它的中心是 941.7 hPa。这一天，英国气象局对北爱尔兰和苏格兰中部发布了红色大风预警。下面先看这一时刻的卫星图像，再看 30 年的气候态。

GOES-16 是美国的静止气象卫星，位于西经 75° 的赤道上空。它的 ABI 仪器每 10 min 拍一张全圆盘图像。第 13 波段的中心波长是 10.3 µm，这是一个红外窗区波段。这个波段测到的是亮温。云顶越冷，亮温越低。

```{code-cell} python
goes = d.page_data(ch01.FILES["goes_image"], ch01.goes_image)
tb = goes["brightness_temperature"]  # K, dims (y, x) in m
print(goes.attrs["platform"], goes.attrs["start_time"])
print(dict(tb.sizes), f"亮温: {float(tb.min()):.0f} K 到 {float(tb.max()):.0f} K")
```

```{code-cell} python
#| label: fig-ch01-goes
#| caption: 2025-01-24 00 UTC，GOES-16 全圆盘图像，ABI 第 13 波段的亮温。红色十字是 Éowyn 的中心。数据来源：NOAA GOES-R 系列，AWS 开放数据。

crs = ch01.goes_crs(goes)
fig = plt.figure(figsize=(6.5, 6.5))
ax = fig.add_subplot(projection=crs)
im = ax.pcolormesh(tb.x, tb.y, tb, cmap="Greys", vmin=200, vmax=300, transform=crs)
mplot.coastlines(ax, "50m", edgecolor="gold", linewidth=0.5)
ax.gridlines(xlocs=range(-180, 181, 30), ylocs=range(-60, 61, 30), color="cyan", linewidth=0.4)
ax.plot(ch01.CASE_LOW_LON, ch01.CASE_LOW_LAT, "r+", ms=14, mew=2, transform=ccrs.PlateCarree())
fig.colorbar(im, ax=ax, shrink=0.7, label="亮温 / K")
plt.show()
```

[](#fig-ch01-goes) 里，冷的云顶发白，暖的海面发黑。网格线每隔 30° 一条。读图时注意下面四点：

- 东太平洋和大西洋的 5°N 附近，各有一条沿纬向伸展的窄云带。这就是热带辐合带。
- 南美洲中部有大片白色的深对流云。1 月是南半球的夏季，这里的空气强烈上升。
- 两个半球的副热带海面大多发黑，也就是晴空。这里是 Hadley 环流的下沉区。
- 中纬度有长长的斜云带，它们属于温带气旋。右上角边缘的红色十字就是 Éowyn。

北美洲的陆地在 1 月很冷，所以那里的亮温也低。那片灰白色是冷的地面，不是云。

一天的图像里有很多天气系统。把很多年的数据平均以后，大气环流的形态才清楚。[](#fig-ch01-msl) 是 12 月至 2 月的海平面气压气候态。

```{code-cell} python
#| label: fig-ch01-msl
#| caption: 1990 年至 2019 年 12 月至 2 月，全球海平面气压的气候态，等压线间隔 4 hPa。黑色十字是 2025-01-24 00 UTC Éowyn 的中心。数据来源：ERA5，WeatherBench 2 气候态。

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
fig.colorbar(cf, ax=ax, shrink=0.8, label="海平面气压 / hPa")
plt.show()
```

[](#fig-ch01-msl) 里，副热带高压是 30°N 和 30°S 附近的红色中心。南半球的副热带高压在海洋上排成一条带。南极大陆周围是一圈很深的低压带。北半球冬季有两个深低压：北大西洋的冰岛低压和北太平洋的阿留申低压。西伯利亚的冷陆地上有一个强高压。

Éowyn 的中心在冰岛低压和亚速尔高压之间。这两个中心之间的气压梯度维持着北大西洋的西风带。青藏高原和南极高原上的海平面气压是外推得到的，读图时不要相信这些值。

## 数据集

本页的大气数据来自 ERA5 再分析。ERA5 是 ECMWF 制作的第五代全球再分析。它给出 1940 年以来每小时的大气状态，网格间距是 0.25°。ERA5 的论文是 Hersbach 等，2020，[doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。ERA5 以 CC BY 4.0 许可发布。

本页用 WeatherBench 2 提供的 ERA5 气候态。这个气候态是 1990 年至 2019 年的平均。它对一年里的每一天和每个 6 h 时刻分别求平均，再用 61 天的滑动窗口平滑。网格间距是 1.5°，有 13 个等压面。WeatherBench 2 的论文是 Rasp 等，2024，[doi:10.1029/2023MS004019](https://doi.org/10.1029/2023MS004019)。数据存放在 Google Cloud Storage 上，不需要账号。

本页的季节平均只用这个气候态的 19 天。从季节的第一天起，每 5 天取一天。再对这 19 天和 00、06、12、18 UTC 四个时刻求平均。气候态已经平滑过，所以这 19 天可以代表整个季节。

案例时刻的海平面气压来自 ARCO-ERA5。ARCO-ERA5 是 Google 把 ERA5 转成的 Zarr 数据集，也不需要账号。

[](#fig-ch01-nao) 的月平均来自 WeatherBench 2 的 ERA5 数据。这份数据每 6 h 一个时刻，网格间距是 1.5°。`d.era5_monthly` 对每个月的全部时刻求平均。

卫星图像来自 GOES-16 的 ABI L2 产品。2025-04-07 起，GOES-East 是 GOES-19。本页的案例在这之前，所以用 GOES-16。NOAA 把 GOES 数据放在 AWS 的开放数据桶 `noaa-goes16` 里，不需要账号。ABI 的论文是 Schmit 等，2017，<https://doi.org/10.1175/BAMS-D-15-00230.1>。

本页从这些数据做了五个小样本，放在 `data/samples/` 里：

| 文件 | 内容 | 大小 |
|---|---|---|
| `ch01-era5-clim-uv-djf-jja.nc` | $u$ 和 $v$ 的两个季节的气候态，13 个等压面，3° 网格 | 1.0 MB |
| `ch01-era5-clim-msl-djf-jja.nc` | 海平面气压的两个季节的气候态，1.5° 网格 | 0.1 MB |
| `ch01-era5-msl-20250124t00.nc` | 案例时刻的海平面气压和同一日、同一时刻的气候态，1.5° 网格 | 0.1 MB |
| `ch01-goes16-c13-20250124t0000.nc` | 案例时刻第 13 波段的亮温，8 × 8 像元平均 | 0.7 MB |
| `ch01-era5-msl-monthly-djf-natl.nc` | 北大西洋海平面气压的月平均，1990 年至 2019 年的 12 月、1 月和 2 月，3° 网格 | 0.1 MB |

模块 `meteo300.pages.ch01` 里的函数记录了样本的制作方法。在线时，`d.page_data` 运行这些函数。离线时，它读取样本。样本的来源和许可见 `data/samples/ATTRIBUTION-ch01.md`。

其他可选的数据集：

- NCEP/NCAR 再分析 1：NOAA PSL 提供它的多年平均场，网格间距 2.5°，可以直接下载。
- JRA-3Q：日本气象厅的再分析，可以和 ERA5 对比气候态。
- Meteosat：EUMETSAT 的静止卫星，覆盖欧洲和非洲，下载数据需要账号。

完整的条目见 [数据集参考页](../reference/datasets.md)。

## 计算

先选一个季节，再求纬向平均。气候态样本里有 12 月至 2 月和 6 月至 8 月两个季节。`.sel(season=SEASON)` 选出一个季节，`xarray.Dataset.mean("longitude")` 求纬向平均。

```{code-cell} python
SEASON = "DJF"

uv = d.page_data(ch01.FILES["clim_uv"], ch01.clim_uv)
zonal = uv.sel(season=SEASON).mean("longitude")
u_zm = zonal["u_component_of_wind"]  # m s-1, dims (level, latitude)
v_zm = zonal["v_component_of_wind"]  # m s-1
print(dict(u_zm.sizes))
```

然后从 $[v]$ 求 $\psi$。函数 `ch01.mass_streamfunction` 用 `xarray.DataArray.cumulative_integrate` 按梯形公式从 50 hPa 向下积分。这里假设 50 hPa 以上的经向质量通量可以忽略。地球半径和标准重力加速度取自 `metpy.constants`。[](#fig-ch01-belts) 的 PSI 指标也用这个函数。

```{code-cell} python
from metpy.constants import earth_avg_radius, g
from metpy.units import units

psi = ch01.mass_streamfunction(v_zm)  # kg s-1, dims (level, latitude)

north = psi.sel(latitude=slice(0, 35)).max()  # Hadley cell of the northern hemisphere
south = psi.sel(latitude=slice(-35, 0)).min()  # Hadley cell of the southern hemisphere
print(f"{SEASON} 北半球 Hadley 环流: psi 最大 {float(north):.2e} kg/s")
print(f"{SEASON} 南半球 Hadley 环流: psi 最小 {float(south):.2e} kg/s")
```

```{code-cell} python
#| label: fig-ch01-section
#| caption: 1990 年至 2019 年 12 月至 2 月，纬向平均的纬向风和经向质量流函数。色块是纬向风。黑线是 ψ，单位 10¹⁰ kg s⁻¹，虚线为负。数据来源：ERA5，WeatherBench 2 气候态。

fig, ax = plt.subplots(figsize=(8.5, 4.5))
cf = ax.contourf(u_zm.latitude, u_zm.level, u_zm, levels=np.arange(-40, 45, 5),
                 cmap="RdBu_r", extend="both")
cs = ax.contour(psi.latitude, psi.level, psi / 1e10, colors="k", linewidths=0.8,
                levels=[-20, -15, -10, -5, -2, 2, 5, 10, 15, 20])
ax.clabel(cs, fmt="%d", fontsize=8)
ax.set(ylim=(1000, 50), xlim=(-90, 90), xticks=range(-90, 91, 30),
       xlabel="纬度 / °", ylabel="气压 / hPa")
fig.colorbar(cf, ax=ax, label="纬向平均的纬向风 / m s$^{-1}$")
plt.show()
```

[](#fig-ch01-section) 是本页最重要的图。10°S 和 30°N 之间有一个顺时针的强环流，这是北半球冬季的 Hadley 环流。它的上升支在赤道附近和赤道以南，也就是夏半球一侧。南半球的 Hadley 环流很弱。两个半球的纬度 30° 到 60° 之间，各有一个转向相反的弱环流，这就是 Ferrel 环流。

纬向风的最大值在 200 hPa 附近。北半球冬季的急流在 30°N，比南半球的急流更强。热带的低层是东风，也就是信风。中纬度的低层是西风。

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

最后检查质量守恒和风速。整层的 $[v]$ 积分应接近零，所以 1000 hPa 的 $\psi$ 应接近零。METEO 300 第 1 课 1.2 节说，250 hPa 的风速约为 50 m s⁻¹。纬向平均会削弱单个急流核，所以纬向平均的最大风速应该略小。

```{code-cell} python
bottom = float(abs(psi.sel(level=1000)).sel(latitude=slice(-30, 30)).max())
jet = u_zm.sel(level=slice(100, 400))
jet_max = float(jet.max())
where = jet.where(jet == jet.max(), drop=True)
print(f"热带 1000 hPa 的 |psi| 最大 {bottom:.1e} kg/s，是最大值的 {bottom / float(north):.0%}")
print(f"急流: {jet_max:.1f} m/s，{float(where.latitude[0]):.0f}°，{int(where.level[0])} hPa")
assert 30 < jet_max < 60
```

1000 hPa 的 $\psi$ 不是零，热带的残差约是最大值的 6%。残差来自三个近似。样本只有 13 个等压面。积分止于 1000 hPa，不是地面。高原上的 1000 hPa 在地面以下，那里的风是外推值。

## AI 天气连接

海平面气压和等压面上的风都是 AI 天气模型的核心变量。GraphCast 和 AIFS 都把它们既当作输入，也当作输出。下表列出本页的量在数据集和模型里的名字。

| 量 | ERA5 短名 | WeatherBench 2 名 | GraphCast | AIFS Single v1.0 |
|---|---|---|---|---|
| 海平面气压 | `msl` | `mean_sea_level_pressure` | 输入和输出 | 输入和输出 |
| 纬向风 | `u` | `u_component_of_wind` | 输入和输出，37 个等压面 | 输入和输出，13 个等压面 |
| 经向风 | `v` | `v_component_of_wind` | 输入和输出，37 个等压面 | 输入和输出，13 个等压面 |
| 大气顶入射太阳辐射 | `tisr` | `toa_incident_solar_radiation` | 只作输入 | 只作输入，按时刻算出 |
| 经向质量流函数 | — | — | 不输出，用 $v$ 算 | 不输出，用 $v$ 算 |

GraphCast 的论文是 Lam 等，2023，[doi:10.1126/science.adi2336](https://doi.org/10.1126/science.adi2336)。它的网格间距是 0.25°，时间步长是 6 h。它读入两个时刻的大气状态，预报 6 h 后的状态。AIFS 是 ECMWF 的 AI 天气模型，见 Lang 等，2024，[arXiv:2406.01465](https://arxiv.org/abs/2406.01465)。AIFS Single v1.0 的网格间距约为 31 km，用 13 个等压面。本页样本的 13 个等压面和 AIFS 的完全相同。

两个模型都把大气顶入射太阳辐射当作输入。它随纬度和季节变化，这个分布驱动大气环流。模型从训练数据里学到 Hadley 环流和急流，不需要显式的环流方程。

WeatherBench 2 是评估 AI 天气模型的公共框架。它用 ERA5 当作真值，用本页的同一个气候态当作基线预报。气候态预报每天都给出这一天的多年平均值。一个模型的误差小于气候态的误差，这个模型才有技巧。WeatherBench 2 的均方根误差用纬度加权，权重正比于每行格点的面积。

下面算一次气候态预报的误差。真值是 ERA5 在 2025-01-24 00 UTC 的海平面气压。距平等于真值减去气候态。

```{code-cell} python
case = d.page_data(ch01.FILES["case_msl"], ch01.case_msl)
anom = (case["mean_sea_level_pressure"] - case["mean_sea_level_pressure_climatology"]) / 100
w = ch01.wb2_latitude_weights(anom.latitude)
rmse = float(np.sqrt((anom**2 * w).mean()))

# 手算核对：纬度加权近似于 cos(纬度) 加权
cos_w = np.cos(np.deg2rad(anom.latitude))
rmse_cos = float(np.sqrt((anom**2).weighted(cos_w).mean()))
assert abs(rmse - rmse_cos) < 0.05, (rmse, rmse_cos)
print(f"气候态预报的海平面气压 RMSE: {rmse:.1f} hPa，cos 加权: {rmse_cos:.1f} hPa")
print(f"最低距平: {float(anom.min()):.0f} hPa")
```

```{code-cell} python
#| label: fig-ch01-anom
#| caption: 2025-01-24 00 UTC，全球海平面气压的距平。距平等于 ERA5 减去 1990 年至 2019 年同一日、同一时刻的气候态。数据来源：ERA5，ARCO-ERA5 和 WeatherBench 2 气候态。

anom_c = ch01.cyclic(anom)
fig = plt.figure(figsize=(9, 4.6))
ax = fig.add_subplot(projection=ccrs.Robinson())
cf = ax.contourf(anom_c.longitude, anom_c.latitude, anom_c, levels=np.arange(-60, 61, 10),
                 cmap="RdBu_r", extend="both", transform=ccrs.PlateCarree())
mplot.coastlines(ax, "50m", linewidth=0.4)
ax.set_global()
fig.colorbar(cf, ax=ax, shrink=0.8, label="海平面气压距平 / hPa")
plt.show()
```

这一时刻，气候态预报的全球 RMSE 约为 7.9 hPa。[](#fig-ch01-anom) 里最深的蓝色中心就是 Éowyn，距平约为 −67 hPa。热带的距平很小，误差主要来自中纬度的天气系统。AI 天气模型的工作就是预报这些距平。

分析师可以用本页的计算检查 AI 天气模型的长时效预报。取同一个预报的第 1 天和第 10 天，对 $v$ 和 $u$ 做纬向平均，再算 $\psi$。比较 Hadley 环流的最大值、急流的纬度和强度。两天的值相差很大时，模型的大尺度环流可能在漂移。

## 练习

:::{exercise}
:label: ex-ch01-1

把 [](#fig-ch01-section) 上方代码里的 `SEASON = "DJF"` 改成 `SEASON = "JJA"`，然后重新运行本节的代码。哪个半球的 Hadley 环流更强？两个半球的急流在哪个纬度，风速是多少？
:::

:::{solution} ex-ch01-1
:class: dropdown

6 月至 8 月，南半球的 Hadley 环流更强。它的 $\psi$ 最小值约为 −2.4×10¹¹ kg s⁻¹，位置在 3°S 附近。南半球的急流在 30°S、200 hPa，风速约 42 m s⁻¹。北半球的急流移到 42°N，风速只有约 22 m s⁻¹。规律是：强的 Hadley 环流在冬半球，它的上升支在夏半球。
:::

:::{exercise}
:label: ex-ch01-2

粗算 Hadley 环流翻转一次热带大气需要多长时间。取地面气压 1000 hPa，$g_0 = 9.81$ m s⁻²，$R_\mathrm{E} = 6.371 \times 10^6$ m。30°S 和 30°N 之间的面积是 $2\pi R_\mathrm{E}^2$。用 $\psi$ 的最大值 2×10¹¹ kg s⁻¹ 作质量通量。
:::

:::{solution} ex-ch01-2
:class: dropdown

单位面积的空气质量是 $p_s / g_0 = 10^5 / 9.81 \approx 1.0 \times 10^4$ kg m⁻²。热带的面积是 $2\pi R_\mathrm{E}^2 \approx 2.6 \times 10^{14}$ m²。热带大气的质量约为 $2.6 \times 10^{18}$ kg。翻转时间约为 $2.6 \times 10^{18} / (2 \times 10^{11}) \approx 1.3 \times 10^{7}$ s，也就是约 150 天。METEO 300 第 12 课 12.1 节说，大气用几个月把空气从赤道运到极地。这个粗算和它的量级一致。
:::

:::{exercise}
:label: ex-ch01-3

改写计算 `rmse` 的代码，只算北大西洋的气候态预报误差。用 `anom.sel(latitude=slice(30, 70), longitude=slice(-60, 0))` 取出这个区域。权重要用这个区域的纬度重新算。再用 `slice(-20, 20)` 只算热带。比较三个 RMSE。
:::

:::{solution} ex-ch01-3
:class: dropdown

```python
box = anom.sel(latitude=slice(30, 70), longitude=slice(-60, 0))
w_box = ch01.wb2_latitude_weights(box.latitude)
print(float(np.sqrt((box**2 * w_box).mean())))
```

北大西洋、热带和全球的 RMSE 分别约为 17.2 hPa、1.7 hPa 和 7.9 hPa。热带的海平面气压每天变化很小，气候态已经接近真值。中纬度的温带气旋使气压偏离气候态几十 hPa。所以 AI 天气模型在中纬度的海平面气压误差最大，也最值得检查。
:::
