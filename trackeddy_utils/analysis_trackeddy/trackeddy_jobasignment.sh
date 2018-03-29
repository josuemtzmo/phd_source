#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

dataorigin=$1
timeinit=$2
timeend=$3
rundir=$4
counter=0
months=(1 4 7 10 13)
cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/analysis_trackeddy/"


if [ "$dataorigin" == "model" ] || [ "$dataorigin" == "satellite" ];
then
  if [ "$dataorigin" == "model" ];
  then
    for i in `seq $timeinit $timeend`;
    do
      echo "/g/data3/hh5/public/apps/miniconda3/envs/analysis3/bin/python ${cdir}trackeddy_$dataorigin.py $i" >> $cdir$rundir/config.$((i-timeinit))
      echo "Running at $((i-timeinit)).  File: $cdir$rundir/config.$((i-timeinit))"
      pbsdsh -v -n $((i-timeinit))*2  -- bash $cdir$rundir/config.$((i-timeinit)) > $cdir$rundir/nohup.$((i-timeinit)) &
    done
    wait
  else
    for i in `seq $timeinit $timeend`;
    do
      for m in `seq 0 $(( ${#months[@]}-2 ))`;
      do 
        echo "/g/data3/hh5/public/apps/miniconda3/envs/analysis3/bin/python ${cdir}trackeddy_$dataorigin.py $i ${months[$m]} ${months[$(($m+1))]} " > $cdir$rundir/config.$counter
        echo "Running year $((i)).  File: $cdir$rundir/config.$counter"
        pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$counter > $cdir$rundir/nohup.$counter &
        counter=$(( $counter + 1 ))
      done
    done
    wait
  fi
else
  echo "First argument (dataorigin) should be 'model' or 'satellite'"
fi


