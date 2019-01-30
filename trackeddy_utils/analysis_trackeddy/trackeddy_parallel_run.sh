#!/bin/bash

#if [ "$dataorigin" == "model" ];
#then
#  ncp=$(($end-$ini))
#else
#  ncp=$((($end-$ini)*4))
#fi

#PBS -q normalbw
#PBS -P v45
# #PBS -l ncpus=140
#PBS -l ncpus=168
#PBS -l mem=1500Gb
# #PBS -l mem=450Gb
#PBS -l walltime=48:00:00
#PBS -N Eeddy_model
# #PBS -N Eeddy_sat

#dataorigin='satellite'
#ini=1993
#end=2018

#dataorigin='satellite'
#ini=1993
#end=2016

dataorigin='model'
ini=1
end=56
#ini=27
#end=52
file_div=3

module load pbs
module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/analysis_trackeddy/"

cd $cdir

if [ "$dataorigin" == "model" ];
then 
  ./trackeddy_jobasignment.sh $dataorigin $ini $end 'run_model' $file_div
elif [ "$dataorigin" == "satellite" ];
then
  ./trackeddy_jobasignment.sh $dataorigin $ini $end 'run_satel'
else
  echo "First argument (dataorigin) should be 'model' or 'satellite'"
fi
