import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

distances=pd.read_csv("final_dist_table.csv")
distances_nz=distances[distances["total-distance"]>0]
distances_nz.reset_index(inplace=True)

bin_thresh=[0, 898.08027231, 1796.16054461, 2694.24081692,
  3592.32108923, 4490.40136154, 5388.48163384, 6286.56190615,
  7184.64217846, 8082.72245077, 8980.80272307, 9878.88299538,
 10776.96326769, 11675.04354, 12573.1238123, 13471.20408461,
 14369.28435692, 15267.36462923, 16165.44490153, 17063.52517384,
 17961.60544615]

for row in range(0,len(distances_nz)):
    dist_val=distances_nz.loc[row,"total-distance"]
    for i in range(1, len(bin_thresh)):
        try:
            if (dist_val < bin_thresh[i]) & (dist_val > bin_thresh[i-1]):
                distances_nz.loc[row,"bin"] = "bin" + str(i)
                break
        except:
            distances_nz.loc[row,"bin"] = "bin" + str(i)

distances_nz.to_csv("test.csv")



distances_array=distances_nz['total-distance'].values

counts, bin_edges, _ = plt.hist(distances_array,bins=20,edgecolor="black")
print(bin_edges)




plt.show()