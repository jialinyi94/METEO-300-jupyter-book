# 术语表

本表给每个概念选定一个中文术语。页面只用“中文术语”一列的词。“弃用词”一列的词不进入正文，检查器发现它们就报错。

表格的列：

- 中文术语：本书使用的唯一说法。
- English term：英文术语。
- 符号：公式里的符号。本书一个符号只表示一个量。
- 单位：正文使用的单位。
- 变量名：ERA5 短名 / ARCO-ERA5 与 WeatherBench 2 的长名。没有对应变量时写“—”。
- 弃用词：不用的同义词，用顿号分隔。

## 气压与高度

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 气压 | pressure | $p$ | hPa | 等压面坐标 `level` | 压强、压力、大气压力、毫巴、mb |
| 地面气压 | surface pressure | $p_s$ | hPa | `sp` / `surface_pressure` | 表面气压、本站气压、站点气压 |
| 海平面气压 | mean sea level pressure | $p_{\mathrm{msl}}$ | hPa | `msl` / `mean_sea_level_pressure` | 海平面压力、海压、平均海平面气压 |
| 修正海平面气压 | QNH; altimeter setting | — | hPa | MetPy `altimeter`，单位 inHg | 修正海压 |
| 等压面 | isobaric surface; pressure level | — | — | 坐标 `level` | 气压层、气压面、等压层 |
| 等压线 | isobar | — | — | — | — |
| 模式层 | model level | — | — | — | 模型层 |
| 气压坐标 | pressure coordinate | — | — | — | p 坐标、p 坐标系 |
| 气压梯度 | pressure gradient | $\nabla p$ | hPa km⁻¹ | — | 压力梯度、压强梯度 |
| 气压倾向 | pressure tendency | $\partial p / \partial t$ | hPa h⁻¹ | — | 气压趋势 |
| 几何高度 | geometric height | $z$ | m | — | 高度、海拔、海拔高度 |
| 位势 | geopotential | $\Phi$ | m² s⁻² | `z` / `geopotential` | 重力位势、地势 |
| 位势高度 | geopotential height | $Z$ | m | `z` 除以 $g_0$ | 高度、重力位势高度 |
| 标准重力加速度 | standard gravity | $g_0$ | m s⁻² | — | 标准重力 |
| 地形高度 | surface geopotential height; orography | $Z_s$ | m | `z` 地面场除以 $g_0$ / `geopotential_at_surface` | 地形海拔 |
| 离地位势高度 | geopotential height above ground | $Z - Z_s$ | m | — | — |
| 厚度 | thickness | $\Delta Z$ | m | — | 位势厚度 |
| 压高公式 | hypsometric equation | — | — | — | 测高方程、测高公式、压高方程 |
| 静力平衡 | hydrostatic balance | — | — | — | 流体静力平衡、静水平衡、静力学平衡 |
| 静力方程 | hydrostatic equation | — | — | — | 静力学方程、流体静力方程 |
| 标高 | scale height | $H$ | km | — | 尺度高度 |
| 标准大气 | standard atmosphere | — | — | MetPy `pressure_to_height_std` | — |
| 密度 | density | $\rho$ | kg m⁻³ | — | — |
| 水压 | water pressure | — | hPa | — | — |
| 对流层 | troposphere | — | — | — | — |
| 对流层顶 | tropopause | — | — | — | — |
| 平流层 | stratosphere | — | — | — | 同温层 |
| 大气顶 | top of atmosphere | TOA | — | — | 大气层顶、大气上界 |

