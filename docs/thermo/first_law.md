# The First Law of Thermodynamics

## 第一定律: system energy balance

能量守恒用来分析air parcel这个包含了很多气体分子的系统

对一个气团(air parcel)来说:
- $U$: 内部能量🟰分子的动能(平动/转动/振动)➕分子间势能
- $Q$: 气团从外界收到的净能量速率，通常和radiation, conduction, latent heat等有关
- $W$: 外界对气团做的功率

一个气团内部增加的能量的速率🟰吸收的热量速率➕外界对系统做的功率
$$
\frac{dU}{dt} = Q + W   
$$
## 大气中最常见的做功形式 — 气团体积变化

我们使用热力学第一定律来分析一个cubic ideal gas parcel，就像我们在[[2.2. The atmosphere’s pressure structure - hydrostatic equilibrium]] 里分析静力平衡一样。
想象气体被装在一个圆柱体活塞装置里，假设我们把气体压缩，保持它的底面积不变，但是高度减少$dz$, 假设气压此时为$P$，此时需要克服气压做功:
$$
Wdt = P A (-dz) = - P dV
$$
- 压缩气体$dV<0$, 外界对气团做功$>0$
- 拉伸气体$dV>0$, 外界对气团做功$<0$
- 注意，只有气团的体积发生变化才会有功。如果只是气压变化，体积不变，是不会有功的。

## 焓
- $H$ 的定义：内能+系统维持体积所需要的

把功和气压体积的关系带入热力学第一定律可知
$$
\frac{dU}{dt} = Q - P \frac{dV}{dt}  
$$
或者说,
$$
Q = \frac{d(U+PV)}{dt}
$$
- 焓: 气团内能➕气压✖️体积
- 外界注入的净能量会改变气团的焓

## Heat Capacity 比热容
- 理想气体的内能$U$ 只由温度$T$ 决定
### Constant volume 定容比热容
- 外界注入能量的过程中，气团的体积保持不变（比如在刚性容器中）
$$
dV = 0 \leftrightarrow Q = \frac{dU}{dt}
$$
- Constant volume heat capacity: 内能对温度变化的导数
$$
C_V = \frac{\partial U}{\partial T}
$$
### Constant pressure 定压比热容
$$
C_p = \frac{\partial H}{\partial T}
$$


