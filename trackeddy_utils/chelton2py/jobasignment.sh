#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

file_div=$1
rundir=$2
counter=0
cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/chelton2py/"
python_path="/g/data/v45/jm5970/env/track_env/bin/python"

for j in `seq 0 $file_div`;
do
    echo "${python_path} ${cdir}Chelton2npy.py $j $file_div" > $cdir$rundir/config.$(printf %05d ${counter%})
    echo "Running at core $counter.  File: config."$(printf %05d ${counter%})
    /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$(printf %05d ${counter%})
    counter=$(( $counter + 1))
done
wait