## 温度家族

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 温度 | temperature | $T$ | K | `t` / `temperature` | 气温 |
| 2 m 温度 | 2 m temperature | $T_{2\mathrm{m}}$ | K | `t2m` / `2m_temperature` | 地面温度、近地面温度 |
| 表皮温度 | skin temperature | $T_{\mathrm{skin}}$ | K | `skt` / `skin_temperature` | 地表温度、皮肤温度、地面温度 |
| 海表温度 | sea surface temperature | SST | K | `sst` / `sea_surface_temperature` | 海温、海面温度 |
| 位温 | potential temperature | $\theta$ | K | — | 势温、潜在温度 |
| 虚温 | virtual temperature | $T_v$ | K | — | 虚拟温度 |
| 虚位温 | virtual potential temperature | $\theta_v$ | K | — | 虚拟位温 |
| 露点温度 | dewpoint temperature | $T_d$ | K | `d2m` / `2m_dewpoint_temperature` | 露点 |
| 温度露点差 | dewpoint depression | $T - T_d$ | K | — | 露点差 |
| 湿球温度 | wet-bulb temperature | $T_w$ | K | — | — |
| 相当位温 | equivalent potential temperature | $\theta_e$ | K | — | 等效位温、当量位温 |
| 饱和相当位温 | saturation equivalent potential temperature | $\theta_{es}$ | K | — | — |
| 有效发射温度 | effective emission temperature | $T_e$ | K | — | 有效温度、有效辐射温度、发射温度 |

## 热力学

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 理想气体定律 | ideal gas law | — | — | — | 理想气体状态方程 |
| 干空气气体常数 | gas constant for dry air | $R_d$ | J kg⁻¹ K⁻¹ | MetPy `Rd` | — |
| 热力学第一定律 | first law of thermodynamics | — | — | — | — |
| 内能 | internal energy | — | J kg⁻¹ | — | — |
| 定压比热容 | specific heat capacity at constant pressure | $c_p$ | J kg⁻¹ K⁻¹ | MetPy `Cp_d` | 定压比热、比定压热容 |
| 绝热过程 | adiabatic process | — | — | — | — |

## 湿度家族

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 水汽 | water vapour | — | — | — | 水蒸气、水蒸汽、水气 |
| 水汽压 | vapour pressure | $e$ | hPa | — | 蒸气压、水汽分压、水汽压力 |
| 饱和水汽压 | saturation vapour pressure | $e_s$ | hPa | — | 饱和蒸气压、饱和水汽分压 |
| 比湿 | specific humidity | $q$ | g kg⁻¹ | `q` / `specific_humidity` | 比湿度 |
| 混合比 | mixing ratio | $r$ | g kg⁻¹ | — | 混合率 |
| 饱和混合比 | saturation mixing ratio | $r_s$ | g kg⁻¹ | — | — |
| 相对湿度 | relative humidity | RH | % | `r` / `relative_humidity` | — |
| 饱和比 | saturation ratio | $S$ | — | — | — |
| 过饱和度 | supersaturation | $S - 1$ | % | — | 超饱和度 |
| 可降水量 | precipitable water; total column water vapour | $W$ | kg m⁻² | `tcwv` / `total_column_water_vapour` | 整层水汽、整层水汽含量、柱水汽、大气可降水量 |
| 整层水汽输送 | integrated vapour transport | IVT | kg m⁻¹ s⁻¹ | `integrated_vapor_transport` | — |
| 潜热 | latent heat | $L_v$ | J kg⁻¹ | — | — |
| 凝结 | condensation | — | — | — | 冷凝 |
| 蒸发 | evaporation | — | — | `e` / `evaporation` | — |
| 饱和 | saturation | — | — | — | — |
| 克劳修斯-克拉珀龙方程 | Clausius–Clapeyron equation | — | — | — | 克-克方程、克拉珀龙方程、克劳修斯-克拉伯龙方程 |
| 降水 | precipitation | — | — | — | — |
| 降水量 | precipitation amount | — | mm | `tp` / `total_precipitation_6hr` | — |

