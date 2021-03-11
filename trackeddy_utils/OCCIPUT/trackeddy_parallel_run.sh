#!/bin/bash

#PBS -q normal
#PBS -P x77
# #PBS -l ncpus=168
#PBS -l ncpus=336
#PBS -l mem=1344Gb
# #PBS -l mem=192Gb
#PBS -l walltime=38:00:00
#PBS -N OCCIPUT_E
#PBS -l storage=gdata/v45

dataorigin='OCCIPUT'
ini=$exp_run
end=$exp_run

file_div=16

module load pbs
#module load netcdf/4.3.3.1
#module use /projects/v45/modules
#module load cmstools
#module use /g/data3/hh5/public/modules
#module load conda/analysis3

cdir='/home/156/jm5970/github/phd_source/trackeddy_utils/OCCIPUT/'

cd $cdir

./trackeddy_jobasignment.sh $dataorigin $ini $end 'run' $file_div
