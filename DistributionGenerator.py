from scipy.stats import truncnorm, pareto, uniform
import numpy as np
import matplotlib.pyplot as plt


class DistributionGenerator:
    """ Provides access to random number generators useful for populating job weights """

    def __init__(self):
        pass

    def generate_jobs(self, n, distribution_type='normal'):
        if distribution_type == 'normal':
            r = self.generate_normal(n)
        elif distribution_type == 'pareto':
            r = self.generate_pareto(n)
        elif distribution_type == 'uniform':
            r = self.generate_uniform(n)
        else:
            raise ValueError("Invalid distribution type specifier. You specified {:}, valid options are normal, pareto, uniform, and constant.".format(distribution_type))
        return np.array(1000*r, dtype=int)

    def generate_normal(self, n):
        lower = 0.0
        upper = 1.0
        mean = .5
        std_dev = .16
        return truncnorm((lower-mean)/std_dev, (upper-mean)/std_dev, loc=mean, scale=std_dev).rvs(size=n)

    def generate_pareto(self, n):
        b = 1.5
        to_return = np.zeros(n, dtype=float)
        for i in range(n):
            while True:
                potential_value = pareto.rvs(b, size=1)
                if potential_value[0] <= 10.0:
                    to_return[i] = potential_value/10.0
                    break
        return to_return

    def generate_uniform(self, n):
        return uniform.rvs(size=n)


if __name__ == "__main__":
    x = DistributionGenerator()
    jobs = x.generate_jobs(1000, distribution_type="pareto")
    print jobs.max()
    print jobs.min()
    plt.hist(jobs)
    plt.show()

