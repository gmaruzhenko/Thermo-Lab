import numpy as np
from matplotlib import pyplot as plt

xArr = np.linspace(0,1,11)
Kc_black = [float(x) for x in '''13.8639508
13.2027766
12.54163107
11.88055341
11.21954508
10.55843546
9.89747516
9.23655566
8.57557674
7.91476273
7.25396135'''.split('\n')]
Kc_bare = [float(x) for x in '''9.6513
8.99195706
8.33267842
7.67343723
7.01422062
6.35502742
5.69586075
5.0367
4.37757
3.7185
3.0594'''.split('\n')]

plt.figure(figsize = (10.0,6.0), dpi = 125)
plt.plot(Kc_black, xArr, label=r"for black rod")
plt.plot(Kc_bare, xArr, label=r"for bare rod")
plt.vlines(Kc_black[-1], 0, 1, linestyles="dotted")
plt.text(
    Kc_black[-1], 1, 
    r"Minimum possible $k_c$ = 7.25", 
    va = "top", ha = "right",
    rotation = 90)
plt.vlines(Kc_bare[0], 0, 1, linestyles="dotted")
plt.text(
    Kc_bare[0] + 0.6, 1, 
    "Maximum possible\n$k_c$ = 9.65", 
    va = "top", ha = "right",
    rotation = 90)
plt.hlines(0.364, Kc_bare[-1], Kc_black[0], linestyles="dotted")
plt.text(
    Kc_bare[-1], 0.364, 
    "Maximum possible $\epsilon$ = 0.36", 
    va = "bottom", ha = "left")
plt.hlines(0.0, Kc_bare[-1], Kc_black[0], linestyles="dotted")
plt.text(
    Kc_bare[-1], 0, 
    "Minimum possible $\epsilon$ = 0", 
    va = "bottom", ha = "left")



plt.xlabel(r"Convection coefficient $k_c$ $[W/(m^2K)]$")
plt.ylabel("Emissivity $\epsilon$")
plt.legend(title=r"Best $k_c$ and $\epsilon$ after fit")
plt.show()