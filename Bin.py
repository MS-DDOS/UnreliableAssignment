import numpy as np

class UserError(Exception):
    """ This class is used to throw customer exceptions """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Bin:
    """ Container used to hold jobs. Can be seen as a server or data center """

    def __init__(self, name="default", capacity=1000):
        self.name = name
        self.capacity = capacity
        self.consumed = 0
        self.reserved = 0
        self.jobCount = 0
        self.jobCapacity = 40
        self.job_ids = np.full(self.jobCapacity, -1, dtype=int)
        self.jobs = np.full(self.jobCapacity, -1, dtype=int)

    def assign_job(self, job):
        if self.consumed + self.reserved + job[1] <= self.capacity:
            if self.jobCount == self.jobCapacity:
                self.jobs = np.concatenate((self.jobs, np.full(self.jobCapacity, -1, dtype=int)), axis=0)
                self.job_ids = np.concatenate((self.job_ids, np.full(self.jobCapacity, -1, dtype=int)), axis=0)
            self.jobs[self.jobCount] = job[1]
            self.job_ids[self.jobCount] = job[0]
            self.jobCount += 1
            if not job[2]:  # if job is not a reservation
                self.consumed += job[1]
            else:
                self.reserved += job[1]
            return True
        else:
            return False

    def assign_reservation(self, job):
        if self.consumed + self.reserved + job[1] <= self.capacity:
            self.reserved += job[1]
            return True
        return False

    def remove_job(self, job):
        self.jobs.remove(job)
        self.consumed -= job[2]
        self.jobCount -= 1

    def empty_bin(self):
        self.jobs = np.full(self.jobCapacity, -1, dtype=int)
        self.jobCount = 0
        self.consumed = 0
        self.reserved = 0

    def consume_reservation(self, job):
        if job <= self.reserved:
            self.reserved -= job
            self.consumed += job
            if self.jobCount == self.jobCapacity:
                self.jobs = np.concatenate((self.jobs, np.full(self.jobCapacity, -1, dtype=int)), axis=0)
                self.job_ids = np.concatenate((self.job_ids, np.full(self.jobCapacity, -1, dtype=int)), axis=0)
            self.jobCount += 1
            self.jobs[self.jobCount] = job
            return True
        else:
            return False

    def describe(self):
        for job in range(len(self.jobs[self.jobs != -1])):
            print "\tJob (" + str(self.job_ids[job]) + "): " + str(self.jobs[job])
        #for res in self.re
        #   print "\tRes (" + str(job[0]) + "): " + str(job[1])

    def ratio(self):
        return (self.consumed + self.reserved)/self.capacity

    def consumed_ratio(self):
        return self.consumed

    def reserved_ratio(self):
        return self.reserved

    def is_empty(self):
        if self.consumed == 0 and self.reserved == 0:
            return True
        else:
            return False

    def only_reserved(self):
        if self.consumed == 0:
            return True
        return False
