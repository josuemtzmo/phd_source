#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

dataorigin=$1

s_ensemble=$2
e_ensemble=$3

timeinit=1995
timeend=2015
#timeend=2015

rundir=$4

file_divisions=$5

counter=0

cdir='/home/156/jm5970/github/phd_source/trackeddy_utils/OCCIPUT/'
python_path="/g/data/v45/jm5970/env_gadi/trackeddy/bin/python"


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
          file_number=$(((year-timeinit)*(file_divisions)+j))
	  echo "${python_path} ${cdir}trackeddy_$dataorigin.py $i $year $file_divisions $j $file_number" > $cdir$rundir/config_$s_ensemble.$(printf %05d ${counter%})
          echo "Running at core $counter.  File: config_$s_ensemble."$(printf %05d ${counter%})
          /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config_$s_ensemble.$(printf %05d ${counter%}) &
        else
          echo $year
          counter=$(((i*(timeend-timeinit+1)*(file_divisions))+(year-timeinit)*(file_divisions) + j - (timeend-timeinit+1)*(file_divisions)))
          core_diff=$(((s_ensemble*(timeend-timeinit+1)*(file_divisions))-(timeend-timeinit+1)*(file_divisions)))
          file_number=$(((year-timeinit)*(file_divisions)+j))
          core_count=$((counter-core_diff))
          echo "${python_path} ${cdir}trackeddy_$dataorigin.py $i $year $file_divisions $j $file_number" > $cdir$rundir/config_$s_ensemble.$(printf %05d ${core_count%})
          echo "Running at core $core_count. File: config_$s_ensemble."$(printf %05d ${core_count%})
          /opt/pbs/default/bin/pbsdsh -v -n $core_count  -- bash $cdir$rundir/config_$s_ensemble.$(printf %05d ${core_count%}) &
        fi
    done
  done
done
wait