## 风

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 风 | wind | $\mathbf{v}$ | m s⁻¹ | — | — |
| 水平风 | horizontal wind | $\mathbf{v}_h$ | m s⁻¹ | — | — |
| 风速 | wind speed | $V$ | m s⁻¹ | `wind_speed` | — |
| 风向 | wind direction | $\chi$ | ° | — | — |
| 去向方位角 | bearing of travel | — | ° | MetPy `wind_direction` 的 `convention="to"` | — |
| 数学角 | math angle | $\gamma$ | ° | — | — |
| 节 | knot | kt | 1 kt ≈ 0.514 m s⁻¹ | — | — |
| 风羽 | wind barb | — | kt | MetPy `StationPlot.plot_barb` | — |
| 纬向风 | zonal wind; u component | $u$ | m s⁻¹ | `u` / `u_component_of_wind` | u 风、东西风分量 |
| 经向风 | meridional wind; v component | $v$ | m s⁻¹ | `v` / `v_component_of_wind` | v 风、南北风分量 |
| 10 m 风 | 10 m wind | $u_{10}$, $v_{10}$ | m s⁻¹ | `u10`, `v10` / `10m_u_component_of_wind`, `10m_v_component_of_wind` | 地面风、近地面风 |
| 阵风 | wind gust | — | m s⁻¹ | `i10fg` / `instantaneous_10m_wind_gust` | — |
| 地转风 | geostrophic wind | $\mathbf{v}_g$ | m s⁻¹ | `geostrophic_wind_speed` | — |
| 非地转风 | ageostrophic wind | $\mathbf{v}_{ag}$ | m s⁻¹ | `ageostrophic_wind_speed` | 偏地转风 |
| 梯度风 | gradient wind | — | m s⁻¹ | — | — |
| 热成风 | thermal wind | $\mathbf{v}_T$ | m s⁻¹ | — | 热风 |
| 垂直风切变 | vertical wind shear | $\partial \mathbf{v}_h / \partial z$ | s⁻¹ | — | 风切、垂直切变 |
| 急流 | jet stream | — | — | — | 喷流 |
| 信风 | trade winds | — | — | — | 贸易风 |
| 西风带 | westerlies | — | — | — | — |

## 力与平衡

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 气压梯度力 | pressure gradient force | PGF | m s⁻² | — | 压力梯度力、压强梯度力 |
| 科里奥利力 | Coriolis force | — | m s⁻² | — | 科氏力、地转偏向力、柯氏力 |
| 科里奥利参数 | Coriolis parameter | $f$ | s⁻¹ | — | 科氏参数、地转参数 |
| 地球自转角速度 | Earth's angular velocity | $\Omega$ | s⁻¹ | — | — |
| 摩擦力 | friction | — | m s⁻² | — | — |
| 地转平衡 | geostrophic balance | — | — | — | — |
| 罗斯贝数 | Rossby number | Ro | — | — | 罗斯比数 |

## 稳定度

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 气块 | air parcel | — | — | — | 空气块 |
| 浮力 | buoyancy | $B$ | m s⁻² | — | 浮升力 |
| 静力稳定度 | static stability | — | — | — | 静力稳定性、大气稳定性、层结稳定度 |
| 层结 | stratification | — | — | — | — |
| 环境直减率 | environmental lapse rate | $\Gamma$ | K km⁻¹ | — | 环境递减率、温度直减率、气温直减率、温度递减率 |
| 干绝热直减率 | dry adiabatic lapse rate | $\Gamma_d$ | K km⁻¹ | — | 干绝热递减率、干绝热减温率 |
| 湿绝热直减率 | moist adiabatic lapse rate | $\Gamma_m$ | K km⁻¹ | — | 湿绝热递减率、饱和绝热直减率、饱和绝热递减率 |
| 干绝热线 | dry adiabat | — | — | — | — |
| 湿绝热线 | moist adiabat | — | — | — | — |
| 绝对稳定 | absolutely stable | $\Gamma < \Gamma_m$ | — | — | — |
| 条件不稳定 | conditionally unstable | $\Gamma_m < \Gamma < \Gamma_d$ | — | — | 条件性不稳定 |
| 绝对不稳定 | absolutely unstable | $\Gamma > \Gamma_d$ | — | — | — |
| 中性 | neutral | — | — | — | — |
| 浮力频率 | buoyancy frequency | $N$ | s⁻¹ | — | 布伦特-维萨拉频率、BV 频率 |
| 逆温 | temperature inversion | — | — | — | 温度逆增 |
| 对流 | convection | — | — | — | — |
| 对流有效位能 | convective available potential energy | CAPE | J kg⁻¹ | `cape` / `convective_available_potential_energy` | 对流可用位能、对流有效势能、对流可用势能 |
| 对流抑制 | convective inhibition | CIN | J kg⁻¹ | `cin` / `convective_inhibition` | 对流抑制能量、对流抑制能 |
| 抬升凝结高度 | lifting condensation level | LCL | hPa | — | 抬升凝结层 |
| 自由对流高度 | level of free convection | LFC | hPa | — | 自由对流层 |
| 平衡高度 | equilibrium level | EL | hPa | — | 平衡层、中性浮力高度 |
| 温熵图 | tephigram | — | — | — | — |
| 斜温图 | skew-T log-p diagram | — | — | MetPy `SkewT` | 斜 T 图、Skew-T 图 |
| 层结曲线 | environmental temperature profile | — | — | — | 环境曲线 |
| 状态曲线 | parcel temperature profile | — | — | MetPy `parcel_profile` | 气块曲线 |

