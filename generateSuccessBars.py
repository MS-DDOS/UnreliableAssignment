import os
import numpy as np
from scipy.stats import norm
from math import sqrt
import matplotlib.pyplot as plt

path = "./single_failure_assigned/single_uniform_assigned/"
length = 41

if not os.path.isdir(path):
    raise ValueError("./single_failure_goanywhere/fragments/ directory does not exist in the working directory")

files = [f for f in os.listdir(path) if f.endswith(".csv")]
files.sort()
result_vector = np.zeros((length, 10000), dtype=float)

base = 0.0
reservation_percentages = []
ticks = [0.0]
for i in range(len(files)):
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

hundred_percent = np.zeros(length, dtype=float)

for i in range(len(result_vector)):
    count = 0
    for j in range(len(result_vector[i])):
        if result_vector[i][j] == 1.0:
            count += 1
    hundred_percent[i] = float(count)/float(len(result_vector[i]))

print hundred_percent[len(result_vector)-1]

labels = []
for i in range(len(reservation_percentages)):
    if i % 2 == 0:
        labels.append("{:.2f}".format(reservation_percentages[i]))
    else:
        labels.append("")
plt.bar(range(len(hundred_percent)), hundred_percent, width=1.0, align="center")
plt.xticks(range(len(hundred_percent)), labels, rotation="vertical")
plt.title('Rate of 100% solutions vs Reservation Percentage')
plt.ylabel('Percentage of trials that resulted in 100% solution feasibility')
plt.xlabel('Reservation Percentage')
plt.xlim([-1, length])
plt.show()

'''
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
plt.savefig("./fragments_10000_pareto/Results1000_10000_Pareto.png", dpi=300)
'''