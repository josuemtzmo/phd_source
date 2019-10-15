#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

dataorigin=$1
timeinit=$2
timeend=$3
rundir=$4
file_divisions=$5
counter=0
months=(1 2 3 4 5 6 7 8 9 10 11 12 13)
cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/satellite_model/trackeddy_analysis_each_file/"
python_path="/g/data/v45/jm5970/env/track_env/bin/python"


for i in `seq $timeinit $timeend`;
do
    for m in `seq 0 $(( ${#months[@]}-2 ))`;
    do 
        echo "${python_path} ${cdir}trackeddy_$dataorigin.py $i ${months[$m]} ${months[$(($m+1))]} " > $cdir$rundir/config.$(printf %05d ${counter%})
        echo "Running year $((i)).  File: $cdir$rundir/config.$(printf %05d ${counter%})"
        /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config.$(printf %05d ${counter%}) &
        counter=$(( $counter + 1 ))
    done
done
wait