## 垂直运动

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 垂直速度 | vertical velocity | $w$ | m s⁻¹ | — | 竖直速度 |
| 气压垂直速度 | pressure vertical velocity; omega | $\omega$ | Pa s⁻¹ | `w` / `vertical_velocity` | 垂直气压速度、p 坐标垂直速度 |
| 上升运动 | ascent | — | — | — | — |
| 下沉运动 | descent; subsidence | — | — | — | — |
| 连续方程 | continuity equation | — | — | — | 连续性方程 |

## 涡度与散度

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 涡度 | vorticity | — | s⁻¹ | — | — |
| 相对涡度 | relative vorticity | $\zeta$ | s⁻¹ | `vo` / `vorticity` | — |
| 行星涡度 | planetary vorticity | $f$ | s⁻¹ | — | — |
| 绝对涡度 | absolute vorticity | $\eta$ | s⁻¹ | — | — |
| 位涡 | potential vorticity | PV | PVU | `pv` / `potential_vorticity` | 位势涡度、潜在涡度 |
| 散度 | divergence | $\delta$ | s⁻¹ | `d` / `divergence` | 辐散度 |
| 辐合 | convergence | $\delta < 0$ | — | — | 汇聚、会聚 |
| 辐散 | divergence of the flow | $\delta > 0$ | — | — | — |
| 环流 | circulation | $C$ | m² s⁻¹ | — | — |
| 气旋式 | cyclonic | — | — | — | — |
| 反气旋式 | anticyclonic | — | — | — | — |

## 平流与向量微积分

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 平流 | advection | $-\mathbf{v}_h \cdot \nabla$ | — | — | — |
| 温度平流 | temperature advection | $-\mathbf{v}_h \cdot \nabla T$ | K h⁻¹ | — | 热力平流、热平流、温度输送 |
| 冷平流 | cold advection | — | — | — | — |
| 暖平流 | warm advection | — | — | — | — |
| 涡度平流 | vorticity advection | $-\mathbf{v}_h \cdot \nabla \eta$ | s⁻² | — | 涡度输送 |
| 梯度 | gradient | $\nabla$ | — | — | — |
| 旋度 | curl | $\nabla \times$ | — | — | — |
| 拉普拉斯算子 | Laplacian | $\nabla^2$ | — | — | 拉普拉斯算符 |
| 偏导数 | partial derivative | $\partial$ | — | — | 偏微分 |
| 偏微分方程 | partial differential equation | — | — | — | — |
| 随体导数 | material derivative | $D/Dt$ | — | — | 物质导数、个别导数 |
| 局地变化 | local rate of change | $\partial / \partial t$ | — | — | — |
| 欧拉视角 | Eulerian view | — | — | — | 欧拉观点 |
| 拉格朗日视角 | Lagrangian view | — | — | — | 拉格朗日观点 |
| 流线 | streamline | — | — | — | — |
| 轨迹 | trajectory | — | — | — | 轨线 |
| 有限差分 | finite difference | — | — | — | — |
| 中心差分 | centred difference | — | — | — | 中央差分 |
| 网格 | grid | — | — | — | 格网 |
| 格点 | grid point | — | — | — | 网格点、格网点 |
| 分辨率 | resolution | — | ° | — | 解析度 |
| 纬向 | zonal | $x$ | — | — | 东西向 |
| 经向 | meridional | $y$ | — | — | 南北向 |
| 纬向平均 | zonal mean | — | — | — | 带状平均、纬圈平均 |
| 局地直角坐标系 | local Cartesian coordinate system | $x$, $y$, $z$ | m | — | 局地笛卡尔坐标系 |
| 大圆距离 | great-circle distance | $d$ | km | pyproj `Geod.inv` | — |
| 地球半径 | Earth radius | $R_\mathrm{E}$ | km | MetPy `earth_avg_radius` | — |

