import pickle
import numpy as np
from matplotlib import pyplot as plt

# with open("PDE_fit_results_2.pickle", 'rb') as f:
#     res = pickle.load(f)

# hessInv = res.hess_inv(np.eye(4))

# ftol = 2.220446049250313e-09
# tmp_i = np.zeros(len(res.x))
# for i in range(len(res.x)):
#     tmp_i[i] = 1.0
#     uncertainty_i = np.sqrt(max(1, abs(res.fun))*ftol*res.hess_inv(tmp_i)[i])
#     tmp_i[i] = 0.0
#     print('{0:12.4e} ± {1:.1e}'.format(res.x[i], uncertainty_i))

# hess = np.linalg.inv(hessInv)
# negHess = -1 * hess
# invNegHess = np.linalg.inv(negHess)
# print(invNegHess)


with open("modelV2_e0.pickle", 'rb') as f:
    e0 = pickle.load(f)
with open("modelV2_e1.pickle", 'rb') as f:
    e1 = pickle.load(f)

time = np.arange(2665)
sensorLocations = [0.013, 0.083, 0.153, 0.223, 0.293]

plt.figure(1, figsize = (10.0,6.0), dpi = 125)
plt.xlabel("Time (s)")
plt.ylabel("Temperature difference (K)")
plt.plot(time, e0-e1)

plt.legend(["Model at {} m".format(location) for location in sensorLocations])

plt.show()