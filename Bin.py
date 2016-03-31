import numpy as np
cimport numpy as np

cdef class Bin:
    """ Container used to hold jobs. Can be seen as a server or data center """

    cdef int capacity, consumed, reserved, jobCount, jobCapacity
    cdef np.int_t[:] job_ids
    cdef np.int_t[:] jobs

    def __init__(self, name="default", int capacity=1000):
        self.name = name
        self.capacity = capacity
        self.consumed = 0
        self.reserved = 0
        self.jobCount = 0
        self.jobCapacity = 40
        self.job_ids = np.full(self.jobCapacity, -1, dtype=int)
        self.jobs = np.full(self.jobCapacity, -1, dtype=int)

    def assign_job(self, int jobid, int job):
        return self._assign_job(jobid, job)

    cdef bint _assign_job(self, int jobid, int job):
        if self.consumed + self.reserved + job <= self.capacity:
            if self.jobCount == self.jobCapacity:
                self.jobs = np.concatenate((self.jobs, np.full(self.jobCapacity, -1, dtype=int)), axis=0)
                self.job_ids = np.concatenate((self.job_ids, np.full(self.jobCapacity, -1, dtype=int)), axis=0)
            self.jobs[self.jobCount] = job
            self.job_ids[self.jobCount] = jobid
            self.jobCount += 1
            self.consumed += job
            return True
        else:
            return False

    def assign_reservation(self, int res):
        return self._assign_reservation(res)

    cdef bint _assign_reservation(self, int res):
        if self.consumed + self.reserved + res <= self.capacity:
            self.reserved += res
            return True
        return False


    cpdef empty_bin(self):
        self.jobs = np.full(self.jobCapacity, -1, dtype=int)
        self.jobCount = 0
        self.consumed = 0
        self.reserved = 0

    def consume_reservation(self, int job):
        return self._consume_reservation(job)

    cdef bint _consume_reservation(self, int job):
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

    cpdef describe(self):
        cdef np.ndarray[np.int32_t, ndim=1] _jobs
        cdef size_t job
        _jobs = np.asarray(self.jobs)
        for job in range(len(_jobs[np.where(_jobs != -1)])):
            print "\tJob (" + str(self.job_ids[job]) + "): " + str(self.jobs[job])
        #for res in self.re
        #   print "\tRes (" + str(job[0]) + "): " + str(job[1])

    cpdef ratio(self):
        return (self.consumed + self.reserved)/self.capacity

    cpdef consumed_ratio(self):
        return self.consumed

    cpdef reserved_ratio(self):
        return self.reserved

    cpdef bint is_empty(self):
        if self.consumed == 0 and self.reserved == 0:
            return True
        else:
            return False

    cpdef bint only_reserved(self):
        if self.consumed == 0:
            return True
        return False
