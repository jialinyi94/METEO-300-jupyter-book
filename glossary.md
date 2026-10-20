# 术语表

本表给每个概念选定一个术语。页面只用“术语”一列的英文词。“中文”和“弃用词”两列的词不进入正文，检查器发现它们就报错。见难选的词第 35 条。

表格的列：

- 术语：本书使用的唯一说法，是一个英文词。它通常是 English term 一列的第一个写法。评分指标写常见的缩写或英文名，例如 RMSE 和 bias，见难选的词第 32 条。
- English term：英文全称和其他英文写法，用分号分隔。
- 中文：术语的中文名。中文名只出现在本表和页面的术语表格里。
- 符号：公式里的符号。本书一个符号只表示一个量。
- 单位：正文使用的单位。
- 变量名：ERA5 短名 / ARCO-ERA5 与 WeatherBench 2 的长名。没有对应变量时写“—”。
- 弃用词：其他不用的同义词，用顿号分隔。

## 气压与高度

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| pressure | pressure | 气压 | $p$ | hPa | 等压面坐标 `level` | 压强、压力、大气压力、毫巴、mb |
| surface pressure | surface pressure | 地面气压 | $p_s$ | hPa | `sp` / `surface_pressure` | 表面气压、本站气压、站点气压 |
| mean sea level pressure | mean sea level pressure | 海平面气压 | $p_{\mathrm{msl}}$ | hPa | `msl` / `mean_sea_level_pressure` | 海平面压力、海压、平均海平面气压 |
| QNH | QNH; altimeter setting | 修正海平面气压 | — | hPa | MetPy `altimeter`，单位 inHg | 修正海压 |
| isobaric surface | isobaric surface; pressure level | 等压面 | — | — | 坐标 `level` | 气压层、气压面、等压层 |
| isobar | isobar | 等压线 | — | — | — | — |
| model level | model level | 模式层 | — | — | — | 模型层 |
| pressure coordinate | pressure coordinate | 气压坐标 | — | — | — | p 坐标、p 坐标系 |
| pressure gradient | pressure gradient | 气压梯度 | $\nabla p$ | hPa km⁻¹ | — | 压力梯度、压强梯度 |
| pressure tendency | pressure tendency | 气压倾向 | $\partial p / \partial t$ | hPa h⁻¹ | — | 气压趋势 |
| geometric height | geometric height | 几何高度 | $z$ | m | — | 高度、海拔、海拔高度 |
| geopotential | geopotential | 位势 | $\Phi$ | m² s⁻² | `z` / `geopotential` | 重力位势、地势 |
| geopotential height | geopotential height | 位势高度 | $Z$ | m | `z` 除以 $g_0$ | 高度、重力位势高度 |
| gravitational acceleration | gravitational acceleration | 重力加速度 | $g$ | m s⁻² | — | — |
| standard gravity | standard gravity | 标准重力加速度 | $g_0$ | m s⁻² | — | 标准重力 |
| surface geopotential height | surface geopotential height; orography | 地形高度 | $Z_s$ | m | `z` 地面场除以 $g_0$ / `geopotential_at_surface` | 地形海拔 |
| land-sea mask | land-sea mask | 海陆掩码 | — | — | `lsm` / `land_sea_mask` | 海陆掩膜、陆海掩码 |
| geopotential height above ground | geopotential height above ground | 离地位势高度 | $Z - Z_s$ | m | — | — |
| thickness | thickness | 厚度 | $\Delta Z$ | m | — | 位势厚度 |
| hypsometric equation | hypsometric equation | 压高公式 | — | — | — | 测高方程、测高公式、压高方程 |
| hydrostatic balance | hydrostatic balance | 静力平衡 | — | — | — | 流体静力平衡、静水平衡、静力学平衡 |
| hydrostatic equation | hydrostatic equation | 静力方程 | — | — | — | 静力学方程、流体静力方程 |
| scale height | scale height | 标高 | $H$ | km | — | 尺度高度 |
| standard atmosphere | standard atmosphere | 标准大气 | — | — | MetPy `pressure_to_height_std` | — |
| density | density | 密度 | $\rho$ | kg m⁻³ | — | — |
| water pressure | water pressure | 水压 | — | hPa | — | — |
| troposphere | troposphere | 对流层 | — | — | — | — |
| tropopause | tropopause | 对流层顶 | — | — | — | — |
| stratosphere | stratosphere | 平流层 | — | — | — | 同温层 |
| top of atmosphere | top of atmosphere | 大气顶 | TOA | — | — | 大气层顶、大气上界 |

## 温度家族

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| temperature | temperature | 温度 | $T$ | K | `t` / `temperature` | 气温 |
| 2 m temperature | 2 m temperature | 2 m 温度 | $T_{2\mathrm{m}}$ | K | `t2m` / `2m_temperature` | 地面温度、近地面温度 |
| skin temperature | skin temperature | 表皮温度 | $T_{\mathrm{skin}}$ | K | `skt` / `skin_temperature` | 地表温度、皮肤温度、地面温度 |
| sea surface temperature | sea surface temperature | 海表温度 | SST | K | `sst` / `sea_surface_temperature` | 海温、海面温度 |
| potential temperature | potential temperature | 位温 | $\theta$ | K | — | 势温、潜在温度 |
| virtual temperature | virtual temperature | 虚温 | $T_v$ | K | — | 虚拟温度 |
| layer-mean temperature | layer-mean temperature | 层平均温度 | $\langle T\rangle$ | K | — | 平均层温度、气层平均温度 |
| virtual potential temperature | virtual potential temperature | 虚位温 | $\theta_v$ | K | — | 虚拟位温 |
| dewpoint temperature | dewpoint temperature | 露点温度 | $T_d$ | K | `d2m` / `2m_dewpoint_temperature` | 露点 |
| dewpoint depression | dewpoint depression | 温度露点差 | $T - T_d$ | K | — | 露点差 |
| wet-bulb temperature | wet-bulb temperature | 湿球温度 | $T_w$ | K | — | — |
| apparent temperature | apparent temperature | 体感温度 | — | °C | MetPy `apparent_temperature` | 表观温度、感觉温度 |
| heat index | heat index | 热指数 | HI | °C | MetPy `heat_index` | 炎热指数 |
| equivalent potential temperature | equivalent potential temperature | 相当位温 | $\theta_e$ | K | — | 等效位温、当量位温 |
| saturation equivalent potential temperature | saturation equivalent potential temperature | 饱和相当位温 | $\theta_{es}$ | K | — | — |
| effective emission temperature | effective emission temperature | 有效发射温度 | $T_e$ | K | — | 有效温度、有效辐射温度、发射温度 |

## 热力学

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| ideal gas law | ideal gas law | 理想气体定律 | — | — | — | 理想气体状态方程 |
| gas constant for dry air | gas constant for dry air | 干空气气体常数 | $R_d$ | J kg⁻¹ K⁻¹ | MetPy `Rd` | — |
| gas constant for water vapour | gas constant for water vapour | 水汽气体常数 | $R_v$ | J kg⁻¹ K⁻¹ | MetPy `Rv` | 水蒸气气体常数 |
| molar gas constant | molar gas constant | 摩尔气体常数 | $R^*$ | J mol⁻¹ K⁻¹ | MetPy `R` | 普适气体常数、通用气体常数 |
| first law of thermodynamics | first law of thermodynamics | 热力学第一定律 | — | — | — | — |
| internal energy | internal energy | 内能 | — | J kg⁻¹ | — | — |
| specific heat capacity at constant pressure | specific heat capacity at constant pressure | 定压比热容 | $c_p$ | J kg⁻¹ K⁻¹ | MetPy `Cp_d` | 定压比热、比定压热容 |
| adiabatic process | adiabatic process | 绝热过程 | — | — | — | — |

