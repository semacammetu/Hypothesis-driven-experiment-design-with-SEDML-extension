import random

import pandas as pd

df = pd.read_excel(r'cases_turkey.xlsx')
df.columns = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10", "v11", "v12"]

x0 = 0
x1 = 0
x2 = 0
x3 = 0
x4 = 0
x5 = 0
j = 0
k = 0

f = open("hospital data", "a")
for i in range(0, 404):

    if (x1 > 1500 and j > 3000 and k > 50) or (x1 > 2500 and j > 3000) or (x3 > 900 and j > 3000 and k>50):
        x1 = random.randint(3000, 3810)
    else:
        x1 = random.randint(1905, 3810)
    x0 = random.randint(60, 117)

    x2 = random.randint(150, 300)
    x3 = random.randint(575, 1150)
    x4 = random.randint(57, 115)
    x5 = random.randint(240, 480)
    j = int(int(df["v9"][i+8]))
    k = random.randrange(int(j / 100), int(j / 10))

    content = str(i+1) + " " + str(x0) + " " + str(x1) + " " + str(x2) + " " + str(x3) + " " + str(x4) + " " + str(x5) + " " + str(j) + " " + str(k) + "\n"

    f.write(content)
f.close()
# open and read the file after the appending:
f = open("hospital data", "r")
print(f.read())
