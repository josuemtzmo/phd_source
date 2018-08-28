#!/bin/bash
#PBS -q expressbw
#PBS -P g40
#PBS -l ncpus=140
#PBS -l mem=256Gb
#PBS -l walltime=24:00:00
#PBS -N EKEeddy

dataorigin='satellite'
ini=1993
end=2014

#dataorigin='model'
#ini=306
#end=334

#ini=312
#end=318

module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
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