## 湿度家族

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| water vapour | water vapour | 水汽 | — | — | — | 水蒸气、水蒸汽、水气 |
| vapour pressure | vapour pressure | 水汽压 | $e$ | hPa | — | 蒸气压、水汽分压、水汽压力 |
| saturation vapour pressure | saturation vapour pressure | 饱和水汽压 | $e_s$ | hPa | — | 饱和蒸气压、饱和水汽分压 |
| specific humidity | specific humidity | 比湿 | $q$ | g kg⁻¹ | `q` / `specific_humidity` | 比湿度 |
| mixing ratio | mixing ratio | 混合比 | $r$ | g kg⁻¹ | — | 混合率 |
| saturation mixing ratio | saturation mixing ratio | 饱和混合比 | $r_s$ | g kg⁻¹ | — | — |
| relative humidity | relative humidity | 相对湿度 | RH | % | `r` / `relative_humidity` | — |
| saturation ratio | saturation ratio | 饱和比 | $S$ | — | — | — |
| supersaturation | supersaturation | 过饱和度 | $S - 1$ | % | — | 超饱和度 |
| precipitable water | precipitable water; total column water vapour | 可降水量 | $W$ | kg m⁻² | `tcwv` / `total_column_water_vapour` | 整层水汽、整层水汽含量、柱水汽、大气可降水量 |
| total column water | total column water | 整层总水量 | — | kg m⁻² | `tcw` / `total_column_water` | 柱总水量 |
| integrated vapour transport | integrated vapour transport | 整层水汽输送 | IVT | kg m⁻¹ s⁻¹ | `integrated_vapor_transport` | — |
| latent heat | latent heat | 潜热 | $L_v$ | J kg⁻¹ | — | — |
| condensation | condensation | 凝结 | — | — | — | 冷凝 |
| evaporation | evaporation | 蒸发 | — | — | `e` / `evaporation` | — |
| saturation | saturation | 饱和 | — | — | — | — |
| Clausius–Clapeyron equation | Clausius–Clapeyron equation | Clausius–Clapeyron 方程 | — | — | — | 克劳修斯-克拉珀龙方程、克-克方程、克拉珀龙方程、克劳修斯-克拉伯龙方程 |
| precipitation | precipitation | 降水 | — | — | — | — |
| precipitation amount | precipitation amount | 降水量 | — | mm | `tp` / `total_precipitation_6hr` | — |
| snowfall | snowfall | 降雪量 | — | mm | `sf` / `snowfall` | — |
| precipitation rate | precipitation rate | 降水率 | — | mm h⁻¹ | IMERG `precipitation` | — |

## 风

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| wind | wind | 风 | $\mathbf{v}$ | m s⁻¹ | — | — |
| horizontal wind | horizontal wind | 水平风 | $\mathbf{v}_h$ | m s⁻¹ | — | — |
| wind speed | wind speed | 风速 | $V$ | m s⁻¹ | `wind_speed` | — |
| wind direction | wind direction | 风向 | $\chi$ | ° | — | — |
| bearing of travel | bearing of travel | 去向方位角 | — | ° | MetPy `wind_direction` 的 `convention="to"` | — |
| math angle | math angle | 数学角 | $\gamma$ | ° | — | — |
| kt | knot | — | kt | 1 kt ≈ 0.514 m s⁻¹ | — | 海里每小时 |
| wind barb | wind barb | 风羽 | — | kt | MetPy `StationPlot.plot_barb` | — |
| zonal wind | zonal wind; u component | 纬向风 | $u$ | m s⁻¹ | `u` / `u_component_of_wind` | u 风、东西风分量 |
| meridional wind | meridional wind; v component | 经向风 | $v$ | m s⁻¹ | `v` / `v_component_of_wind` | v 风、南北风分量 |
| 10 m wind | 10 m wind | 10 m 风 | $u_{10}$, $v_{10}$ | m s⁻¹ | `u10`, `v10` / `10m_u_component_of_wind`, `10m_v_component_of_wind` | 地面风、近地面风 |
| 100 m wind | 100 m wind | 100 m 风 | $u_{100}$, $v_{100}$ | m s⁻¹ | `u100`, `v100` / `100m_u_component_of_wind`, `100m_v_component_of_wind` | — |
| wind gust | wind gust | 阵风 | — | m s⁻¹ | `i10fg` / `instantaneous_10m_wind_gust` | — |
| geostrophic wind | geostrophic wind | 地转风 | $\mathbf{v}_g$ | m s⁻¹ | `geostrophic_wind_speed` | — |
| geostrophic wind speed | geostrophic wind speed | 地转风速 | $V_g$ | m s⁻¹ | — | — |
| ageostrophic wind | ageostrophic wind | 非地转风 | $\mathbf{v}_{ag}$ | m s⁻¹ | `ageostrophic_wind_speed` | 偏地转风 |
| gradient wind | gradient wind | 梯度风 | — | m s⁻¹ | — | — |
| subgeostrophic wind | subgeostrophic wind | 次地转风 | — | m s⁻¹ | — | 亚地转风 |
| supergeostrophic wind | supergeostrophic wind | 超地转风 | — | m s⁻¹ | — | — |
| cross-isobar angle | cross-isobar angle | 穿越角 | $\gamma - \gamma_g$ | ° | — | 越等压线角 |
| ageostrophic wind fraction | ageostrophic wind fraction | 非地转风比例 | — | — | — | — |
| thermal wind | thermal wind | 热成风 | $\mathbf{v}_T$ | m s⁻¹ | — | 热风 |
| thermal wind equation | thermal wind equation | 热成风方程 | — | — | — | 热风方程 |
| veering | veering | 顺转 | — | — | — | 顺时针转向 |
| backing | backing | 逆转 | — | — | — | 逆时针转向 |
| hodograph | hodograph | 风矢端图 | — | m s⁻¹ | MetPy `Hodograph` | 风速矢端图、速端图 |
| vertical wind shear | vertical wind shear | 垂直风切变 | $\partial \mathbf{v}_h / \partial z$ | s⁻¹ | — | 风切、垂直切变 |
| jet stream | jet stream | 急流 | — | — | — | 喷流 |
| subtropical jet | subtropical jet | 副热带急流 | — | m s⁻¹ | — | — |
| eddy-driven jet | eddy-driven jet | 涡驱动急流 | — | m s⁻¹ | — | 极锋急流 |
| low-level jet | low-level jet | 低空急流 | — | m s⁻¹ | — | 低层急流、夜间急流、边界层急流 |
| trade winds | trade winds | 信风 | — | — | — | 贸易风 |
| westerlies | westerlies | 西风带 | — | — | — | — |

