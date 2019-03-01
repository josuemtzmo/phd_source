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
cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/analysis_trackeddy/"
python_path="/g/data/v45/jm5970/env/track_env/bin/python"

if [ "$dataorigin" == "model" ] || [ "$dataorigin" == "satellite" ];
then
  timeinit=$((timeinit-1))
  timeend=$((timeend-1))
  if [ "$dataorigin" == "model" ];
  then
    for i in `seq $timeinit $timeend`;
    do
      for j in `seq 0 $((file_divisions-1))`;
      do
        if [ "$timeinit" == "0" ];
        then
	   counter=$(( i*(file_divisions) + j))
           echo "${python_path} ${cdir}trackeddy_$dataorigin.py $((i+1)) $j $file_divisions $counter" > $cdir$rundir/config.$(printf %05d ${counter%})
           echo "Running at core $counter.  File: config."$(printf %05d ${counter%})
           /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$(printf %05d ${counter%})
        else
           core_diff=$(((timeinit*file_divisions)))
           counter=$(( i*(file_divisions) + j))
           echo "${python_path} ${cdir}trackeddy_$dataorigin.py $((i+1)) $j $file_divisions $counter" > $cdir$rundir/config.$(printf %05d ${counter%})
           echo "Running at core $((counter)).  File: config."$(printf %05d ${counter%})
           /opt/pbs/default/bin/pbsdsh -v -n $((counter-core_diff))  -- bash $cdir$rundir/config.$(printf %05d ${counter%})
        fi
      done
    done
    wait
  else
    for i in `seq $timeinit $timeend`;
    do
      for m in `seq 0 $(( ${#months[@]}-2 ))`;
      do 
        echo "${python_path} ${cdir}trackeddy_$dataorigin.py $i ${months[$m]} ${months[$(($m+1))]} " > $cdir$rundir/config.$counter
        echo "Running year $((i)).  File: $cdir$rundir/config.$counter"
        /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$counter > $cdir$rundir/nohup.$counter &
        counter=$(( $counter + 1 ))
      done
    done
    wait
  fi
else
  echo "First argument (dataorigin) should be 'model' or 'satellite'"
fi
