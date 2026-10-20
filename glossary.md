# 术语表

本表给每个概念选定一个中文术语。页面只用“中文术语”一列的词。“弃用词”一列的词不进入正文，检查器发现它们就报错。

表格的列：

- 中文术语：本书使用的唯一说法。人名术语写英文人名加中文通用词，例如 Coriolis 力。评分指标写常见的英文名，例如 RMSE 和 bias，见难选的词第 32 条。六个动力学术语也写英文原词，例如 geostrophic wind speed，见难选的词第 34 条。
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
| 重力加速度 | gravitational acceleration | $g$ | m s⁻² | — | — |
| 标准重力加速度 | standard gravity | $g_0$ | m s⁻² | — | 标准重力 |
| 地形高度 | surface geopotential height; orography | $Z_s$ | m | `z` 地面场除以 $g_0$ / `geopotential_at_surface` | 地形海拔 |
| 海陆掩码 | land-sea mask | — | — | `lsm` / `land_sea_mask` | 海陆掩膜、陆海掩码 |
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
| 层平均温度 | layer-mean temperature | $\langle T\rangle$ | K | — | 平均层温度、气层平均温度 |
| 虚位温 | virtual potential temperature | $\theta_v$ | K | — | 虚拟位温 |
| 露点温度 | dewpoint temperature | $T_d$ | K | `d2m` / `2m_dewpoint_temperature` | 露点 |
| 温度露点差 | dewpoint depression | $T - T_d$ | K | — | 露点差 |
| 湿球温度 | wet-bulb temperature | $T_w$ | K | — | — |
| 体感温度 | apparent temperature | — | °C | MetPy `apparent_temperature` | 表观温度、感觉温度 |
| 热指数 | heat index | HI | °C | MetPy `heat_index` | 炎热指数 |
| 相当位温 | equivalent potential temperature | $\theta_e$ | K | — | 等效位温、当量位温 |
| 饱和相当位温 | saturation equivalent potential temperature | $\theta_{es}$ | K | — | — |
| 有效发射温度 | effective emission temperature | $T_e$ | K | — | 有效温度、有效辐射温度、发射温度 |

## 热力学

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 理想气体定律 | ideal gas law | — | — | — | 理想气体状态方程 |
| 干空气气体常数 | gas constant for dry air | $R_d$ | J kg⁻¹ K⁻¹ | MetPy `Rd` | — |
| 水汽气体常数 | gas constant for water vapour | $R_v$ | J kg⁻¹ K⁻¹ | MetPy `Rv` | 水蒸气气体常数 |
| 摩尔气体常数 | molar gas constant | $R^*$ | J mol⁻¹ K⁻¹ | MetPy `R` | 普适气体常数、通用气体常数 |
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
| 整层总水量 | total column water | — | kg m⁻² | `tcw` / `total_column_water` | 柱总水量 |
| 整层水汽输送 | integrated vapour transport | IVT | kg m⁻¹ s⁻¹ | `integrated_vapor_transport` | — |
| 潜热 | latent heat | $L_v$ | J kg⁻¹ | — | — |
| 凝结 | condensation | — | — | — | 冷凝 |
| 蒸发 | evaporation | — | — | `e` / `evaporation` | — |
| 饱和 | saturation | — | — | — | — |
| Clausius–Clapeyron 方程 | Clausius–Clapeyron equation | — | — | — | 克劳修斯-克拉珀龙方程、克-克方程、克拉珀龙方程、克劳修斯-克拉伯龙方程 |
| 降水 | precipitation | — | — | — | — |
| 降水量 | precipitation amount | — | mm | `tp` / `total_precipitation_6hr` | — |
| 降雪量 | snowfall | — | mm | `sf` / `snowfall` | — |
| 降水率 | precipitation rate | — | mm h⁻¹ | IMERG `precipitation` | — |

