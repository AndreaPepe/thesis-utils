import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'

df_orig = pd.read_csv('av_global.csv')

df = df_orig
#max_num = 4
df = df.loc[df['detection rate 0'] != 0.0]
df = df.sort_values(by=['detection rate 0'], ascending=False)
df = df.head(15)
df['decrease'] = df['detection rate 0'] - df['detection rate 2']
df = df.sort_values(by=['decrease'], ascending=True)
df = df.head(5)
bar_width = 0.25


matplotlib.style.use('seaborn-v0_8-paper')
df.plot(x='name', y=['detection rate 0', 'detection rate 1', 'detection rate 2'],
         kind="bar", width=bar_width, rot=0, figsize=(10, 6), edgecolor='black')
plt.title('Detection rate degli anti-virus più robusti al variare dei passi di trasformazione sui malware', fontweight='bold')
plt.xlabel('Antivirus', fontweight='bold')
plt.ylabel('Detection rate', fontweight='bold')
plt.legend(['Passo 0', 'Passo 1', 'Passo 2'])
#plt.grid(axis='y', alpha=0.5, linestyle='--', color='lightgray')
#plt.ylim(0, 1)
plt.savefig('av_best_barplot.png', dpi=300)
plt.show()


df = df_orig
df = df.loc[df['detection rate 0'] != 0.0]
df = df.sort_values(by=['detection rate 0'], ascending=False)
# from the 15 AV with the highest detection rate, we take the most decrease in detection rate in the first step
df = df.head(15)
df['decrease'] = df['detection rate 0'] - df['detection rate 1']
df = df.sort_values(by=['decrease'], ascending=False)
df = df.head(5)

'''
df['detection rate 0'] = df['detection rate 0'] * 100
df['detection rate 1'] = df['detection rate 1'] * 100
df['detection rate 2'] = df['detection rate 2'] * 100
'''
df.plot(x='name', y=['detection rate 0', 'detection rate 1', 'detection rate 2'], 
        kind="bar", width=bar_width, rot=0, figsize=(10, 6), edgecolor='black')
plt.title('Detection rate degli anti-virus le cui prestazioni peggiorano maggiormente al variare dei passi di trasformazione sui malware', fontweight='bold')
plt.xlabel('Antivirus', fontweight='bold')
plt.ylabel('Detection rate', fontweight='bold')
plt.legend(['Passo 0', 'Passo 1', 'Passo 2'])
#plt.ylim(0, 1)
plt.savefig('av_worst_barplot.png', dpi=300)
plt.show()