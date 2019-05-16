#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

timeinit=$1
timeend=$2
rundir=$3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/simple_ocean_w_ridges/2layer/"
python_path="/g/data/v45/jm5970/env/track_env/bin/python"

for i in `seq $timeinit $timeend`;
do
   if [ "$timeinit" == "0" ];
   then
      counter=$((i))
      echo "${python_path} ${cdir}trackeddy_run.py $((i))" > $cdir$rundir/config.$(printf %05d ${counter%})
      echo "Running at core $counter.  File: config."$(printf %05d ${counter%})
      /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$(printf %05d ${counter%}) &
   else
      core_diff=$((timeinit))
      counter=$((i))
      echo "${python_path} ${cdir}trackeddy_run.py $((i))" > $cdir$rundir/config.$(printf %05d ${counter%})
      echo "Running at core $((counter-core_diff)).  File: config."$(printf %05d ${counter%})
      /opt/pbs/default/bin/pbsdsh -v -n $((counter-core_diff))  -- bash $cdir$rundir/config.$(printf %05d ${counter%}) &
   fi
done
wait
