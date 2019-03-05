#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

timeinit=$1
timeend=$2
rundir=$3
timestepdiv=$4
counter=0
cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/validation/"
python_path="/g/data/v45/jm5970/env/track_env/bin/python"

for j in `seq $timeinit $timestepdiv $timeend`;
do
    echo "${python_path} ${cdir}so_synthetic.py $j" > $cdir$rundir/config.$(printf %05d ${counter%})
    echo "Running at core $counter.  File: config."$(printf %05d ${counter%})
    /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$(printf %05d ${counter%})
    counter=$(( $counter + 1))
done
wait
