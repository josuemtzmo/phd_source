#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

dataorigin='model'
timeinit=$1
timeend=$2
rundir=$3
file_divisions=$4
counter=0
#months=(1 3 5 7 9 11 13)
# months=(1 2 3 4 5 6 7 8 9 10 11 12 13)
cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/access_om2_3rd_cycle/ke_field/"
python_path="/g/data/v45/jm5970/env/track_env/bin/python"

output_folder=${PBS_JOBFS}
OUTPUT_DIR="/home/156/jm5970/scratch/ACCESS_trackeddy_3rd_cycle/"

echo $output_folder
timeinit=$((timeinit-1))
timeend=$((timeend-1))
for i in `seq $timeinit $timeend`;
do
  for j in `seq 0 $((file_divisions-1))`;
  do
    if [ "$timeinit" == "0" ];
    then
      counter=$(( i*(file_divisions) + j))
      echo "${python_path} ${cdir}kineticenergy_$dataorigin.py $((i+1)) $j $file_divisions $counter $output_folder" > $cdir$rundir/config_$timeinit.$(printf %05d ${counter%})
      #echo "cp $output_folder/reconstruct_*$(printf %05d $((i+1))%)_$(printf %02d ${j%})*  $OUTPUT_DIR" >> $cdir$rundir/config_$timeinit.$(printf %05d ${counter%})
      
      echo "Running at core $counter.  File: config_$timeinit."$(printf %05d ${counter%})
      /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config_$timeinit.$(printf %05d ${counter%}) &
    else
      core_diff=$(((timeinit*file_divisions)))
      counter=$(( i*(file_divisions) + j -core_diff))
      echo "${python_path} ${cdir}kineticenergy_$dataorigin.py $((i+1)) $j $file_divisions $counter $output_folder" > $cdir$rundir/config_$timeinit.$(printf %05d ${counter%})
      #echo "cp $output_folder/reconstruct_*$(printf %05d $((i+1)))_$(printf %02d ${j%})*  $OUTPUT_DIR" >> $cdir$rundir/config_$timeinit.$(printf %05d ${counter%})
      
      echo "Running at core $counter.  File: config_$timeinit."$(printf %05d ${counter%})
      /opt/pbs/default/bin/pbsdsh -v -n $counter  -- bash $cdir$rundir/config_$timeinit.$(printf %05d ${counter%}) &
    fi
  done
done
wait

