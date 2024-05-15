import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# RTTs = pd.read_csv("RTTs.csv")

RTTs = pd.DataFrame()  # for debugging
RTTs["RTT"] = np.random.normal(loc=50, scale=10, size=500)

RTTs["smooth RTT"] = 0.0
# calculate the smoothed rtt which is a rolling wighted mean by an exponent
for i in range(len(RTTs)):
    smoothRTT_sum = 0
    exp_sum = 0
    exp = math.exp(len(RTTs)-1-i)
    for j in range(len(RTTs)-1-i, len(RTTs)):
        smoothRTT_sum += exp*RTTs.loc[j, "RTT"]
        exp_sum += exp
        exp /= math.exp(1)
    RTTs.loc[len(RTTs)-1-i, "smooth RTT"] = smoothRTT_sum/exp_sum

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(RTTs['RTT'], color='blue', label='RTT')
plt.plot(RTTs['smooth RTT'], color='red', label='Smoothed RTT')

# Add labels and title
plt.xlabel('Time')
plt.ylabel('RTT value')
plt.title('RTT across time')

# Add legend
plt.legend()

# save plot (or show)
plt.savefig('RTTs.png')