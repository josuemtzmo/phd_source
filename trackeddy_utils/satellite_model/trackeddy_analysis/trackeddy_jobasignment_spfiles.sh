#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

dataorigin=$1
rundir=$2

#files=(307 308 309 310 311 312 313 318 319 320 321 323 324 326 327 328 329 333 334 335 336 337 338 340 344)

files=(312 328 337 339)

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/analysis_trackeddy/"

filenum=${#files[@]}

if [ "$dataorigin" == "model" ] || [ "$dataorigin" == "satellite" ];
then
  for i in `seq 0 $((filenum-1))`;
  do
    echo "/g/data3/hh5/public/apps/miniconda3/envs/analysis3/bin/python ${cdir}trackeddy_$dataorigin.py ${files[i]}" > $cdir$rundir/config.${files[i]}
    echo "Running at $i.  File: $cdir$rundir/config.${files[i]}"
    pbsdsh -v -n $(((i)*2))  -- bash $cdir$rundir/config.${files[i]} > $cdir$rundir/nohup.${files[i]} &
  done
  wait
else
  echo "First argument (dataorigin) should be 'model' or 'satellite'"
fi


