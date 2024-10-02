import seaborn as sns
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

font = {'family' : 'normal',
        'size'   : 10}

matplotlib.rc('font', **font)
records = pd.read_csv("records_data.csv")

i=0
while i < len(records):
    if records.loc[i,"Wins"]+records.loc[i,"Losses"]+records.loc[i,"t"]>17:
        records.drop(i,inplace=True)
        i+=1
    else:
        i+=1


cols=[0,1,4,5,6]
records.drop(records.columns[cols], axis=1, inplace=True)
records=records.pivot_table(values='percent', index='Wins', columns='Losses',aggfunc="first")
records.to_csv("records_pivot.csv")
plt.ticklabel_format(useOffset=False)
plt.figure(figsize=(5,5))
heatmap = sns.heatmap(records, annot=True, fmt=".0f", cbar=False)
heatmap.invert_yaxis()
plt.show()

