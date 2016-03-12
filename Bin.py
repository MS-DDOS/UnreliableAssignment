class UserError(Exception):
    """ This class is used to throw customer exceptions """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Bin:
    """ Container used to hold jobs. Can be seen as a server or data center """

    def __init__(self, name="default", capacity=1.0):
        self.name = name
        self.capacity = capacity
        self.consumed = 0.0
        self.reserved = 0.0
        self.jobCount = 0
        self.jobs = []

    def assign_job(self, job):
        if self.consumed + self.reserved + job[1] <= self.capacity:
            self.jobs.append(job)
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
        self.jobs = []
        self.jobCount = 0
        self.consumed = 0
        self.reserved = 0

    def consume_reservation(self, job):
        if job[1] <= self.reserved:
            self.reserved -= job[1]
            self.consumed += job[1]
            self.jobCount += 1
            self.jobs.append(job)
            return True
        else:
            return False

    def describe(self):
        for job in self.jobs:
            if job[2] is False:
                print "\tJob (" + str(job[0]) + "): " + str(job[1])
            else:
                print "\tRes (" + str(job[0]) + "): " + str(job[1])

    def ratio(self):
        return (self.consumed + self.reserved)/self.capacity

    def consumed_ratio(self):
        return self.consumed

    def reserved_ratio(self):
        return self.reserved

    def is_empty(self):
        if self.consumed == 0.0 and self.reserved == 0.0:
            return True
        else:
            return False