## 辐射

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 短波辐射 | shortwave radiation | — | W m⁻² | 地面向下：`ssrd` / `surface_solar_radiation_downwards` | 太阳辐射 |
| 长波辐射 | longwave radiation | — | W m⁻² | 地面向下：`strd` / `surface_thermal_radiation_downwards` | 地球辐射、红外辐射、热辐射 |
| 大气顶入射太阳辐射 | TOA incident solar radiation | TISR | W m⁻² | `tisr` / `toa_incident_solar_radiation` | 大气层顶太阳辐射、入射太阳辐射 |
| 射出长波辐射 | outgoing longwave radiation | OLR | W m⁻² | `ttr` 取负号 / `mean_top_net_long_wave_radiation_flux` 取负号 | 向外长波辐射、出射长波辐射 |
| 净辐射 | net radiation | $R_n$ | W m⁻² | 地面：`ssr` 加 `str` | — |
| 辐照度 | irradiance; radiative flux density | $F$ | W m⁻² | — | 辐射通量密度、辐射通量 |
| 光谱辐照度 | spectral irradiance | $F_\lambda$ | W m⁻² μm⁻¹ | — | 单色辐照度、分光辐照度 |
| 太阳常数 | solar constant | $S_0$ | W m⁻² | — | — |
| 太阳天顶角 | solar zenith angle | — | ° | — | — |
| 反照率 | albedo | $\alpha$ | — | `fal` / `forecast_albedo` | 反照度 |
| 发射率 | emissivity | $\varepsilon$ | — | — | 比辐射率、发射本领 |
| 吸收率 | absorptivity | $a$ | — | — | 吸收比 |
| 黑体 | blackbody | — | — | — | 绝对黑体 |
| 普朗克函数 | Planck function | $B_\lambda$ | W m⁻² sr⁻¹ μm⁻¹ | — | — |
| 亮温 | brightness temperature | $T_b$ | K | GOES ABI L2 `CMI` | 亮度温度 |
| 斯特藩-玻尔兹曼定律 | Stefan–Boltzmann law | $\sigma$ | W m⁻² K⁻⁴ | — | 斯蒂芬-玻尔兹曼定律、斯特番-玻尔兹曼定律 |
| 维恩位移定律 | Wien's displacement law | — | — | — | 维恩定律 |
| 基尔霍夫定律 | Kirchhoff's law | — | — | — | 克希霍夫定律 |
| 比尔-朗伯定律 | Beer–Lambert law | — | — | — | 比尔定律、朗伯-比尔定律 |
| 光学厚度 | optical depth | $\tau$ | — | — | 光学深度 |
| 瑞利散射 | Rayleigh scattering | — | — | — | — |
| 米散射 | Mie scattering | — | — | — | 米氏散射 |
| 温室效应 | greenhouse effect | — | — | — | — |
| 辐射平衡 | radiative equilibrium | — | — | — | 辐射均衡 |
| 累积量 | accumulated field | — | J m⁻² | — | 累计量 |

