#!/bin/bash
#PBS -q normal
#PBS -P v45
#PBS -l ncpus=48
#PBS -l mem=128Gb
#PBS -l walltime=24:00:00
#PBS -N extract_eddy_trackeddy

module load conda/analysis3
module load openmpi/1.10.7

cd /home/156/jm5970/github/phd_source/trackeddy_utils/analysis/
./runjobs.sh model 306 345 ./nohup/
