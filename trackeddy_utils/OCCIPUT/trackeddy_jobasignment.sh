#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

dataorigin=$1

s_ensemble=$2
e_ensemble=$3

timeinit=1995
timeend=2015

rundir=$4

file_divisions=$5

counter=0

cdir='/home/156/jm5970/github/phd_source/trackeddy_utils/OCCIPUT/'
python_path="/g/data/v45/jm5970/env/track_env/bin/python"


for i in `seq $s_ensemble $e_ensemble`;
  do
    for year in `seq $timeinit $timeend`;
    do 
      for j in `seq 0 $((file_divisions-1))`;
      do
        if [ "$s_ensemble" == "0" ];
        then
          echo $year $(((timeend-timeinit+1)*file_divisions))
          counter=$(( (i*(timeend-timeinit+1)*(file_divisions))+(year-timeinit)*(file_divisions) + j - (timeend-timeinit+1)*(file_divisions)))
          echo "${python_path} ${cdir}trackeddy_$dataorigin.py $i $year $file_divisions $j $counter" > $cdir$rundir/config.$(printf %05d ${counter%})
          echo "Running at core $counter.  File: config."$(printf %05d ${counter%})
          /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$(printf %05d ${counter%}) &
        else
          echo $year
          counter=$(( (i*(timeend-timeinit+1)*(file_divisions))+(year-timeinit)*(file_divisions) + j - (timeend-timeinit+1)*(file_divisions)))
          echo "${python_path} ${cdir}trackeddy_$dataorigin.py $i $year $file_divisions $j $counter" > $cdir$rundir/config.$(printf %05d ${counter%})
          echo "Running at core $((counter-core_diff)).  File: config."$(printf %05d ${counter%})
          /opt/pbs/default/bin/pbsdsh -v -n $((counter-core_diff))  -- bash $cdir$rundir/config.$(printf %05d ${counter%}) &
        fi
    done
  done
done
wait
