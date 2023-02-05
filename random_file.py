from matplotlib import pyplot as plt


X = []
Y = []
Xo = [-1000, 0, 1000, 2000, 5050]

for xo in Xo:
    Xi = []
    Yi = []
    for x in range(24000):
        Xi.append(x)
        y = (xo - x) % 6000 - 1000
        Yi.append(y)
    X.append(Xi)
    Y.append(Yi)

plt.figure(1)
for i in range(len(X)):
    plt.plot(X[i], Y[i])
plt.show()