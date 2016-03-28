import sys
import Bin
import DistributionGenerator
import multiprocessing as mp
from copy import deepcopy
import numpy as np


class Collection:
    """ Collection is a series of bins used to fit a set of jobs and subsequently test failure of individual bins. """

    def __init__(self):
        self.bin_capacity = 800
        self.bins = np.empty(self.bin_capacity, dtype=object)
        self.reservation_map = {}
        self.num_containers = 0
        self.reservation_percentage = 0.0
        self.infeasible_solutions = 0
        self.dist_gen = DistributionGenerator.DistributionGenerator()
        self.simulation_number = 0

    def describe(self):
        for my_bin in self.bins:
            print my_bin.name, "({:.2%}) --> {:.2%}".format(my_bin.ratio(), my_bin.reserved_ratio())
            my_bin.describe()

    def fail(self, bin_id):
        jobs_to_remove = deepcopy(self.bins[bin_id].jobs[self.bins[bin_id].jobs != -1])
        job_ids_to_remove = deepcopy(self.bins[bin_id].job_ids[self.bins[bin_id].jobs != -1])
        self.bins[bin_id].empty_bin()
        self.migrate_jobs(job_ids_to_remove, jobs_to_remove)
        '''
        try:
            self.migrate_jobs(jobs_to_remove)
        except ValueError:
            self.infeasible_solutions += 1
            return
        '''

    def migrate_jobs(self, job_ids, jobs):
        '''
        # GO ANYWHERE #
        for i in range(len(jobs)):
            job_assigned = False
            for j in range(len(self.bins[self.bins != np.array(None)])):
                if self.bins[j].consume_reservation(jobs[i]):
                    job_assigned = True
                    break
            if not job_assigned:
                raise ValueError("Insufficient space to migrate jobs. Simulation Failed.")
        '''
        # ONLY TO ASSIGNED LOCATION #
        for i in range(len(jobs)):
            job_assigned = False
            bin_num = self.reservation_map[job_ids[i]]
            if self.bins[bin_num[0]].consume_reservation(jobs[i]):
                job_assigned = True
            if not job_assigned:
                raise ValueError("Insufficient space to migrate jobs. Simulation Failed.")

    def firstFitTopo(self, jobs, reservations):
        if len(jobs) != len(reservations):
            raise IndexError("Length of jobs and reservations input lists do no match")

        import networkx as nx
        skeleton = nx.barabasi_albert_graph(780)
        G = nx.empty_graph()

    def firstFit(self, jobs, reservations):
        if len(jobs) != len(reservations):
            raise IndexError("Length of jobs and reservations input lists do not match")
        for i in range(len(jobs)):
            # FIT THE JOBS
            job_assigned = False
            reservation_assigned = False
            assigned_to = -1
            for j in range(len(self.bins[self.bins != np.array(None)])): # find an open spot for job
                if self.bins[j].assign_job(jobs[i][0], jobs[i][1]):
                    job_assigned = True
                    assigned_to = j
                    break
            for j in range(len(self.bins[self.bins != np.array(None)])):
                reservation_assigned = False
                if (j != assigned_to) and self.bins[j].assign_reservation(reservations[i][1]): #find a place for the reservation
                    reservation_assigned = True
                    self.reservation_map[reservations[i][0]] = (j, self.bins[j].name)
                    break
            # IF NO SPACE FOR JOB OR RESERVATION
            if not job_assigned or not reservation_assigned: # then open a new container
                if self.num_containers == self.bin_capacity:
                    self.bins = np.concatenate((self.bins, np.empty(self.bin_capacity, dtype=object)), axis=0)
                self.bins[self.num_containers] = Bin.Bin("Bin_"+str(self.num_containers))
                self.num_containers += 1
                if not job_assigned:
                    if not self.bins[self.num_containers-1].assign_job(jobs[i][0], jobs[i][1]):
                        raise ValueError("Job size exceeds every container's capacity")
                    if not reservation_assigned:
                        if self.num_containers == self.bin_capacity:
                            self.bins = np.concatenate((self.bins, np.empty(self.bin_capacity, dtype=object)), axis=0)
                        self.bins[self.num_containers] = Bin.Bin("Bin_"+str(self.num_containers))
                        self.num_containers += 1
                        if not self.bins[self.num_containers-1].assign_reservation(reservations[i][1]):
                            raise ValueError("Reservation size exceeds every container's capacity")
                        self.reservation_map[reservations[i][0]] = (self.num_containers-1, self.bins[self.num_containers-1].name)
                elif not reservation_assigned:
                    if not self.bins[self.num_containers-1].assign_reservation(reservations[i][1]):
                        raise ValueError("Reservation size exceeds every container's capacity")
                    self.reservation_map[reservations[i][0]] = (self.num_containers-1, self.bins[self.num_containers-1].name)

    def exhaustive_fail(self):
        base = deepcopy(self.bins)
        for i in range(len(self.bins[self.bins != np.array(None)])):
            try:
                self.fail(i)
            except ValueError:
                self.infeasible_solutions += 1
                print "BIN ",i," IS RESPONSIBLE"
            self.bins = deepcopy(base)
        if self.infeasible_solutions != 0:
            print self.reservation_map
            for i in range(len(self.bins[self.bins != np.array(None)])):
                print "Bin ",i
                print self.bins[i].describe()
            #self.plot_errythang()
        return self.infeasible_solutions, len(self.bins[self.bins != np.array(None)])

    def plot_errythang(self):
        import matplotlib.pyplot as plt
        res = [my_bin.reserved_ratio() for my_bin in self.bins[self.bins != np.array(None)]]
        con = [my_bin.consumed_ratio() for my_bin in self.bins[self.bins != np.array(None)]]
        fig, ax = plt.subplots(1,1)
        rect = ax.bar(range(len(self.bins[self.bins != np.array(None)])), res, width=1.0, color='r')
        rect2 = ax.bar(range(len(self.bins[self.bins != np.array(None)])), con, width=1.0, color='b', bottom=res)
        ax.set_xlim([0, len(self.bins[self.bins != np.array(None)])])
        plt.title('Job and Reservation fit')
        plt.ylabel('Bin capacity')
        plt.xlabel('Bin')
        plt.xticks([x for x in range(len(self.bins[self.bins != np.array(None)])) if x % 2 == 0], rotation="vertical")
        plt.legend((rect[0],rect2[0]),("Reserved", "Consumed"))
        plt.savefig("failed_100.png", dpi=150)
        print "OUTPUT PNG"
        #plt.show()

    def run(self, _num_jobs, _reservation_percentage):
        # Jobs are represented as a triple (jobId, jobSize, isReservation)
        test_jobs = zip(range(_num_jobs), self.dist_gen.generate_jobs(_num_jobs, distribution_type='uniform'), [False for x in range(_num_jobs)])
        reservations = []
        for job in test_jobs:
            reservations.append((job[0], job[1]*_reservation_percentage, True))
        self.firstFit(test_jobs, reservations)


