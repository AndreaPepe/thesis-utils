import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

df_orig = pd.read_csv('av_global.csv')

df = df_orig
#max_num = 4
df = df.loc[df['detection rate 0'] != 0.0]
df = df.sort_values(by=['detection rate 3'], ascending=False)
df = df.head(5)

names = df['name']
step0 = df['detection rate 0']
step1 = df['detection rate 1']
step2 = df['detection rate 2']
step3 = df['detection rate 3']

indexes = range(len(names))

bar_width = 0.3
'''
fig = plt.figure(figsize=(10, 8))

plt.barh(indexes, step0, bar_width, color="green", label='Passo 0')
plt.barh(indexes, step1, bar_width, color="orange", label='Passo 1', left=step0)
plt.barh(indexes, step2, bar_width, color="blue", label='Passo 2', left=step0+step1)
plt.barh(indexes, step3, bar_width, color="violet", label='Passo 3', left=step0+step1+step2)

plt.title('Detection rate degli anti-virus al variare dei passi di trasformazione sui malware', fontweight='bold')
plt.xlabel('Detection rate', fontweight='bold')
plt.ylabel('Antivirus', fontweight='bold')
plt.yticks(indexes, names)
plt.xlim(0, 1)

plt.legend(loc='upper right')


plt.show()
'''

matplotlib.style.use('seaborn-v0_8-paper')
df.plot(x='name', kind="bar", width=bar_width, rot=0, figsize=(10, 6), edgecolor='black')
plt.title('Detection rate degli anti-virus più robusti al variare dei passi di trasformazione sui malware', fontweight='bold')
plt.xlabel('Antivirus', fontweight='bold')
plt.ylabel('Detection rate', fontweight='bold')
plt.legend(['Passo 0', 'Passo 1', 'Passo 2', 'Passo 3'])
#plt.grid(axis='y', alpha=0.5, linestyle='--', color='lightgray')
plt.ylim(0, 1)
#plt.savefig('av_best_barplot.png', dpi=300)
plt.show()


df = df_orig
df = df.loc[df['detection rate 0'] != 0.0]
df = df.sort_values(by=['detection rate 3'], ascending=False)
# from the 15 AV with the highest detection rate, we take the most decrease in detection rate in the first step
df = df.head(15)
df['decrease'] = df['detection rate 0'] - df['detection rate 1']
df = df.sort_values(by=['decrease'], ascending=False)
df = df.head(5)

df['detection rate 0'] = df['detection rate 0'] * 100
df['detection rate 1'] = df['detection rate 1'] * 100
df['detection rate 2'] = df['detection rate 2'] * 100
df['detection rate 3'] = df['detection rate 3'] * 100

df.plot(x='name', y= ['detection rate 0', 'detection rate 1', 'detection rate 2', 'detection rate 3'], 
        kind="bar", width=bar_width, rot=0, figsize=(10, 6), edgecolor='black')
plt.title('Detection rate degli anti-virus le cui prestazioni peggiorano maggiormente al variare dei passi di trasformazione sui malware', fontweight='bold')
plt.xlabel('Antivirus', fontweight='bold')
plt.ylabel('Detection rate (%)', fontweight='bold')
plt.legend(['Passo 0', 'Passo 1', 'Passo 2', 'Passo 3'])
plt.ylim(0, 100)
plt.savefig('av_worst_barplot.png', dpi=300)
plt.show()