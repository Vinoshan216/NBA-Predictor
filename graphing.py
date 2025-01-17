import pandas as pd
import matplotlib.pyplot as plt


a = pd.read_csv("csv/merged_stats/player_DPOY_stats.csv")

i = a[a["GS"] < 2].sort_values("PTS", ascending=False).head(10)

a.corr(numeric_only=True)["Share"].plot.bar()

plt.show()