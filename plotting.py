import math

import numpy as np
import pandas as pd

# RTTs = pd.read_csv("RTTs.csv")

RTTs = pd.DataFrame()  # for debugging
RTTs["RTT"] = np.random.normal(loc=50, scale=10, size=500)

RTTs["smooth RTT"] = 0
# calculate the smoothed rtt which is a rolling wighted mean by an exponent
for i in range(len(RTTs)):
    smoothRTT_sum = 0
    exp_sum = 0
    exp = math.exp(len(RTTs)-1-i)
    for j in range(len(RTTs)-1-i, len(RTTs)):
        smoothRTT_sum += exp*RTTs["RTT"][j]
        exp_sum += exp
        exp /= math.exp(1)
    RTTs["smooth RTT"][len(RTTs)-1-i] = smoothRTT_sum/exp_sum

print("hey")
