import os
import numpy as np
from scipy.stats import norm
from math import sqrt
import matplotlib.pyplot as plt

path = "./fragments_10000_pareto/"

if not os.path.isdir(path):
    raise ValueError(path + " directory does not exist in the working directory")

files = [f for f in os.listdir(path) if f.endswith(".csv")]
files.sort()
result_vector = np.zeros((40, 10000), dtype=float)
result_vec = []

base = 0.0
reservation_percentages = []
ticks = [0.0]
for i in range(len(files)):
    result_vec.append([])
    line_counter = 0
    with open(path + files[i]) as fin:
        for line in fin:
            sanitized_line = [token.rstrip("\n") for token in line.split(", ")]
            try:
                result_vector[i, line_counter] = 1.0 - (float(sanitized_line[0])/float(sanitized_line[1]))
            except ValueError:
                print sanitized_line
                print "From: ", files[i]
                exit(1)
            line_counter += 1
    reservation_percentages.append(base)
    base += .025
    if i % 2 == 1:
        ticks.append(base)

mins = np.array(np.min(result_vector, axis=1))
avgs = np.array(np.mean(result_vector, axis=1))
maxs = np.array(np.max(result_vector, axis=1))
std_devs = np.array(np.std(result_vector, axis=1))

z_critical = norm.ppf(q=0.975)

confidences = []
sampleMeans = np.zeros(40, dtype=float)
errs = np.zeros(40, dtype=float)
for i in range(len(result_vector)):
    if i == 3 or i == 4:
        plt.hist(result_vector[i])
        plt.show()
    samples = np.zeros(50, dtype=float)
    for j in range(50):
        sample = np.random.choice(a=result_vector[i], size=1000)
        sample_mean = sample.mean()
        err = z_critical * (std_devs[i]/sqrt(1000))
        samples[j] = err
    confidences.append(samples.mean())

plt.figure(figsize=(16, 9))
plt.plot(reservation_percentages, mins, linewidth=.5, linestyle='--', marker='x', color='r', label='Worst')
plt.plot(reservation_percentages, avgs, linewidth=1.5, marker='o', color='b', label='Avg')
plt.plot(reservation_percentages, maxs, linewidth=.5, linestyle='--', marker='^', color='g', label='Best')
plt.errorbar(reservation_percentages, avgs, yerr=confidences)
#plt.errorbar([res[1] for res in reservation_percentages], [r[2] for r in results], yerr=[[err[4][0], err[4][1]] for err in results])
plt.grid(True)
plt.xlim([-0.01, 1.01])
plt.ylim([-0.01, 1.01])
plt.title('Solution Feasibility Vs Reservation Percentage')
plt.ylabel('Percentage of Solutions considered feasible')
plt.xlabel('Reservation Percentage')
plt.xticks(ticks)
plt.legend(loc='lower right', shadow=True)
plt.savefig(path + "Results1000_10000_Pareto.png", dpi=300)