## 风

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 风 | wind | $\mathbf{v}$ | m s⁻¹ | — | — |
| 水平风 | horizontal wind | $\mathbf{v}_h$ | m s⁻¹ | — | — |
| 风速 | wind speed | $V$ | m s⁻¹ | `wind_speed` | — |
| 风向 | wind direction | $\chi$ | ° | — | — |
| 去向方位角 | bearing of travel | — | ° | MetPy `wind_direction` 的 `convention="to"` | — |
| 数学角 | math angle | $\gamma$ | ° | — | — |
| kt | knot | kt | 1 kt ≈ 0.514 m s⁻¹ | — | 海里每小时 |
| 风羽 | wind barb | — | kt | MetPy `StationPlot.plot_barb` | — |
| 纬向风 | zonal wind; u component | $u$ | m s⁻¹ | `u` / `u_component_of_wind` | u 风、东西风分量 |
| 经向风 | meridional wind; v component | $v$ | m s⁻¹ | `v` / `v_component_of_wind` | v 风、南北风分量 |
| 10 m 风 | 10 m wind | $u_{10}$, $v_{10}$ | m s⁻¹ | `u10`, `v10` / `10m_u_component_of_wind`, `10m_v_component_of_wind` | 地面风、近地面风 |
| 100 m 风 | 100 m wind | $u_{100}$, $v_{100}$ | m s⁻¹ | `u100`, `v100` / `100m_u_component_of_wind`, `100m_v_component_of_wind` | — |
| 阵风 | wind gust | — | m s⁻¹ | `i10fg` / `instantaneous_10m_wind_gust` | — |
| 地转风 | geostrophic wind | $\mathbf{v}_g$ | m s⁻¹ | `geostrophic_wind_speed` | — |
| geostrophic wind speed | geostrophic wind speed | $V_g$ | m s⁻¹ | — | 地转风速 |
| 非地转风 | ageostrophic wind | $\mathbf{v}_{ag}$ | m s⁻¹ | `ageostrophic_wind_speed` | 偏地转风 |
| 梯度风 | gradient wind | — | m s⁻¹ | — | — |
| subgeostrophic wind | subgeostrophic wind | — | m s⁻¹ | — | 次地转风、亚地转风 |
| supergeostrophic wind | supergeostrophic wind | — | m s⁻¹ | — | 超地转风 |
| 穿越角 | cross-isobar angle | $\gamma - \gamma_g$ | ° | — | 越等压线角 |
| 非地转风比例 | ageostrophic wind fraction | — | — | — | — |
| 热成风 | thermal wind | $\mathbf{v}_T$ | m s⁻¹ | — | 热风 |
| 热成风方程 | thermal wind equation | — | — | — | 热风方程 |
| 顺转 | veering | — | — | — | 顺时针转向 |
| 逆转 | backing | — | — | — | 逆时针转向 |
| 风矢端图 | hodograph | — | m s⁻¹ | MetPy `Hodograph` | 风速矢端图、速端图 |
| 垂直风切变 | vertical wind shear | $\partial \mathbf{v}_h / \partial z$ | s⁻¹ | — | 风切、垂直切变 |
| 急流 | jet stream | — | — | — | 喷流 |
| 副热带急流 | subtropical jet | — | m s⁻¹ | — | — |
| 涡驱动急流 | eddy-driven jet | — | m s⁻¹ | — | 极锋急流 |
| 低空急流 | low-level jet | — | m s⁻¹ | — | 低层急流、夜间急流、边界层急流 |
| 信风 | trade winds | — | — | — | 贸易风 |
| 西风带 | westerlies | — | — | — | — |

