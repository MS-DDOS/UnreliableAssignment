import Collection
import multiprocessing as mp
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

class Simulation:

    def __init__(self):
        self.simulation_number = 1

    def run(self, num_jobs, reservation_percentage):
        print "Running simulation {:} --> {:} jobs @ {:.2%} reservation".format(self.simulation_number, num_jobs, reservation_percentage)
        c = Collection.Collection()
        c.run(num_jobs, reservation_percentage)
        self.simulation_number += 1
        return c.exhaustive_fail()

def run_sim(sim, position, num_jobs, reservation_percentage, trials):
    trials = [sim.run(num_jobs, reservation_percentage) for i in range(trials)]
    ratios = np.array([1-(float(t[0])/float(t[1])) for t in trials])
    minimum_val = np.amin(ratios)
    maximum_val = np.amax(ratios)
    std_dev = np.std(ratios)
    mean = np.mean(ratios)
    print mean, std_dev
    try:
        confidence = norm.interval(.95, loc=mean, scale=std_dev)
    except RuntimeWarning:
        print mean, std_dev

    '''
    plt.hist(ratios)
    plt.show()
    exit(1)
    '''
    return position, minimum_val, mean, maximum_val, confidence

if __name__ == "__main__":
    s = Simulation()
    base_percentage = 0.0
    reservation_percentages = []
    ticks = [0.0]
    for i in range(40):
        base_percentage += .025
        reservation_percentages.append((i, base_percentage))
        if i % 2 != 0:
            ticks.append(base_percentage)


    #result = run_sim(s, 0, 100, .05, 5)


    # Begin multi core processing
    pool = mp.Pool(processes=2)
    results = [pool.apply_async(run_sim, args=(s, pos, 100, per, 5)) for pos, per in reservation_percentages]
    results = [p.get() for p in results]
    # End multi core processing

    results.sort()

    tuples = [(err[2]-err[4][0], err[4][1]-err[2]) for err in results]
    transposed = [list(t) for t in zip(*tuples)]
    print transposed

    # res = [my_bin.reserved_ratio() for my_bin in self.bins]
    # con = [my_bin.consumed_ratio() for my_bin in self.bins]
    # fig, ax = plt.subplots(1, 1)
    # ax.bar(range(len(self.bins)), res, width=1.0, color='r')
    # ax.bar(range(len(self.bins)), con, width=1.0, color='b', bottom=res)
    # ax.set_xlim([0, len(self.bins)])
    plt.figure(figsize=(16, 9))
    plt.plot([res[1] for res in reservation_percentages], [r[1] for r in results], linewidth=.5, linestyle='--', marker='x', color='r', label='Worst')
    plt.plot([res[1] for res in reservation_percentages], [r[2] for r in results], linewidth=2, marker='o', color='b', label='Avg')
    plt.plot([res[1] for res in reservation_percentages], [r[3] for r in results], linewidth=.5, linestyle='--', marker='^', color='g', label='Best')
    plt.errorbar([res[1] for res in reservation_percentages], [r[2] for r in results], yerr=transposed)
    #plt.errorbar([res[1] for res in reservation_percentages], [r[2] for r in results], yerr=[[err[4][0], err[4][1]] for err in results])
    plt.grid(True)
    plt.xlim([0.0, 1.0])
    plt.title('Solution Feasibility Vs Reservation Percentage')
    plt.ylabel('Percentage of Solutions considered feasible')
    plt.xlabel('Reservation Percentage')
    plt.xticks(ticks)
    plt.legend(loc='lower right', shadow=True)
    plt.savefig("Results100_250.png", dpi=300)