## 力与平衡

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| pressure gradient force | pressure gradient force | 气压梯度力 | PGF | m s⁻² | — | 压力梯度力、压强梯度力 |
| Coriolis force | Coriolis force | Coriolis 力 | — | m s⁻² | — | 科里奥利力、科氏力、地转偏向力、柯氏力 |
| Coriolis parameter | Coriolis parameter | Coriolis 参数 | $f$ | s⁻¹ | — | 科里奥利参数、科氏参数、地转参数 |
| Earth's angular velocity | Earth's angular velocity | 地球自转角速度 | $\Omega$ | s⁻¹ | — | — |
| friction | friction | 摩擦力 | — | m s⁻² | — | — |
| geostrophic balance | geostrophic balance | 地转平衡 | — | — | — | — |
| gradient wind balance | gradient wind balance | 梯度风平衡 | — | — | — | 梯度平衡 |
| centripetal acceleration | centripetal acceleration | 向心加速度 | $V^2/R$ | m s⁻² | — | — |
| radius of curvature | radius of curvature | 曲率半径 | $R$ | km | — | — |
| Rossby number | Rossby number | Rossby 数 | Ro | — | — | 罗斯贝数、罗斯比数 |
| scale analysis | scale analysis | 尺度分析 | — | — | — | 量级分析 |
| f-plane | f-plane | f 平面 | — | — | — | — |
| inertial oscillation | inertial oscillation | 惯性振荡 | — | — | — | 惯性振动 |
| inertial circle | inertial circle | 惯性圆 | — | km | — | — |
| inertial period | inertial period | 惯性周期 | — | h | — | — |

## 稳定度

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| air parcel | air parcel | 气块 | — | — | — | 空气块 |
| buoyancy | buoyancy | 浮力 | $B$ | m s⁻² | — | 浮升力 |
| static stability | static stability | 静力稳定度 | — | — | — | 静力稳定性、大气稳定性、层结稳定度 |
| stratification | stratification | 层结 | — | — | — | — |
| environmental lapse rate | environmental lapse rate | 环境直减率 | $\Gamma$ | K km⁻¹ | — | 环境递减率、温度直减率、气温直减率、温度递减率 |
| dry adiabatic lapse rate | dry adiabatic lapse rate | 干绝热直减率 | $\Gamma_d$ | K km⁻¹ | — | 干绝热递减率、干绝热减温率 |
| moist adiabatic lapse rate | moist adiabatic lapse rate | 湿绝热直减率 | $\Gamma_m$ | K km⁻¹ | — | 湿绝热递减率、饱和绝热直减率、饱和绝热递减率 |
| dry adiabat | dry adiabat | 干绝热线 | — | — | — | — |
| moist adiabat | moist adiabat | 湿绝热线 | — | — | — | — |
| absolutely stable | absolutely stable | 绝对稳定 | $\Gamma < \Gamma_m$ | — | — | — |
| conditionally unstable | conditionally unstable | 条件不稳定 | $\Gamma_m < \Gamma < \Gamma_d$ | — | — | 条件性不稳定 |
| absolutely unstable | absolutely unstable | 绝对不稳定 | $\Gamma > \Gamma_d$ | — | — | — |
| neutral | neutral | 中性 | — | — | — | — |
| buoyancy frequency | buoyancy frequency | 浮力频率 | $N$ | s⁻¹ | — | 布伦特-维萨拉频率、BV 频率 |
| temperature inversion | temperature inversion | 逆温 | — | — | — | 温度逆增 |
| convection | convection | 对流 | — | — | — | — |
| convective available potential energy | convective available potential energy | 对流有效位能 | CAPE | J kg⁻¹ | `cape` / `convective_available_potential_energy` | 对流可用位能、对流有效势能、对流可用势能 |
| convective inhibition | convective inhibition | 对流抑制 | CIN | J kg⁻¹ | `cin` / `convective_inhibition` | 对流抑制能量、对流抑制能 |
| lifting condensation level | lifting condensation level | 抬升凝结高度 | LCL | hPa | — | 抬升凝结层 |
| level of free convection | level of free convection | 自由对流高度 | LFC | hPa | — | 自由对流层 |
| equilibrium level | equilibrium level | 平衡高度 | EL | hPa | — | 平衡层、中性浮力高度 |
| tephigram | tephigram | 温熵图 | — | — | — | — |
| skew-T log-p diagram | skew-T log-p diagram | 斜温图 | — | — | MetPy `SkewT` | 斜 T 图、Skew-T 图 |
| environmental temperature profile | environmental temperature profile | 层结曲线 | — | — | — | 环境曲线 |
| parcel temperature profile | parcel temperature profile | 状态曲线 | — | — | MetPy `parcel_profile` | 气块曲线 |
| thermodynamic diagram | thermodynamic diagram | 热力图 | — | — | — | 热力学图解、热力学图 |
| specific entropy | specific entropy | 比熵 | $s$ | J kg⁻¹ K⁻¹ | — | — |
| isotherm | isotherm | 等温线 | — | — | — | — |
| saturation mixing ratio line | saturation mixing ratio line | 等饱和混合比线 | — | g kg⁻¹ | MetPy `plot_mixing_lines` | 等混合比线 |
| thunderstorm | thunderstorm | 雷暴 | — | — | — | 雷雨 |
| severe convective weather | severe convective weather | 强对流 | — | — | — | — |
| tornado | tornado | 龙卷 | — | — | — | 龙卷风 |

## 垂直运动

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| vertical velocity | vertical velocity | 垂直速度 | $w$ | m s⁻¹ | — | 竖直速度 |
| pressure vertical velocity | pressure vertical velocity; omega | 气压垂直速度 | $\omega$ | Pa s⁻¹ | `w` / `vertical_velocity` | 垂直气压速度、p 坐标垂直速度 |
| ascent | ascent | 上升运动 | — | — | — | — |
| descent | descent; subsidence | 下沉运动 | — | — | — | — |
| continuity equation | continuity equation | 连续方程 | — | — | — | 连续性方程 |
| kinematic method | kinematic method | 运动学方法 | — | — | — | 运动学法 |
| O'Brien correction | O'Brien correction | O'Brien 订正 | — | — | — | — |

## 涡度与散度

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| vorticity | vorticity | 涡度 | — | s⁻¹ | — | — |
| relative vorticity | relative vorticity | 相对涡度 | $\zeta$ | s⁻¹ | `vo` / `vorticity` | — |
| planetary vorticity | planetary vorticity | 行星涡度 | $f$ | s⁻¹ | — | — |
| absolute vorticity | absolute vorticity | 绝对涡度 | $\eta$ | s⁻¹ | — | — |
| potential vorticity | potential vorticity | 位涡 | PV | PVU | `pv` / `potential_vorticity` | 位势涡度、潜在涡度 |
| divergence | divergence | 散度 | $\delta$ | s⁻¹ | `d` / `divergence` | 辐散度 |
| convergence | convergence | 辐合 | $\delta < 0$ | — | — | 汇聚、会聚 |
| divergence of the flow | divergence of the flow | 辐散 | $\delta > 0$ | — | — | — |
| deformation | deformation | 变形 | — | s⁻¹ | — | 形变 |
| circulation | circulation | 环流 | $C$ | m² s⁻¹ | — | — |
| cyclonic | cyclonic | 气旋式 | — | — | — | — |
| anticyclonic | anticyclonic | 反气旋式 | — | — | — | — |
| vorticity equation | vorticity equation | 涡度方程 | — | s⁻² | — | — |
| level of nondivergence | level of nondivergence | 无辐散层 | — | hPa | — | 无辐散高度 |
| dynamical tropopause | dynamical tropopause | 动态对流层顶 | — | PVU | 2 PVU 等值面 | 动力对流层顶 |

