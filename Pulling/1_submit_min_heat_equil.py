import os

sim = ['01_Min', '02_Heat', '03_Heat2', '04_Equil']

ion = raw_input('Please enter the ion (acd, cho, ger): ')
sys = raw_input('Please enter the lipid (POPC, POPE): ')

wd = '/scratch/btw47/US/%s/%s/1_pulling' % (sys, ion)

for i in sim:
	with open('%s/%s.script' % (wd, i), 'w') as f1:
		if i != '01_Min':
			dpn = '#SBATCH --dependency=afterany:%s' % job_id
		if i == '01_Min':
			f1.write('''#!/bin/bash
#SBATCH --job-name=%s_POPE_%s
#SBATCH --time=2:00:00
#SBATCH --ntasks=48
#SBATCH --nodes=2
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=btw47@nau.edu
#SBATCH --workdir=%s
 
module load amber/16-intel-2016.0/
 
mpirun -np 48 /packages/amber/amber16-intel-2016.0/bin/pmemd.MPI -O -i %s.in -o %s.out -p POPE_%s.prmtop -c POPE_%s.inpcrd -r %s.rst''' % (i, ion, wd, i, i, ion, ion, i))

		elif i == '02_Heat':
			f1.write('''#!/bin/bash
#SBATCH --job-name=%s_POPE_%s
#SBATCH --time=4:00:00
#SBATCH --ntasks=48
#SBATCH --nodes=2
%s
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=btw47@nau.edu
#SBATCH --workdir=%s

module load amber/16-intel-2016.0/

mpirun -np 48 /packages/amber/amber16-intel-2016.0/bin/pmemd.MPI -O -i %s.in -o %s.out -p POPE_%s.prmtop -c 01_Min.rst -r %s.rst -x %s.nc -ref 01_Min.rst''' % (i, ion, dpn, wd, i, i, ion, i, i))

		elif i == '03_Heat2':
			f1.write('''#!/bin/bash
#SBATCH --job-name=%s_POPE_%s
#SBATCH --time=4:00:00
#SBATCH --ntasks=48
#SBATCH --nodes=2
%s
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=btw47@nau.edu
#SBATCH --workdir=%s

module load amber/16-intel-2016.0/

mpirun -np 48 /packages/amber/amber16-intel-2016.0/bin/pmemd.MPI -O -i %s.in -o %s.out -p POPE_%s.prmtop -c 02_Heat.rst -r %s.rst -x %s.nc -ref 02_Heat.rst''' % (i, ion, dpn, wd, i, i, ion,  i, i))

		elif i == '04_Equil':
			 f1.write('''#!/bin/bash
#SBATCH --job-name=%s_POPE_%s
#SBATCH --time=4:00:00
#SBATCH --ntasks=48
#SBATCH --nodes=2
%s
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=btw47@nau.edu
#SBATCH --workdir=%s

module load amber/16-intel-2016.0/

mpirun -np 48 /packages/amber/amber16-intel-2016.0/bin/pmemd.MPI -O -i %s.in -o %s.out -p POPE_%s.prmtop -c 03_Heat2.rst -r %s.rst -x %s.nc -inf %s.mdinfo''' % (i, ion, dpn, wd, i, i, ion, i, i, i))

	slurmCommand = 'sbatch %s.script' % i
	job_id = os.popen(slurmCommand).read()[20:]		
	print "Submitted %s as JOB_ID %s" % (i, job_id)


	with open('JOB_INFO.dat', 'a') as f1:
		f1.write('%s %s %s %s \n' % (sys, ion, i, job_id))