def run_sim(_num_jobs, _reservation_percentage, _simulation_number):
    c = Collection()
    print "Running simulation {:} --> {:} jobs @ {:.2%} reservation...".format(_simulation_number, _num_jobs, _reservation_percentage)
    c.run(num_jobs, reservation_percentage)  # run(num_jobs, reservation_percentage)
    return c.exhaustive_fail()

if __name__ == "__main__":
    # program in invoked as:
    # python Collection.py <num_jobs> <reservation_percentage> <num_trials> <output_file>
    if len(sys.argv) != 5:
        raise ValueError("Invalid number of args. Usage is: python Collection.py <num_jobs> <reservation_percentage> <num_trials> <output_file>")

    output_array = np.zeros(int(sys.argv[3]), dtype=(int, 2))
    num_jobs = int(sys.argv[1])
    reservation_percentage = float(sys.argv[2])
    num_trials = int(sys.argv[3])

    '''
    pool = mp.Pool(processes=2)
    procs = [pool.apply_async(run_sim, args=(num_jobs, reservation_percentage, i+1)) for i in range(num_trials)]
    for i in range(len(procs)):
        output_array[i, 0], output_array[i, 1] = procs[i].get()

    '''
    for i in range(num_trials):
        output_array[i, 0], output_array[i, 1] = run_sim(num_jobs, reservation_percentage, i+1)

    with open(sys.argv[4], 'w') as fout:
        for i in range(len(output_array)):
            fout.write("{:}, {:}\n".format(str(output_array[i, 0]), str(output_array[i, 1])))