## 平流与向量微积分

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| advection | advection | 平流 | $-\mathbf{v}_h \cdot \nabla$ | — | — | — |
| temperature advection | temperature advection | 温度平流 | $-\mathbf{v}_h \cdot \nabla T$ | K h⁻¹ | — | 热力平流、热平流、温度输送 |
| cold advection | cold advection | 冷平流 | — | — | — | — |
| warm advection | warm advection | 暖平流 | — | — | — | — |
| vorticity advection | vorticity advection | 涡度平流 | $-\mathbf{v}_h \cdot \nabla \eta$ | s⁻² | — | 涡度输送 |
| gradient | gradient | 梯度 | $\nabla$ | — | — | — |
| curl | curl | 旋度 | $\nabla \times$ | — | — | — |
| Laplacian | Laplacian | Laplace 算子 | $\nabla^2$ | — | — | 拉普拉斯算子、拉普拉斯算符 |
| Fourier transform | Fourier transform | Fourier 变换 | — | — | NumPy `fft.rfft` | 傅里叶变换、傅立叶变换 |
| Parseval's theorem | Parseval's theorem | Parseval 定理 | — | — | — | 帕塞瓦尔定理 |
| spherical harmonics | spherical harmonics | 球谐函数 | — | — | pyshtools | 球面调和函数 |
| partial derivative | partial derivative | 偏导数 | $\partial$ | — | — | 偏微分 |
| partial differential equation | partial differential equation | 偏微分方程 | — | — | — | — |
| material derivative | material derivative | 随体导数 | $D/Dt$ | — | — | 物质导数、个别导数 |
| local rate of change | local rate of change | 局地变化 | $\partial / \partial t$ | — | — | — |
| Eulerian view | Eulerian view | Euler 视角 | — | — | — | 欧拉视角、欧拉观点 |
| Lagrangian view | Lagrangian view | Lagrange 视角 | — | — | — | 拉格朗日视角、拉格朗日观点 |
| streamline | streamline | 流线 | — | — | — | — |
| trajectory | trajectory | 轨迹 | — | — | — | 轨线 |
| finite difference | finite difference | 有限差分 | — | — | — | — |
| centred difference | centred difference | 中心差分 | — | — | — | 中央差分 |
| grid | grid | 网格 | — | — | — | 格网 |
| grid point | grid point | 格点 | — | — | — | 网格点、格网点 |
| grid spacing | grid spacing | 网格间距 | $\Delta\lambda$, $\Delta\varphi$ | °, km | — | 格距、格点间距、网格距 |
| resolution | resolution | 分辨率 | — | ° | — | 解析度 |
| zonal | zonal | 纬向 | $x$ | — | — | 东西向 |
| meridional | meridional | 经向 | $y$ | — | — | 南北向 |
| longitude | longitude | 经度 | $\lambda$ | ° | 坐标 `longitude` | — |
| latitude | latitude | 纬度 | $\varphi$ | ° | 坐标 `latitude` | — |
| zonal mean | zonal mean | 纬向平均 | — | — | — | 带状平均、纬圈平均 |
| latitude circle | latitude circle | 纬圈 | — | — | — | — |
| local Cartesian coordinate system | local Cartesian coordinate system | 局地直角坐标系 | $x$, $y$, $z$ | m | — | 局地笛卡尔坐标系 |
| Lambert conformal conic projection | Lambert conformal conic projection | Lambert 投影 | — | — | cartopy `LambertConformal` | 兰伯特投影、兰勃特投影 |
| great-circle distance | great-circle distance | 大圆距离 | $d$ | km | pyproj `Geod.inv` | — |
| central angle | central angle | 地心夹角 | $\xi$ | rad | — | 圆心角 |
| Earth radius | Earth radius | 地球半径 | $R_\mathrm{E}$ | km | MetPy `earth_avg_radius` | — |
| metric term | metric term | 曲率项 | — | — | — | 度量项 |
| midpoint method | midpoint method | 中点法 | — | — | — | 中点公式 |
| linear interpolation | linear interpolation | 线性插值 | — | — | — | — |
| bilinear interpolation | bilinear interpolation | 双线性插值 | — | — | — | — |

## 辐射

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| shortwave radiation | shortwave radiation | 短波辐射 | — | W m⁻² | 地面向下：`ssrd` / `surface_solar_radiation_downwards` | 太阳辐射 |
| longwave radiation | longwave radiation | 长波辐射 | — | W m⁻² | 地面向下：`strd` / `surface_thermal_radiation_downwards` | 地球辐射、红外辐射、热辐射 |
| TOA incident solar radiation | TOA incident solar radiation | 大气顶入射太阳辐射 | TISR | W m⁻² | `tisr` / `toa_incident_solar_radiation` | 大气层顶太阳辐射、入射太阳辐射 |
| outgoing longwave radiation | outgoing longwave radiation | 射出长波辐射 | OLR | W m⁻² | `ttr` 取负号 / `mean_top_net_long_wave_radiation_flux` 取负号 | 向外长波辐射、出射长波辐射 |
| net radiation | net radiation | 净辐射 | $R_n$ | W m⁻² | 地面：`ssr` 加 `str` | — |
| irradiance | irradiance; radiative flux density | 辐照度 | $F$ | W m⁻² | — | 辐射通量密度、辐射通量 |
| spectral irradiance | spectral irradiance | 光谱辐照度 | $F_\Lambda$ | W m⁻² μm⁻¹ | — | 单色辐照度、分光辐照度 |
| wavelength | wavelength | 波长 | $\Lambda$ | μm | — | — |
| solar constant | solar constant | 太阳常数 | $S_0$ | W m⁻² | — | — |
| solar zenith angle | solar zenith angle | 太阳天顶角 | $Z$ | ° | earthkit-meteo `cos_solar_zenith_angle` 给出 $\cos Z$ | — |
| albedo | albedo | 反照率 | $\alpha$ | — | `fal` / `forecast_albedo` | 反照度 |
| emissivity | emissivity | 发射率 | $\varepsilon$ | — | — | 比辐射率、发射本领 |
| absorptivity | absorptivity | 吸收率 | $a$ | — | — | 吸收比 |
| blackbody | blackbody | 黑体 | — | — | — | 绝对黑体 |
| Planck function | Planck function | Planck 函数 | $B_\Lambda$ | W m⁻² sr⁻¹ μm⁻¹ | — | 普朗克函数 |
| brightness temperature | brightness temperature | 亮温 | $T_b$ | K | GOES ABI L2 `CMI` | 亮度温度 |
| Stefan–Boltzmann law | Stefan–Boltzmann law | Stefan–Boltzmann 定律 | $\sigma$ | W m⁻² K⁻⁴ | — | 斯特藩-玻尔兹曼定律、斯蒂芬-玻尔兹曼定律、斯特番-玻尔兹曼定律 |
| Wien's displacement law | Wien's displacement law | Wien 位移定律 | — | — | — | 维恩位移定律、维恩定律 |
| Kirchhoff's law | Kirchhoff's law | Kirchhoff 定律 | — | — | — | 基尔霍夫定律、克希霍夫定律 |
| Beer–Lambert law | Beer–Lambert law | Beer–Lambert 定律 | — | — | — | 比尔-朗伯定律、比尔定律、朗伯-比尔定律 |
| optical depth | optical depth | 光学厚度 | $\tau$ | — | — | 光学深度 |
| Rayleigh scattering | Rayleigh scattering | Rayleigh 散射 | — | — | — | 瑞利散射 |
| Mie scattering | Mie scattering | Mie 散射 | — | — | — | 米散射、米氏散射 |
| greenhouse effect | greenhouse effect | 温室效应 | — | — | — | — |
| radiative equilibrium | radiative equilibrium | 辐射平衡 | — | — | — | 辐射均衡 |
| accumulated field | accumulated field | 累积量 | — | J m⁻² | — | 累计量 |
| radiance | radiance | 辐亮度 | $I$ | W m⁻² sr⁻¹ μm⁻¹ | GOES ABI L1b `Rad` | 辐射亮度 |
| wavenumber | wavenumber | 波数 | $\tilde{\nu}$ | cm⁻¹ | — | — |
| spectral band | spectral band | 波段 | — | μm | GOES ABI `C02`、`C08`、`C13` | 光谱通道 |
| atmospheric window | atmospheric window | 大气窗区 | — | μm | — | 大气窗口、窗口区 |
| reflectance | reflectance | 反射率 | — | % | GOES ABI L2 `CMI`，可见光波段 | 反射比 |
| transmittance | transmittance | 透过率 | $\mathcal{T}$ | — | — | 透射率、透射比 |
| relative optical air mass | relative optical air mass | 大气光学质量 | $m$ | — | pvlib `get_relative_airmass` | — |
| effective optical depth | effective optical depth | 等效光学厚度 | $\tau_{\mathrm{eff}}$ | — | — | — |
| solar declination | solar declination | 太阳赤纬 | $\delta_\odot$ | ° | earthkit-meteo `solar_declination_angle` | 赤纬角 |
| hour angle | hour angle | 时角 | $h_\odot$ | ° | — | 太阳时角 |
| clear sky | clear sky | 晴空 | — | — | ERA5 `ssrdc`；pvlib `Location.get_clearsky` | — |
| grey atmosphere | grey atmosphere | 灰体大气 | — | — | climlab `GreyRadiationModel` | 灰色大气 |
| radiative–convective equilibrium | radiative–convective equilibrium | 辐射对流平衡 | RCE | — | climlab `RadiativeConvectiveModel` | 辐射-对流平衡 |
| convective adjustment | convective adjustment | 对流调整 | — | — | climlab `ConvectiveAdjustment` | — |
| geostationary satellite | geostationary satellite | 静止卫星 | — | — | GOES、Meteosat、Himawari | 地球静止卫星、同步卫星 |
| polar-orbiting satellite | polar-orbiting satellite | 极轨卫星 | — | — | NOAA-20、Metop | 极地轨道卫星 |
| radiative transfer model | radiative transfer model | 辐射传输模式 | — | — | RTTOV | 辐射传输模型 |
| Planck constant | Planck constant | Planck 常数 | $h$ | J s | `scipy.constants.h` | 普朗克常数 |
| Boltzmann constant | Boltzmann constant | Boltzmann 常数 | $k_B$ | J K⁻¹ | `scipy.constants.k` | 玻尔兹曼常数 |
| speed of light | speed of light | 光速 | $c$ | m s⁻¹ | `scipy.constants.c` | — |
| PV power output | PV power output | 光伏出力 | $P_{\mathrm{PV}}$ | MW | pvlib `pvwatts_dc` | 光伏功率 |

