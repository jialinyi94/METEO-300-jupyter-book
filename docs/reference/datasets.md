---
title: 数据集
---

本页列出本书用到的数据集。本页的信息在 2026-10-17 检查。

每个条目写明数据的内容、分辨率、时间范围、读取函数、许可和使用页面。
读取函数在 `meteo300.data` 里。用法见 [数据读取演示](data-access-demo.md)。
“使用页面”列出已经写完并读取这个数据集的页面。

## 总表

| 数据集 | 类别 | 读取函数 | 需要账户 | 离线样本 |
|---|---|---|---|---|
| [ERA5](#ds-era5) | 再分析 | `era5`、`era5_monthly`、`era5_daily_mean`、`era5_climatology` | 否 | 有 |
| [IGRA2](#ds-igra2) | 探空 | `sounding` | 否 | 有 |
| [University of Wyoming 探空](#ds-wyoming) | 探空 | `sounding` | 否 | 无 |
| [IEM METAR](#ds-metar) | 地面观测 | `metar` | 否 | 有 |
| [ECMWF 开放数据](#ds-ecmwf) | 业务预报 | `ecmwf_forecast` | 否 | 有 |
| [WeatherBench 2](#ds-wb2) | AI 预报评估 | `weatherbench2`、`wb2_scores` | 否 | 无 |
| [GraphCastGFS](#ds-graphcastgfs) | AI 预报 | `meteo300.pages.ch02` | 否 | 有 |
| [NOAA GML 二氧化碳](#ds-co2) | 大气成分 | `co2` | 否 | 有 |
| [GOES ABI](#ds-goes) | 卫星 | `goes_abi` | 否 | 有 |
| [Meteosat](#ds-meteosat) | 卫星 | `meteosat_image`、`meteosat` | 数值数据需要 | 无 |
| [VIIRS](#ds-viirs) | 卫星 | `meteo300.pages.ch12.viirs_m15` | 是 | 有 |
| [AERONET](#ds-aeronet) | 气溶胶 | `aeronet_aod` | 否 | 无 |
| [CAMS](#ds-cams) | 大气成分 | `cams` | 是 | 无 |
| [GPCP](#ds-gpcp) | 降水量 | `gpcp` | 否 | 有 |
| [GPM IMERG](#ds-imerg) | 降水量 | `imerg` | 是 | 无 |
| [CERES EBAF](#ds-ceres) | 辐射 | `ceres_ebaf` | 是 | 无 |
| [KNMI Cabauw](#ds-cabauw) | 边界层 | `cabauw` | 否 | 有 |
| [DE-Har 涡动协方差](#ds-dehar) | 湍流 | `turbulence_20hz` | 否 | 有 |
| [Natural Earth](#ds-natural-earth) | 地图 | `meteo300.plot.coastlines` | 否 | 有 |

(ds-accounts)=
## 账户和条款

需要账户的数据集用用户自己的账户。下面的命令列出已经可用的账户：

```bash
uv run python -m meteo300.check_credentials
```

有两个数据源要求用户先在网站上同意条款。用户没有同意时，下载返回 HTTP 403。

- EUMETSAT Data Store 返回 `GeneralLicense required to access this collection`。
  用户登录 [EUMETSAT User Portal 的数据许可页](https://user.eumetsat.int/profile?activeTab=data-licenses)。
  在 Data licences 里，用户申请 General Licence，它的名称是 Meteosat > 1 hr latency & Metop。
  然后用户勾选 I accept these licensing terms and conditions。
  接受 General Licence 以后仍返回 403 时，用户先确认 API key 属于接受协议的同一个 EUMETSAT 账户。
  然后用户在 Data Store 网页上试下载一个文件。
- NASA GES DISC 返回 `EULA Acceptance Failure`。读取 IMERG 时会遇到这个错误。
  用户登录 [Earthdata Login](https://urs.earthdata.nasa.gov)，打开 Applications 菜单的 Authorized Apps。
  用户点击 Approve More Applications，搜索 NASA GESDISC DATA ARCHIVE，再点击 Authorize。
  403 的响应里有 `resolution_url`。用户也可以直接打开这个网址，批准应用。

下面的命令用每个账户登录，并试读一个小文件。遇到这两种 403 时，命令列出上面的操作。

```bash
uv run python -m meteo300.check_credentials --verify
```

## 再分析

(ds-era5)=
### ERA5

ERA5 是 ECMWF 为 Copernicus 气候变化服务制作的全球再分析。

本书从三个公开的 Zarr 存储读取 ERA5。三个存储都在 Google Cloud 上，不需要账户。

| 存储 | 网格 | 时间间隔 | 等压面 | 时间范围 | 读取函数 |
|---|---|---|---|---|---|
| ARCO-ERA5 | 0.25° | 1 h | 37 个 | 1940-01-01 至 2026-10-11 | `era5`、`era5_daily_mean` |
| WeatherBench 2 ERA5 | 1.5° | 6 h | 13 个 | 1959-01-01 至 2023-01-10 | `era5(grid="1.5")`、`era5_monthly` |
| WeatherBench 2 气候态 | 1.5° | 每天 4 个时刻 | 13 个 | 1990 年到 2019 年的平均 | `era5_climatology` |

- 内容：等压面变量有温度、位势、风、比湿和垂直速度。单层变量有海平面气压、2 m 温度、10 m 风、降水量和辐照度。
- 存储地址：
  - `gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`
  - `gs://weatherbench2/datasets/era5/1959-2023_01_10-6h-240x121_equiangular_with_poles_conservative.zarr`
  - `gs://weatherbench2/datasets/era5-hourly-climatology/1990-2019_6h_240x121_equiangular_with_poles_conservative.zarr`
- 许可：CC BY 4.0。Copernicus 在 2025-07-02 把 Climate Data Store 的许可改为 CC BY 4.0。
- 引用：Hersbach, H. et al., 2020: The ERA5 global reanalysis. QJRMS, 146, 1999–2049. [doi:10.1002/qj.3803](https://doi.org/10.1002/qj.3803)。
- 署名：Contains modified Copernicus Climate Change Service information。
- 样本：`era5_ciaran_pl.nc`、`era5_ciaran_sfc.nc`、`era5_global_1p5.nc`、`era5_monthly_1p5.nc`、`era5_daily_toa.nc`、`era5_climatology_1p5.nc`。
- 使用页面：[ch01](../topics/ch01-global-circulation.md)、[ch03](../topics/ch03-pressure-hydrostatic.md)、[ch04](../topics/ch04-thermodynamics-stability.md)、[ch05](../topics/ch05-dynamics-geostrophic.md)、[ch06](../topics/ch06-water-vapour.md)、[ch07](../topics/ch07-stability-tephigram.md)、[ch08](../topics/ch08-geopotential-thickness.md)、[ch09](../topics/ch09-vector-calculus.md)、[ch10](../topics/ch10-thermal-wind.md)、[ch11](../topics/ch11-vorticity-divergence.md)、[ch12](../topics/ch12-extratropical-cyclone.md)、[t1](../topics/t1-cloud-composition.md)、[t2](../topics/t2-radiation.md)、[t3](../topics/t3-boundary-layer.md)。

注意事项：

- ARCO-ERA5 的一个分块包含一个时刻、37 个等压面和整个地球。一个等压面变量的一个时刻约 150 MB。只读取一个小区域，也要下载整个分块。读取函数一次最多读取 48 个这样的分块。
- ARCO-ERA5 的经度在 ［0, 360］ 之内，纬度从北到南。读取函数把经度换到 -180° 到 180°。ECMWF 开放数据的经度本来就在 ［-180, 180］ 之内。
- WeatherBench 2 的维度顺序是 time、level、longitude、latitude，纬度从南到北。读取函数把纬度换成从北到南。
- WeatherBench 2 的 1.5° ERA5 和气候态里，大气顶的净短波和净长波辐照度全是 NaN。大气顶辐照度改用 `era5_daily_mean`。
- ERA5 把向上的辐照度记为负值。射出长波辐射等于大气顶净长波辐照度乘以 -1。
- ERA5 的 `mean_*_flux` 变量在时刻 t 的值，是截至 t 的一小时平均值。
- ARCO-ERA5 的最后约 3 个月是初步数据 ERA5T。ECMWF 以后可能修订这段数据。

## 探空

(ds-igra2)=
### IGRA2

IGRA2 是 NOAA NCEI 的全球探空数据集。

- 内容：气压、位势高度、温度、相对湿度、温度露点差、风向和风速。读取函数算出露点温度和风的分量。
- `height` 列是位势高度，单位 m。
- 观测站：超过 2800 个。约 800 个观测站现在仍有观测。
- 时间：大多数观测站在 00 UTC 和 12 UTC 观测。最早的数据在 1905 年。
- 读取：`sounding(time, station)`。`station` 可以写 IGRA2 编号，例如 `UKM00003808`，也可以写 WMO 编号。
- 网址：<https://www.ncei.noaa.gov/products/weather-balloon/integrated-global-radiosonde-archive>
- 许可：NOAA 数据，使用不受限制。
- 引用：Durre, I. et al., 2016: Integrated Global Radiosonde Archive, Version 2. NOAA NCEI. [doi:10.7289/V5X63K0Q](https://doi.org/10.7289/V5X63K0Q)。
- 样本：`sounding_igra2.csv`，有 Camborne 的两次探空和 Norman 的一次探空。
- 使用页面：[ch03](../topics/ch03-pressure-hydrostatic.md)、[ch04](../topics/ch04-thermodynamics-stability.md)、[ch07](../topics/ch07-stability-tephigram.md)、[ch10](../topics/ch10-thermal-wind.md)。

注意事项：

- 当年的数据在 `data-y2d/` 目录里，每个观测站一个文件。读取函数每 24 h 更新一次这个文件。
- 往年的数据在 `data-por/` 目录里，每个观测站一个文件。一个文件可能有 70 MB。读取函数只下载一次，然后存入缓存。
- 位势高度只在部分气压上有值。需要每层的位势高度时，用压高公式计算。

(ds-wyoming)=
### University of Wyoming 探空

- 内容：和 IGRA2 相同的探空，以及从探空算出的指数。
- 读取：`sounding(time, station, source="wyoming")`，通过 siphon 读取。
- 网址：<https://weather.uwyo.edu/upperair/sounding.html>
- 许可：网站没有写明许可。所以本书不提交 Wyoming 样本。
- 使用页面：IGRA2 读取失败时，作为备用来源。

## 地面观测

(ds-metar)=
### IEM METAR

Iowa Environmental Mesonet 保存全世界机场的 METAR 报告。

- 内容：温度、露点温度、风向、风速、阵风、QNH、海平面气压、能见度、云和天气现象，以及 METAR 原文。
- 时间：多数机场每 30 min 或 60 min 一份报告。
- 读取：`metar(station, start, end)`。函数把单位换成国际单位。一次最多读取 366 天。
- 网址：<https://mesonet.agron.iastate.edu/request/download.phtml>
- 许可：公有领域。IEM 希望用户注明 Iowa Environmental Mesonet of Iowa State University。
- 样本：`metar_egll.csv`，风暴 Ciarán 期间的 London Heathrow。
- 使用页面：[ch02](../topics/ch02-station-observations.md)、[ch06](../topics/ch06-water-vapour.md)。ch02 用 `meteo300.pages.ch02` 的读取函数，一次读取一个观测网的报告。

注意事项：

- 欧洲的 METAR 报告 QNH，不报告海平面气压。`altimeter` 列是 QNH。
- 美国的 METAR 常在附注里报告海平面气压。`mslp` 列是这个值。
- QNH 和海平面气压用不同的方法订正到海平面。观测站越高，两者的差越大。

## 预报

(ds-ecmwf)=
### ECMWF 开放数据

ECMWF 公开一部分业务预报。IFS 是数值模式，AIFS Single 是 AI 天气模型。
2025-02-25 以前，开放数据里的 AI 天气模型是 AIFS 的试验版本，模型名是 `aifs`。

- 网格：0.25°，GRIB2 格式。
- 起报时间：每天 00、06、12、18 UTC。
- 预报时效：IFS 在 00 UTC 和 12 UTC 的预报，0 h 到 144 h 每 3 h 一个，150 h 到 360 h 每 6 h 一个。IFS 在 06 UTC 和 18 UTC 的预报到 144 h。AIFS 每次预报都是 0 h 到 360 h，每 6 h 一个。
- 读取：`ecmwf_forecast(params, steps=..., levels=..., model="ifs" 或 "aifs-single", run=...)`。
  读取试验版 AIFS 时写 `model="aifs"`，`run` 要早于 2025-02-25。
- 网址：<https://www.ecmwf.int/en/forecasts/datasets/open-data>
- 许可：CC BY 4.0。署名写 Source: www.ecmwf.int。
- 样本：`ecmwf_opendata.nc`，起报时间 2026-10-15 00 UTC，IFS 和 AIFS。
- 使用页面：[ch03](../topics/ch03-pressure-hydrostatic.md)、[ch04](../topics/ch04-thermodynamics-stability.md)、[ch05](../topics/ch05-dynamics-geostrophic.md)、[ch06](../topics/ch06-water-vapour.md)、[ch07](../topics/ch07-stability-tephigram.md)、[ch09](../topics/ch09-vector-calculus.md)、[ch10](../topics/ch10-thermal-wind.md)、[ch11](../topics/ch11-vorticity-divergence.md)、[ch12](../topics/ch12-extratropical-cyclone.md)、[t1](../topics/t1-cloud-composition.md)、[t2](../topics/t2-radiation.md)、[t3](../topics/t3-boundary-layer.md)。
  ch03 和 ch12 读取试验版 AIFS。

注意事项：

- ECMWF 门户只保留最近 12 次起报，约 ［2, 3］ 天。读取函数先试 Google 镜像，再试 AWS 镜像，最后试 ECMWF 门户。
- Google 镜像和 AWS 镜像都保留多年的起报。2026-10-17 检查时，Google 镜像有本书页面用到的 2025 年和 2026 年的起报。Google 镜像的回答比 AWS 镜像快。
- Google 镜像缺少少数旧的起报，例如 2025 年 1 月下旬的试验版 AIFS。ch03 用的 2025-01-22 起报只在 AWS 镜像上。
- AWS 镜像常常返回 503 Slow Down。读取函数对 AWS 最多重试 6 次，每次间隔 20 s。环境变量 `METEO300_ECMWF_SOURCES=aws` 让函数直接读取 AWS。
- ECMWF 门户在请求过多时返回 429。
- cfgrib 把位势高度的单位写成 `gpm`。读取函数把它改成 `m`。
- 页面要写明 `run`。不写时，函数读取最新的起报，页面的结果每天都会变。

(ds-wb2)=
### WeatherBench 2

WeatherBench 2 是 Google Research 的 AI 天气模型评估基准。

- 内容：多个模型的预报、ERA5 真值、IFS HRES 真值，以及算好的评分。
- 模型：`graphcast`、`pangu`、`neuralgcm`、`fuxi`、`hres`。
- 网格：1.5° 和 0.25°。评分文件按年份和网格分开。
- 读取：`weatherbench2(model, variables, time, lead_times=..., levels=...)` 和 `wb2_scores(model)`。
- 网址：<https://weatherbench2.readthedocs.io/>
- 许可：ERA5 部分的许可是 CC BY 4.0。各模型预报的许可没有统一写明。所以本书不提交 WeatherBench 2 样本。
- 引用：Rasp, S. et al., 2024: WeatherBench 2. JAMES, 16, e2023MS004019. [doi:10.1029/2023MS004019](https://doi.org/10.1029/2023MS004019)。
- 使用页面：[ch08](../topics/ch08-geopotential-thickness.md)。离线时，ch08 读取从这些预报算出的评分样本。
- WeatherBench 2 的 ERA5 和 ERA5 气候态见 [ERA5](#ds-era5) 条目。

注意事项：

- 预报时效的坐标是 `prediction_timedelta`。xarray 2026 版本需要 `decode_timedelta=True` 才能把它读成时间差。读取函数已经设置这个参数。
- 评分文件是 netCDF3 格式。读取函数用 scipy 引擎打开它。

(ds-graphcastgfs)=
### GraphCastGFS

NOAA NCEP 用 GFS 分析场驱动 GraphCast，每天发布预报。

- 网格：0.25°。
- 读取：`meteo300.pages.ch02.graphcastgfs_10m_wind`，只读取 10 m 风。
- 网址：<https://registry.opendata.aws/noaa-nws-graphcastgfs-pds/>
- 许可：CC0。
- 样本：`ch02-graphcastgfs-10m-wind-20250123T00.nc`，来源和许可见 `data/samples/ATTRIBUTION-ch02.md`。
- 使用页面：[ch02](../topics/ch02-station-observations.md)。

## 大气成分

(ds-co2)=
### NOAA GML 二氧化碳

- 内容：二氧化碳的月平均体积混合比，单位 ppm，以及去掉季节循环的值。
- 观测站：Mauna Loa 从 1958 年 3 月开始。全球海洋表面平均值从 1979 年 1 月开始。
- 读取：`co2(site="mlo")` 或 `co2(site="gl")`。缓存 7 天后更新。
- 网址：<https://gml.noaa.gov/ccgg/trends/>
- 许可：免费使用。NOAA GML 要求引用数据来源。
- 引用：Lan, X., P. Tans and K. W. Thoning: Trends in globally-averaged CO2 determined from NOAA Global Monitoring Laboratory measurements. [doi:10.15138/9N0H-ZH07](https://doi.org/10.15138/9N0H-ZH07)。
- 样本：`co2_mm_mlo.csv`、`co2_mm_gl.csv`。
- 使用页面：[t1](../topics/t1-cloud-composition.md)，读取 Mauna Loa 的月平均值。

(ds-aeronet)=
### AERONET

AERONET 是 NASA 的地基太阳光度计网。

- 内容：多个波长的气溶胶光学厚度和 Ångström 指数。
- 读取：`aeronet_aod(site, start, end, level=1.5, daily=True)`，通过 AERONET 第 3 版网络服务读取。
- 网址：<https://aeronet.gsfc.nasa.gov/>
- 许可：数据公开。AERONET 要求用户在发表前联系观测站负责人。所以本书不提交 AERONET 样本。
- 使用页面：暂无。

(ds-cams)=
### CAMS

CAMS 是 Copernicus 大气监测服务。它提供气溶胶、臭氧和其他成分的再分析和预报。

- 数据集：EAC4 再分析，网格 0.75°，每 3 h 一个值，从 2003 年开始。CAMS 全球预报，每天两次。
- 读取：`cams(variables, time, area=..., dataset="eac4" 或 "forecast")`，通过 cdsapi 读取。
- 账户：Copernicus Atmosphere Data Store。凭证在 `~/.adsapirc` 或 `~/.cdsapirc` 里。用户还要在网站上接受每个数据集的许可。
- 网址：<https://ads.atmosphere.copernicus.eu/>
- 许可：CC BY 4.0。
- 署名：Contains modified Copernicus Atmosphere Monitoring Service information。
- 引用：Copernicus Atmosphere Monitoring Service, 2026: CAMS global atmospheric composition forecasts. ADS. [doi:10.24381/04a0b097](https://doi.org/10.24381/04a0b097)。
- 页面样本：`t1-cams-aod-20260304.nc`，2026-03-04 到 2026-03-06 的 550 nm 气溶胶光学厚度。t1 通过 `page_data` 读取它。
- 使用页面：[t1](../topics/t1-cloud-composition.md)，读取 `cams(..., dataset="forecast", leadtime_hours=[0])`。预报时效 0 h 的值是预报系统的分析场。

注意事项：

- ADS 的请求先排队，再处理。一个请求可能等几分钟。
- 本书用 `cdsapi` 0.7.7 或更新的版本。

## 卫星

(ds-goes)=
### GOES ABI

GOES-R 系列卫星的 ABI 成像仪有 16 个波段。

- 内容：本书用二级产品 CMIP。可见光波段是反射率，红外波段是亮温。
- 区域和时间：CONUS 区域每 5 min 一幅，全圆盘每 10 min 一幅。红外波段的分辨率是 2 km。
- 读取：`goes_abi(time, band=13, sector="CONUS", satellite="east")`。函数用 satpy 打开文件。
- 网址：<https://registry.opendata.aws/noaa-goes/>
- 许可：NOAA 开放数据，使用不受限制。
- 样本：GOES-19 第 13 波段，2026-10-15 18:01 UTC。
- 使用页面：[ch01](../topics/ch01-global-circulation.md)、[t2](../topics/t2-radiation.md)。ch01 读取 GOES-16 的全圆盘图像，t2 还读取一级辐亮度。

注意事项：

- 2025-04-07 起，GOES-East 是 GOES-19。2023-01-04 起，GOES-West 是 GOES-18。函数按时间选择卫星。
- 文件里的 `license` 属性写着访问受限。这是地面系统的模板文字。NOAA 通过开放数据计划公开这些数据。

(ds-meteosat)=
### Meteosat

EUMETSAT 运营欧洲的静止气象卫星 Meteosat。

- 图片：`meteosat_image` 从 EUMETView 的 WMS 服务读取图片，不需要账户。图片的像素值是颜色，不是亮温。
- 数值数据：`meteosat` 从 EUMETSAT Data Store 读取 SEVIRI 一级数据。用户需要 EUMETSAT 账户，凭证在 `~/.eumdac/credentials` 里。
- 条款：用户还要在 EUMETSAT User Portal 接受 General Licence。步骤见 [账户和条款](#ds-accounts)。
- 网址：<https://view.eumetsat.int/> 和 <https://data.eumetsat.int/>
- 许可：EUMETSAT 数据政策在 2025-11-25 修订。整点的 SEVIRI 和 FCI 一级数据属于 Core 数据，许可是 CC BY 4.0。
  Core 数据可以再分发。所以本书可以提交整点数据的样本。
- 其他时刻的一级数据属于 Recommended 数据。EUMETSAT 禁止再分发这些数据的原始数值。
- 整点数据指参考时间是整点 UTC 的全圆盘扫描。`meteosat("2025-07-01T12:00")` 读取的是整点数据。
- 署名：EUMETSAT 要求写 `[Contains modified] EUMETSAT [Meteosat/Metop] [data/product] [Year]`，例如 Contains modified EUMETSAT Meteosat data 2026。
- 数据政策：<https://www-cdn.eumetsat.int/files/2026-01/45173%20-%20Data_Policy.pdf>，第 4 条到第 6 条。
- 使用页面：暂无。[ch12](../topics/ch12-extratropical-cyclone.md) 把它列为备选数据集。

(ds-viirs)=
### VIIRS

VIIRS 是 NOAA-20 等极轨卫星上的成像仪。NASA LAADS DAAC 保存它的一级数据。

- 内容：本书用 NOAA-20 的 M15 波段，中心波长 10.76 µm。M 波段的像元在星下点是 750 m。
- 读取：`meteo300.pages.ch12.viirs_m15()`。函数用 earthaccess 下载一个 6 min 的 L1B 文件和它的地理定位文件，约 120 MB。
  satpy 读取 M15 波段的亮温，再把像元平均到 0.05° 的经纬度网格上。
- 账户：NASA Earthdata。凭证在 `~/.netrc` 里。
- 网址：<https://ladsweb.modaps.eosdis.nasa.gov/>
- 许可：NASA 的地球科学数据可以自由使用和再分发。NASA 要求引用数据集。
- 样本：`ch12-viirs-m15-2024120703.nc`，2024-12-07 02:54 UTC 到 03:00 UTC 的扫描。来源和许可见 `data/samples/ATTRIBUTION-ch12.md`。
- 使用页面：[ch12](../topics/ch12-extratropical-cyclone.md)。

% ste-ignore
引用：VIIRS Calibration Support Team (VCST), 2021: VIIRS/JPSS1 Moderate Resolution 6-Min L1B Swath 750m. NASA LAADS DAAC. [doi:10.5067/VIIRS/VJ102MOD.021](https://doi.org/10.5067/VIIRS/VJ102MOD.021)。
地理定位文件的 DOI 是 [10.5067/VIIRS/VJ103MOD.021](https://doi.org/10.5067/VIIRS/VJ103MOD.021)。

## 降水量

(ds-gpcp)=
### GPCP

GPCP 合并卫星和雨量计的数据，得到全球降水量。

- 月数据：第 2.3 版，网格 2.5°，从 1979 年开始。
- 日数据：第 1.3 版，网格 1°，从 1996 年开始。
- 读取：`gpcp(time, area=..., frequency="monthly" 或 "daily")`，从 AWS 上的 NOAA 气候数据记录读取。
- 网址：<https://registry.opendata.aws/noaa-cdr-atmospheric/>
- 许可：NOAA 气候数据记录，使用不受限制。
- 引用：Adler, R. F. et al., 2018: The Global Precipitation Climatology Project monthly analysis, new version 2.3. Atmosphere, 9, 138. [doi:10.3390/atmos9040138](https://doi.org/10.3390/atmos9040138)。
- 样本：`gpcp_monthly.nc`，2020 年 1 月和 7 月。
- 使用页面：暂无。`gpcp_monthly.nc` 只用于 [数据读取演示](data-access-demo.md)。

(ds-imerg)=
### GPM IMERG

- 内容：全球降水率，网格 0.1°，从 2000 年 6 月开始。半小时数据每 30 min 一个值。日数据是一个 UTC 日的降水量，单位 mm/day。
- 读取：`imerg(time, area=..., frequency=..., run=...)`，通过 earthaccess 读取第 07 版。
  `frequency` 是 `"half-hourly"`、`"daily"` 或 `"monthly"`。
  `run` 是 `"final"`、`"late"` 或 `"early"`。Final 用雨量计订正，比实时晚约 3.5 个月。Late 晚约 14 h，Early 晚约 4 h。
  2026 年 10 月检查时，GES DISC 的 Final 只到 2025-09-30。以后的日期用 `"late"`。
- 账户：NASA Earthdata。凭证在 `~/.netrc` 里。
- 条款：用户还要在 Earthdata 账户里批准 GES DISC 应用。步骤见 [账户和条款](#ds-accounts)。
- 网址：<https://gpm.nasa.gov/data/imerg>
- 许可：NASA 开放数据，使用不受限制。
- 引用：Huffman, G. J., E. F. Stocker, D. T. Bolvin, E. J. Nelkin and J. Tan, 2023: GPM IMERG Late Precipitation L3 1 day 0.1 degree x 0.1 degree V07. NASA GES DISC. [doi:10.5067/GPM/IMERGDL/DAY/07](https://doi.org/10.5067/GPM/IMERGDL/DAY/07)。
- 页面样本：`t1-imerg-late-20260305.nc`，2026-03-05 和 2026-03-06 两个 UTC 日的降水量。t1 通过 `page_data` 读取它。
- 使用页面：[t1](../topics/t1-cloud-composition.md)，读取 `imerg(..., frequency="daily", run="late")`。

## 辐射

(ds-ceres)=
### CERES EBAF

- 内容：大气顶和地面的短波和长波辐照度月平均，网格 1°，从 2000 年 3 月开始。
- 读取：`ceres_ebaf(variables, time, area=...)`，通过 earthaccess 读取。
- 账户：NASA Earthdata。凭证在 `~/.netrc` 里。
- 网址：<https://ceres.larc.nasa.gov/data/>
- 许可：NASA 开放数据，使用不受限制。
- 使用页面：[t2](../topics/t2-radiation.md)。离线时，页面用 ERA5 日平均样本 `era5_daily_toa.nc` 代替。

注意事项：

- 全部记录在一个约 2 GB 的文件里。读取函数远程打开文件，只读取需要的部分。

## 边界层和湍流

(ds-cabauw)=
### KNMI Cabauw

KNMI 在荷兰 Cabauw 运营一座 213 m 的观测塔。

- 时间：每 10 min 一个值，每月一个文件。
- 读取：`cabauw(start, end, dataset=...)`。`dataset` 选择下表中的一个 KNMI 数据集。

| `dataset` | KNMI 数据集 | 内容 |
|---|---|---|
| `tower_meteo` | `cesar_tower_meteo_lc1_t10` v1.1 | 观测塔上的温度、露点温度、比湿、相对湿度、风速和风向 |
| `surface_radiation` | `cesar_surface_radiation_lc1_t10` v1.0 | 地面的向下和向上短波辐射，向下和向上长波辐射 |
| `surface_meteo` | `cesar_surface_meteo_lc1_t10` v1.0 | 地面气象观测 |
| `surface_flux` | `cesar_surface_flux_lc1_t10` v1.0 | 地面通量 |

- 几何高度：`tower_meteo` 的温度在 2、10、20、40、80、140、200 m。风从 10 m 开始。
- `surface_radiation` 的变量是 `SWD`、`SWU`、`LWD` 和 `LWU`，单位 W m⁻²。Cabauw 是 BSRN 的观测站。
- 账户：不需要。函数默认用 KNMI 开放数据接口的公开匿名密钥。用户有自己的密钥时，函数改用自己的密钥。
- 网址：<https://dataplatform.knmi.nl/>
- 许可：CC BY 4.0。
- 样本：`cesar_tower_meteo_lc1_t10_v1.1_202507.nc`，2025 年 7 月的 `tower_meteo`。离线时，`cabauw` 只能读取这个样本。
- 页面样本：`t2-cabauw-radiation-20250628.csv`，2025-06-28 到 2025-07-04 的 `surface_radiation`。t2 通过 `page_data` 读取它。
- 页面样本：`t3-cabauw-tower-202604.nc`，2026-04-16 到 2026-04-30 的 `tower_meteo`。
- 页面样本：`t3-cabauw-surface-202604.csv`，同一时段的 `surface_flux` 和 `surface_meteo`。t3 通过 `page_data` 读取这两个文件。
- 使用页面：[t2](../topics/t2-radiation.md) 读取 `surface_radiation`，[t3](../topics/t3-boundary-layer.md) 读取 `tower_meteo`、`surface_flux` 和 `surface_meteo`。

注意事项：

- 所有用户共用匿名密钥的请求上限：每分钟 50 次，每小时 3000 次。达到上限时，接口返回 429，函数改读样本。
- KNMI 把单位写成比例因子。函数把 `1e-3` 改成 `g/kg`，把 `1e-2` 改成 `percent`。

(ds-dehar)=
### DE-Har 涡动协方差

DE-Har 是德国 Hartheim 的森林观测站。Zenodo 公开它的 20 Hz 原始数据。

- 内容：超声风速仪的三个风速分量和超声温度，以及气体分析仪的水汽和二氧化碳。
- 时间：每 30 min 一个 `.ghg` 文件，有 36000 个值。读取函数支持 2023 年和 2024 年。
- 读取：`turbulence_20hz(start, periods=1)`。`df.attrs["eddypro"]` 是同一时段 EddyPro 的通量结果。
- 网址：[Zenodo 18713191](https://doi.org/10.5281/zenodo.18713191) 是 2024 年，[Zenodo 18712865](https://doi.org/10.5281/zenodo.18712865) 是 2023 年。
- 许可：CC BY 4.0。
- 样本：`2024-07-01T120000_AIU-1660.ghg`，2024-07-01 12:00 UTC 起的 30 min。
- 页面样本：`t3-dehar-20hz-20240701t2100.nc`，2024-07-01 21:00 UTC 起的 30 min。
- 使用页面：[t3](../topics/t3-boundary-layer.md)。离线时，t3 从样本读取 12:00 UTC 的时段，从页面样本读取 21:00 UTC 的时段。

% ste-ignore
引用：Christen, A., S. Haberstroh, T. Plapp, D. Schindler and M. Sulzer, 2026: Eddy Covariance measurements at Hartheim Research Forest Site (DE-Har) [RAW]. Zenodo.

注意事项：

- 每个月的数据是一个压缩包。函数按顺序读取压缩包，读到需要的文件为止。月末的时段要读取更多数据。
- `cell_pressure` 是分析仪测量室的气压，不是环境气压。环境气压在 `df.attrs["biomet"]` 里。
- ICOS 的同类数据需要账户。检查时，NEON 的下载接口返回 403。所以本书选用 DE-Har。

## 地图

(ds-natural-earth)=
### Natural Earth

- 内容：海岸线、陆地和国界，比例尺 1:1.1 亿和 1:5000 万。
- 读取：`meteo300.plot.coastlines(ax)`。文件在 `data/natural_earth/`，画图不需要网络。
- 网址：<https://www.naturalearthdata.com/>
- 许可：公有领域。
- 使用页面：[ch01](../topics/ch01-global-circulation.md)、[ch03](../topics/ch03-pressure-hydrostatic.md)、[ch04](../topics/ch04-thermodynamics-stability.md)、[ch05](../topics/ch05-dynamics-geostrophic.md)、[ch06](../topics/ch06-water-vapour.md)、[ch07](../topics/ch07-stability-tephigram.md)、[ch08](../topics/ch08-geopotential-thickness.md)、[ch09](../topics/ch09-vector-calculus.md)、[ch10](../topics/ch10-thermal-wind.md)、[ch11](../topics/ch11-vorticity-divergence.md)、[ch12](../topics/ch12-extratropical-cyclone.md)、[t1](../topics/t1-cloud-composition.md)、[t2](../topics/t2-radiation.md) 的地图。
