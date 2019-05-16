#!/bin/bash

#PBS -q express
#PBS -P v45
#PBS -l ncpus=160
# #PBS -l mem=450Gb
#PBS -l mem=1280Gb
#PBS -l walltime=24:00:00
#PBS -N Reddy_M

#dataorigin='satellite'
#ini=1993
#end=2017

#dataorigin='model'
#ini=0
#end=160

module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/satellite_model/reconstruct_field"

cd $cdir

if [ "$dataorigin" == "model" ];
then
  ./trackeddy_jobasignment.sh $dataorigin $ini $end 'run_model'
elif [ "$dataorigin" == "satellite" ];
then
  ./trackeddy_jobasignment.sh $dataorigin $ini $end 'run_satel'
else
  echo "First argument (dataorigin) should be 'model' or 'satellite'"
fi
