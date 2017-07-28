import os

#BE SURE TO CHANGE THE ION NAME IN 3_WRITE_COM_PULL* SCRIPTS

sims = ['05_Pull_neg', '05_Pull_pos']

ion = raw_input('Please enter the ion (acd, cho, ger): ')
sys = raw_input('Please enter the lipid (POPC, POPE): ')

equil_jobid = input('Please enter the JobID of 04_Equil: ')
wd = '/scratch/btw47/US/POPE/%s/1_pulling/' % ion

for i in sims:
	if i == '05_Pull_neg':
		for x in xrange(0, 10):
			if x == 0:
				dpn = '#SBATCH --dependency=afterany:%s' % equil_jobid
				prev_sim = '04_Equil.rst'
			else:
				dpn = '#SBATCH --dependency=afterany:%s' % job_id
				prev_iter = x - 1 
				prev_sim = '%s%s.rst' % (i, prev_iter)
				
			with open('%s%s%s.in' % (wd, i, x), 'w') as f:
				f.write('''pull 32ns LIPID 303K
 &cntrl
   imin=0, ntx=5, irest=1, 
   ntc=2, ntf=2, tol=0.0000001,
   nstlim=1600000, ntt=3, gamma_ln=1.0,
   temp0=303.0,
   ntpr=1000, ntwr=10000, ntwx=1000,
   dt=0.002, ig=-1,
   ntb=2, cut=10.0, ioutfm=1, ntxo=2,
   nmropt=1, ntp=2, pres0=1.0, taup=1.0, jar=1,
 /
 &wt type='DUMPFREQ', istep1=1000 /
 &wt type='END', /
DISANG=COM_pull_neg%s.RST
DUMPAVE=05_Pull_distneg%s.dat
LISTIN=POUT
LISTOUT=POUT
 /
 /
 &ewald
  skinnb=3.0,
 /
''' % (x, x))

			with open('%s%s%s.script' % (wd, i, x), 'w') as f1:
				f1.write('''#!/bin/bash
#SBATCH --job-name=%s_%s_POPE_%s
#SBATCH --time=7:00:00
#SBATCH --ntasks=48
#SBATCH --nodes=2
%s
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=btw47@nau.edu
#SBATCH --workdir=%s

module load amber/16-intel-2016.0/

python 3_write_COM_pullneg.py

mpirun -np 48 /packages/amber/amber16-intel-2016.0/bin/pmemd.MPI -O -i %s%s.in -o %s%s.out -p POPE_%s.prmtop -c %s -r %s%s.rst -x %s%s.nc -inf %s%s.mdinfo''' % (i, x, ion, dpn, wd, i, x, i, x, ion, prev_sim, i, x, i, x, i, x))
		
			slurmCommand = 'sbatch %s%s%s.script' % (wd, i, x)
			job_id = os.popen(slurmCommand).read()[20:]
			print "Submitted %s_%s as JOB_ID %s" % (i, x, job_id)

		
			with open('JOB_INFO.dat', 'a') as f1:
				f1.write('%s %s %s %s \n' % (sys, ion, i, job_id))

	
	elif i == '05_Pull_pos':
		for x in xrange(0, 10):
			if x == 0:
				dpn = '#SBATCH --dependency=afterany:%s' % equil_jobid
				prev_sim = '04_Equil.rst'
			else:
				dpn = '#SBATCH --dependency=afterany:%s' % job_id
				prev_iter = x - 1 
				prev_sim = '%s%s.rst' % (i, prev_iter)

			with open('%s%s%s.in' % (wd, i, x), 'w') as f:
				f.write('''pull 32ns LIPID 303K
 &cntrl
   imin=0, ntx=5, irest=1, 
   ntc=2, ntf=2, tol=0.0000001,
   nstlim=1600000, ntt=3, gamma_ln=1.0,
   temp0=303.0,
   ntpr=1000, ntwr=10000, ntwx=1000,
   dt=0.002, ig=-1,
   ntb=2, cut=10.0, ioutfm=1, ntxo=2,
   nmropt=1, ntp=2, pres0=1.0, taup=1.0, jar=1,
 /
 &wt type='DUMPFREQ', istep1=1000 /
 &wt type='END', /
DISANG=COM_pull_pos%s.RST
DUMPAVE=05_Pull_distpos%s.dat
LISTIN=POUT
LISTOUT=POUT
 /
 /
 &ewald
  skinnb=3.0,
 /
''' % (x, x))


			with open('%s%s%s.script' % (wd, i, x), 'w') as f1:
				f1.write('''#!/bin/bash
#SBATCH --job-name=%s_%s_POPE_%s
#SBATCH --time=7:00:00
#SBATCH --ntasks=48
#SBATCH --nodes=2
%s
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=btw47@nau.edu
#SBATCH --workdir=%s

module load amber/16-intel-2016.0/

python 3_write_COM_pullpos.py

mpirun -np 48 /packages/amber/amber16-intel-2016.0/bin/pmemd.MPI -O -i %s%s.in -o %s%s.out -p POPE_%s.prmtop -c %s -r %s%s.rst -x %s%s.nc -inf %s%s.mdinfo''' % (i, x, ion, dpn, wd, i, x, i, x, ion, prev_sim, i, x, i, x, i, x))
		
			slurmCommand = 'sbatch %s%s%s.script' % (wd, i, x)
			job_id = os.popen(slurmCommand).read()[20:]
			print "Submitted %s_%s as JOB_ID %s" % (i, x, job_id)


			with open('JOB_INFO.dat', 'a') as f1:
				f1.write('%s %s %s %s \n' % (sys, ion, i, job_id))
