import numpy as np
import matplotlib.pyplot as plt
import Material_Init as mi

def fitting(x, y):
    X = 1 / x
    Y = 1 / y
    X2 = X * X
    XY = X * Y
    sumX = sum(X)
    sumY = sum(Y)
    sumX2 = sum(X2)
    sumXY = sum(XY)

    a0 = 1 / len(X) * (sumY * sumX2 - sumX * sumXY) / (sumX2 - 1 / len(X) * sumX ** 2)

    a1 = (sumXY - 1 / len(X) * sumX * sumY) / (sumX2 - 1 / len(X) * sumX ** 2)

    a = 1 / a0
    b = a1*a

    return a, b


#x = np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
#y = np.array([16, 25, 32, 33, 38, 36, 39, 40, 42, 42])

y = mi.MgSt_ffvec

x = np.linspace(1, len(y), 10)

plt.scatter(x, y)

a, b = fitting(x,y)

plt.plot(x, a*(x/(b+x)))

plt.show()