## 边界层

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| surface | surface | 地面 | — | — | — | 地表 |
| atmospheric boundary layer | atmospheric boundary layer | 边界层 | ABL | — | — | 大气边界层、行星边界层 |
| boundary layer height | boundary layer height | 边界层高度 | $z_i$ | m | `blh` / `boundary_layer_height` | 边界层厚度、边界层顶高度 |
| mixed layer | mixed layer | 混合层 | — | — | — | — |
| stable boundary layer | stable boundary layer | 稳定边界层 | SBL | — | — | 夜间边界层 |
| residual layer | residual layer | 残留层 | — | — | — | 残余层、剩余层 |
| entrainment | entrainment | 夹卷 | — | — | — | 卷夹、挟卷、卷挟 |
| surface layer | surface layer | 近地层 | — | — | — | 近地面层、表面层 |
| turbulence | turbulence | 湍流 | — | — | — | 乱流 |
| turbulent flux | turbulent flux | 湍流通量 | — | — | — | 涡动通量、涡旋通量 |
| sensible heat flux | sensible heat flux | 感热通量 | $Q_H$ | W m⁻² | `sshf` / `surface_sensible_heat_flux` | 显热通量 |
| latent heat flux | latent heat flux | 潜热通量 | $Q_E$ | W m⁻² | `slhf` / `surface_latent_heat_flux` | — |
| surface energy balance | surface energy balance | 地面能量平衡 | — | — | — | — |
| friction velocity | friction velocity | 摩擦速度 | $u_*$ | m s⁻¹ | `zust` / `friction_velocity` | 摩阻速度 |
| roughness length | roughness length | 粗糙度长度 | $z_0$ | m | `fsr` / `forecast_surface_roughness` | 粗糙长度、地面粗糙度 |
| logarithmic wind profile | logarithmic wind profile | 对数风廓线 | — | — | — | 对数风速廓线 |
| Obukhov length | Obukhov length | Monin–Obukhov 长度 | $L$ | m | — | 莫宁-奥布霍夫长度、奥布霍夫长度 |
| Richardson number | Richardson number | Richardson 数 | Ri | — | — | 理查森数、理查逊数、里查森数 |
| turbulent kinetic energy | turbulent kinetic energy | 湍流动能 | TKE | m² s⁻² | — | 湍能、湍动能 |
| Reynolds averaging | Reynolds averaging | Reynolds 平均 | — | — | — | 雷诺平均 |
| diurnal cycle | diurnal cycle | 日变化 | — | — | — | 日循环、日周期 |
| Ekman spiral | Ekman spiral | Ekman 螺线 | — | — | — | 埃克曼螺线、艾克曼螺线、埃克曼螺旋 |
| turbulent fluctuation | turbulent fluctuation | 脉动量 | $u'$ | 与变量相同 | — | 脉动值、湍流脉动 |
| variance | variance | 方差 | $\overline{u'^2}$ | 变量单位的平方 | — | — |
| covariance | covariance | 协方差 | $\overline{a'b'}$ | 两个变量单位的乘积 | — | — |
| kinematic flux | kinematic flux | 运动学通量 | — | — | — | — |
| momentum flux | momentum flux | 动量通量 | $\overline{u'w'}$ | m² s⁻² | — | — |
| eddy covariance | eddy covariance | 涡动协方差 | — | — | — | 涡度相关、涡动相关 |
| sonic anemometer | sonic anemometer | 超声风速仪 | — | — | — | 超声风速计 |
| sonic temperature | sonic temperature | 超声温度 | $T_s$ | °C | — | — |
| power-law wind profile | power-law wind profile | 幂律风廓线 | — | — | — | 指数风廓线 |
| power-law exponent | power-law exponent | 幂律指数 | $n$ | — | — | 风切变指数、Hellmann 指数 |
| hub height | hub height | 轮毂高度 | $z_{\mathrm{hub}}$ | m | — | 轮毂高 |
| wind power output | wind power output | 风电出力 | $P_{\mathrm{W}}$ | MW | — | 风电功率 |
| power curve | power curve | 功率曲线 | — | — | — | 功率特性曲线 |
| capacity factor | capacity factor | 容量系数 | — | % | — | 容量因子 |
| cut-in wind speed | cut-in wind speed | 切入风速 | $V_{\mathrm{in}}$ | m s⁻¹ | — | 启动风速 |
| rated wind speed | rated wind speed | 额定风速 | $V_{\mathrm{rated}}$ | m s⁻¹ | — | — |
| cut-out wind speed | cut-out wind speed | 切出风速 | $V_{\mathrm{out}}$ | m s⁻¹ | — | 停机风速 |
| rated power | rated power | 额定功率 | — | MW | — | — |
| installed capacity | installed capacity | 装机容量 | — | GW | — | 装机量 |

## 云与气溶胶

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| atmospheric composition | atmospheric composition | 大气成分 | — | — | — | — |
| dry air | dry air | 干空气 | — | — | — | 干燥空气 |
| volume mixing ratio | volume mixing ratio | 体积混合比 | — | ppm | — | — |
| carbon dioxide | carbon dioxide | 二氧化碳 | CO₂ | ppm | NOAA GML `average` | — |
| greenhouse gas | greenhouse gas | 温室气体 | — | — | — | — |
| seasonal cycle | seasonal cycle | 季节循环 | — | — | — | — |
| seasonal amplitude | seasonal amplitude; peak-to-trough amplitude | 季节振幅 | — | ppm | — | — |
| annual growth rate | annual growth rate | 年增长率 | — | ppm a⁻¹ | — | — |
| ozone | ozone | 臭氧 | O₃ | kg kg⁻¹ | `o3` / `ozone_mass_mixing_ratio` | — |
| aerosol | aerosol | 气溶胶 | — | — | — | 气胶、悬浮微粒 |
| aerosol optical depth | aerosol optical depth | 气溶胶光学厚度 | AOD | — | CAMS `aod550` | 气溶胶光学深度 |
| mineral dust | mineral dust | 沙尘 | — | — | CAMS `duaod550` | — |
| sea salt | sea salt | 海盐 | — | — | CAMS `ssaod550` | — |
| sulphate | sulphate | 硫酸盐 | — | — | CAMS `suaod550` | — |
| organic matter | organic matter | 有机物 | — | — | CAMS `omaod550` | — |
| wet deposition | wet deposition | 湿沉降 | — | — | — | — |
| cloud condensation nuclei | cloud condensation nuclei | 云凝结核 | CCN | cm⁻³ | — | 凝结核 |
| ice-nucleating particle | ice-nucleating particle | 冰核 | INP | — | — | — |
| activation | activation | 活化 | — | — | — | — |
| haze droplet | haze droplet | 霾滴 | — | μm | — | — |
| drop radius | drop radius | 滴半径 | $r_\mathrm{d}$ | μm | — | — |
| critical radius | critical radius | 临界半径 | $r_\mathrm{c}$ | μm | — | — |
| dry particle radius | dry particle radius | 干颗粒半径 | $r_0$ | μm | — | — |
| equilibrium vapour pressure | equilibrium vapour pressure | 平衡水汽压 | $e_\mathrm{eq}$ | hPa | — | — |
| equilibrium saturation ratio | equilibrium saturation ratio | 平衡饱和比 | $S_\mathrm{eq}$ | — | — | — |
| critical supersaturation | critical supersaturation | 临界过饱和度 | $S_\mathrm{c} - 1$ | % | — | — |
| surface tension | surface tension | 表面张力 | $\sigma_\mathrm{w}$ | N m⁻¹ | — | — |
| molar concentration of liquid water | molar concentration of liquid water | 液态水摩尔浓度 | $n_\mathrm{L}$ | mol m⁻³ | — | — |
| Kelvin coefficient | Kelvin coefficient | Kelvin 系数 | $a_\mathrm{K}$ | m | — | — |
| Raoult's law | Raoult's law | Raoult 定律 | — | — | — | 拉乌尔定律 |
| amount of solute | amount of solute | 溶质物质的量 | $N_\mathrm{s}$ | mol | — | — |
| mole fraction of solute | mole fraction of solute | 溶质摩尔分数 | $x_\mathrm{s}$ | — | — | — |
| van 't Hoff factor | van 't Hoff factor | van 't Hoff 因子 | $i$ | — | — | 范特霍夫因子 |
| solute coefficient | solute coefficient | 溶质系数 | $b_\mathrm{s}$ | m³ | — | — |
| cloud droplet | cloud droplet | 云滴 | — | μm | — | 云粒 |
| raindrop | raindrop | 雨滴 | — | mm | — | — |
| ice crystal | ice crystal | 冰晶 | — | — | — | — |
| Kelvin effect | Kelvin effect; curvature effect | Kelvin 效应 | — | — | — | 开尔文效应、曲率效应 |
| solute effect | solute effect | 溶质效应 | — | — | — | 拉乌尔效应 |
| Köhler curve | Köhler curve | Köhler 曲线 | — | — | — | 科勒曲线、克勒曲线、柯勒曲线 |
| collision–coalescence | collision–coalescence | 碰并 | — | — | — | 碰撞并合、碰撞合并 |
| Wegener–Bergeron–Findeisen process | Wegener–Bergeron–Findeisen process | Bergeron 过程 | — | — | — | 贝吉龙过程、冰晶效应、伯杰龙过程 |
| cloud cover | cloud cover | 云量 | — | — | `tcc` / `total_cloud_cover` | 云覆盖率、云覆盖度、云分数 |
| low cloud cover | low cloud cover | 低云量 | — | — | `lcc` / `low_cloud_cover` | — |
| cloud base height | cloud base height | 云底高度 | — | m | `cbh` / `cloud_base_height` | — |
| cloud top height | cloud top height | 云顶高度 | — | m | — | — |
| freezing level | freezing level | 零度层高度 | — | m | `deg0l` / `zero_degree_level` | — |
| specific cloud liquid water content | specific cloud liquid water content | 云液水含量 | — | g kg⁻¹ | `clwc` / `specific_cloud_liquid_water_content` | 云水含量 |
| specific cloud ice water content | specific cloud ice water content | 云冰含量 | — | g kg⁻¹ | `ciwc` / `specific_cloud_ice_water_content` | 云冰水含量 |

## 环流与天气系统

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| general circulation | general circulation | 大气环流 | — | — | — | 大气总环流、全球环流 |
| meridional overturning circulation | meridional overturning circulation | 经圈环流 | — | — | — | — |
| meridional mass streamfunction | meridional mass streamfunction | 经向质量流函数 | $\psi$ | kg s⁻¹ | — | — |
| Hadley cell | Hadley cell | Hadley 环流 | — | — | — | 哈得来环流、哈德莱环流、哈德利环流、哈得来环流圈 |
| Ferrel cell | Ferrel cell | Ferrel 环流 | — | — | — | 费雷尔环流、费雷尔环流圈 |
| polar cell | polar cell | 极地环流 | — | — | — | 极地环流圈 |
| intertropical convergence zone | intertropical convergence zone | 热带辐合带 | ITCZ | — | — | 赤道辐合带 |
| subtropical high | subtropical high | 副热带高压 | — | — | — | 副高 |
| equatorial low-pressure belt | equatorial low-pressure belt | 赤道低压带 | — | — | — | 赤道低压槽 |
| subtropical high-pressure belt | subtropical high-pressure belt | 副热带高压带 | — | — | — | — |
| subpolar low-pressure belt | subpolar low-pressure belt | 副极地低压带 | — | — | — | 副极地低压槽 |
| Icelandic Low | Icelandic Low | 冰岛低压 | — | — | — | — |
| Azores High | Azores High | 亚速尔高压 | — | — | — | — |
| Aleutian Low | Aleutian Low | 阿留申低压 | — | — | — | — |
| North Atlantic Oscillation | North Atlantic Oscillation | 北大西洋涛动 | NAO | — | — | 北大西洋振荡 |
| air mass | air mass | 气团 | — | — | — | — |
| front | front | 锋 | — | — | — | 锋面 |
| cold front | cold front | 冷锋 | — | — | — | — |
| warm front | warm front | 暖锋 | — | — | — | — |
| occluded front | occluded front | 锢囚锋 | — | — | — | 囚锢锋 |
| warm sector | warm sector | 暖区 | — | — | — | 暖扇区 |
| frontogenesis | frontogenesis | 锋生 | — | — | — | 锋面生成 |
| frontogenesis function | frontogenesis function | 锋生函数 | $\mathcal{F}$ | K (100 km)⁻¹ (3 h)⁻¹ | MetPy `frontogenesis`，单位 K m⁻¹ s⁻¹ | — |
| stationary front | stationary front | 静止锋 | — | — | — | 准静止锋 |
| cyclone | cyclone | 气旋 | — | — | — | — |
| anticyclone | anticyclone | 反气旋 | — | — | — | — |
| extratropical cyclone | extratropical cyclone | 温带气旋 | — | — | — | 温带低压、中纬度气旋、锋面气旋 |
| low | low | 低压 | — | — | — | 低气压 |
| high | high | 高压 | — | — | — | 高气压 |
| trough | trough | 槽 | — | — | — | — |
| ridge | ridge | 脊 | — | — | — | — |
| barotropic | barotropic | 正压 | — | — | — | — |
| baroclinic | baroclinic | 斜压 | — | — | — | — |
| baroclinic instability | baroclinic instability | 斜压不稳定 | — | — | — | 斜压不稳定性 |
| cyclogenesis | cyclogenesis | 气旋生成 | — | — | — | 气旋发生、气旋新生 |
| explosive cyclone | explosive cyclone | 爆发性气旋 | — | — | — | 炸弹气旋 |
| low centre | low centre | 低压中心 | — | — | `msl` 的局地极小值 | 风暴中心 |
| cyclone centre | cyclone centre | 气旋中心 | — | — | — | 风暴中心 |
| central pressure | central pressure | 中心气压 | $p_c$ | hPa | 低压中心的 `msl` | 中心压力 |
| cyclone track | cyclone track | 气旋路径 | — | — | — | 气旋轨迹 |
| cyclone tracking | cyclone tracking | 气旋追踪 | — | — | — | 气旋跟踪 |
| local minimum | local minimum | 局地极小值 | — | — | — | 局部极小值、局部最小值 |
| search radius | search radius | 搜索半径 | — | km | — | — |
| match radius | match radius | 匹配半径 | — | km | — | 匹配距离 |
| storm track | storm track | 风暴路径 | — | — | — | 风暴轴 |
| gravity wave | gravity wave | 重力波 | — | — | — | — |

## 观测与数据

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| data | data | 数据 | — | — | — | 观测资料、再分析资料 |
| dataset | dataset | 数据集 | — | — | — | 资料集、数据组 |
| weather station | weather station | 观测站 | — | — | — | 测站、站点 |
| surface observation | surface observation | 地面观测 | — | — | — | 地面观察 |
| rain gauge | rain gauge | 雨量计 | — | — | — | — |
| METAR report | METAR report | METAR 报文 | — | — | IEM `metar` | — |
| visibility | visibility | 能见度 | — | m | MetPy `visibility` | — |
| okta | okta | — | okta | 1 okta = 天空的 1/8 | — | — |
| station plot | station plot | 观测站填图 | — | — | MetPy `StationPlot` | — |
| significant figures | significant figures | 有效数字 | — | — | — | — |
| sounding | sounding | 探空 | — | — | — | 高空探测 |
| radiosonde | radiosonde | 探空仪 | — | — | — | 无线电探空仪 |
| mandatory pressure level | mandatory pressure level | 标准等压面 | — | — | — | 标准层 |
| significant level | significant level | 特性层 | — | — | — | — |
| full disk image | full disk image | 全圆盘图像 | — | — | GOES 产品 `ABI-L2-CMIPF` | — |
| analysis | analysis | 分析场 | — | — | — | 分析资料、分析数据 |
| reanalysis | reanalysis | 再分析 | — | — | ERA5 | 重分析 |
| data assimilation | data assimilation | 数据同化 | — | — | — | 资料同化 |
| climatology | climatology | 气候态 | — | — | — | 气候平均态、气候场、气候均值 |
| anomaly | anomaly | 距平 | — | — | — | — |
| empirical orthogonal function | empirical orthogonal function | 经验正交函数 | EOF | — | — | 经验正交分解 |
| mode | mode | 模态 | — | — | — | — |
| principal component | principal component | 主成分 | PC | — | — | 主分量 |
| explained variance fraction | explained variance fraction | 方差贡献 | — | % | — | 方差贡献率 |

## AI 天气预报与评估

| 术语 | English term | 中文 | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|---|
| numerical weather prediction | numerical weather prediction | 数值天气预报 | NWP | — | — | 数值预报 |
| numerical weather prediction model | numerical weather prediction model | 数值模式 | — | — | — | 数值模型 |
| AI weather model | AI weather model | AI 天气模型 | — | — | — | AI 气象模型、气象大模型、机器学习天气模型 |
| experimental version | experimental version | 试验版本 | — | — | ECMWF 开放数据 2025-02-25 以前的 AIFS，模型名 `aifs` | 实验版本、实验版 |
| forecast | forecast | 预报 | — | — | — | 预测 |
| predictability | predictability | 可预报性 | — | — | — | 可预测性 |
| initialization time | initialization time | 起报时间 | — | UTC | WeatherBench 2 预报数据的 `time` | 初始化时间、初始时间、起始时间 |
| lead time | lead time | 预报时效 | — | h | `prediction_timedelta` | 提前期、预见期、领先时间、前置时间、预报时长 |
| valid time | valid time | 有效时间 | — | UTC | `valid_time` | 生效时间 |
| initial condition | initial condition | 初始条件 | — | — | — | 初始场、初值、初值场 |
| autoregressive rollout | autoregressive rollout | 自回归预报 | — | — | — | 滚动预报 |
| deterministic forecast | deterministic forecast | 确定性预报 | — | — | — | 确定预报、单一预报 |
| persistence forecast | persistence forecast | 持续性预报 | — | — | — | 持续预报、持久性预报 |
| ensemble forecast | ensemble forecast | 集合预报 | — | — | — | 系综预报、集成预报 |
| ensemble member | ensemble member | 集合成员 | — | — | `number` | 系综成员 |
| ensemble mean | ensemble mean | 集合平均 | — | — | — | 系综平均 |
| spread | ensemble spread | 集合离散度 | — | — | — | 系综离散度、集合发散度 |
| MSE | mean squared error | 均方误差 | MSE | — | — | — |
| RMSE | root mean squared error | 均方根误差 | RMSE | 与变量相同 | — | 均方误差根、均方根差、均方差 |
| bias | bias | 偏差 | — | 与变量相同 | — | — |
| MAE | mean absolute error | 平均绝对误差 | MAE | 与变量相同 | — | 平均绝对偏差 |
| track error | track error | 路径误差 | — | km | `ch12.track_errors` 的 `dist_km` | 轨迹误差 |
| hit | hit | 命中 | — | — | — | — |
| miss | miss | 漏报 | — | — | — | 未命中 |
| false alarm | false alarm | 空报 | — | — | — | — |
| hit rate | hit rate | 命中率 | — | — | — | — |
| correlation | Pearson correlation coefficient | 相关系数 | — | — | earthkit-meteo `score.pearson_correlation` | 皮尔逊相关系数 |
| percentile | percentile | 百分位数 | — | 与变量相同 | — | 百分位、分位点 |
| standard error | standard error | 标准误差 | — | 与变量相同 | — | 标准误 |
| standard deviation | standard deviation | 标准差 | — | 与变量相同 | — | 标准偏差 |
| ACC | anomaly correlation coefficient | 距平相关系数 | ACC | — | — | 异常相关系数、距平相关 |
| CRPS | continuous ranked probability score | 连续分级概率评分 | CRPS | 与变量相同 | — | 连续排序概率评分、连续等级概率评分 |
| SEEPS | stable equitable error in probability space | SEEPS 评分 | SEEPS | — | WeatherBench 2 的降水评分 | — |
| skill score | skill score | 技巧评分 | — | — | — | 技巧分数 |
| latitude weighting | latitude weighting | 纬度加权 | — | — | — | — |
| RMS | root mean square | 均方根 | RMS | 与变量相同 | — | — |
| loss function | loss function | 损失函数 | — | — | — | 代价函数 |
| kinetic energy spectrum | kinetic energy spectrum | 动能谱 | $E(k)$ | m² s⁻² | — | 能谱、能量谱 |
| zonal wavenumber | zonal wavenumber | 纬向波数 | $k$ | — | — | — |
| effective resolution | effective resolution | 有效分辨率 | — | km | — | — |

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

下面每一条说明一个选择和它的理由。用户在 2026-10-17 批准了前 17 条。第 1 条到第 34 条记录了中文术语的选择。2026-10-20 起，这些中文名只出现在“中文”一列，正文写英文术语，见第 35 条。

1. 等压面：选它，不选“气压层”和“气压面”。等压面是标准术语，也对应 ERA5 的 pressure levels。
2. 位势高度：选它，不用单独的“高度”。单独的“高度”可以指位势高度，也可以指几何高度。几何意义的高度写“几何高度”。
3. 温度平流：选它，不选“热力平流”。“热力”可以指温度，也可以指能量。
4. 温度：选它，不选“气温”。2 m 的温度写“2 m 温度”，对应 `t2m`。
5. 直减率：选它，不选“递减率”。“直减率”是大气科学名词审定的用词。
6. Coriolis 力：选它，不选“地转偏向力”。它和“Coriolis 参数”共用人名 Coriolis。
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
18. 波长：写 $\Lambda$，不写 $\lambda$。本书按动力学的惯例，用 $\lambda$ 表示经度。
19. kt：风速的单位 knot 只写符号 kt，和 hPa 一样。“节”只表示文档的节，例如“第 2 课 2.2 节”。
20. 人名术语：写英文人名加中文通用词，例如 Coriolis 力、Hadley 环流、Clausius–Clapeyron 方程。一个人名有多种中文音译，英文人名只有一种写法。英文人名和中文之间留一个半角空格。旧的音译词都是弃用词，例如“科里奥利力”和“哈得来环流”。用户在 2026-10-17 做了这个决定。
21. Bergeron 过程和 Monin–Obukhov 长度：人名取自原来的中文术语“贝吉龙过程”和“莫宁-奥布霍夫长度”。English term 一列保留文献的常用名。
22. 西风带和两种急流：中纬度的西风叫“西风带”，不另立“中纬度西风带”。对流层上部、纬度 30° 附近的急流叫“副热带急流”。温带气旋维持的、从地面伸到对流层顶的急流叫“涡驱动急流”，不叫“极锋急流”。
23. 顺转和逆转：风随几何高度顺时针转动叫顺转，逆时针转动叫逆转。两个词只描述风随几何高度的转动，不描述风随时间的转动。风随时间的转动写“风向顺时针转了多少度”。
24. 风矢端图：选它，不选“速端图”。它是 hodograph 的大气科学名词，图上画的是风向量的端点。
25. 层平均温度：两个等压面之间的温度对 $\ln p$ 的平均，记作 $\langle T\rangle$。厚度正比于它。
26. 滴半径：写 $r_\mathrm{d}$，沿用 METEO 300 第 5 课的符号。下标 d 表示滴。它和混合比 $r$ 是两个符号。表面张力写 $\sigma_\mathrm{w}$，因为 $\sigma$ 已经用于 Stefan–Boltzmann 定律。溶质系数写 $b_\mathrm{s}$，因为 METEO 300 的 $B$ 在本书表示浮力。气溶胶文献常用下标 d 表示干颗粒。本书的 $r_\mathrm{d}$ 是滴半径，干颗粒半径写 $r_0$。
27. 季节振幅：指一年里最高月和最低月的差，即峰谷差。二氧化碳的文献都这样定义。它是正弦振幅的 2 倍。
28. 涡动协方差：选它，不选“涡度相关”。“涡度”在本书里只表示风的旋转，见“涡度与散度”一节。
29. 幂律指数：符号写 $n$，不写风能文献常用的 $\alpha$。本书用 $\alpha$ 表示反照率。
30. 低空急流：选它，不选“夜间急流”。低空急流常在夜间出现，但白天也可以出现。“急流”单独使用时指对流层上部的急流。
31. 低压中心和气旋中心：低压中心是天气图上海平面气压的局地极小值。描述天气图、气压场和个例时，写“低压中心”。气旋中心是气旋追踪器找到并跟踪的低压中心。写气旋路径、气旋追踪、hit、miss 和中心的移动时，写“气旋中心”。同一个低压，在一个时刻的天气图上叫低压中心，在追踪的结果里叫气旋中心。不写“风暴中心”。用户在 2026-10-17 做了这个决定。
32. 评分指标：写常见的英文名，不写中文。缩写全部大写：MAE、MSE、RMSE、RMS、ACC、CRPS 和 SEEPS。普通英文词在句中小写：bias、hit、miss、false alarm、correlation、skill score、spread 和 track error。英文和中文之间留一个空格，和 ERA5 的写法一样。正文第一次出现时也不加中文。“偏差”“均方根”“相关系数”等中文名是弃用词。用户在 2026-10-17 做了这个决定。
33. track error：预报的气旋中心和参考的气旋中心之间的距离，单位是 km。track error 只指这个距离，不包括中心气压的误差。不写“路径误差”或“轨迹误差”。“位置误差”不是弃用词。槽、锋和其他天气系统放错了位置，可以写“位置误差”。
34. 六个动力学术语：写英文原词，不写中文。这六个词是 geostrophic wind speed、subgeostrophic wind、supergeostrophic wind、gradient wind balance、centripetal acceleration 和 radius of curvature。它们在句中小写。英文和中文之间留一个半角空格。正文第一次出现时也不加中文。“地转风速”“次地转风”“超地转风”“梯度风平衡”“向心加速度”和“曲率半径”是弃用词。其他术语仍写中文，例如地转风、梯度风和风速。用户在 2026-10-20 做了这个决定。
35. 全书术语：写英文，不写中文。“术语”一列是英文词，“中文”一列的中文名是弃用词。这一条取代第 20 条的人名术语写法，也取消第 32 条和第 34 条的范围限制。一个概念有多种英文写法时，取 English term 一列的第一个，例如等压面写 isobaric surface。英文在句中小写，专有名词和缩写照原样写。英文和中文、数字之间留一个半角空格。西风、风暴、预报员和中纬度等常用词含有术语的字，但不是术语，仍写中文。pyproject.toml 的 allow 列表列出这些词。书名和副标题不变。用户在 2026-10-20 做了这个决定。
