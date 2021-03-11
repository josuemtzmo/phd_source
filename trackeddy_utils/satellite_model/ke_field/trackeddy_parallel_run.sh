#!/bin/bash
#PBS -q normal
#PBS -P v45
##PBS -l ncpus=448
#PBS -l ncpus=48
#PBS -l storage=gdata/v45+gdata/hh5+gdata/ua8
##PBS -l mem=2000Gb
#PBS -l mem=192Gb
#PBS -l walltime=6:00:00
#PBS -N EKEeddy

dataorigin='satellite'
ini=2018
end=2019

process=17
#dataorigin='model'
#ini=306
#end=334

#ini=312
#end=318

module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/satellite_model/ke_field"

cd $cdir

if [ "$dataorigin" == "model" ];
then
  ./trackeddy_jobasignment.sh $dataorigin $ini $end 'run_model'
elif [ "$dataorigin" == "satellite" ];
then
  ./trackeddy_jobasignment.sh $dataorigin $ini $end 'run_satel' $process
else
  echo "First argument (dataorigin) should be 'model' or 'satellite'"
fi

