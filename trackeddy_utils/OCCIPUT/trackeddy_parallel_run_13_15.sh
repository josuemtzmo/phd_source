#!/bin/bash

#PBS -q normalbw
#PBS -P v45
#PBS -l ncpus=252
#PBS -l mem=2300Gb
#PBS -l walltime=48:00:00
#PBS -N OCCIPUT_E

dataorigin='OCCIPUT'
ini=13
end=15

file_div=4

module load pbs
module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir='/home/156/jm5970/github/phd_source/trackeddy_utils/OCCIPUT/'

cd $cdir

./trackeddy_jobasignment.sh $dataorigin $ini $end 'run' $file_div
