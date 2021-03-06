#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

dataorigin=$1
timeinit=$2
timeend=$3
rundir=$4
file_divisions=$5
counter=0
months=(1 3 5 7 9 11 13)
cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/satellite_model/ke_field/"
python_path="/g/data/v45/jm5970/env/track_env/bin/python"


if [ "$dataorigin" == "model" ] || [ "$dataorigin" == "satellite" ];
then
  if [ "$dataorigin" == "model" ];
  then
    for i in `seq $timeinit $timeend`;
    do
      echo "${python_path} ${cdir}kineticenergy_$dataorigin.py $i" > $cdir$rundir/config.$((i-timeinit))
      echo "Running at $((i-timeinit)).  File: $cdir$rundir/config.$((i-timeinit))"
      /opt/pbs/default/bin/pbsdsh -v -n $((i-timeinit))  -- bash $cdir$rundir/config.$((i-timeinit)) > $cdir$rundir/nohup.$((i-timeinit)) &
    done
    wait
    else
    for i in `seq $timeinit $timeend`;
    do
      for m in `seq 0 $((file_divisions-1))`;
      do
        echo "${python_path} ${cdir}kineticenergy_$dataorigin.py $i $m $file_divisions" > $cdir$rundir/config.$(printf %05d ${counter%})
        echo "Running year $((i)).  File: $cdir$rundir/config.$(printf %05d ${counter%})"
        /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$(printf %05d ${counter%}) > $cdir$rundir/nohup.$(printf %05d ${counter%}) &
        counter=$(( $counter + 1 ))
      done
    done
    wait
  fi
else
  echo "First argument (dataorigin) should be 'model' or 'satellite'"
fi
      
