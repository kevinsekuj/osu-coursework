#!/bin/bash

module load slurm
module load openmpi
#SBATCH -J autocorrelation
#SBATCH -A cs475-575
#SBATCH -p class
#SBATCH -N 8 # number of nodes
#SBATCH -n 8 # number of tasks
#SBATCH --constraint=ib
#SBATCH -o autocorrelation.out
#SBATCH -e autocorrelation.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=sekujk@oregonstate.edu

for p in 1 2 4 8
do
        mpic++ autocorrelation.cpp -o autocorrelation -lm
        mpiexec -mca btl self,tcp -np $p ./autocorrelation
done