#!/bin/bash
#PBS -q expressbw
#PBS -P v45
#PBS -l ncpus=28
#PBS -l mem=256Gb
#PBS -l walltime=24:00:00
#PBS -N EKEeddy

module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/ke_field/"

cd $cdir

./trackeddy_jobasignment.sh model 306 334 'run'
#./trackeddy_jobasignment.sh model 306 322 'run'
