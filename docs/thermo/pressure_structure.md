# The Atmosphere Pressure Structure

## Hydrostatic equilibrium
假设气压是高度的函数: $P(z)$ 
想象一个边长为$\delta z$ 的立方体气团，位于高度为$z$ 的空中。它在竖直方向上会受到3个力的作用：
- 来自上方空气，向下挤压的力$F_d = - P(z+\delta z)\delta z^2$  
- 来自下方空气，向上挤压的力$F_u = P(z)\delta z^2$ 
- 气团自身的重力 $G = -mg$ 
三种力达到平衡时 — hydrostatic equilibrium:
$$
P(z)\delta z^2 - P(z+\delta z)\delta z^2 - mg = 0
$$
如果我们认为气团的密度是$\rho$, 
$$
P(Z)\delta z^2 - P(z + \delta z)\delta z^2 = \rho \delta z^3 g
$$
等式两边同时除以$\delta z > 0$, 得到
$$
-\delta P(z) = \rho g \delta z
$$
让$\delta z \to 0$, 得到
$$
\frac{dP(z)}{dz} = -\rho g
$$
所以，可以得到气压函数的导数等于$-\rho g$, 即 气压随高度上升会下降，下降的速度等它的密度和重力加速度的乘积。
直觉性的理解是，重力把气体分子往下拉，下方的气体分子比上方多，由此产生了向上的气压差。
## 理想气体的气压结构
如果我们假设空气团是理想气体，那么根据 [[2.1. Ideal Gas Law]], 它的密度取决于它的气压和温度
$$
\frac{dP}{P} = - \frac{g}{R_d T}dz
$$
也就是说，理想大气的气压随高度上升下降固定的百分比。下降速度由温度决定，温度越低下降越快。
$$
P = P_0 \exp\{- z / H\}
$$
其中$H = R_d T / g$ 被称为scaled height。如果取空气的$R_d$和大气层 的平均温度$\bar{T}$, $H\sim 7km$ 。也就是说，几乎每上升7km，气压下降2/3.
注意到大气散射光的能力和分子数目，也就是气压是成正比的。所以高空中，天空气压低，散射能力弱，天空就更接近黑色。