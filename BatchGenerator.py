"""
#!/bin/bash
#SBATCH -J sim_n            # job name
#SBATCH -o sim_n.log        # output and error file name (%j expands to jobID)
#SBATCH -N 1                # total number of nodes
#SBATCH --exclusive         # processes per node
#SBATCH -p parallel-medium  # queue (partition) -- batch, parallel, etc.

module load anaconda/2.2.0

python simulation_script args
"""

import os
import subprocess

if os.path.isdir("./UnreliableAssignmentFragments"):
    raise ValueError("Folder already exists. Delete /UnreliableAssignmentFragments/ to continue")

num_jobs = 1000
step = .025
base = 0.0
trials = 10000
percentage = base

os.mkdir("UnreliableAssignmentFragments")
os.chdir("./UnreliableAssignmentFragments")

for i in range(40):
    os.mkdir("Fragment_" + str(i))
    os.chdir("./Fragment_" + str(i))
    with open("trials_{:}_{:}_{:}.sh".format(str(trials), int(percentage*100), str(num_jobs)), 'w') as fout:
        fout.write("#!/bin/bash\n")
        fout.write("#SBATCH -J sim_{:}_{:}\n".format(int(percentage*100), str(num_jobs)))
        fout.write("#SBATCH -o sim_{:}_{:}.log\n".format(int(percentage*100), str(num_jobs)))
        fout.write("#SBATCH -e sim_{:}_{:}.err\n".format(int(percentage*100), str(num_jobs)))
        fout.write("#SBATCH -N 1\n")
        fout.write("#SBATCH --exclusive\n")
        fout.write("#SBATCH -p parallel-medium\n\n")
        fout.write("module load anaconda/2.2.0\n\n")
        fout.write("python Collection.py {:} {:} {:} {:}".format(str(num_jobs), str(percentage), str(trials), "trials_{:}_{:}_{:}.csv".format(str(trials), int(percentage*100), str(num_jobs))))
    subprocess.call(["sbatch", "./trials_{:}_{:}_{:}.sh".format(str(trials), int(percentage*100), str(num_jobs))])
    os.chdir("../")



