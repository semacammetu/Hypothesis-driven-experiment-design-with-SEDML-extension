import matplotlib.pyplot as plt

X, Y = [], []
for line in open('test_data/traffic_data/sabit-folder/test_0.txt', 'r'):
    values = [float(s) for s in line.split()]
    X.append(values[0])
    Y.append(values[1])

plt.plot(X, Y)
plt.show()