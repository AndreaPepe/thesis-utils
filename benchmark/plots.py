import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#df = pd.read_csv("pagerank_global.csv", sep=",")
df = pd.read_csv("mooncalc_global.csv", sep=",")

columns = ["Elapsed_0", "Elapsed_1", "Elapsed_2", "Elapsed_3"]
steps = ["Passo 0" ,"Passo 1", "Passo 2", "Passo 3"]

means = []
variances = []
stddev = []
max = []
min = []

for col_name in columns:
    col = df[col_name]
    means.append(col.mean())
    variances.append(col.var())
    stddev.append(col.std())
    max.append(col.max())
    min.append(col.min())

# plot the data
plt.figure(figsize=(10, 6))
plt.plot(steps, means, color="black", marker="o", markersize=5, label="tempo di esecuzione medio (s)")
plt.errorbar(steps, means, color="red", yerr=stddev, fmt="o", capsize=4, label="deviazione standard")
plt.xlabel("Passi di trasformazione", fontweight="bold")
plt.ylabel("Tempo di esecuzione (s)", fontweight="bold")
#plt.title("Tempi di esecuzione del benchmark 'pagerank' al variare dei passi di trasformazione", fontweight="bold")
plt.title("Tempi di esecuzione del benchmark 'moon-calc' al variare dei passi di trasformazione", fontweight="bold")
#plt.legend(loc="upper right")
'''
for i, mean in enumerate(means):
    #plt.annotate(f"{mean:.2f}", (steps[i], means[i] + 0.02))
    plt.annotate(f'media: {mean:.2f}s\ndev std: {stddev[i]:.2f}s', xy=(i + 0.02, mean + 0.02), xytext=(5, 5), textcoords='offset points',
                 ha='left', va='bottom', fontsize=8, bbox=dict(facecolor='white', edgecolor='black', boxstyle='square'))
'''

#plt.ylim(min[0] - 0.2, max[3] + 0.2)
plt.ylim(min[0] - 0.5, max[3] + 0.5)

#plt.savefig("pagerank.png", dpi=300)
plt.savefig("moon-calc.png", dpi=300)
plt.show()