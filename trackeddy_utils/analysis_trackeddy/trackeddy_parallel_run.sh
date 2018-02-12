#!/bin/bash
#PBS -q express
#PBS -P v45
#PBS -l ncpus=80
#PBS -l mem=100Gb
#PBS -l walltime=07:00:00
#PBS -N extract_eddy_trackeddy

module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/analysis_trackeddy/"

cd $cdir

./trackeddy_jobasignment.sh model 306 345 'run'
