from scipy.stats import norm, pareto, uniform


class DistributionGenerator:
    'Provides access to random number generators useful for populating job weights'

    def __init__(self, seedValue=1234):
        self.seed_val = seedValue

    def generateJobs(self, n, type='normal', plotVals=True):
        if type == 'normal':
            r = self.generateNormal(n)
        elif type == 'pareto':
            r = self.generatePareto(n)
        elif type == 'uniform':
            r = self.generateUniform(n)
        else:
            raise ValueError(
                "Invalid distribution type specifier. You specified " + type + ", valid options are 'normal,' 'pareto,' 'uniform,' and 'constant.'")
        return r

    def generateNormal(self, n):
        return norm(loc=.5, scale=.1).rvs(size=n, random_state=self.seed_val)

    def generatePareto(self, n):
        b = 1.0
        return pareto.rvs(b, size=n, random_state=self.seed_val)

    def generateUniform(self, n):
        return uniform.rvs(size=n)


if __name__ == '__main__':
    dist = DistributionGenerator()
    print dist.generateJobs(2000, type="pareto")
