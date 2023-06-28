import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'

boxplot_options = {
    'widths': 0.25,  # Larghezza dei box
    'patch_artist': True,  # Abilita l'uso di colori personalizzati
    'medianprops': {'color': 'black'},  # Colore della linea della mediana
    'boxprops': {'color': 'black'},  # Colore del box
    'whiskerprops': {'color': 'black'},  # Colore delle linee dei baffi
    'capprops': {'color': 'black'},  # Colore delle linee delle estremità dei baffi
    'flierprops': {'marker': 'o', 'markerfacecolor': 'black', 'markersize': 3},  # Opzioni per gli outliers
}


df = pd.read_csv('malwares_global.csv')

plt.figure(figsize=(10, 6))
# Opzioni per il boxplot

#TODO: change these columns with real ones
plt.boxplot([df['detection rate 0'], df['detection rate 1'], df['detection rate 2']], labels=['Passo 0', 'Passo 1', 'Passo 2'], **boxplot_options)
plt.title('Detection rate dei malware al variare dei passi di trasformazione', fontweight='bold')
plt.xlabel('Passo di trasformazione', fontweight='bold')
plt.ylabel('Detection rate', fontweight='bold')

plt.ylim(0, 1)
plt.grid(axis='y', linestyle="dashed", alpha=0.5)
plt.savefig('detection_rate_boxplot.png', dpi=300)
plt.show()


df = pd.read_csv('../entropy_global.csv')

plt.figure(figsize=(10, 6))
plt.boxplot([df['Entropy_0'], df['Entropy_1'], df['Entropy_2']], labels=['Passo 0', 'Passo 1', 'Passo 2'], **boxplot_options)
plt.title('Entropia dei malware al variare dei passi di trasformazione', fontweight='bold')
plt.xlabel('Passo di trasformazione', fontweight='bold')
plt.ylabel('Entropia', fontweight='bold')

#plt.ylim(0, 8)
plt.grid(axis='y', linestyle="dashed", alpha=0.5)
plt.savefig('entropy_boxplot.png', dpi=300)
plt.show()
