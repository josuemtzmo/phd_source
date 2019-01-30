#!/bin/bash
#PBS -q expressbw
#PBS -P v45
#PBS -l ncpus=140
#PBS -l mem=520Gb
#PBS -l walltime=24:00:00
#PBS -N EKEeddy

dataorigin='satellite'
ini=1993
end=2016

#dataorigin='model'
#ini=306
#end=334

#ini=312
#end=318

module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/ke_field/"

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

