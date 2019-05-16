#!/bin/bash

#PBS -q normalbw
#PBS -P v45
#PBS -l ncpus=168
#PBS -l mem=1500Gb
#PBS -l walltime=48:00:00
#PBS -N Eeddy_model

dataorigin='model'
ini=0
end=153
#ini=85
#end=168
#ini=169
#end=197
file_div=1

module load pbs
module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/access_om2/trackeddy_analysis/"

cd $cdir

./trackeddy_jobasignment.sh $ini $end 'run_model' $file_div