## 力与平衡

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 气压梯度力 | pressure gradient force | PGF | m s⁻² | — | 压力梯度力、压强梯度力 |
| Coriolis 力 | Coriolis force | — | m s⁻² | — | 科里奥利力、科氏力、地转偏向力、柯氏力 |
| Coriolis 参数 | Coriolis parameter | $f$ | s⁻¹ | — | 科里奥利参数、科氏参数、地转参数 |
| 地球自转角速度 | Earth's angular velocity | $\Omega$ | s⁻¹ | — | — |
| 摩擦力 | friction | — | m s⁻² | — | — |
| 地转平衡 | geostrophic balance | — | — | — | — |
| gradient wind balance | gradient wind balance | — | — | — | 梯度风平衡、梯度平衡 |
| centripetal acceleration | centripetal acceleration | $V^2/R$ | m s⁻² | — | 向心加速度 |
| radius of curvature | radius of curvature | $R$ | km | — | 曲率半径 |
| Rossby 数 | Rossby number | Ro | — | — | 罗斯贝数、罗斯比数 |
| 尺度分析 | scale analysis | — | — | — | 量级分析 |
| f 平面 | f-plane | — | — | — | — |
| 惯性振荡 | inertial oscillation | — | — | — | 惯性振动 |
| 惯性圆 | inertial circle | — | km | — | — |
| 惯性周期 | inertial period | — | h | — | — |

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
| 热力图 | thermodynamic diagram | — | — | — | 热力学图解、热力学图 |
| 比熵 | specific entropy | $s$ | J kg⁻¹ K⁻¹ | — | — |
| 等温线 | isotherm | — | — | — | — |
| 等饱和混合比线 | saturation mixing ratio line | — | g kg⁻¹ | MetPy `plot_mixing_lines` | 等混合比线 |
| 雷暴 | thunderstorm | — | — | — | 雷雨 |
| 强对流 | severe convective weather | — | — | — | — |
| 龙卷 | tornado | — | — | — | 龙卷风 |

## 垂直运动

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 垂直速度 | vertical velocity | $w$ | m s⁻¹ | — | 竖直速度 |
| 气压垂直速度 | pressure vertical velocity; omega | $\omega$ | Pa s⁻¹ | `w` / `vertical_velocity` | 垂直气压速度、p 坐标垂直速度 |
| 上升运动 | ascent | — | — | — | — |
| 下沉运动 | descent; subsidence | — | — | — | — |
| 连续方程 | continuity equation | — | — | — | 连续性方程 |
| 运动学方法 | kinematic method | — | — | — | 运动学法 |
| O'Brien 订正 | O'Brien correction | — | — | — | — |

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
| 变形 | deformation | — | s⁻¹ | — | 形变 |
| 环流 | circulation | $C$ | m² s⁻¹ | — | — |
| 气旋式 | cyclonic | — | — | — | — |
| 反气旋式 | anticyclonic | — | — | — | — |
| 涡度方程 | vorticity equation | — | s⁻² | — | — |
| 无辐散层 | level of nondivergence | — | hPa | — | 无辐散高度 |
| 动态对流层顶 | dynamical tropopause | — | PVU | 2 PVU 等值面 | 动力对流层顶 |

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
| Laplace 算子 | Laplacian | $\nabla^2$ | — | — | 拉普拉斯算子、拉普拉斯算符 |
| Fourier 变换 | Fourier transform | — | — | NumPy `fft.rfft` | 傅里叶变换、傅立叶变换 |
| Parseval 定理 | Parseval's theorem | — | — | — | 帕塞瓦尔定理 |
| 球谐函数 | spherical harmonics | — | — | pyshtools | 球面调和函数 |
| 偏导数 | partial derivative | $\partial$ | — | — | 偏微分 |
| 偏微分方程 | partial differential equation | — | — | — | — |
| 随体导数 | material derivative | $D/Dt$ | — | — | 物质导数、个别导数 |
| 局地变化 | local rate of change | $\partial / \partial t$ | — | — | — |
| Euler 视角 | Eulerian view | — | — | — | 欧拉视角、欧拉观点 |
| Lagrange 视角 | Lagrangian view | — | — | — | 拉格朗日视角、拉格朗日观点 |
| 流线 | streamline | — | — | — | — |
| 轨迹 | trajectory | — | — | — | 轨线 |
| 有限差分 | finite difference | — | — | — | — |
| 中心差分 | centred difference | — | — | — | 中央差分 |
| 网格 | grid | — | — | — | 格网 |
| 格点 | grid point | — | — | — | 网格点、格网点 |
| 网格间距 | grid spacing | $\Delta\lambda$, $\Delta\varphi$ | °, km | — | 格距、格点间距、网格距 |
| 分辨率 | resolution | — | ° | — | 解析度 |
| 纬向 | zonal | $x$ | — | — | 东西向 |
| 经向 | meridional | $y$ | — | — | 南北向 |
| 经度 | longitude | $\lambda$ | ° | 坐标 `longitude` | — |
| 纬度 | latitude | $\varphi$ | ° | 坐标 `latitude` | — |
| 纬向平均 | zonal mean | — | — | — | 带状平均、纬圈平均 |
| 纬圈 | latitude circle | — | — | — | — |
| 局地直角坐标系 | local Cartesian coordinate system | $x$, $y$, $z$ | m | — | 局地笛卡尔坐标系 |
| Lambert 投影 | Lambert conformal conic projection | — | — | cartopy `LambertConformal` | 兰伯特投影、兰勃特投影 |
| 大圆距离 | great-circle distance | $d$ | km | pyproj `Geod.inv` | — |
| 地心夹角 | central angle | $\xi$ | rad | — | 圆心角 |
| 地球半径 | Earth radius | $R_\mathrm{E}$ | km | MetPy `earth_avg_radius` | — |
| 曲率项 | metric term | — | — | — | 度量项 |
| 中点法 | midpoint method | — | — | — | 中点公式 |
| 线性插值 | linear interpolation | — | — | — | — |
| 双线性插值 | bilinear interpolation | — | — | — | — |

