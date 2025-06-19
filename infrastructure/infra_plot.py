import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('results/infra_dump.csv')
df = pd.DataFrame(data)

# Feel free to modify the dataframe, in order to exclude/include only certain values, like below:
# df = df[df['Fac'] != 1]
# df = df[df['Fac'] == 10]
# df = df[df['CGF'] != 0.4]
# df = df[df['Days'] <= 600]

plt.figure(figsize=(10, 6))

sns.boxplot(data=df, x='Infra_Fac', y='Days', hue='Infra_Upgrade')
plt.axhline(500, color='r', linestyle='--', label='500-Day Threshold')
plt.title("Days to Break-Even by Infrastructure Level")
plt.legend()
plt.show()

fast_cases = df[df['Days'] < 500].pivot_table(
    index=['Infra_Upgrade', 'Con_Mod'],
    columns='Fac',
    values='Days',
    aggfunc='count'
)
plt.figure(figsize=(8, 6))
sns.heatmap(fast_cases.fillna(0), annot=True, cmap='YlGnBu')
plt.title("Fast Break-Even Cases (Days < 500)");
