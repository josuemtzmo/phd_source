#!/bin/bash

#if [ "$dataorigin" == "model" ];
#then
#  ncp=$(($end-$ini))
#else
#  ncp=$((($end-$ini)*4))
#fi

#PBS -q normalbw
#PBS -P v45
#PBS -l ncpus=112
#PBS -l mem=1024Gb
#PBS -l walltime=48:00:00
#PBS -N Eeddy_model

ini=0
end=1120
file_div=10

module load pbs
module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/validation/"

cd $cdir 

./trackeddy_jobasignment.sh $ini $end 'run_validation' $file_div
