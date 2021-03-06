#!/bin/bash
#PBS -q express
#PBS -P v45
#PBS -l ncpus=16
#PBS -l mem=256Gb
#PBS -l walltime=24:00:00
#PBS -N Eeddy

module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/analysis_trackeddy/"

cd $cdir

./trackeddy_jobasignment_spfiles.sh model 'run'