## 边界层

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 地面 | surface | — | — | — | 地表 |
| 边界层 | atmospheric boundary layer | ABL | — | — | 大气边界层、行星边界层 |
| 边界层高度 | boundary layer height | $z_i$ | m | `blh` / `boundary_layer_height` | 边界层厚度、边界层顶高度 |
| 混合层 | mixed layer | — | — | — | — |
| 稳定边界层 | stable boundary layer | SBL | — | — | 夜间边界层 |
| 残留层 | residual layer | — | — | — | 残余层、剩余层 |
| 夹卷 | entrainment | — | — | — | 卷夹、挟卷、卷挟 |
| 近地层 | surface layer | — | — | — | 近地面层、表面层 |
| 湍流 | turbulence | — | — | — | 乱流 |
| 湍流通量 | turbulent flux | — | — | — | 涡动通量、涡旋通量 |
| 感热通量 | sensible heat flux | $Q_H$ | W m⁻² | `sshf` / `surface_sensible_heat_flux` | 显热通量 |
| 潜热通量 | latent heat flux | $Q_E$ | W m⁻² | `slhf` / `surface_latent_heat_flux` | — |
| 地面能量平衡 | surface energy balance | — | — | — | — |
| 摩擦速度 | friction velocity | $u_*$ | m s⁻¹ | `zust` / `friction_velocity` | 摩阻速度 |
| 粗糙度长度 | roughness length | $z_0$ | m | `fsr` / `forecast_surface_roughness` | 粗糙长度、地面粗糙度 |
| 对数风廓线 | logarithmic wind profile | — | — | — | 对数风速廓线 |
| 莫宁-奥布霍夫长度 | Obukhov length | $L$ | m | — | 奥布霍夫长度 |
| 理查森数 | Richardson number | Ri | — | — | 理查逊数、里查森数 |
| 湍流动能 | turbulent kinetic energy | TKE | m² s⁻² | — | 湍能、湍动能 |
| 雷诺平均 | Reynolds averaging | — | — | — | — |
| 日变化 | diurnal cycle | — | — | — | 日循环、日周期 |
| 埃克曼螺线 | Ekman spiral | — | — | — | 艾克曼螺线、埃克曼螺旋 |

## 云与气溶胶

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 大气成分 | atmospheric composition | — | — | — | — |
| 干空气 | dry air | — | — | — | 干燥空气 |
| 体积混合比 | volume mixing ratio | — | ppm | — | — |
| 臭氧 | ozone | O₃ | kg kg⁻¹ | `o3` / `ozone_mass_mixing_ratio` | — |
| 气溶胶 | aerosol | — | — | — | 气胶、悬浮微粒 |
| 气溶胶光学厚度 | aerosol optical depth | AOD | — | CAMS `aod550` | 气溶胶光学深度 |
| 云凝结核 | cloud condensation nuclei | CCN | cm⁻³ | — | 凝结核 |
| 云滴 | cloud droplet | — | μm | — | 云粒 |
| 雨滴 | raindrop | — | mm | — | — |
| 冰晶 | ice crystal | — | — | — | — |
| 开尔文效应 | Kelvin effect; curvature effect | — | — | — | 曲率效应 |
| 溶质效应 | solute effect | — | — | — | 拉乌尔效应 |
| 科勒曲线 | Köhler curve | — | — | — | 克勒曲线、柯勒曲线 |
| 碰并 | collision–coalescence | — | — | — | 碰撞并合、碰撞合并 |
| 贝吉龙过程 | Wegener–Bergeron–Findeisen process | — | — | — | 冰晶效应、伯杰龙过程 |
| 云量 | cloud cover | — | — | `tcc` / `total_cloud_cover` | 云覆盖率、云覆盖度、云分数 |
| 低云量 | low cloud cover | — | — | `lcc` / `low_cloud_cover` | — |
| 云底高度 | cloud base height | — | m | `cbh` / `cloud_base_height` | — |
| 云顶高度 | cloud top height | — | m | — | — |
| 零度层高度 | freezing level | — | m | `deg0l` / `zero_degree_level` | — |
| 云液水含量 | specific cloud liquid water content | — | g kg⁻¹ | `clwc` / `specific_cloud_liquid_water_content` | 云水含量 |
| 云冰含量 | specific cloud ice water content | — | g kg⁻¹ | `ciwc` / `specific_cloud_ice_water_content` | 云冰水含量 |

