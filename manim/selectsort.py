import numpy as np
import time
import matplotlib as mpl
import matplotlib.pyplot as plt

def selectsort(ar):
    for i in range(len(ar)):
        mn = i
        for j in range(i + 1, len(ar)):
            if ar[j] < ar[mn]:
                mn = j
        ar[i], ar[mn] = ar[mn], ar[i]
 

T = 1000
N = 200
results = []
for n in range(N):
    avg_time = 0.0
    for t in range(T):
        test_ar = np.random.permutation(np.array(range(n)))
        time1 = time.time_ns()

        selectsort(test_ar)

        time2 = time.time_ns()

        avg_time += time2 - time1
    
    avg_time /= T
    avg_time /= 1e6
    results.append(avg_time)

plt.plot(range(N), results)
fontsize = 30
plt.xlabel("array length", fontsize = fontsize)
plt.ylabel("Time (ms)", fontsize = fontsize)

plt.savefig("img/select.png")