## 辐射

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 短波辐射 | shortwave radiation | — | W m⁻² | 地面向下：`ssrd` / `surface_solar_radiation_downwards` | 太阳辐射 |
| 长波辐射 | longwave radiation | — | W m⁻² | 地面向下：`strd` / `surface_thermal_radiation_downwards` | 地球辐射、红外辐射、热辐射 |
| 大气顶入射太阳辐射 | TOA incident solar radiation | TISR | W m⁻² | `tisr` / `toa_incident_solar_radiation` | 大气层顶太阳辐射、入射太阳辐射 |
| 射出长波辐射 | outgoing longwave radiation | OLR | W m⁻² | `ttr` 取负号 / `mean_top_net_long_wave_radiation_flux` 取负号 | 向外长波辐射、出射长波辐射 |
| 净辐射 | net radiation | $R_n$ | W m⁻² | 地面：`ssr` 加 `str` | — |
| 辐照度 | irradiance; radiative flux density | $F$ | W m⁻² | — | 辐射通量密度、辐射通量 |
| 光谱辐照度 | spectral irradiance | $F_\Lambda$ | W m⁻² μm⁻¹ | — | 单色辐照度、分光辐照度 |
| 波长 | wavelength | $\Lambda$ | μm | — | — |
| 太阳常数 | solar constant | $S_0$ | W m⁻² | — | — |
| 太阳天顶角 | solar zenith angle | $Z$ | ° | earthkit-meteo `cos_solar_zenith_angle` 给出 $\cos Z$ | — |
| 反照率 | albedo | $\alpha$ | — | `fal` / `forecast_albedo` | 反照度 |
| 发射率 | emissivity | $\varepsilon$ | — | — | 比辐射率、发射本领 |
| 吸收率 | absorptivity | $a$ | — | — | 吸收比 |
| 黑体 | blackbody | — | — | — | 绝对黑体 |
| Planck 函数 | Planck function | $B_\Lambda$ | W m⁻² sr⁻¹ μm⁻¹ | — | 普朗克函数 |
| 亮温 | brightness temperature | $T_b$ | K | GOES ABI L2 `CMI` | 亮度温度 |
| Stefan–Boltzmann 定律 | Stefan–Boltzmann law | $\sigma$ | W m⁻² K⁻⁴ | — | 斯特藩-玻尔兹曼定律、斯蒂芬-玻尔兹曼定律、斯特番-玻尔兹曼定律 |
| Wien 位移定律 | Wien's displacement law | — | — | — | 维恩位移定律、维恩定律 |
| Kirchhoff 定律 | Kirchhoff's law | — | — | — | 基尔霍夫定律、克希霍夫定律 |
| Beer–Lambert 定律 | Beer–Lambert law | — | — | — | 比尔-朗伯定律、比尔定律、朗伯-比尔定律 |
| 光学厚度 | optical depth | $\tau$ | — | — | 光学深度 |
| Rayleigh 散射 | Rayleigh scattering | — | — | — | 瑞利散射 |
| Mie 散射 | Mie scattering | — | — | — | 米散射、米氏散射 |
| 温室效应 | greenhouse effect | — | — | — | — |
| 辐射平衡 | radiative equilibrium | — | — | — | 辐射均衡 |
| 累积量 | accumulated field | — | J m⁻² | — | 累计量 |
| 辐亮度 | radiance | $I$ | W m⁻² sr⁻¹ μm⁻¹ | GOES ABI L1b `Rad` | 辐射亮度 |
| 波数 | wavenumber | $\tilde{\nu}$ | cm⁻¹ | — | — |
| 波段 | spectral band | — | μm | GOES ABI `C02`、`C08`、`C13` | 光谱通道 |
| 大气窗区 | atmospheric window | — | μm | — | 大气窗口、窗口区 |
| 反射率 | reflectance | — | % | GOES ABI L2 `CMI`，可见光波段 | 反射比 |
| 透过率 | transmittance | $\mathcal{T}$ | — | — | 透射率、透射比 |
| 大气光学质量 | relative optical air mass | $m$ | — | pvlib `get_relative_airmass` | — |
| 等效光学厚度 | effective optical depth | $\tau_{\mathrm{eff}}$ | — | — | — |
| 太阳赤纬 | solar declination | $\delta_\odot$ | ° | earthkit-meteo `solar_declination_angle` | 赤纬角 |
| 时角 | hour angle | $h_\odot$ | ° | — | 太阳时角 |
| 晴空 | clear sky | — | — | ERA5 `ssrdc`；pvlib `Location.get_clearsky` | — |
| 灰体大气 | grey atmosphere | — | — | climlab `GreyRadiationModel` | 灰色大气 |
| 辐射对流平衡 | radiative–convective equilibrium | RCE | — | climlab `RadiativeConvectiveModel` | 辐射-对流平衡 |
| 对流调整 | convective adjustment | — | — | climlab `ConvectiveAdjustment` | — |
| 静止卫星 | geostationary satellite | — | — | GOES、Meteosat、Himawari | 地球静止卫星、同步卫星 |
| 极轨卫星 | polar-orbiting satellite | — | — | NOAA-20、Metop | 极地轨道卫星 |
| 辐射传输模式 | radiative transfer model | — | — | RTTOV | 辐射传输模型 |
| Planck 常数 | Planck constant | $h$ | J s | `scipy.constants.h` | 普朗克常数 |
| Boltzmann 常数 | Boltzmann constant | $k_B$ | J K⁻¹ | `scipy.constants.k` | 玻尔兹曼常数 |
| 光速 | speed of light | $c$ | m s⁻¹ | `scipy.constants.c` | — |
| 光伏出力 | PV power output | $P_{\mathrm{PV}}$ | MW | pvlib `pvwatts_dc` | 光伏功率 |

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
| Monin–Obukhov 长度 | Obukhov length | $L$ | m | — | 莫宁-奥布霍夫长度、奥布霍夫长度 |
| Richardson 数 | Richardson number | Ri | — | — | 理查森数、理查逊数、里查森数 |
| 湍流动能 | turbulent kinetic energy | TKE | m² s⁻² | — | 湍能、湍动能 |
| Reynolds 平均 | Reynolds averaging | — | — | — | 雷诺平均 |
| 日变化 | diurnal cycle | — | — | — | 日循环、日周期 |
| Ekman 螺线 | Ekman spiral | — | — | — | 埃克曼螺线、艾克曼螺线、埃克曼螺旋 |
| 脉动量 | turbulent fluctuation | $u'$ | 与变量相同 | — | 脉动值、湍流脉动 |
| 方差 | variance | $\overline{u'^2}$ | 变量单位的平方 | — | — |
| 协方差 | covariance | $\overline{a'b'}$ | 两个变量单位的乘积 | — | — |
| 运动学通量 | kinematic flux | — | — | — | — |
| 动量通量 | momentum flux | $\overline{u'w'}$ | m² s⁻² | — | — |
| 涡动协方差 | eddy covariance | — | — | — | 涡度相关、涡动相关 |
| 超声风速仪 | sonic anemometer | — | — | — | 超声风速计 |
| 超声温度 | sonic temperature | $T_s$ | °C | — | — |
| 幂律风廓线 | power-law wind profile | — | — | — | 指数风廓线 |
| 幂律指数 | power-law exponent | $n$ | — | — | 风切变指数、Hellmann 指数 |
| 轮毂高度 | hub height | $z_{\mathrm{hub}}$ | m | — | 轮毂高 |
| 风电出力 | wind power output | $P_{\mathrm{W}}$ | MW | — | 风电功率 |
| 功率曲线 | power curve | — | — | — | 功率特性曲线 |
| 容量系数 | capacity factor | — | % | — | 容量因子 |
| 切入风速 | cut-in wind speed | $V_{\mathrm{in}}$ | m s⁻¹ | — | 启动风速 |
| 额定风速 | rated wind speed | $V_{\mathrm{rated}}$ | m s⁻¹ | — | — |
| 切出风速 | cut-out wind speed | $V_{\mathrm{out}}$ | m s⁻¹ | — | 停机风速 |
| 额定功率 | rated power | — | MW | — | — |
| 装机容量 | installed capacity | — | GW | — | 装机量 |

## 云与气溶胶

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 大气成分 | atmospheric composition | — | — | — | — |
| 干空气 | dry air | — | — | — | 干燥空气 |
| 体积混合比 | volume mixing ratio | — | ppm | — | — |
| 二氧化碳 | carbon dioxide | CO₂ | ppm | NOAA GML `average` | — |
| 温室气体 | greenhouse gas | — | — | — | — |
| 季节循环 | seasonal cycle | — | — | — | — |
| 季节振幅 | seasonal amplitude; peak-to-trough amplitude | — | ppm | — | — |
| 年增长率 | annual growth rate | — | ppm a⁻¹ | — | — |
| 臭氧 | ozone | O₃ | kg kg⁻¹ | `o3` / `ozone_mass_mixing_ratio` | — |
| 气溶胶 | aerosol | — | — | — | 气胶、悬浮微粒 |
| 气溶胶光学厚度 | aerosol optical depth | AOD | — | CAMS `aod550` | 气溶胶光学深度 |
| 沙尘 | mineral dust | — | — | CAMS `duaod550` | — |
| 海盐 | sea salt | — | — | CAMS `ssaod550` | — |
| 硫酸盐 | sulphate | — | — | CAMS `suaod550` | — |
| 有机物 | organic matter | — | — | CAMS `omaod550` | — |
| 湿沉降 | wet deposition | — | — | — | — |
| 云凝结核 | cloud condensation nuclei | CCN | cm⁻³ | — | 凝结核 |
| 冰核 | ice-nucleating particle | INP | — | — | — |
| 活化 | activation | — | — | — | — |
| 霾滴 | haze droplet | — | μm | — | — |
| 滴半径 | drop radius | $r_\mathrm{d}$ | μm | — | — |
| 临界半径 | critical radius | $r_\mathrm{c}$ | μm | — | — |
| 干颗粒半径 | dry particle radius | $r_0$ | μm | — | — |
| 平衡水汽压 | equilibrium vapour pressure | $e_\mathrm{eq}$ | hPa | — | — |
| 平衡饱和比 | equilibrium saturation ratio | $S_\mathrm{eq}$ | — | — | — |
| 临界过饱和度 | critical supersaturation | $S_\mathrm{c} - 1$ | % | — | — |
| 表面张力 | surface tension | $\sigma_\mathrm{w}$ | N m⁻¹ | — | — |
| 液态水摩尔浓度 | molar concentration of liquid water | $n_\mathrm{L}$ | mol m⁻³ | — | — |
| Kelvin 系数 | Kelvin coefficient | $a_\mathrm{K}$ | m | — | — |
| Raoult 定律 | Raoult's law | — | — | — | 拉乌尔定律 |
| 溶质物质的量 | amount of solute | $N_\mathrm{s}$ | mol | — | — |
| 溶质摩尔分数 | mole fraction of solute | $x_\mathrm{s}$ | — | — | — |
| van 't Hoff 因子 | van 't Hoff factor | $i$ | — | — | 范特霍夫因子 |
| 溶质系数 | solute coefficient | $b_\mathrm{s}$ | m³ | — | — |
| 云滴 | cloud droplet | — | μm | — | 云粒 |
| 雨滴 | raindrop | — | mm | — | — |
| 冰晶 | ice crystal | — | — | — | — |
| Kelvin 效应 | Kelvin effect; curvature effect | — | — | — | 开尔文效应、曲率效应 |
| 溶质效应 | solute effect | — | — | — | 拉乌尔效应 |
| Köhler 曲线 | Köhler curve | — | — | — | 科勒曲线、克勒曲线、柯勒曲线 |
| 碰并 | collision–coalescence | — | — | — | 碰撞并合、碰撞合并 |
| Bergeron 过程 | Wegener–Bergeron–Findeisen process | — | — | — | 贝吉龙过程、冰晶效应、伯杰龙过程 |
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
| Hadley 环流 | Hadley cell | — | — | — | 哈得来环流、哈德莱环流、哈德利环流、哈得来环流圈 |
| Ferrel 环流 | Ferrel cell | — | — | — | 费雷尔环流、费雷尔环流圈 |
| 极地环流 | polar cell | — | — | — | 极地环流圈 |
| 热带辐合带 | intertropical convergence zone | ITCZ | — | — | 赤道辐合带 |
| 副热带高压 | subtropical high | — | — | — | 副高 |
| 赤道低压带 | equatorial low-pressure belt | — | — | — | 赤道低压槽 |
| 副热带高压带 | subtropical high-pressure belt | — | — | — | — |
| 副极地低压带 | subpolar low-pressure belt | — | — | — | 副极地低压槽 |
| 冰岛低压 | Icelandic Low | — | — | — | — |
| 亚速尔高压 | Azores High | — | — | — | — |
| 阿留申低压 | Aleutian Low | — | — | — | — |
| 北大西洋涛动 | North Atlantic Oscillation | NAO | — | — | 北大西洋振荡 |
| 气团 | air mass | — | — | — | — |
| 锋 | front | — | — | — | 锋面 |
| 冷锋 | cold front | — | — | — | — |
| 暖锋 | warm front | — | — | — | — |
| 锢囚锋 | occluded front | — | — | — | 囚锢锋 |
| 暖区 | warm sector | — | — | — | 暖扇区 |
| 锋生 | frontogenesis | — | — | — | 锋面生成 |
| 锋生函数 | frontogenesis function | $\mathcal{F}$ | K (100 km)⁻¹ (3 h)⁻¹ | MetPy `frontogenesis`，单位 K m⁻¹ s⁻¹ | — |
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
| 低压中心 | low centre | — | — | `msl` 的局地极小值 | 风暴中心 |
| 气旋中心 | cyclone centre | — | — | — | 风暴中心 |
| 中心气压 | central pressure | $p_c$ | hPa | 低压中心的 `msl` | 中心压力 |
| 气旋路径 | cyclone track | — | — | — | 气旋轨迹 |
| 气旋追踪 | cyclone tracking | — | — | — | 气旋跟踪 |
| 局地极小值 | local minimum | — | — | — | 局部极小值、局部最小值 |
| 搜索半径 | search radius | — | km | — | — |
| 匹配半径 | match radius | — | km | — | 匹配距离 |
| 风暴路径 | storm track | — | — | — | 风暴轴 |
| 重力波 | gravity wave | — | — | — | — |

## 观测与数据

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 数据 | data | — | — | — | 观测资料、再分析资料 |
| 数据集 | dataset | — | — | — | 资料集、数据组 |
| 观测站 | weather station | — | — | — | 测站、站点 |
| 地面观测 | surface observation | — | — | — | 地面观察 |
| 雨量计 | rain gauge | — | — | — | — |
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
| 经验正交函数 | empirical orthogonal function | EOF | — | — | 经验正交分解 |
| 模态 | mode | — | — | — | — |
| 主成分 | principal component | PC | — | — | 主分量 |
| 方差贡献 | explained variance fraction | — | % | — | 方差贡献率 |

## AI 天气预报与评估

| 中文术语 | English term | 符号 | 单位 | 变量名 | 弃用词 |
|---|---|---|---|---|---|
| 数值天气预报 | numerical weather prediction | NWP | — | — | 数值预报 |
| 数值模式 | numerical weather prediction model | — | — | — | 数值模型 |
| AI 天气模型 | AI weather model | — | — | — | AI 气象模型、气象大模型、机器学习天气模型 |
| 试验版本 | experimental version | — | — | ECMWF 开放数据 2025-02-25 以前的 AIFS，模型名 `aifs` | 实验版本、实验版 |
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
| spread | ensemble spread | — | — | — | 集合离散度、系综离散度、集合发散度 |
| MSE | mean squared error | MSE | — | — | 均方误差 |
| RMSE | root mean squared error | RMSE | 与变量相同 | — | 均方根误差、均方误差根、均方根差、均方差 |
| bias | bias | — | 与变量相同 | — | 偏差 |
| MAE | mean absolute error | MAE | 与变量相同 | — | 平均绝对误差、平均绝对偏差 |
| track error | track error | — | km | `ch12.track_errors` 的 `dist_km` | 路径误差、轨迹误差 |
| hit | hit | — | — | — | 命中 |
| miss | miss | — | — | — | 漏报、未命中 |
| false alarm | false alarm | — | — | — | 空报 |
| hit rate | hit rate | — | — | — | 命中率 |
| correlation | Pearson correlation coefficient | — | — | earthkit-meteo `score.pearson_correlation` | 相关系数、皮尔逊相关系数 |
| 百分位数 | percentile | — | 与变量相同 | — | 百分位、分位点 |
| 标准误差 | standard error | — | 与变量相同 | — | 标准误 |
| 标准差 | standard deviation | — | 与变量相同 | — | 标准偏差 |
| ACC | anomaly correlation coefficient | ACC | — | — | 距平相关系数、异常相关系数、距平相关 |
| CRPS | continuous ranked probability score | CRPS | 与变量相同 | — | 连续分级概率评分、连续排序概率评分、连续等级概率评分 |
| SEEPS | stable equitable error in probability space | SEEPS | — | WeatherBench 2 的降水评分 | SEEPS 评分 |
| skill score | skill score | — | — | — | 技巧评分、技巧分数 |
| 纬度加权 | latitude weighting | — | — | — | — |
| RMS | root mean square | RMS | 与变量相同 | — | 均方根 |
| 损失函数 | loss function | — | — | — | 代价函数 |
| 动能谱 | kinetic energy spectrum | $E(k)$ | m² s⁻² | — | 能谱、能量谱 |
| 纬向波数 | zonal wavenumber | $k$ | — | — | — |
| 有效分辨率 | effective resolution | — | km | — | — |

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

下面每一条说明一个选择和它的理由。用户在 2026-10-17 批准了前 17 条。

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
