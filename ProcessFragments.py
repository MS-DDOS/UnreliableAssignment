import os
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

if not os.path.isdir("./fragments/"):
    raise ValueError("./fragments/ directory does not exist in the working directory")

dirs = os.listdir("./fragments/")
result_vector = np.zeros((40, 10000), dtype=float)

base = 0.0
reservation_percentages = []
ticks = [0.0]
for i in range(len(dirs)):
    line_counter = 0
    with open("./fragments/" + dirs[i]) as fin:
        for line in fin:
            sanitized_line = [token.rstrip("\n") for token in line.split(", ")]
            result_vector[i, line_counter] = 1.0 - (float(sanitized_line[0])/float(sanitized_line[1]))
            line_counter += 1
    reservation_percentages.append(base)
    base += .025
    if i % 2 == 1:
        ticks.append(base)

mins = np.array(np.min(result_vector, axis=1))
avgs = np.array(np.mean(result_vector, axis=1))
maxs = np.array(np.max(result_vector, axis=1))
std_devs = np.array(np.std(result_vector, axis=1))
confidences = []
for i in range(len(mins)):
    try:
        confidence = norm.interval(.95, loc=avgs[i], scale=std_devs[i])
    except RuntimeWarning:
        confidence = None
    confidences.append(confidence)

tuples = []
for i in range(len(mins)):
    tuples.append((avgs[i] - confidences[i][0], confidences[i][1] - avgs[i]))
transposed = [list(t) for t in zip(*tuples)]
print transposed[0:10]

plt.figure(figsize=(16, 9))
plt.plot(reservation_percentages, mins, linewidth=.5, linestyle='--', marker='x', color='r', label='Worst')
plt.plot(reservation_percentages, avgs, linewidth=2, marker='o', color='b', label='Avg')
plt.plot(reservation_percentages, maxs, linewidth=.5, linestyle='--', marker='^', color='g', label='Best')
plt.errorbar(reservation_percentages, avgs, yerr=transposed)
#plt.errorbar([res[1] for res in reservation_percentages], [r[2] for r in results], yerr=[[err[4][0], err[4][1]] for err in results])
plt.grid(True)
plt.xlim([0.0, 1.0])
plt.title('Solution Feasibility Vs Reservation Percentage')
plt.ylabel('Percentage of Solutions considered feasible')
plt.xlabel('Reservation Percentage')
plt.xticks(ticks)
plt.legend(loc='lower right', shadow=True)
plt.savefig("Results1000_10000.png", dpi=300)