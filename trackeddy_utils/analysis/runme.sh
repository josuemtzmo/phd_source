#!/bin/bash
#PBS -q express
#PBS -P v45
#PBS -l ncpus=32
#PBS -l mem=236GB
#PBS -N trackeddy

bash /home/156/jm5970/github/phd_source/trackeddy_utils/analysis/runjobs.sh model 306 338 /home/156/jm5970/github/phd_source/trackeddy_utils/analysis/nohup/
