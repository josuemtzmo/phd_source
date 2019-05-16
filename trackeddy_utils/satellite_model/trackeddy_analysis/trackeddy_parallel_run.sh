#!/bin/bash

#if [ "$dataorigin" == "model" ];
#then
#  ncp=$(($end-$ini))
#else
#  ncp=$((($end-$ini)*4))
#fi

#PBS -q normalbw
#PBS -P v45
# #PBS -l ncpus=84
#PBS -l ncpus=252
#PBS -l mem=2300Gb
# #PBS -l mem=750Gb
# #PBS -l mem=200Gb
#PBS -l walltime=48:00:00
#PBS -N Eeddy_model
# #PBS -N Eeddy_sat

#dataorigin='satellite'
#ini=1993
#end=2018

#dataorigin='satellite'
#ini=1993
#end=2015

#ini=2015
#end=2018

dataorigin='model'
ini=1
end=84
#ini=85
#end=168
#ini=169
#end=197
file_div=3

module load pbs
module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/satellite_model/trackeddy_analysis/"

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
