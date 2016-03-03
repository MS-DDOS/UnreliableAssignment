import Bin
import DistributionGenerator
import matplotlib.pyplot as plt
from copy import deepcopy
from numba import jit

class Collection:

    def __init__(self):
        self.bins = []
        self.reservation_map = {}
        self.num_containers = 0
        self.reservation_percentage = 0.0
        self.infeasible_solutions = 0
        self.dist_gen = DistributionGenerator.DistributionGenerator()

    def describe(self):
        for my_bin in self.bins:
            print my_bin.name, "({:.2%}) --> {:.2%}".format(my_bin.ratio(), my_bin.reserved_ratio())
            my_bin.describe()

    def fail(self, bin_id):
        jobs_to_remove = deepcopy(self.bins[bin_id].jobs)
        self.bins[bin_id].empty_bin()
        self.migrate_jobs(jobs_to_remove)
        '''
        try:
            self.migrate_jobs(jobs_to_remove)
        except ValueError:
            self.infeasible_solutions += 1
            return
        '''

    def migrate_jobs(self, jobs):
        for i in range(len(jobs)):
            job_assigned = False
            assignedTo = -1
            for j in range(len(self.bins)):
                if self.bins[j].consume_reservation(jobs[i]):
                    job_assigned = True
                    assignedTo = j
                    break
            if not job_assigned:
                raise ValueError("Insufficient space to migrate jobs. Simulation Failed.")

    def firstFit(self, jobs, reservations):
        if len(jobs) != len(reservations):
            raise IndexError("Length of jobs and reservations input lists do not match")
        for i in range(len(jobs)):
            ### FIT THE JOBS ###
            job_assigned = False
            reservation_assigned = False
            assignedTo = -1
            for j in range(len(self.bins)): # find an open spot for job
                if self.bins[j].assign_job(jobs[i]):
                    job_assigned = True
                    assignedTo = j
                    break
            for j in range(len(self.bins)):
                reservation_assigned = False
                if j is not assignedTo and self.bins[j].assign_reservation(reservations[i]): #find a place for the reservation
                    reservation_assigned = True
                    self.reservation_map[reservations[i][0]] = (j, self.bins[j].name)
                    break
            ### IF NO SPACE FOR JOB OR RESERVATION ###
            if not job_assigned or not reservation_assigned: # then open a new container
                self.bins.append(Bin.Bin("Bin_"+str(self.num_containers), 1.0))
                self.num_containers += 1
                if not job_assigned:
                    if not self.bins[-1].assign_job(jobs[i]):
                        raise ValueError("Job size exceeds every container's capacity")
                    if not reservation_assigned:
                        self.bins.append(Bin.Bin("Bin_"+str(self.num_containers), 1.0))
                        self.num_containers += 1
                        if not self.bins[-1].assign_reservation(reservations[i]):
                            raise ValueError("Reservation size exceeds every container's capacity")
                        self.reservation_map[reservations[i][0]] = (len(self.bins)-1, self.bins[-1].name)
                elif not reservation_assigned:
                    if not self.bins[-1].assign_reservation(reservations[i]):
                        raise ValueError("Reservation size exceeds every container's capacity")
                    self.reservation_map[reservations[i][0]] = (len(self.bins)-1, self.bins[-1].name)

    def exhaustive_fail(self):
        base = deepcopy(self.bins)
        for i in range(len(self.bins)):
            try:
                self.fail(i)
            except ValueError:
                self.infeasible_solutions += 1
            self.bins = deepcopy(base)
        return self.infeasible_solutions, len(self.bins)

    def plot_errythang(self):
        res = [my_bin.reserved_ratio() for my_bin in self.bins]
        con = [my_bin.consumed_ratio() for my_bin in self.bins]
        fig, ax = plt.subplots(1, 1)
        ax.bar(range(len(self.bins)), res, width=1.0, color='r')
        ax.bar(range(len(self.bins)), con, width=1.0, color='b', bottom=res)
        ax.set_xlim([0, len(self.bins)])
        plt.title('Job and Reservation fit')
        plt.ylabel('Bin capacity')
        plt.xlabel('Bin')
        plt.xticks([x for x in range(len(self.bins)) if x % 2 == 0])
        plt.show()

    def run(self, num_jobs, reservation_percentage):
        # Jobs are represented as a triple (jobId, jobSize, isReservation)
        test_jobs = zip(range(num_jobs), self.dist_gen.generateJobs(num_jobs, 'uniform', False), [False for x in range(num_jobs)])
        reservations = []
        for job in test_jobs:
            reservations.append((job[0], job[1]*reservation_percentage, True))
        self.firstFit(test_jobs, reservations)
        #self.describe()
        #print self.reservation_map

if __name__ == "__main__":
    c = Collection()
    c.run()
    #c.plot_errythang()
    #c.fail(0)
    #c.plot_errythang()
    #c.describe()
    print c.exhaustive_fail()
