#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

dataorigin=$1
timeinit=$2
timeend=$3
rundir=$4
counter=0
months=(1 3 5 7 9 11 13)
cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/satellite_model/reconstruct_field/"
python_path="/g/data/v45/jm5970/env/track_env/bin/python"

if [ "$dataorigin" == "model" ] || [ "$dataorigin" == "satellite" ];
then
  if [ "$dataorigin" == "model" ];
  then
    for i in `seq $timeinit $timeend`;
    do
      counter=$((i-timeinit))
      echo "${python_path} ${cdir}reconstruct_$dataorigin.py $i" > $cdir$rundir/config.$(printf %05d ${counter%})
      echo "Running at $((i-timeinit)).  File: $cdir$rundir/config.$(printf %05d ${counter%})"
      /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$(printf %05d ${counter%}) &
    done
    wait
  else
    for i in `seq $timeinit $timeend`;
    do
      for m in `seq 0 $(( ${#months[@]}-2 ))`;
      do
        echo "${python_path} ${cdir}reconstruct_$dataorigin.py $i ${months[$m]} ${months[$(($m+1))]} " > $cdir$rundir/config.$counter
        echo "Running year $((i)).  File: $cdir$rundir/config.$counter"
        /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$counter &
        counter=$(( $counter + 1 ))
      done
    done
    wait
  fi
else
  echo "First argument (dataorigin) should be 'model' or 'satellite'"
fi
