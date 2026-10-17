---
title: 工具包
---

本页列出处理气象数据的 Python 软件包。每个条目写明用途、成熟度、最新版本和替代软件包。

本页的版本在 2026-10-17 从 PyPI 检查。成熟度取自 PyPI 的 Development Status 分类。
软件包没有这个分类时，本页写“未标注”。
“本书”一栏是 `uv.lock` 锁定的版本。“未安装”表示本书现在不安装这个软件包。

## 数据结构、格式和单位

| 软件包 | 用途 | 成熟度 | 最新版本 | 发布日期 | 检查日期 | 本书 | 替代 |
|---|---|---|---|---|---|---|---|
| [xarray](https://pypi.org/project/xarray/) | 带坐标的多维数组，读写 netCDF 和 Zarr | 稳定 | 2026.9.0 | 2026-09-29 | 2026-10-17 | 2026.9.0 | — |
| [zarr](https://pypi.org/project/zarr/) | 云存储上的分块数组格式 | 成熟 | 3.4.1 | 2026-10-08 | 2026-10-17 | 3.4.1 | — |
| [netCDF4](https://pypi.org/project/netCDF4/) | 读写 netCDF 文件 | Alpha | 1.7.5 | 2026-10-15 | 2026-10-17 | 1.7.5 | h5netcdf |
| [gcsfs](https://pypi.org/project/gcsfs/) | 读取 Google Cloud Storage | Beta | 2026.10.1 | 2026-10-16 | 2026-10-17 | 2026.10.1 | — |
| [s3fs](https://pypi.org/project/s3fs/) | 读取 AWS S3 | Beta | 2026.9.0 | 2026-09-18 | 2026-10-17 | 2026.9.0 | boto3 |
| [Pint](https://pypi.org/project/Pint/) | 物理单位 | Beta | 0.26.1 | 2026-09-10 | 2026-10-17 | 0.26.1 | — |
| [pint-xarray](https://pypi.org/project/pint-xarray/) | 让 xarray 对象带 Pint 单位 | Alpha | 0.6.1 | 2026-03-23 | 2026-10-17 | 0.6.1 | MetPy 的 `.metpy.quantify()` |

## GRIB 和卫星数据

| 软件包 | 用途 | 成熟度 | 最新版本 | 发布日期 | 检查日期 | 本书 | 替代 |
|---|---|---|---|---|---|---|---|
| [eccodes](https://pypi.org/project/eccodes/) | ECMWF 的 GRIB 和 BUFR 库 | Beta | 2.50.0 | 2026-10-15 | 2026-10-17 | 2.42.0 | — |
| [cfgrib](https://pypi.org/project/cfgrib/) | 用 xarray 打开 GRIB 文件 | Beta | 0.9.15.1 | 2025-09-30 | 2026-10-17 | 0.9.15.1 | earthkit-data |
| [satpy](https://pypi.org/project/satpy/) | 读取和处理气象卫星数据 | 稳定 | 0.60.0 | 2026-03-04 | 2026-10-17 | 0.60.0 | — |
| [pyresample](https://pypi.org/project/pyresample/) | 卫星数据的投影和重采样 | 稳定 | 1.35.0 | 2025-12-02 | 2026-10-17 | 1.35.0 | — |

本书把 eccodes 固定为 2.42.0。
更新的 eccodes 带有自己的 PROJ 库。它和 pyproj 一起导入时，程序崩溃。

## 数据访问

| 软件包 | 用途 | 成熟度 | 最新版本 | 发布日期 | 检查日期 | 本书 | 替代 |
|---|---|---|---|---|---|---|---|
| [ecmwf-opendata](https://pypi.org/project/ecmwf-opendata/) | 下载 ECMWF 开放数据 | Alpha | 0.3.35 | 2026-10-16 | 2026-10-17 | 0.3.35 | Herbie |
| [herbie-data](https://pypi.org/project/herbie-data/) | 下载多个模式的 GRIB 预报 | Beta | 2026.9.2 | 2026-09-27 | 2026-10-17 | 未安装 | ecmwf-opendata |
| [siphon](https://pypi.org/project/siphon/) | 读取 THREDDS 服务器和 Wyoming 探空 | 稳定 | 0.11.0 | 2026-07-20 | 2026-10-17 | 0.11.0 | — |
| [cdsapi](https://pypi.org/project/cdsapi/) | 从 CDS 和 ADS 下载数据 | Beta | 0.7.7 | 2025-09-30 | 2026-10-17 | 0.7.7 | ecmwf-datastores-client |
| [ecmwf-datastores-client](https://pypi.org/project/ecmwf-datastores-client/) | CDS 和 ADS 的新客户端 | 稳定 | 0.5.3 | 2026-07-31 | 2026-10-17 | 0.5.3 | cdsapi |
| [earthaccess](https://pypi.org/project/earthaccess/) | 搜索和下载 NASA Earthdata 数据 | Beta | 0.19.0 | 2026-09-04 | 2026-10-17 | 0.19.0 | — |
| [eumdac](https://pypi.org/project/eumdac/) | 从 EUMETSAT Data Store 下载数据 | 稳定 | 3.1.1 | 2025-12-11 | 2026-10-17 | 3.1.1 | — |
| [icoscp_core](https://pypi.org/project/icoscp_core/) | 下载 ICOS 观测数据 | 未标注 | 0.3.13 | 2026-08-24 | 2026-10-17 | 未安装 | — |

`cdsapi` 和 `ecmwf-datastores-client` 都能访问 CDS 和 ADS。
ADS 的说明要求 `cdsapi` 0.7.7 或更新的版本。
ECMWF 把 `ecmwf-datastores-client` 作为新的客户端，但不要求用户迁移。本书用 `cdsapi`。

## earthkit

earthkit 是 ECMWF 的一组软件包。它们处理数据访问、气象计算、统计汇总、画图和插值。
全部 earthkit 软件包都使用 Apache-2.0 许可证。

| 软件包 | 用途 | 成熟度 | 最新版本 | 发布日期 | 检查日期 | 本书 | 替代 |
|---|---|---|---|---|---|---|---|
| [earthkit](https://pypi.org/project/earthkit/) | 一次安装全部 earthkit 软件包 | 稳定 | 1.0.0 | 2026-06-29 | 2026-10-17 | 未安装 | — |
| [earthkit-data](https://pypi.org/project/earthkit-data/) | 用一个接口读取 GRIB、netCDF、CDS 和 MARS 数据 | 稳定 | 1.3.0 | 2026-10-15 | 2026-10-17 | 未安装 | cfgrib、climetlab |
| [earthkit-meteo](https://pypi.org/project/earthkit-meteo/) | 气象计算，例如热力学量、风和太阳位置 | 稳定 | 1.2.1 | 2026-10-15 | 2026-10-17 | 1.2.1 | MetPy |
| [earthkit-transforms](https://pypi.org/project/earthkit-transforms/) | 按时间、区域和集合成员做统计，例如日平均和气候态 | 稳定 | 1.0.0 | 2026-06-29 | 2026-10-17 | 1.0.0 | xarray |
| [earthkit-utils](https://pypi.org/project/earthkit-utils/) | earthkit 软件包共用的工具 | 稳定 | 1.0.3 | 2026-10-15 | 2026-10-17 | 1.0.3 | — |
| [earthkit-plots](https://pypi.org/project/earthkit-plots/) | 气象地图和图表 | Beta | 1.0.4 | 2026-08-26 | 2026-10-17 | 未安装 | cartopy |
| [earthkit-geo](https://pypi.org/project/earthkit-geo/) | 地理计算 | 稳定 | 1.2.0 | 2026-10-15 | 2026-10-17 | 未安装 | pyproj |
| [earthkit-regrid](https://pypi.org/project/earthkit-regrid/) | 网格之间的插值 | Pre-Alpha | 0.5.1 | 2025-12-11 | 2026-10-17 | 未安装 | xESMF |

本书安装 earthkit-meteo 和 earthkit-transforms。它们不依赖 eccodes。
`import earthkit.transforms` 要导入 geopandas，但 earthkit-transforms 没有把 geopandas 列为依赖。
所以本书另外安装 geopandas。

本书暂时不安装 earthkit-data、earthkit-plots 和 earthkit-geo：

- earthkit-data 1.3.0 要求 eccodes 2.48.0 或更新的版本。本书把 eccodes 固定为 2.42.0，原因见“GRIB 和卫星数据”一节。
- earthkit-plots 依赖 earthkit-data，所以有同样的冲突。
- earthkit-geo 依赖 eckit 和 mir-python。它和 pyproj 一起导入时，程序在退出时崩溃。
- 软件包 earthkit 安装全部 earthkit 软件包，包括上面三个。

## 气象计算

| 软件包 | 用途 | 成熟度 | 最新版本 | 发布日期 | 检查日期 | 本书 | 替代 |
|---|---|---|---|---|---|---|---|
| [MetPy](https://pypi.org/project/MetPy/) | 气象计算、斜温图和观测站填图 | 稳定 | 1.7.1 | 2025-08-29 | 2026-10-17 | 1.7.1 | — |
| [tephi](https://pypi.org/project/tephi/) | 温熵图 | Beta | 0.4.0.post0 | 2026-01-30 | 2026-10-17 | 0.4.0.post0 | MetPy 的斜温图 |
| [xeofs](https://pypi.org/project/xeofs/) | 用 xarray 计算经验正交函数 | 未标注 | 3.0.4 | 2024-10-28 | 2026-10-17 | 3.0.4 | — |
| [climlab](https://pypi.org/project/climlab/) | 简单的辐射和能量平衡气候模式 | 未标注 | 0.9.2 | 2026-03-18 | 2026-10-17 | 未安装 | — |
| [pvlib](https://pypi.org/project/pvlib/) | 太阳位置和地面短波辐射 | Beta | 0.16.1 | 2026-09-26 | 2026-10-17 | 未安装 | — |

## 画图

| 软件包 | 用途 | 成熟度 | 最新版本 | 发布日期 | 检查日期 | 本书 | 替代 |
|---|---|---|---|---|---|---|---|
| [Matplotlib](https://pypi.org/project/matplotlib/) | 画图 | 稳定 | 3.11.2 | 2026-09-11 | 2026-10-17 | 3.10.9 | — |
| [Cartopy](https://pypi.org/project/Cartopy/) | 地图投影、海岸线和国界 | Beta | 0.26.0 | 2026-09-17 | 2026-10-17 | 0.26.0 | earthkit-plots |

本书把 Matplotlib 限制在 3.10。MetPy 1.7.1 的 `StationPlot` 在 Matplotlib 3.11 上出错。
MetPy 发布修复后，本书再升级 Matplotlib。

## 预报评估

| 软件包 | 用途 | 成熟度 | 最新版本 | 发布日期 | 检查日期 | 本书 | 替代 |
|---|---|---|---|---|---|---|---|
| [scores](https://pypi.org/project/scores/) | 预报评分，包括连续分级概率评分 | 未标注 | 2.7.0 | 2026-09-05 | 2026-10-17 | 未安装 | xskillscore |
| [xskillscore](https://pypi.org/project/xskillscore/) | 基于 xarray 的预报评分 | 稳定 | 0.0.29 | 2026-02-18 | 2026-10-17 | 未安装 | scores |
| [WeatherBench 2](https://github.com/google-research/weatherbench2) | AI 天气模型的评估代码和数据 | 未标注 | v0.2.0 | 2023-12-04 | 2026-10-17 | 未安装 | scores |

WeatherBench 2 不在 PyPI 上。用户从 GitHub 安装它。
它最后的版本号是 v0.2.0，但仓库在 2026 年 10 月仍有提交。
本书的 `weatherbench2` 和 `wb2_scores` 函数直接读取它的 Zarr 存储，不需要安装它。

## 不再活跃的软件包

[climetlab](https://pypi.org/project/climetlab/) 是 ECMWF 早期的数据访问软件包。

- 最新版本：0.24.0，发布日期 2024-06-20，检查日期 2026-10-17。
- 它的 GitHub 仓库最后一次更新在 2024 年 11 月。
- ECMWF 没有发布正式的弃用声明。
- earthkit-data 提供 climetlab 的主要功能。新的代码用 earthkit-data。
