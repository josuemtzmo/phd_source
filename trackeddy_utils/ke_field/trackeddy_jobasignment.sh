#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

dataorigin=$1
timeinit=$2
timeend=$3
rundir=$4

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/ke_field/"

for i in `seq $timeinit $timeend`;
do
  echo "/g/data3/hh5/public/apps/miniconda3/envs/analysis3/bin/python ${cdir}kineticenergy_field.py $i" >> $cdir$rundir/config.$((i-timeinit))
  echo "Running at $((i-timeinit)).  File: $cdir$rundir/config.$((i-timeinit))"
  pbsdsh -v -n $((i-timeinit))  -- bash $cdir$rundir/config.$((i-timeinit)) > $cdir$rundir/nohup.$((i-timeinit)) &
done
wait

