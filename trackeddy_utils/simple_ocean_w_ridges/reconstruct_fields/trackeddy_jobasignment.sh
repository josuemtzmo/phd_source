#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'
dataorigin='model'
timeinit=$1
timeend=$2
rundir=$3
expt=$4
level=$5
counter=0
cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/simple_ocean_w_ridges/reconstruct_fields/"
python_path="/g/data/v45/jm5970/env/track_env/bin/python"


for i in `seq $timeinit $timeend`;
do
   counter=$((i-timeinit))
   echo "${python_path} ${cdir}reconstruct_$dataorigin.py $i $expt $level" > $cdir$rundir/config.$(printf %05d ${counter%})
   echo "Running at $counter.  File: $rundir/config.$(printf %05d ${counter%})"
   /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$(printf %05d ${counter%})&
done
wait