## 环流与天气系统

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 大气环流 | general circulation | — | — | — | 大气总环流、全球环流 |
| 经圈环流 | meridional overturning circulation | — | — | — | — |
| 经向质量流函数 | meridional mass streamfunction | $\psi$ | kg s⁻¹ | — | — |
| 哈得来环流 | Hadley cell | — | — | — | 哈德莱环流、哈德利环流、哈得来环流圈 |
| 费雷尔环流 | Ferrel cell | — | — | — | 费雷尔环流圈 |
| 极地环流 | polar cell | — | — | — | 极地环流圈 |
| 热带辐合带 | intertropical convergence zone | ITCZ | — | — | 赤道辐合带 |
| 副热带高压 | subtropical high | — | — | — | 副高 |
| 气团 | air mass | — | — | — | — |
| 锋 | front | — | — | — | 锋面 |
| 冷锋 | cold front | — | — | — | — |
| 暖锋 | warm front | — | — | — | — |
| 锢囚锋 | occluded front | — | — | — | 囚锢锋 |
| 静止锋 | stationary front | — | — | — | 准静止锋 |
| 气旋 | cyclone | — | — | — | — |
| 反气旋 | anticyclone | — | — | — | — |
| 温带气旋 | extratropical cyclone | — | — | — | 温带低压、中纬度气旋、锋面气旋 |
| 低压 | low | — | — | — | 低气压 |
| 高压 | high | — | — | — | 高气压 |
| 槽 | trough | — | — | — | — |
| 脊 | ridge | — | — | — | — |
| 正压 | barotropic | — | — | — | — |
| 斜压 | baroclinic | — | — | — | — |
| 斜压不稳定 | baroclinic instability | — | — | — | 斜压不稳定性 |
| 气旋生成 | cyclogenesis | — | — | — | 气旋发生、气旋新生 |
| 爆发性气旋 | explosive cyclone | — | — | — | 炸弹气旋 |
| 风暴路径 | storm track | — | — | — | 风暴轴 |

## 观测与数据

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 数据 | data | — | — | — | 观测资料、再分析资料 |
| 数据集 | dataset | — | — | — | 资料集、数据组 |
| 观测站 | weather station | — | — | — | 测站、站点 |
| 地面观测 | surface observation | — | — | — | 地面观察 |
| METAR 报文 | METAR report | — | — | IEM `metar` | — |
| 能见度 | visibility | — | m | MetPy `visibility` | — |
| okta | okta | okta | 1 okta = 天空的 1/8 | — | — |
| 观测站填图 | station plot | — | — | MetPy `StationPlot` | — |
| 有效数字 | significant figures | — | — | — | — |
| 探空 | sounding | — | — | — | 高空探测 |
| 探空仪 | radiosonde | — | — | — | 无线电探空仪 |
| 标准等压面 | mandatory pressure level | — | — | — | 标准层 |
| 特性层 | significant level | — | — | — | — |
| 全圆盘图像 | full disk image | — | — | GOES 产品 `ABI-L2-CMIPF` | — |
| 分析场 | analysis | — | — | — | 分析资料、分析数据 |
| 再分析 | reanalysis | — | — | ERA5 | 重分析 |
| 数据同化 | data assimilation | — | — | — | 资料同化 |
| 气候态 | climatology | — | — | — | 气候平均态、气候场、气候均值 |
| 距平 | anomaly | — | — | — | — |

## AI 天气预报与评估

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 数值天气预报 | numerical weather prediction | NWP | — | — | 数值预报 |
| 数值模式 | numerical weather prediction model | — | — | — | 数值模型 |
| AI 天气模型 | AI weather model | — | — | — | AI 气象模型、气象大模型、机器学习天气模型 |
| 预报 | forecast | — | — | — | 预测 |
| 可预报性 | predictability | — | — | — | 可预测性 |
| 起报时间 | initialization time | — | UTC | WeatherBench 2 预报数据的 `time` | 初始化时间、初始时间、起始时间 |
| 预报时效 | lead time | — | h | `prediction_timedelta` | 提前期、预见期、领先时间、前置时间、预报时长 |
| 有效时间 | valid time | — | UTC | `valid_time` | 生效时间 |
| 初始条件 | initial condition | — | — | — | 初始场、初值、初值场 |
| 自回归预报 | autoregressive rollout | — | — | — | 滚动预报 |
| 确定性预报 | deterministic forecast | — | — | — | 确定预报、单一预报 |
| 持续性预报 | persistence forecast | — | — | — | 持续预报、持久性预报 |
| 集合预报 | ensemble forecast | — | — | — | 系综预报、集成预报 |
| 集合成员 | ensemble member | — | — | `number` | 系综成员 |
| 集合平均 | ensemble mean | — | — | — | 系综平均 |
| 集合离散度 | ensemble spread | — | — | — | 系综离散度、集合发散度 |
| 均方误差 | mean squared error | MSE | — | — | — |
| 均方根误差 | root mean squared error | RMSE | 与变量相同 | — | 均方误差根、均方根差、均方差 |
| 偏差 | bias | — | 与变量相同 | — | — |
| 距平相关系数 | anomaly correlation coefficient | ACC | — | — | 异常相关系数、距平相关 |
| 连续分级概率评分 | continuous ranked probability score | CRPS | 与变量相同 | — | 连续排序概率评分、连续等级概率评分 |
| 技巧评分 | skill score | — | — | — | 技巧分数 |
| 纬度加权 | latitude weighting | — | — | — | — |

