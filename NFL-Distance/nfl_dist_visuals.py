import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns

distances=pd.read_csv("final_dist_table.csv")
distances_nz=distances[distances["total-distance"]>0]
distances_nz.reset_index(inplace=True)

zscores = np.abs(stats.zscore(distances_nz["total-distance"].values))
distances_nz['zscores'] = zscores

bin_thresh=[1699.57658575, 2710.12766132, 3720.67873689, 4731.22981246,
  5741.78088803, 6752.3319636, 7762.88303918, 8773.43411475,
  9783.98519032, 10794.53626589, 11805.08734146, 12815.63841703,
 13826.1894926, 14836.74056817, 15847.29164375, 16857.84271932,
 17868.39379489, 18878.94487046, 19889.49594603, 20900.0470216,
 21910.59809717]

for row in range(0,len(distances_nz)):
    dist_val=distances_nz.loc[row,"total-distance"]
    for i in range(1, len(bin_thresh)):
        try:
            if (dist_val < bin_thresh[i]) and (dist_val > bin_thresh[i-1]):
                distances_nz.loc[row,"bin"] = "bin" + str(i)
                distances_nz.loc[row,"bin-low"] = str(bin_thresh[i-1])
                distances_nz.loc[row,"bin-high"] = str(bin_thresh[i])
                break
        except:
            distances_nz.loc[row,"bin"] = "bin" + str(i)

#playoff odds calculation

bin_df = pd.DataFrame(columns=["bin","playoff-odds", "bin-range"])
distances_nz=distances_nz[distances_nz["zscores"]<3]
distances_nz.reset_index(inplace=True)
print(distances_nz)
for i in range(1,21):
    try:
        temp = distances_nz[distances_nz["bin"]=="bin" + str(i)]
        bin_range = str(int(bin_thresh[i-1])) + "-" + str(int(bin_thresh[i]))
        bin_count = len(temp)
        playoff_count = len(temp[temp.playoffs == "y"])
        odds = playoff_count / bin_count
        bin_df.loc[len(bin_df)] = ["bin"+str(i), odds, bin_range]
    except:
        odds = 0.0
        bin_range = str(int(bin_thresh[i-1])) + "-" + str(int(bin_thresh[i]))
        bin_df.loc[len(bin_df)] = ["bin"+str(i), odds, bin_range]

bin_df=bin_df[bin_df["playoff-odds"]>0]

distances_nz.to_csv("test.csv")
bin_df.to_csv("test2.csv")

distances_array=distances_nz['total-distance'].values

plt.figure(figsize=(10, 6))
fig1=sns.histplot(data=distances_nz, x="total-distance", color="#301934", edgecolor="orange")
plt.title('Distribution of Travel Distances by Team-Season')
plt.xlabel('Travel Distance (in miles)')
plt.ylabel('Frequency')
plt.savefig('or_miles_traveled.png', bbox_inches="tight")

plt.figure(2)
sns.lineplot(data=bin_df, x="bin-range", y="playoff-odds", color="#301934")
plt.xticks(rotation=90)
plt.xlabel('Bins of Miles Traveled')
plt.ylabel('Historical % of Making Playoffs')
plt.savefig('or_playoff_prob.png', bbox_inches="tight")