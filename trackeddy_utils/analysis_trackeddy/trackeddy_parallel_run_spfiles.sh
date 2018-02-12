#!/bin/bash
#PBS -q express
#PBS -P v45
#PBS -l ncpus=48
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

files=(308 309 310 312 319 321 322 324 328 329 331 332 334 335 336 340 344)
./trackeddy_jobasignment_spfiles.sh model $files 'run'
