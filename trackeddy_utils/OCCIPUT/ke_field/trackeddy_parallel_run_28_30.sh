#!/bin/bash

#PBS -q normalbw
#PBS -P x77
#PBS -l ncpus=252
#PBS -l mem=2000Gb
#PBS -l walltime=04:00:00
#PBS -N OCCIPUT_REF

dataorigin='OCCIPUT'
ini=28
end=30

file_div=4

module load pbs
module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir='/home/156/jm5970/github/phd_source/trackeddy_utils/OCCIPUT/ke_field/'

cd $cdir

./trackeddy_jobasignment.sh $dataorigin $ini $end 'run' $file_div