## 数据约定

下面的约定决定数值的正负号和单位。页面用到这些变量时，必须写出换算。

1. ERA5 的 `z` 是位势，单位 m² s⁻²。位势高度 $Z = \Phi / g_0$，$g_0 = 9.80665$ m s⁻²。
2. WeatherBench 2 的 Z500 是 500 hPa 的位势，单位 m² s⁻²。它不是位势高度。
3. ERA5 的 `w` 是气压垂直速度 $\omega$，单位 Pa s⁻¹。负值表示上升运动。
4. ERA5 的辐射变量和通量变量是累积量，单位 J m⁻²。小时数据除以 3600 s 得到 W m⁻²。
5. ERA5 的垂直通量向下为正。`sshf` 小于零表示地面加热大气。
6. ERA5 的 `ttr` 是大气顶的净长波辐射，向下为正。射出长波辐射等于 `ttr` 取负号。
7. ERA5 的 `tp` 是累积降水量，单位 m。乘以 1000 得到 mm。
8. ERA5 的 `tcc` 是云量，取值区间为 ［0, 1］。
9. `r`、`vo`、`d` 是 ERA5 的短名。ARCO-ERA5 的 37 层数据不含这三个变量。WeatherBench 2 的派生数据集含 `relative_humidity`、`vorticity`、`divergence`。
10. METEO 300 把混合比写作 $w$。本书把混合比写作 $r$，因为 $w$ 已经表示垂直速度。
11. ERA5 的 `r` 是相对湿度，不是混合比。

## 难选的词

下面每一条说明一个选择和它的理由。用户在 2026-10-17 批准了这些选择。

1. 等压面：选它，不选“气压层”和“气压面”。等压面是标准术语，也对应 ERA5 的 pressure levels。
2. 位势高度：选它，不用单独的“高度”。单独的“高度”可以指位势高度，也可以指几何高度。几何意义的高度写“几何高度”。
3. 温度平流：选它，不选“热力平流”。“热力”可以指温度，也可以指能量。
4. 温度：选它，不选“气温”。2 m 的温度写“2 m 温度”，对应 `t2m`。
5. 直减率：选它，不选“递减率”。“直减率”是大气科学名词审定的用词。
6. 科里奥利力：选它，不选“地转偏向力”。它和“科里奥利参数”共用一个词根。
7. 预报：选它，不选“预测”。AI 天气模型的输出也叫预报。
8. 数据：选它，不选“资料”。所以写“数据同化”，不写“资料同化”。
9. 数值模式和 AI 天气模型：物理方程的模型叫“数值模式”，机器学习的模型叫“AI 天气模型”。
10. 辐照度：选它，不选“辐射通量密度”。它对应 METEO 300 第 6 课的 irradiance。
11. 短波辐射：选它，不选“太阳辐射”。只有 `tisr` 用“大气顶入射太阳辐射”。
12. 相当位温：MetPy 的 `equivalent_potential_temperature` 用 Bolton 1980 的公式。严格地说，这个公式算的是假相当位温。本书不把“假相当位温”列为弃用词，因为两者是不同的量。
13. 射出长波辐射：选它，不选“向外长波辐射”。这是 OLR 的标准中文名。
14. 表皮温度：`skt` 用它。“地面温度”和“地表温度”会和 2 m 温度混淆。
15. 压高公式：选它，不选“测高方程”。
16. 锋：选它，不选“锋面”。冷锋、暖锋、锢囚锋都以“锋”结尾。
17. 观测站：选它，不选“站点”和“测站”。
