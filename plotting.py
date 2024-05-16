import math
import sys

import matplotlib.pyplot as plt
import pandas as pd

RTTs = pd.read_csv(f"CSV/RTTs_{sys.argv[1]}.csv")

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(RTTs['RTT'], color='blue', label='RTT')
plt.plot(RTTs['Smoothed RTT'], color='red', label='Smoothed RTT')

# Add labels and title
plt.xlabel('Packets')
plt.ylabel('RTT value')
plt.title('RTT across time - ' + sys.argv[1])

# Add legend
plt.legend()

# save plot (or show)
plt.savefig(f'plots/RTTs_{sys.argv[1]}.png')